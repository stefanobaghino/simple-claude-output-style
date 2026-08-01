"""Tests for the fidelity gate. The linter runs for real; no test
touches the network."""

import json
from pathlib import Path

import pytest
import yaml

from gate import cli, load_gate_config, score_run
from linter import Linter, load_rules
from runner.provenance import linter_toolchain

HERE = Path(__file__).parent
RULES_DIR = HERE.parent / "rules"
GATE_CONFIG = RULES_DIR / "gate.yaml"

CLEAN_TS = "The tests pass. Commit the change."
DIRTY_TS = "You should utilize the tool. However, it isn't ready, e.g. today."
CLEAN_PL = "You must attach the logs before noon."
CODE_TS = "```python\nclient.utilize()\n```\n\nThe code runs."


def answer(prompt_id, style, text):
    return {"prompt_id": prompt_id, "style": style, "answer": text}


@pytest.fixture(scope="session")
def linters():
    return {
        path.name.removesuffix(".rules.yaml"): Linter(load_rules(path))
        for path in RULES_DIR.glob("*.rules.yaml")
    }


@pytest.fixture(scope="session")
def config():
    return load_gate_config(GATE_CONFIG)


def make_run(tmp_path, answers, toolchain=None):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "answers.jsonl").write_text(
        "".join(json.dumps(a) + "\n" for a in answers), encoding="utf-8"
    )
    (run_dir / "provenance.json").write_text(
        json.dumps({"linter_toolchain": toolchain or linter_toolchain()}), encoding="utf-8"
    )
    return run_dir


def run_gate(run_dir):
    return cli.main(
        [str(run_dir), "--rules-dir", str(RULES_DIR), "--gate-config", str(GATE_CONFIG)]
    )


def test_gate_config_loads_a_threshold_per_style(config):
    assert config.thresholds["technical-simplified"] > 0
    assert config.thresholds["plain-language"] > 0


def test_gate_config_rejects_a_file_without_thresholds(tmp_path):
    empty = tmp_path / "gate.yaml"
    empty.write_text("{}\n")
    with pytest.raises(ValueError, match="no thresholds"):
        load_gate_config(empty)


def test_a_clean_styled_answer_passes(linters, config):
    (row,) = score_run([answer("p1", "technical-simplified", CLEAN_TS)], linters, config).rows
    assert row["pass"] is True
    assert row["violations"] == 0
    assert row["answer_sha256"]


def test_a_dirty_styled_answer_fails_with_detail(linters, config):
    result = score_run([answer("p1", "technical-simplified", DIRTY_TS)], linters, config)
    (row,) = result.rows
    assert row["pass"] is False
    assert row["rate"] > row["threshold"]
    assert row["by_rule"]["banned-modal"] == 1
    assert row["by_rule"]["contraction"] == 1
    assert ("p1", "technical-simplified") in result.failing


def test_the_threshold_boundary_is_inclusive(linters, tmp_path):
    gate_file = tmp_path / "gate.yaml"
    gate_file.write_text(
        yaml.safe_dump({"thresholds": {"technical-simplified": {"max_rate": 50.0}}})
    )
    boundary = answer("p1", "technical-simplified", "You should retry. The test failed.")
    (row,) = score_run([boundary], linters, load_gate_config(gate_file)).rows
    assert row["rate"] == 50.0
    assert row["pass"] is True


def test_an_unstyled_answer_gets_baseline_rows_without_a_mark(linters, config):
    answers = [
        answer("p1", "technical-simplified", CLEAN_TS),
        answer("p1", "plain-language", CLEAN_PL),
        answer("p1", None, DIRTY_TS),
    ]
    rows = score_run(answers, linters, config).rows
    baseline = [r for r in rows if r["style"] is None]
    assert {r["rule_set"] for r in baseline} == {"technical-simplified", "plain-language"}
    assert all(r["pass"] is None and r["threshold"] is None for r in baseline)


def test_a_zero_sentence_answer_fails_with_a_warning(linters, config):
    result = score_run([answer("p1", "technical-simplified", "")], linters, config)
    (row,) = result.rows
    assert row["pass"] is False
    assert any("no sentences" in warning for warning in result.warnings)


def test_a_missing_counterpart_produces_a_warning(linters, config):
    result = score_run([answer("p1", "technical-simplified", CLEAN_TS)], linters, config)
    assert any("unstyled counterpart is missing" in warning for warning in result.warnings)


def test_a_banned_word_inside_a_code_block_does_not_count(linters, config):
    (row,) = score_run([answer("p1", "technical-simplified", CODE_TS)], linters, config).rows
    assert row["violations"] == 0
    assert row["pass"] is True


COMPLETE_ANSWERS = [
    answer("p1", "technical-simplified", CLEAN_TS),
    answer("p1", "plain-language", CLEAN_PL),
    answer("p1", None, DIRTY_TS),
]


def test_cli_gates_a_complete_passing_run(tmp_path, capsys):
    run_dir = make_run(tmp_path, COMPLETE_ANSWERS)
    assert run_gate(run_dir) == 0
    assert "technical-simplified: 1/1 pair(s) pass the gate" in capsys.readouterr().out

    rows = [json.loads(line) for line in (run_dir / "fidelity.jsonl").read_text().splitlines()]
    assert len(rows) == 4  # 2 styled + 1 unstyled x 2 rule sets
    summary = json.loads((run_dir / "fidelity.json").read_text())
    assert summary["summary"]["technical-simplified"]["passed"] == 1
    assert summary["rules"]["plain-language"]["sha256"]
    assert summary["gate_config"]["sha256"]
    assert summary["warnings"] == []
    assert "# Fidelity report" in (run_dir / "fidelity.md").read_text()


def test_cli_marks_a_failing_pair_and_exits_1(tmp_path):
    answers = COMPLETE_ANSWERS + [
        answer("p2", "technical-simplified", DIRTY_TS),
        answer("p2", "plain-language", CLEAN_PL),
        answer("p2", None, CLEAN_TS),
    ]
    run_dir = make_run(tmp_path, answers)
    assert run_gate(run_dir) == 1
    report = (run_dir / "fidelity.md").read_text()
    assert "### Failing pairs" in report
    assert "- p2 (rate" in report
    assert "[banned-modal]" in report


def test_cli_warns_on_an_incomplete_run_and_exits_1(tmp_path):
    run_dir = make_run(tmp_path, [answer("p1", "technical-simplified", CLEAN_TS)])
    assert run_gate(run_dir) == 1
    summary = json.loads((run_dir / "fidelity.json").read_text())
    assert any("unstyled counterpart" in warning for warning in summary["warnings"])


def test_cli_warns_on_a_toolchain_mismatch(tmp_path):
    toolchain = {"spacy": "0.0.0", "en-core-web-sm": "0.0.0"}
    run_dir = make_run(tmp_path, COMPLETE_ANSWERS, toolchain=toolchain)
    assert run_gate(run_dir) == 1
    summary = json.loads((run_dir / "fidelity.json").read_text())
    assert any("toolchain differs" in warning for warning in summary["warnings"])


def test_cli_is_idempotent(tmp_path):
    run_dir = make_run(tmp_path, COMPLETE_ANSWERS)
    run_gate(run_dir)
    first = {name: (run_dir / name).read_text() for name in ("fidelity.jsonl", "fidelity.md")}
    first_summary = json.loads((run_dir / "fidelity.json").read_text())
    run_gate(run_dir)
    second = {name: (run_dir / name).read_text() for name in ("fidelity.jsonl", "fidelity.md")}
    second_summary = json.loads((run_dir / "fidelity.json").read_text())
    assert first == second
    del first_summary["date"], second_summary["date"]
    assert first_summary == second_summary


def test_cli_rejects_a_run_without_answers(tmp_path):
    (tmp_path / "empty").mkdir()
    with pytest.raises(SystemExit) as excinfo:
        run_gate(tmp_path / "empty")
    assert excinfo.value.code == 2


def test_cli_rejects_a_style_without_a_rule_file(tmp_path):
    run_dir = make_run(tmp_path, [answer("p1", "ghost", CLEAN_TS)])
    with pytest.raises(SystemExit) as excinfo:
        run_gate(run_dir)
    assert excinfo.value.code == 2


def test_cli_rejects_a_style_without_a_threshold(tmp_path):
    gate_file = tmp_path / "gate.yaml"
    gate_file.write_text(yaml.safe_dump({"thresholds": {"plain-language": {"max_rate": 5.0}}}))
    run_dir = make_run(tmp_path, [answer("p1", "technical-simplified", CLEAN_TS)])
    with pytest.raises(SystemExit) as excinfo:
        cli.main([str(run_dir), "--rules-dir", str(RULES_DIR), "--gate-config", str(gate_file)])
    assert excinfo.value.code == 2
