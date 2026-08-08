"""Tests for the pair runner. No test touches the network: the claude
subprocess is replaced with a fake runner that returns canned
stream-json output."""

import json
import re
import threading
from collections import Counter
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from string import ascii_lowercase

import pytest
import yaml

from cost.analysis import task_type
from runner import (
    GenerationError,
    PluginLeakError,
    build_argv,
    cli,
    generate,
    manifest_sha256,
    style_reference,
)
from runner.provenance import build_provenance
from runner.report import build_report
from runner.screening import screening_provenance, screening_section, select_screening_prompts

HERE = Path(__file__).parent
PROMPTS = HERE.parent / "prompts" / "prompts.yaml"
HOLDOUT = HERE.parent / "prompts" / "holdout.yaml"

TASK_TYPES = {"explanation", "code-review", "summarization", "debugging"}


def stream_output(output_style="default", answer="ok", is_error=False, plugins=()):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": "claude-sonnet-5",
        "claude_code_version": "2.1.220",
        "plugins": [{"name": name} for name in plugins],
        "tools": [],
        "mcp_servers": [],
    }
    result = {
        "type": "result",
        "is_error": is_error,
        "result": answer,
        "usage": {
            "output_tokens": 7,
            "input_tokens": 3,
            "cache_creation_input_tokens": 2,
            "cache_read_input_tokens": 1,
        },
        "modelUsage": {"claude-sonnet-5": {}},
        "duration_ms": 100,
    }
    return "\n".join(json.dumps(event) for event in (init, result))


def style_of(argv):
    settings = json.loads(argv[argv.index("--settings") + 1])
    return settings.get("outputStyle")


class FakeRunner:
    """Returns stream-json output that matches the requested style."""

    def __init__(self):
        self.calls = []

    def __call__(self, argv, cwd, env=None):
        self.calls.append(argv)
        style = style_of(argv)
        plugins = ("test-plugin",) if "--plugin-dir" in argv else ()
        return stream_output(
            output_style=style or "default", answer=f"answer under {style}", plugins=plugins
        )


def test_prompt_set_is_complete():
    prompts = yaml.safe_load(PROMPTS.read_text())["prompts"]
    assert len(prompts) == 32
    ids = [p["id"] for p in prompts]
    assert len(set(ids)) == 32
    types = {p["type"] for p in prompts}
    assert types == TASK_TYPES
    for kind in TASK_TYPES:
        assert sum(1 for p in prompts if p["type"] == kind) == 8
    assert all(p["text"].strip() for p in prompts)


def test_holdout_set_is_complete():
    prompts = yaml.safe_load(HOLDOUT.read_text())["prompts"]
    assert len(prompts) == 24
    ids = [p["id"] for p in prompts]
    assert len(set(ids)) == 24
    types = {p["type"] for p in prompts}
    assert types == TASK_TYPES
    for kind in TASK_TYPES:
        assert sum(1 for p in prompts if p["type"] == kind) == 6
    assert all(p["text"].strip() for p in prompts)
    # The h mark keeps the ids disjoint from the main set under any
    # growth, and the per-type tables still resolve the type.
    for prompt in prompts:
        assert re.fullmatch(rf"{re.escape(prompt['type'])}-h\d{{2}}", prompt["id"])
        assert task_type(prompt["id"]) == prompt["type"]
    main_ids = {p["id"] for p in yaml.safe_load(PROMPTS.read_text())["prompts"]}
    assert not main_ids & set(ids)


def make_plugin(root, name="test-plugin", styles=("alpha",)):
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": name}))
    style_dir = root / "output-styles"
    style_dir.mkdir()
    for style in styles:
        (style_dir / f"{style}.md").write_text(f"# {style}\n")
    return root


def test_style_reference_is_plugin_qualified(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    assert style_reference(plugin, "alpha") == "test-plugin:alpha"


def test_build_argv_styled(tmp_path):
    plugin = make_plugin(tmp_path / "plugin", styles=("plain-language",))
    argv = build_argv("prompt", "sonnet", "plain-language", plugin)
    assert argv[:3] == ["claude", "-p", "prompt"]
    assert argv[argv.index("--model") + 1] == "sonnet"
    assert argv[argv.index("--plugin-dir") + 1] == str(plugin)
    settings = json.loads(argv[argv.index("--settings") + 1])
    # The bare style name does not resolve; only the qualified form
    # injects the style.
    assert settings == {"disableAllHooks": True, "outputStyle": "test-plugin:plain-language"}
    assert "--disallowedTools" in argv
    assert "--no-session-persistence" in argv
    assert "--exclude-dynamic-system-prompt-sections" in argv


def test_build_argv_unstyled_forces_the_default_style():
    argv = build_argv("prompt", "sonnet", None, None)
    assert "--plugin-dir" not in argv
    settings = json.loads(argv[argv.index("--settings") + 1])
    assert settings == {"disableAllHooks": True, "outputStyle": "default"}


def test_generate_parses_the_stream(tmp_path):
    plugin = make_plugin(tmp_path / "plugin", styles=("plain-language",))

    def run(argv, cwd, env=None):
        return stream_output(
            output_style="test-plugin:plain-language",
            answer="the answer",
            plugins=("test-plugin",),
        )

    result = generate("prompt", "sonnet", "plain-language", plugin, tmp_path, run=run)
    assert result.answer == "the answer"
    assert result.output_style == "test-plugin:plain-language"
    assert result.resolved_model == "claude-sonnet-5"
    assert result.output_tokens == 7
    assert result.input_tokens == 3
    assert result.cache_creation_input_tokens == 2
    assert result.cache_read_input_tokens == 1
    assert result.plugins == ("test-plugin",)
    assert isinstance(result.wall_ms, int)


def test_generate_rejects_a_wrong_active_style(tmp_path):
    plugin = make_plugin(tmp_path / "plugin", styles=("plain-language",))

    def run(argv, cwd, env=None):
        return stream_output(output_style="default", plugins=("test-plugin",))

    with pytest.raises(GenerationError, match="output style"):
        generate("prompt", "sonnet", "plain-language", plugin, tmp_path, run=run)


def test_generate_rejects_an_error_result(tmp_path):
    def run(argv, cwd, env=None):
        return stream_output(answer="Not logged in", is_error=True)

    with pytest.raises(GenerationError, match="error"):
        generate("prompt", "sonnet", None, None, tmp_path, run=run)


def test_generate_rejects_an_undeclared_plugin(tmp_path):
    plugin = make_plugin(tmp_path / "plugin", styles=("plain-language",))

    def run(argv, cwd, env=None):
        return stream_output(
            output_style="test-plugin:plain-language",
            plugins=("test-plugin", "user-plugin"),
        )

    with pytest.raises(PluginLeakError, match="user-plugin"):
        generate("prompt", "sonnet", "plain-language", plugin, tmp_path, run=run)


def test_generate_unstyled_rejects_any_plugin(tmp_path):
    def run(argv, cwd, env=None):
        return stream_output(plugins=("user-plugin",))

    with pytest.raises(PluginLeakError, match="user-plugin"):
        generate("prompt", "sonnet", None, None, tmp_path, run=run)


def make_pairs_project(tmp_path, monkeypatch, prompts):
    (tmp_path / "prompts.yaml").write_text(yaml.safe_dump({"prompts": prompts}))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "alpha.rules.yaml").write_text("style: alpha\n")
    make_plugin(tmp_path / "plugin")
    monkeypatch.setattr(cli, "claude_version", lambda *args: "0.0.0 (test)")
    return tmp_path


@pytest.fixture
def project(tmp_path, monkeypatch):
    """A minimal project: 2 prompts, 1 style, a plugin directory."""
    prompts = [
        {"id": "explanation-01", "type": "explanation", "text": "Explain A."},
        {"id": "debugging-01", "type": "debugging", "text": "Debug B."},
    ]
    return make_pairs_project(tmp_path, monkeypatch, prompts)


@pytest.fixture
def screening_project(tmp_path, monkeypatch):
    """Like project, but with 3 prompts per type, so the subset reduces."""
    prompts = [
        {"id": f"{task_type}-{n:02d}", "type": task_type, "text": f"{task_type} {n}."}
        for task_type in ("explanation", "debugging")
        for n in (1, 2, 3)
    ]
    return make_pairs_project(tmp_path, monkeypatch, prompts)


def run_cli(project, runner, out="run", *extra):
    return cli.main(
        [
            "--prompts",
            str(project / "prompts.yaml"),
            "--rules-dir",
            str(project / "rules"),
            "--plugin-dir",
            str(project / "plugin"),
            "--out",
            str(project / out),
            *extra,
        ],
        run=runner,
    )


def run_cli_default_out(project, runner, *extra):
    """Invoke the CLI without --out; the caller must chdir into the project."""
    return cli.main(
        [
            "--prompts",
            str(project / "prompts.yaml"),
            "--rules-dir",
            str(project / "rules"),
            "--plugin-dir",
            str(project / "plugin"),
            *extra,
        ],
        run=runner,
    )


def test_cli_produces_a_complete_run(project):
    runner = FakeRunner()
    assert run_cli(project, runner) == 0
    assert len(runner.calls) == 4  # 2 prompts x (unstyled + alpha)

    out = project / "run"
    answers = [json.loads(line) for line in (out / "answers.jsonl").read_text().splitlines()]
    assert {(a["prompt_id"], a["style"]) for a in answers} == {
        ("explanation-01", None),
        ("debugging-01", None),
        ("explanation-01", "alpha"),
        ("debugging-01", "alpha"),
    }
    assert all(
        (a["input_tokens"], a["cache_creation_input_tokens"], a["cache_read_input_tokens"])
        == (3, 2, 1)
        for a in answers
    )
    assert all(isinstance(a["wall_ms"], int) for a in answers)
    provenance = json.loads((out / "provenance.json").read_text())
    assert provenance["styles"]["alpha"]["sha256"]
    report = (out / "report.md").read_text()
    assert "| unstyled | 2/2 | none |" in report
    assert "| alpha | 2/2 | none |" in report
    assert "## Call timing" in report
    assert "## Harness spend" in report
    assert "Input tokens: 12 uncached, 8 cache write, 4 cache read. Output tokens: 28." in report


def test_report_states_not_measured_for_rows_without_wall(project):
    runner = FakeRunner()
    run_cli(project, runner)
    out = project / "run"
    rows = [json.loads(line) for line in (out / "answers.jsonl").read_text().splitlines()]
    for row in rows:
        row.pop("wall_ms", None)
    prompts = yaml.safe_load((project / "prompts.yaml").read_text())["prompts"]
    provenance = json.loads((out / "provenance.json").read_text())
    report = build_report(prompts, ["alpha"], rows, provenance, [])
    assert "The wall is not measured" in report


def test_cli_resumes_and_only_runs_the_missing_answers(project):
    first = FakeRunner()
    run_cli(project, first)
    answers_path = project / "run" / "answers.jsonl"
    lines = answers_path.read_text().splitlines()
    answers_path.write_text("\n".join(lines[:1]) + "\n")

    second = FakeRunner()
    assert run_cli(project, second) == 0
    assert len(second.calls) == 3
    assert len(answers_path.read_text().splitlines()) == 4


def test_cli_runs_the_calls_in_parallel(project):
    # All 4 calls must be live at once to pass the barrier. A serial
    # runner blocks on the first call, the barrier times out, and the
    # test fails.
    barrier = threading.Barrier(4, timeout=10)

    class BlockingRunner(FakeRunner):
        def __call__(self, argv, cwd, env=None):
            barrier.wait()
            return super().__call__(argv, cwd, env)

    runner = BlockingRunner()
    assert run_cli(project, runner) == 0
    assert len(runner.calls) == 4


def test_cli_with_parallel_one_runs_serially(project):
    live = {"now": 0, "peak": 0}
    lock = threading.Lock()

    class CountingRunner(FakeRunner):
        def __call__(self, argv, cwd, env=None):
            with lock:
                live["now"] += 1
                live["peak"] = max(live["peak"], live["now"])
            try:
                return super().__call__(argv, cwd, env)
            finally:
                with lock:
                    live["now"] -= 1

    runner = CountingRunner()
    assert run_cli(project, runner, "run", "--parallel", "1") == 0
    assert len(runner.calls) == 4
    assert live["peak"] == 1


def test_cli_rejects_a_parallel_below_one(project):
    with pytest.raises(SystemExit, match="--parallel"):
        run_cli(project, FakeRunner(), "run", "--parallel", "0")


def test_cli_calls_run_in_a_workdir_outside_the_project(project):
    seen = []

    class WorkdirProbe(FakeRunner):
        def __call__(self, argv, cwd, env=None):
            seen.append((Path(cwd), Path(cwd).is_dir()))
            return super().__call__(argv, cwd, env)

    assert run_cli(project, WorkdirProbe()) == 0
    assert seen
    workdirs = {cwd for cwd, _ in seen}
    assert len(workdirs) == 1
    assert all(existed for _, existed in seen)
    workdir = workdirs.pop()
    assert project.resolve() not in workdir.resolve().parents
    assert not workdir.exists()


def test_cli_same_day_repeats_pick_the_next_letter_suffix(project, monkeypatch, capsys):
    monkeypatch.chdir(project)
    date = datetime.now(UTC).strftime("%Y-%m-%d")

    first = FakeRunner()
    assert run_cli_default_out(project, first) == 0
    assert len(first.calls) == 4
    assert (project / "runs" / date / "answers.jsonl").exists()

    second = FakeRunner()
    assert run_cli_default_out(project, second) == 0
    assert len(second.calls) == 4
    assert (project / "runs" / f"{date}b" / "answers.jsonl").exists()
    assert f"runs/{date} is complete; starting" in capsys.readouterr().err

    third = FakeRunner()
    assert run_cli_default_out(project, third) == 0
    assert len(third.calls) == 4
    assert (project / "runs" / f"{date}c" / "answers.jsonl").exists()


def test_cli_a_same_day_incomplete_run_still_resumes(project, monkeypatch):
    monkeypatch.chdir(project)
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    first = FakeRunner()
    assert run_cli_default_out(project, first) == 0
    answers_path = project / "runs" / date / "answers.jsonl"
    lines = answers_path.read_text().splitlines()
    answers_path.write_text("\n".join(lines[:1]) + "\n")

    second = FakeRunner()
    assert run_cli_default_out(project, second) == 0
    assert len(second.calls) == 3
    assert len(answers_path.read_text().splitlines()) == 4
    assert not (project / "runs" / f"{date}b").exists()


def test_pick_default_out_refuses_when_every_suffix_is_complete(tmp_path):
    prompts = [{"id": "p1"}]
    arms = [None]
    runs = tmp_path / "runs"
    for suffix in ("", *ascii_lowercase[1:]):
        run_dir = runs / f"2026-01-01{suffix}"
        run_dir.mkdir(parents=True)
        answer = {"prompt_id": "p1", "style": None}
        (run_dir / "answers.jsonl").write_text(json.dumps(answer) + "\n")
    with pytest.raises(SystemExit, match="--out"):
        cli.pick_default_out(runs, "2026-01-01", arms, prompts)


def test_cli_reports_a_failed_call_and_keeps_going(project):
    def failing_runner(argv, cwd, env=None):
        if style_of(argv) == "alpha":
            # The style did not activate.
            return stream_output(output_style="default", plugins=("test-plugin",))
        return stream_output()

    assert run_cli(project, failing_runner) == 1
    report = (project / "run" / "report.md").read_text()
    assert "Failed call: alpha/" in report
    assert "| unstyled | 2/2 | none |" in report
    assert "| alpha | 0/2 |" in report


def test_screening_subset_is_deterministic_and_balanced():
    prompts = yaml.safe_load(PROMPTS.read_text())["prompts"]
    first = select_screening_prompts(prompts)
    second = select_screening_prompts(prompts)
    assert first == second
    assert len(first) == 8
    counts = Counter(prompt["type"] for prompt in first)
    assert counts == {task_type: 2 for task_type in TASK_TYPES}
    ids = [prompt["id"] for prompt in prompts]
    positions = [ids.index(prompt["id"]) for prompt in first]
    assert positions == sorted(positions)


def test_screening_keeps_a_small_type_whole():
    prompts = [
        {"id": "explanation-01", "type": "explanation", "text": "Explain A."},
        {"id": "debugging-01", "type": "debugging", "text": "Debug B."},
    ]
    assert select_screening_prompts(prompts) == prompts


def test_screening_section_is_empty_without_the_block():
    assert screening_section(None) == []
    assert screening_section({"date": "2026-08-06"}) == []


def test_screening_section_states_the_design_fractions():
    subset = [{"id": f"p{index}"} for index in range(8)]
    provenance = {"screening": screening_provenance(subset, 20)}
    text = "\n".join(screening_section(provenance))
    assert "8 of 20 prompts" in text
    assert "13% of a full campaign" in text
    assert "40%" in text
    assert "design numbers" in text


def test_cli_screening_run_marks_the_provenance(screening_project):
    runner = FakeRunner()
    assert run_cli(screening_project, runner, "run", "--screening") == 0
    prompts = yaml.safe_load((screening_project / "prompts.yaml").read_text())["prompts"]
    subset = select_screening_prompts(prompts)
    assert len(subset) == 4
    assert len(runner.calls) == 8  # 4 prompts x (unstyled + alpha)

    out = screening_project / "run"
    answers = [json.loads(line) for line in (out / "answers.jsonl").read_text().splitlines()]
    assert {a["prompt_id"] for a in answers} == {prompt["id"] for prompt in subset}
    provenance = json.loads((out / "provenance.json").read_text())
    assert provenance["screening"] == {
        "prompts_per_type": 2,
        "seed": 0,
        "prompt_ids": sorted(prompt["id"] for prompt in subset),
        "full_prompt_count": 6,
    }
    report = (out / "report.md").read_text()
    assert "**Screening run.** This run covers 4 of 6 prompts" in report


def test_cli_full_run_carries_no_screening_mark(project):
    assert run_cli(project, FakeRunner()) == 0
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    assert "screening" not in provenance
    assert "**Screening run.**" not in (project / "run" / "report.md").read_text()


def test_cli_a_screening_run_uses_its_own_directory_family(project, monkeypatch):
    monkeypatch.chdir(project)
    date = datetime.now(UTC).strftime("%Y-%m-%d")

    assert run_cli_default_out(project, FakeRunner(), "--screening") == 0
    assert (project / "runs" / f"{date}-screening" / "answers.jsonl").exists()

    assert run_cli_default_out(project, FakeRunner()) == 0
    assert (project / "runs" / date / "answers.jsonl").exists()

    assert run_cli_default_out(project, FakeRunner(), "--screening") == 0
    assert (project / "runs" / f"{date}b-screening" / "answers.jsonl").exists()


def test_cli_rejects_a_mode_mismatch_on_resume(project):
    assert run_cli(project, FakeRunner()) == 0
    with pytest.raises(SystemExit, match="full run"):
        run_cli(project, FakeRunner(), "run", "--screening")

    assert run_cli(project, FakeRunner(), "screening-run", "--screening") == 0
    with pytest.raises(SystemExit, match="screening run"):
        run_cli(project, FakeRunner(), "screening-run")


def test_cli_rejects_screening_answers_outside_the_subset(screening_project):
    assert run_cli(screening_project, FakeRunner()) == 0
    (screening_project / "run" / "provenance.json").unlink()
    with pytest.raises(SystemExit, match="outside the screening subset"):
        run_cli(screening_project, FakeRunner(), "run", "--screening")


def test_cli_rejects_screening_with_holdout(project):
    with pytest.raises(SystemExit, match="never uses the held-out set"):
        run_cli(project, FakeRunner(), "run", "--screening", "--holdout")


def test_cli_holdout_defaults_to_the_holdout_prompt_file(project, monkeypatch):
    monkeypatch.chdir(project)
    (project / "prompts").mkdir()
    holdout = [{"id": "explanation-h01", "type": "explanation", "text": "Explain H."}]
    (project / "prompts" / "holdout.yaml").write_text(yaml.safe_dump({"prompts": holdout}))
    argv = [
        "--rules-dir",
        str(project / "rules"),
        "--plugin-dir",
        str(project / "plugin"),
        "--out",
        str(project / "run"),
        "--holdout",
    ]
    assert cli.main(argv, run=FakeRunner()) == 0
    answers = [
        json.loads(line) for line in (project / "run" / "answers.jsonl").read_text().splitlines()
    ]
    assert {a["prompt_id"] for a in answers} == {"explanation-h01"}
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    assert provenance["prompt_set"]["path"] == "prompts/holdout.yaml"


def test_cli_a_holdout_run_uses_its_own_directory_family(project, monkeypatch):
    # run_cli_default_out passes an explicit --prompts, which also
    # pins that --prompts wins over the holdout default.
    monkeypatch.chdir(project)
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    assert run_cli_default_out(project, FakeRunner(), "--holdout") == 0
    assert (project / "runs" / f"{date}-holdout" / "answers.jsonl").exists()
    assert not (project / "runs" / date).exists()


def test_cli_rejects_a_prompt_set_mismatch_on_resume(project):
    assert run_cli(project, FakeRunner()) == 0
    provenance_path = project / "run" / "provenance.json"
    provenance = json.loads(provenance_path.read_text())
    provenance["prompt_set"]["sha256"] = "0" * 64
    provenance_path.write_text(json.dumps(provenance))
    with pytest.raises(SystemExit, match="another prompt set"):
        run_cli(project, FakeRunner())


def test_provenance_holds_the_linter_toolchain(project):
    provenance = build_provenance(
        model="sonnet",
        prompts_path=project / "prompts.yaml",
        styles=["alpha"],
        plugin_dir=project / "plugin",
        cli_version="0.0.0 (test)",
    )
    toolchain = provenance["linter_toolchain"]
    assert toolchain["spacy"] == metadata.version("spacy")
    assert toolchain["en-core-web-sm"] == metadata.version("en-core-web-sm")
    assert provenance["prompt_set"]["sha256"]
    assert provenance["conditions"]["model_requested"] == "sonnet"
    assert provenance["conditions"]["workdir"] == "temp"
    assert "--disallowedTools" in provenance["conditions"]["flags"]


def test_provenance_holds_the_config_fields(project):
    runner = FakeRunner()
    assert run_cli(project, runner) == 0
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    conditions = provenance["conditions"]
    assert conditions["config"] == "hermetic"
    assert conditions["config_manifest_sha256"] == manifest_sha256()
    assert "claude_binary" in conditions
    assert "CLAUDE_CONFIG_DIR" in conditions["env_passed"]
    # The names of the variables land here, never the values.
    assert all(isinstance(name, str) and "/" not in name for name in conditions["env_passed"])


def test_cli_reuse_imports_the_source_answers(project):
    run_cli(project, FakeRunner(), "source")
    second = FakeRunner()
    assert run_cli(project, second, "run", "--reuse-from", str(project / "source")) == 0
    assert second.calls == []
    answers = [
        json.loads(line) for line in (project / "run" / "answers.jsonl").read_text().splitlines()
    ]
    assert len(answers) == 4
    assert all(answer["reused_from"] == "source" for answer in answers)
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    assert provenance["reuse"] == {"source": "source", "imported_answers": 4}
    report = (project / "run" / "report.md").read_text()
    assert "- Answers imported from source: 4 (generated live: 0)" in report


def test_cli_reuse_generates_only_the_new_style(project):
    run_cli(project, FakeRunner(), "source")
    (project / "rules" / "beta.rules.yaml").write_text("style: beta\n")
    (project / "plugin" / "output-styles" / "beta.md").write_text("Beta style.\n")
    second = FakeRunner()
    assert run_cli(project, second, "run", "--reuse-from", str(project / "source")) == 0
    assert len(second.calls) == 2
    assert all(style_of(argv) == "test-plugin:beta" for argv in second.calls)
    answers = {
        (a["prompt_id"], a["style"]): a
        for a in map(json.loads, (project / "run" / "answers.jsonl").read_text().splitlines())
    }
    assert len(answers) == 6
    assert "reused_from" not in answers[("explanation-01", "beta")]
    assert answers[("explanation-01", "alpha")]["reused_from"] == "source"
    assert answers[("explanation-01", None)]["reused_from"] == "source"


def test_cli_reuse_regenerates_a_changed_style(project):
    run_cli(project, FakeRunner(), "source")
    (project / "plugin" / "output-styles" / "alpha.md").write_text("Changed alpha.\n")
    second = FakeRunner()
    assert run_cli(project, second, "run", "--reuse-from", str(project / "source")) == 0
    assert len(second.calls) == 2
    answers = {
        (a["prompt_id"], a["style"]): a
        for a in map(json.loads, (project / "run" / "answers.jsonl").read_text().splitlines())
    }
    assert "reused_from" not in answers[("explanation-01", "alpha")]
    assert answers[("explanation-01", None)]["reused_from"] == "source"


def test_cli_reuse_rejects_another_prompt_set(project):
    run_cli(project, FakeRunner(), "source")
    prompts = [
        {"id": "explanation-01", "type": "explanation", "text": "Explain C."},
        {"id": "debugging-01", "type": "debugging", "text": "Debug D."},
    ]
    (project / "prompts.yaml").write_text(yaml.safe_dump({"prompts": prompts}))
    with pytest.raises(SystemExit, match="another prompt set"):
        run_cli(project, FakeRunner(), "run", "--reuse-from", str(project / "source"))


def test_cli_reuse_rejects_another_model(project):
    run_cli(project, FakeRunner(), "source")
    with pytest.raises(SystemExit, match="the model"):
        run_cli(
            project, FakeRunner(), "run", "--model", "opus", "--reuse-from", str(project / "source")
        )


def test_cli_reuse_rejects_a_screening_mismatch(screening_project):
    run_cli(screening_project, FakeRunner(), "source")
    with pytest.raises(SystemExit, match="screening"):
        run_cli(
            screening_project,
            FakeRunner(),
            "run",
            "--screening",
            "--reuse-from",
            str(screening_project / "source"),
        )


def test_cli_reuse_rejects_the_run_itself(project):
    run_cli(project, FakeRunner(), "source")
    with pytest.raises(SystemExit, match="the run itself"):
        run_cli(project, FakeRunner(), "source", "--reuse-from", str(project / "source"))


def test_cli_reuse_needs_a_source_with_provenance(project):
    (project / "empty").mkdir()
    with pytest.raises(SystemExit, match="not a run"):
        run_cli(project, FakeRunner(), "run", "--reuse-from", str(project / "empty"))


def test_cli_reuse_imports_only_the_missing_pairs(project):
    run_cli(project, FakeRunner(), "source")
    run_cli(project, FakeRunner(), "run")
    answers_path = project / "run" / "answers.jsonl"
    lines = answers_path.read_text().splitlines()
    answers_path.write_text("\n".join(lines[:1]) + "\n")

    second = FakeRunner()
    assert run_cli(project, second, "run", "--reuse-from", str(project / "source")) == 0
    assert second.calls == []
    answers = [json.loads(line) for line in answers_path.read_text().splitlines()]
    assert len(answers) == 4
    assert len({(a["prompt_id"], a["style"]) for a in answers}) == 4
    assert sum(1 for a in answers if "reused_from" in a) == 3

    third = FakeRunner()
    assert run_cli(project, third, "run", "--reuse-from", str(project / "source")) == 0
    assert third.calls == []
    assert len(answers_path.read_text().splitlines()) == 4


def test_cli_without_reuse_writes_no_reuse_marks(project):
    assert run_cli(project, FakeRunner()) == 0
    answers = [
        json.loads(line) for line in (project / "run" / "answers.jsonl").read_text().splitlines()
    ]
    assert all("reused_from" not in answer for answer in answers)
    assert "reuse" not in json.loads((project / "run" / "provenance.json").read_text())
    assert "imported" not in (project / "run" / "report.md").read_text()
