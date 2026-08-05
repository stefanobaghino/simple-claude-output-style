"""Tests for the cross-run comparison."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from compare import cli

CHECKS = ("comprehension", "paraphrase", "roundtrip")


def write_run(
    runs_dir: Path,
    name: str,
    *,
    rate: float = 2.0,
    passed: int = 3,
    ratio: float = 0.9,
    wins: int = 2,
    losses: int = 1,
    fact_median: float = 0.8,
    hedge_median: float | None = 0.5,
    style_sha: str = "s" * 8,
    claude_version: str = "2.0.0 (Claude Code)",
    skip: tuple[str, ...] = (),
) -> Path:
    run_dir = runs_dir / name
    run_dir.mkdir(parents=True)
    files = {
        "provenance": {
            "prompt_set": {"path": "prompts/prompts.yaml", "sha256": "p" * 8},
            "conditions": {"model_requested": "sonnet", "claude_version": claude_version},
            "styles": {"alpha": {"file": "alpha.md", "sha256": style_sha}},
            "linter_toolchain": {"spacy": "1.0"},
        },
        "fidelity": {
            "summary": {
                "alpha": {
                    "gated": 3,
                    "passed": passed,
                    "failed": 3 - passed,
                    "styled_rate": rate,
                    "baseline_rate": 9.9,
                }
            },
            "rules": {"alpha": {"file": "alpha.rules.yaml", "sha256": "r" * 8}},
            "gate_config": {"file": "gate.yaml", "sha256": "g" * 8},
        },
        "cost": {"answer_ratio": {"per_style": {"alpha": {"ratio_of_totals": ratio}}}},
        "value": {
            "judges": {
                "models": {"reader": "haiku", "grader": "opus"},
                "questions": 6,
                "paraphrases": 3,
                "replicates": 3,
                "comprehension_design": "balanced-facts-v3",
                "language": "Italian",
            },
            "checks": {
                check: {
                    "judged": True,
                    "per_style": {"alpha": {"wins": wins, "losses": losses, "ties": 0}},
                }
                for check in CHECKS
            },
        },
        "loss": {
            "judge": {"model": "opus"},
            "checks": {
                "completeness": {"per_style": {"alpha": {"median": fact_median}}},
                "hedging": {"per_style": {"alpha": {"median": hedge_median}}},
            },
        },
    }
    for stem, content in files.items():
        if stem in skip:
            continue
        (run_dir / f"{stem}.json").write_text(json.dumps(content), encoding="utf-8")
    return run_dir


def run_cli(tmp_path: Path, *names: str) -> tuple[int, dict, str]:
    out = tmp_path / "compare"
    code = cli.main([str(tmp_path / "runs" / name) for name in names] + ["--out", str(out)])
    summary = json.loads((out / "compare.json").read_text(encoding="utf-8"))
    report = (out / "compare.md").read_text(encoding="utf-8")
    return code, summary, report


def test_cli_states_the_spread_over_three_runs(tmp_path, capsys):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", rate=1.0, wins=3, losses=1)
    write_run(runs, "run-b", rate=2.0, wins=2, losses=2)
    write_run(runs, "run-c", rate=3.0, wins=1, losses=3)
    code, summary, report = run_cli(tmp_path, "run-a", "run-b", "run-c")
    assert code == 0
    assert summary["warnings"] == []
    assert summary["runs"] == ["run-a", "run-b", "run-c"]
    axes = summary["axes"]["alpha"]
    assert list(axes) == [
        "fidelity: styled violation rate",
        "fidelity: gated pairs passed",
        "cost: output-token ratio",
        "value: net wins (comprehension)",
        "value: net wins (paraphrase)",
        "value: net wins (roundtrip)",
        "loss: fact survival median",
        "loss: hedge survival median",
    ]
    assert axes["fidelity: styled violation rate"] == {
        "n": 3,
        "per_run": {"run-a": 1.0, "run-b": 2.0, "run-c": 3.0},
        "min": 1.0,
        "mean": 2.0,
        "max": 3.0,
        "stdev": 1.0,
    }
    assert axes["value: net wins (comprehension)"] == {
        "n": 3,
        "per_run": {"run-a": 2, "run-b": 0, "run-c": -2},
        "min": -2,
        "mean": 0.0,
        "max": 2,
        "stdev": 2.0,
    }
    assert capsys.readouterr().out == "alpha: 8 axes across 3 runs\n"
    assert "| Axis | run-a | run-b | run-c | n | Min | Mean | Max | Stdev |" in report
    assert "| fidelity: styled violation rate | 1.0 | 2.0 | 3.0 | 3 | 1.0 | 2.0 | 3.0 | 1.0 |" in (
        report
    )
    assert "## Warnings\n\n- none" in report


def test_a_single_sample_axis_has_no_stdev(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b", skip=("cost",))
    code, summary, report = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["axes"]["alpha"]["cost: output-token ratio"] == {
        "n": 1,
        "per_run": {"run-a": 0.9},
        "min": 0.9,
        "mean": 0.9,
        "max": 0.9,
        "stdev": None,
    }
    assert "| cost: output-token ratio | 0.9 | n/a | 1 | 0.9 | 0.9 | 0.9 | n/a |" in report


def test_a_null_hedge_median_drops_the_sample(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b")
    write_run(runs, "run-c", hedge_median=None)
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b", "run-c")
    assert code == 0
    axes = summary["axes"]["alpha"]
    assert axes["loss: hedge survival median"]["n"] == 2
    assert "run-c" not in axes["loss: hedge survival median"]["per_run"]
    assert axes["loss: fact survival median"]["n"] == 3


def test_a_missing_artifact_warns_and_drops_only_its_axes(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b", skip=("loss",))
    write_run(runs, "run-c")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b", "run-c")
    assert code == 1
    assert summary["warnings"] == [
        "run-b: no loss.json, so the loss axes miss this run",
    ]
    axes = summary["axes"]["alpha"]
    assert axes["loss: fact survival median"]["n"] == 2
    assert "run-b" not in axes["loss: fact survival median"]["per_run"]
    assert axes["fidelity: styled violation rate"]["n"] == 3


def test_a_condition_mismatch_warns(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b", style_sha="x" * 8, claude_version="2.0.1 (Claude Code)")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        "condition mismatch on style hash (alpha): run-a ssssssss, run-b xxxxxxxx",
        (
            "condition mismatch on claude version: "
            "run-a 2.0.0 (Claude Code), run-b 2.0.1 (Claude Code)"
        ),
    ]


def test_fewer_than_two_runs_exits_2(tmp_path):
    runs = tmp_path / "runs"
    run_a = write_run(runs, "run-a")
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_a)])
    assert error.value.code == 2


def test_a_directory_without_provenance_exits_2(tmp_path):
    runs = tmp_path / "runs"
    run_a = write_run(runs, "run-a")
    run_b = write_run(runs, "run-b", skip=("provenance",))
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_a), str(run_b)])
    assert error.value.code == 2


def test_a_duplicate_run_name_exits_2(tmp_path):
    runs = tmp_path / "runs"
    run_a = write_run(runs, "run-a")
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_a), str(run_a)])
    assert error.value.code == 2
