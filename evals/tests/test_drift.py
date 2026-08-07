"""Tests for the drift measurement. The linter runs for real; no test
touches the network: the claude subprocess is replaced with a fake
runner that returns canned stream-json output with session ids."""

import json
from pathlib import Path

import pytest
import yaml

from drift import (
    SESSION_FLAGS,
    build_session_argv,
    cli,
    deep_script,
    generate_turn,
    load_session_script,
    run_session,
    score_sessions,
    session_script,
)
from linter import Linter, load_rules
from runner.cli import load_prompts
from runner.generate import GenerationError, PluginLeakError

HERE = Path(__file__).parent
PROMPTS = HERE.parent / "prompts" / "prompts.yaml"

CLEAN = "The test passed. The build works. The cache is warm. The log is empty."


def growing_answer(turn):
    """Four sentences; turn - 1 of them hold a contraction."""
    dirty = ["It doesn't work."] * (turn - 1)
    clean = ["The test passed."] * (4 - (turn - 1))
    return " ".join(dirty + clean)


def stream_output(
    output_style="test-plugin:alpha",
    answer="ok",
    session_id="sid-1",
    init_session_id=None,
    is_error=False,
    plugins=("test-plugin",),
):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": "claude-sonnet-5",
        "claude_code_version": "2.1.220",
        "plugins": [{"name": name} for name in plugins],
    }
    if init_session_id is not None:
        init["session_id"] = init_session_id
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
        "duration_ms": 100,
    }
    if session_id is not None:
        result["session_id"] = session_id
    return "\n".join(json.dumps(event) for event in (init, result))


def style_of(argv):
    settings = json.loads(argv[argv.index("--settings") + 1])
    return settings.get("outputStyle")


def resume_of(argv):
    return argv[argv.index("--resume") + 1] if "--resume" in argv else None


class FakeSessionRunner:
    """Emits a fresh session id per call and tracks the turn number
    inside the current session, so the answer can vary per turn."""

    def __init__(self, answer_for=lambda turn: CLEAN):
        self.calls = []
        self.answer_for = answer_for
        self.count = 0
        self.turn = 0

    def __call__(self, argv, cwd, env=None):
        self.calls.append(argv)
        self.count += 1
        self.turn = 1 if "--resume" not in argv else self.turn + 1
        return stream_output(
            output_style=style_of(argv),
            answer=self.answer_for(self.turn),
            session_id=f"sid-{self.count}",
        )


def make_plugin(root, name="test-plugin", styles=("alpha",)):
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": name}))
    style_dir = root / "output-styles"
    style_dir.mkdir()
    for style in styles:
        (style_dir / f"{style}.md").write_text(f"# {style}\n")
    return root


def test_session_script_rotates_per_repeat():
    prompts = load_prompts(PROMPTS)
    base = session_script(prompts, 15, 1, 3)
    assert len(base) == 15
    assert session_script(prompts, 15, 2, 3) == base[5:] + base[:5]
    assert session_script(prompts, 15, 3, 3) == base[10:] + base[:10]


def test_session_script_interleaves_task_types():
    prompts = load_prompts(PROMPTS)
    base = session_script(prompts, 15, 1, 3)
    assert len({prompt["type"] for prompt in base[:4]}) == 4
    assert len({prompt["type"] for prompt in base[4:8]}) == 4


def test_session_script_rejects_too_few_prompts():
    prompts = load_prompts(PROMPTS)
    turns = len(prompts) + 1
    with pytest.raises(ValueError, match=f"{turns} prompts"):
        session_script(prompts, turns, 1, 3)


def test_build_session_argv_first_turn(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    argv = build_session_argv("prompt", "sonnet", "alpha", plugin, None)
    assert argv[:3] == ["claude", "-p", "prompt"]
    assert "--resume" not in argv
    assert "--no-session-persistence" not in argv
    assert "--no-session-persistence" not in SESSION_FLAGS
    assert argv[argv.index("--max-turns") + 1] == "1"
    assert "--disallowedTools" in argv
    settings = json.loads(argv[argv.index("--settings") + 1])
    assert settings == {"disableAllHooks": True, "outputStyle": "test-plugin:alpha"}


def test_build_session_argv_resumed_turn(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    argv = build_session_argv("prompt", "sonnet", "alpha", plugin, "sid-7")
    assert argv[argv.index("--resume") + 1] == "sid-7"
    assert argv[argv.index("--max-turns") + 1] == "1"


def test_generate_turn_captures_session_id(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        return stream_output(answer="the answer", session_id="sid-9")

    turn = generate_turn("prompt", "sonnet", "alpha", plugin, tmp_path, None, run=run)
    assert turn.answer == "the answer"
    assert turn.session_id == "sid-9"
    assert turn.resume_from is None
    assert turn.output_tokens == 7
    assert isinstance(turn.wall_ms, int)


def test_generate_turn_rejects_missing_session_id(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        return stream_output(session_id=None)

    with pytest.raises(GenerationError, match="session id"):
        generate_turn("prompt", "sonnet", "alpha", plugin, tmp_path, None, run=run)


def test_generate_turn_verifies_style_each_turn(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        return stream_output(output_style="default")

    with pytest.raises(GenerationError, match="output style"):
        generate_turn("prompt", "sonnet", "alpha", plugin, tmp_path, "sid-1", run=run)


def test_turn_rejects_an_undeclared_plugin(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        return stream_output(plugins=("test-plugin", "user-plugin"))

    with pytest.raises(PluginLeakError, match="user-plugin"):
        generate_turn("prompt", "sonnet", "alpha", plugin, tmp_path, None, run=run)


def test_run_session_chains_forked_session_ids(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    runner = FakeSessionRunner()
    script = [{"id": f"p{n}", "type": "explanation", "text": f"prompt {n}"} for n in range(1, 4)]
    recorded = []
    run_session(
        script,
        "sonnet",
        "alpha",
        plugin,
        tmp_path,
        runner,
        lambda number, prompt, turn: recorded.append((number, prompt["id"], turn)),
    )
    assert [resume_of(argv) for argv in runner.calls] == [None, "sid-1", "sid-2"]
    assert [turn.session_id for _, _, turn in recorded] == ["sid-1", "sid-2", "sid-3"]
    assert [turn.resume_from for _, _, turn in recorded] == [None, "sid-1", "sid-2"]


@pytest.fixture
def project(tmp_path, monkeypatch):
    """A minimal project: 4 prompts, 1 style with a contraction rule."""
    prompts = {
        "prompts": [
            {"id": "explanation-01", "type": "explanation", "text": "Explain A."},
            {"id": "code-review-01", "type": "code-review", "text": "Review B."},
            {"id": "summarization-01", "type": "summarization", "text": "Summarize C."},
            {"id": "debugging-01", "type": "debugging", "text": "Debug D."},
        ]
    }
    (tmp_path / "prompts.yaml").write_text(yaml.safe_dump(prompts))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "alpha.rules.yaml").write_text("style: alpha\ncontractions:\n  banned: true\n")
    make_plugin(tmp_path / "plugin")
    monkeypatch.setattr(cli, "claude_version", lambda *args: "0.0.0 (test)")
    return tmp_path


def run_cli(project, runner, *extra, generate=True, turns="3"):
    argv = [
        "--prompts",
        str(project / "prompts.yaml"),
        "--rules-dir",
        str(project / "rules"),
        "--plugin-dir",
        str(project / "plugin"),
        "--out",
        str(project / "run"),
        "--repeats",
        "2",
        *extra,
    ]
    if turns is not None:
        argv += ["--turns", turns]
    if generate:
        argv.append("--generate")
    return cli.main(argv, run=runner)


def load_rows(project):
    path = project / "run" / "sessions.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_cli_generates_complete_sessions(project):
    runner = FakeSessionRunner()
    assert run_cli(project, runner) == 0
    assert len(runner.calls) == 6  # 1 style x 2 repeats x 3 turns

    rows = load_rows(project)
    assert {(r["style"], r["repeat"], r["turn"]) for r in rows} == {
        ("alpha", repeat, turn) for repeat in (1, 2) for turn in (1, 2, 3)
    }
    assert all(r["session_id"] for r in rows)
    assert all(isinstance(r["wall_ms"], int) for r in rows)

    provenance = json.loads((project / "run" / "provenance.json").read_text())
    assert "--no-session-persistence" not in provenance["conditions"]["flags"]
    assert "--max-turns" in provenance["conditions"]["flags"]
    assert provenance["drift"]["turns"] == 3
    assert provenance["drift"]["repeats"] == 2
    script = provenance["drift"]["script"]
    assert len(script["1"]) == 3
    assert sorted(script["1"]) == sorted(script["2"])
    assert script["1"] != script["2"]


def test_cli_skips_complete_and_restarts_incomplete_sessions(project):
    first = FakeSessionRunner()
    run_cli(project, first)
    sessions_path = project / "run" / "sessions.jsonl"
    kept = [
        line
        for line in sessions_path.read_text().splitlines()
        if not (json.loads(line)["repeat"] == 2 and json.loads(line)["turn"] == 3)
    ]
    sessions_path.write_text("\n".join(kept) + "\n")

    second = FakeSessionRunner()
    assert run_cli(project, second) == 0
    # Session 1 is complete and is skipped; session 2 restarts from turn 1.
    assert len(second.calls) == 3
    assert resume_of(second.calls[0]) is None

    rows = {(r["repeat"], r["turn"]): r for r in load_rows(project)}
    assert rows[(2, 1)]["session_id"] == "sid-1"
    assert len(rows) == 6


def test_cli_rescoring_needs_no_runner(project):
    run_cli(project, FakeSessionRunner())

    idle = FakeSessionRunner()
    assert run_cli(project, idle, generate=False) == 0
    assert idle.calls == []

    first = json.loads((project / "run" / "drift.json").read_text())
    first_md = (project / "run" / "drift.md").read_text()
    assert run_cli(project, idle, generate=False) == 0
    second = json.loads((project / "run" / "drift.json").read_text())
    second_md = (project / "run" / "drift.md").read_text()
    del first["date"], second["date"]
    assert first == second
    assert first_md == second_md


def test_cli_without_sessions_and_without_generate_exits_2(project):
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), generate=False)
    assert excinfo.value.code == 2


def test_flat_series_gets_a_flat_verdict_and_exit_0(project, capsys):
    assert run_cli(project, FakeSessionRunner()) == 0
    out = capsys.readouterr().out
    assert "alpha: slope 0.0, threshold 0.0 (derived), verdict flat (2/2 session(s))" in out
    summary = json.loads((project / "run" / "drift.json").read_text())
    stats = summary["styles"]["alpha"]
    assert stats["verdict"] == "flat"
    assert stats["pooled_series"] == [0.0, 0.0, 0.0]
    assert stats["threshold"] == 0.0
    assert stats["threshold_source"] == "derived"
    assert stats["complete_sessions"] == 2
    assert summary["warnings"] == []


def test_growing_series_gets_a_growing_verdict_and_exit_1(project):
    assert run_cli(project, FakeSessionRunner(answer_for=growing_answer)) == 1
    summary = json.loads((project / "run" / "drift.json").read_text())
    stats = summary["styles"]["alpha"]
    # Four sentences per answer, turn - 1 contractions: rates 0, 25, 50.
    assert stats["pooled_series"] == [0.0, 25.0, 50.0]
    assert stats["slope"] == 25.0
    assert stats["threshold"] == 18.75
    assert stats["threshold_source"] == "derived"
    assert stats["null"] == {"permutations": 1000, "seed": 0, "quantile": 0.95, "threshold": 18.75}
    assert stats["verdict"] == "growing"
    rows = stats["turns"]
    assert {r["by_rule"].get("contraction", 0) for r in rows} == {0, 1, 2}


def test_incomplete_session_is_excluded_with_a_warning(project):
    run_cli(project, FakeSessionRunner())
    sessions_path = project / "run" / "sessions.jsonl"
    kept = [
        line
        for line in sessions_path.read_text().splitlines()
        if not (json.loads(line)["repeat"] == 2 and json.loads(line)["turn"] == 3)
    ]
    sessions_path.write_text("\n".join(kept) + "\n")

    assert run_cli(project, FakeSessionRunner(), generate=False) == 1
    summary = json.loads((project / "run" / "drift.json").read_text())
    assert summary["styles"]["alpha"]["complete_sessions"] == 1
    assert any("misses turn(s) 3" in warning for warning in summary["warnings"])


def test_report_md_holds_the_turn_table_and_verdict(project):
    run_cli(project, FakeSessionRunner())
    report = (project / "run" / "drift.md").read_text()
    assert "# Drift report" in report
    assert "| Turn | Pooled rate | Repeat 1 | Repeat 2 |" in report
    assert "- Slope threshold: 0.0 (the 0.95 quantile of 1000 shuffled slopes, seed 0)" in report
    assert "- Verdict: flat" in report
    assert "## Harness spend" in report
    assert "## Warnings" in report
    assert "- none" in report


def score_answers(project, answers, turns=3, repeats=2):
    """Score hand-built rows: answers maps (repeat, turn) to a text."""
    rows = {
        ("alpha", repeat, turn): {
            "style": "alpha",
            "repeat": repeat,
            "turn": turn,
            "prompt_id": "p",
            "answer": answer,
        }
        for (repeat, turn), answer in answers.items()
    }
    linter = Linter(load_rules(project / "rules" / "alpha.rules.yaml"))
    return score_sessions(rows=rows, linters={"alpha": linter}, turns=turns, repeats=repeats)


def test_pooling_weights_the_turns_by_sentence_count(project):
    # Turn 2 of repeat 1 has 1 sentence with 1 violation (rate 100),
    # and turn 2 of repeat 2 has 4 clean sentences (rate 0). The pool
    # is 1 violation over 5 sentences, not the mean of the rates.
    result = score_answers(
        project,
        {
            (1, 1): CLEAN,
            (1, 2): "It doesn't work.",
            (1, 3): CLEAN,
            (2, 1): CLEAN,
            (2, 2): CLEAN,
            (2, 3): CLEAN,
        },
    )
    stats = result.styles["alpha"]
    assert stats["sessions"][0]["series"] == [0.0, 100.0, 0.0]
    assert stats["pooled_series"] == [0.0, 20.0, 0.0]


def test_a_zero_sentence_turn_pools_to_zero_with_a_warning(project):
    result = score_answers(
        project,
        {
            (1, 1): CLEAN,
            (1, 2): "",
            (1, 3): CLEAN,
            (2, 1): CLEAN,
            (2, 2): "",
            (2, 3): CLEAN,
        },
    )
    stats = result.styles["alpha"]
    assert stats["pooled_series"] == [0.0, 0.0, 0.0]
    assert stats["verdict"] == "flat"
    assert sum("has no sentences" in warning for warning in result.warnings) == 2


def test_threshold_flag_overrides_the_derived_threshold(project, capsys):
    assert run_cli(project, FakeSessionRunner(answer_for=growing_answer)) == 1
    idle = FakeSessionRunner()
    assert run_cli(project, idle, "--slope-threshold", "30", generate=False) == 0
    assert idle.calls == []
    assert "threshold 30.0 (override)" in capsys.readouterr().out
    summary = json.loads((project / "run" / "drift.json").read_text())
    assert summary["slope_threshold"] == 30.0
    stats = summary["styles"]["alpha"]
    assert stats["threshold"] == 30.0
    assert stats["threshold_source"] == "override"
    assert stats["null"]["threshold"] == 18.75
    assert stats["verdict"] == "flat"
    report = (project / "run" / "drift.md").read_text()
    assert "- Slope threshold: 30.0 (override; the null quantile is 18.75)" in report


SESSIONS_DIR = HERE.parent / "prompts" / "sessions"


def make_script(path, script_id, turns=3):
    data = {
        "session": {
            "id": script_id,
            "description": "A test script.",
            "turns": [
                {"id": f"turn-{n:02d}", "text": f"The turn asks question {n}."}
                for n in range(1, turns + 1)
            ],
        }
    }
    path.write_text(yaml.safe_dump(data))
    return path


def test_load_session_script_loads_a_valid_file(tmp_path):
    path = make_script(tmp_path / "incident.yaml", "incident")
    script = load_session_script(path)
    assert script["id"] == "incident"
    assert script["path"] == str(path)
    assert [turn["id"] for turn in script["turns"]] == ["turn-01", "turn-02", "turn-03"]
    assert all(turn["text"] for turn in script["turns"])


@pytest.mark.parametrize(
    ("data", "match"),
    [
        ({"turns": []}, "session mapping"),
        ({"session": {"id": "", "turns": [{"id": "a", "text": "t"}] * 2}}, "non-empty id"),
        ({"session": {"id": "x", "turns": [{"id": "a", "text": "t"}]}}, "at least 2 turns"),
        (
            {"session": {"id": "x", "turns": [{"id": "a", "text": "t"}, {"id": "b"}]}},
            "turn 2 needs",
        ),
        (
            {
                "session": {
                    "id": "x",
                    "turns": [{"id": "a", "text": "t"}, {"id": "a", "text": "u"}],
                }
            },
            "duplicate turn id",
        ),
    ],
)
def test_load_session_script_rejects_a_contract_breach(tmp_path, data, match):
    path = tmp_path / "bad.yaml"
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match=match):
        load_session_script(path)


def test_deep_script_cycles_over_the_scripts_and_composes_ids(tmp_path):
    scripts = [
        load_session_script(make_script(tmp_path / "one.yaml", "one")),
        load_session_script(make_script(tmp_path / "two.yaml", "two")),
    ]
    first = deep_script(scripts, 1)
    assert [turn["id"] for turn in first] == ["one/turn-01", "one/turn-02", "one/turn-03"]
    assert deep_script(scripts, 2)[0]["id"] == "two/turn-01"
    assert deep_script(scripts, 3)[0]["id"] == "one/turn-01"
    assert first[0]["text"] == "The turn asks question 1."


def deep_args(project):
    one = make_script(project / "one.yaml", "one")
    two = make_script(project / "two.yaml", "two")
    return ("--scripts", str(one), str(two))


def test_cli_deep_generates_sessions_with_composed_ids(project):
    runner = FakeSessionRunner()
    assert run_cli(project, runner, *deep_args(project), turns=None) == 0
    assert len(runner.calls) == 6  # 1 style x 2 repeats x 3 turns

    rows = load_rows(project)
    assert {r["prompt_id"] for r in rows if r["repeat"] == 1} == {
        "one/turn-01",
        "one/turn-02",
        "one/turn-03",
    }
    assert {r["prompt_id"] for r in rows if r["repeat"] == 2} == {
        "two/turn-01",
        "two/turn-02",
        "two/turn-03",
    }
    # The row schema equals the shallow schema.
    assert set(rows[0]) == {
        "style",
        "repeat",
        "turn",
        "prompt_id",
        "session_id",
        "resume_from",
        "answer",
        "model",
        "claude_code_version",
        "output_tokens",
        "input_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
        "duration_ms",
        "wall_ms",
    }


def test_deep_provenance_holds_the_scripts_and_the_mapping(project):
    run_cli(project, FakeSessionRunner(), *deep_args(project), turns=None)
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    drift = provenance["drift"]
    assert drift["mode"] == "deep"
    assert drift["turns"] == 3
    assert set(drift["scripts"]) == {"one", "two"}
    for entry in drift["scripts"].values():
        assert entry["path"] and len(entry["sha256"]) == 64
    assert drift["repeat_scripts"] == {"1": "one", "2": "two"}
    assert drift["script"]["1"] == ["one/turn-01", "one/turn-02", "one/turn-03"]
    assert drift["script"]["2"] == ["two/turn-01", "two/turn-02", "two/turn-03"]
    assert provenance["prompt_set"] == {"path": None, "sha256": None}


def test_shallow_output_holds_no_deep_keys(project):
    run_cli(project, FakeSessionRunner())
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    assert "mode" not in provenance["drift"]
    assert "scripts" not in provenance["drift"]
    assert "repeat_scripts" not in provenance["drift"]
    assert provenance["prompt_set"]["sha256"]
    summary = json.loads((project / "run" / "drift.json").read_text())
    assert "mode" not in summary
    assert "scripts" not in summary


def test_cli_rejects_turns_with_scripts(project, capsys):
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), *deep_args(project))
    assert excinfo.value.code == 2
    assert "the scripts fix the turn count" in capsys.readouterr().err


def test_cli_rejects_scripts_of_unequal_length(project):
    one = make_script(project / "one.yaml", "one", turns=3)
    two = make_script(project / "two.yaml", "two", turns=4)
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), "--scripts", str(one), str(two), turns=None)
    assert excinfo.value.code == 2


def test_cli_rejects_duplicate_script_ids(project):
    one = make_script(project / "one.yaml", "same")
    two = make_script(project / "two.yaml", "same")
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), "--scripts", str(one), str(two), turns=None)
    assert excinfo.value.code == 2


def test_cli_rejects_repeats_that_do_not_spread_over_the_scripts(project):
    scripts = [str(make_script(project / f"s{n}.yaml", f"s{n}")) for n in (1, 2, 3)]
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), "--scripts", *scripts, turns=None)
    assert excinfo.value.code == 2


def test_cli_shallow_default_is_15_turns(project, capsys):
    # The project set holds 4 prompts, so the default of 15 turns
    # fails with a message that names the default.
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), turns=None)
    assert excinfo.value.code == 2
    assert "15 turns need 15 prompts" in capsys.readouterr().err


def test_cli_rejects_a_mode_mismatch_on_the_run_directory(project, capsys):
    run_cli(project, FakeSessionRunner())
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner(), *deep_args(project), turns=None)
    assert excinfo.value.code == 2
    assert "shallow run" in capsys.readouterr().err


def test_cli_rejects_a_shallow_invocation_on_a_deep_run(project, capsys):
    run_cli(project, FakeSessionRunner(), *deep_args(project), turns=None)
    with pytest.raises(SystemExit) as excinfo:
        run_cli(project, FakeSessionRunner())
    assert excinfo.value.code == 2
    assert "deep run" in capsys.readouterr().err


def test_cli_deep_skips_complete_and_restarts_incomplete_sessions(project):
    run_cli(project, FakeSessionRunner(), *deep_args(project), turns=None)
    sessions_path = project / "run" / "sessions.jsonl"
    kept = [
        line
        for line in sessions_path.read_text().splitlines()
        if not (json.loads(line)["repeat"] == 2 and json.loads(line)["turn"] == 3)
    ]
    sessions_path.write_text("\n".join(kept) + "\n")

    second = FakeSessionRunner()
    assert run_cli(project, second, *deep_args(project), turns=None) == 0
    assert len(second.calls) == 3
    assert resume_of(second.calls[0]) is None


def test_cli_deep_rescores_offline_and_is_deterministic(project):
    run_cli(project, FakeSessionRunner(), *deep_args(project), turns=None)

    idle = FakeSessionRunner()
    assert run_cli(project, idle, *deep_args(project), turns=None, generate=False) == 0
    assert idle.calls == []

    first = json.loads((project / "run" / "drift.json").read_text())
    assert run_cli(project, idle, *deep_args(project), turns=None, generate=False) == 0
    second = json.loads((project / "run" / "drift.json").read_text())
    del first["date"], second["date"]
    assert first == second


def test_deep_report_states_the_script_design(project):
    run_cli(project, FakeSessionRunner(), *deep_args(project), turns=None)
    summary = json.loads((project / "run" / "drift.json").read_text())
    assert summary["mode"] == "deep"
    assert summary["scripts"] == {"1": "one", "2": "two"}
    report = (project / "run" / "drift.md").read_text()
    assert "coherent script" in report
    assert "The shallow rotated run is the control." in report
    assert "- Repeat 1: script `one`" in report
    assert "- Repeat 2: script `two`" in report
    assert "rotates the prompt order" not in report


def test_the_authored_scripts_obey_the_contract():
    paths = sorted(SESSIONS_DIR.glob("*.yaml"))
    scripts = [load_session_script(path) for path in paths]
    assert len(scripts) == 3
    assert {len(script["turns"]) for script in scripts} == {15}
    assert len({script["id"] for script in scripts}) == 3
    for path, script in zip(paths, scripts, strict=True):
        assert path.stem == script["id"]
        for turn in script["turns"]:
            size = len(turn["text"].encode("utf-8"))
            assert size >= 20_000, f"{script['id']}/{turn['id']}: {size} bytes is too short"
