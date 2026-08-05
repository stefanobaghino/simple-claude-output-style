"""Tests for the pair runner. No test touches the network: the claude
subprocess is replaced with a fake runner that returns canned
stream-json output."""

import json
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from string import ascii_lowercase

import pytest
import yaml

from runner import GenerationError, build_argv, cli, generate, style_reference
from runner.provenance import build_provenance

HERE = Path(__file__).parent
PROMPTS = HERE.parent / "prompts" / "prompts.yaml"

TASK_TYPES = {"explanation", "code-review", "summarization", "debugging"}


def stream_output(output_style="default", answer="ok", is_error=False):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": "claude-sonnet-5",
        "claude_code_version": "2.1.220",
        "plugins": [{"name": "simple-output-styles"}],
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

    def __call__(self, argv, cwd):
        self.calls.append(argv)
        style = style_of(argv)
        return stream_output(output_style=style or "default", answer=f"answer under {style}")


def test_prompt_set_is_complete():
    prompts = yaml.safe_load(PROMPTS.read_text())["prompts"]
    assert len(prompts) == 20
    ids = [p["id"] for p in prompts]
    assert len(set(ids)) == 20
    types = {p["type"] for p in prompts}
    assert types == TASK_TYPES
    for task_type in TASK_TYPES:
        assert sum(1 for p in prompts if p["type"] == task_type) == 5
    assert all(p["text"].strip() for p in prompts)


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

    def run(argv, cwd):
        return stream_output(output_style="test-plugin:plain-language", answer="the answer")

    result = generate("prompt", "sonnet", "plain-language", plugin, tmp_path, run=run)
    assert result.answer == "the answer"
    assert result.output_style == "test-plugin:plain-language"
    assert result.resolved_model == "claude-sonnet-5"
    assert result.output_tokens == 7
    assert result.input_tokens == 3
    assert result.cache_creation_input_tokens == 2
    assert result.cache_read_input_tokens == 1
    assert result.plugins == ("simple-output-styles",)


def test_generate_rejects_a_wrong_active_style(tmp_path):
    plugin = make_plugin(tmp_path / "plugin", styles=("plain-language",))

    def run(argv, cwd):
        return stream_output(output_style="default")

    with pytest.raises(GenerationError, match="output style"):
        generate("prompt", "sonnet", "plain-language", plugin, tmp_path, run=run)


def test_generate_rejects_an_error_result(tmp_path):
    def run(argv, cwd):
        return stream_output(answer="Not logged in", is_error=True)

    with pytest.raises(GenerationError, match="error"):
        generate("prompt", "sonnet", None, None, tmp_path, run=run)


@pytest.fixture
def project(tmp_path, monkeypatch):
    """A minimal project: 2 prompts, 1 style, a plugin directory."""
    prompts = {
        "prompts": [
            {"id": "explanation-01", "type": "explanation", "text": "Explain A."},
            {"id": "debugging-01", "type": "debugging", "text": "Debug B."},
        ]
    }
    (tmp_path / "prompts.yaml").write_text(yaml.safe_dump(prompts))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "alpha.rules.yaml").write_text("style: alpha\n")
    make_plugin(tmp_path / "plugin")
    monkeypatch.setattr(cli, "claude_version", lambda: "0.0.0 (test)")
    return tmp_path


def run_cli(project, runner, out="run"):
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
        ],
        run=runner,
    )


def run_cli_default_out(project, runner):
    """Invoke the CLI without --out; the caller must chdir into the project."""
    return cli.main(
        [
            "--prompts",
            str(project / "prompts.yaml"),
            "--rules-dir",
            str(project / "rules"),
            "--plugin-dir",
            str(project / "plugin"),
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
    provenance = json.loads((out / "provenance.json").read_text())
    assert provenance["styles"]["alpha"]["sha256"]
    report = (out / "report.md").read_text()
    assert "| unstyled | 2/2 | none |" in report
    assert "| alpha | 2/2 | none |" in report


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


def test_cli_calls_run_in_a_workdir_outside_the_project(project):
    seen = []

    class WorkdirProbe(FakeRunner):
        def __call__(self, argv, cwd):
            seen.append((Path(cwd), Path(cwd).is_dir()))
            return super().__call__(argv, cwd)

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
    def failing_runner(argv, cwd):
        if style_of(argv) == "alpha":
            return stream_output(output_style="default")  # style did not activate
        return stream_output()

    assert run_cli(project, failing_runner) == 1
    report = (project / "run" / "report.md").read_text()
    assert "Failed call: alpha/" in report
    assert "| unstyled | 2/2 | none |" in report
    assert "| alpha | 0/2 |" in report


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
