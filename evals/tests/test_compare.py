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
    strength: float = 2.0,
    net: int = 4,
    rank_model: str = "opus",
    rank_resolved: str | None = None,
    style_sha: str = "s" * 8,
    claude_version: str = "2.0.0 (Claude Code)",
    workdir: str | None = "temp",
    config: str | None = "hermetic",
    manifest_sha: str | None = "m" * 8,
    screening: dict | None = None,
    skip: tuple[str, ...] = (),
) -> Path:
    run_dir = runs_dir / name
    run_dir.mkdir(parents=True)
    conditions = {"model_requested": "sonnet", "claude_version": claude_version}
    if workdir is not None:
        conditions["workdir"] = workdir
    if config is not None:
        conditions["config"] = config
    if manifest_sha is not None:
        conditions["config_manifest_sha256"] = manifest_sha
    files = {
        "provenance": {
            "prompt_set": {"path": "prompts/prompts.yaml", "sha256": "p" * 8},
            "conditions": conditions,
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
        "rank": {
            "judge": {"model": rank_model, "model_resolved": rank_resolved},
            "design": "clarity-v1",
            "bradley_terry": {
                "fitted": True,
                "anchored_on": "unstyled",
                "strengths": {
                    "alpha": {"strength": strength},
                    "unstyled": {"strength": 1.0, "ci_low": None, "ci_high": None},
                },
            },
            "matchups": [
                {
                    "a": "alpha",
                    "b": "unstyled",
                    "contests": 8,
                    "wins_a": 5,
                    "wins_b": 1,
                    "splits": 2,
                    "unscored": 0,
                    "net": net,
                }
            ],
        },
    }
    if screening is not None:
        files["provenance"]["screening"] = screening
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
    write_run(runs, "run-a", rate=1.0, wins=3, losses=1, strength=1.5, net=4)
    write_run(runs, "run-b", rate=2.0, wins=2, losses=2, strength=2.0, net=0)
    write_run(runs, "run-c", rate=3.0, wins=1, losses=3, strength=2.5, net=-4)
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
        "rank: Bradley-Terry strength",
        "rank: net wins vs unstyled",
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
    assert axes["rank: Bradley-Terry strength"] == {
        "n": 3,
        "per_run": {"run-a": 1.5, "run-b": 2.0, "run-c": 2.5},
        "min": 1.5,
        "mean": 2.0,
        "max": 2.5,
        "stdev": 0.5,
    }
    assert axes["rank: net wins vs unstyled"] == {
        "n": 3,
        "per_run": {"run-a": 4, "run-b": 0, "run-c": -4},
        "min": -4,
        "mean": 0.0,
        "max": 4,
        "stdev": 4.0,
    }
    # The unstyled anchor is a competitor, not a style, so it gets
    # no section of its own.
    assert list(summary["axes"]) == ["alpha"]
    assert capsys.readouterr().out == "alpha: 10 axes across 3 runs\n"
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


def test_a_missing_rank_artifact_drops_only_the_rank_axes(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b", skip=("rank",))
    write_run(runs, "run-c")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b", "run-c")
    assert code == 1
    assert summary["warnings"] == [
        "run-b: no rank.json, so the rank axes miss this run",
    ]
    axes = summary["axes"]["alpha"]
    assert axes["rank: Bradley-Terry strength"]["n"] == 2
    assert axes["rank: net wins vs unstyled"]["n"] == 2
    assert "run-b" not in axes["rank: Bradley-Terry strength"]["per_run"]
    assert axes["fidelity: styled violation rate"]["n"] == 3


def test_an_unfitted_rank_drops_only_the_strength_sample(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b")
    run_c = write_run(runs, "run-c")
    rank = json.loads((run_c / "rank.json").read_text(encoding="utf-8"))
    rank["bradley_terry"] = {
        "fitted": False,
        "note": "the fit needs at least 3 competitors with a scored contest",
    }
    (run_c / "rank.json").write_text(json.dumps(rank), encoding="utf-8")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b", "run-c")
    assert code == 0
    axes = summary["axes"]["alpha"]
    assert axes["rank: Bradley-Terry strength"]["n"] == 2
    assert "run-c" not in axes["rank: Bradley-Terry strength"]["per_run"]
    assert axes["rank: net wins vs unstyled"]["n"] == 3


def test_a_matchup_with_the_style_on_the_b_side_flips_the_net(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", net=4)
    run_b = write_run(runs, "run-b")
    rank = json.loads((run_b / "rank.json").read_text(encoding="utf-8"))
    matchup = rank["matchups"][0]
    matchup["a"], matchup["b"] = "unstyled", "alpha"
    matchup["wins_a"], matchup["wins_b"] = matchup["wins_b"], matchup["wins_a"]
    matchup["net"] = 4
    (run_b / "rank.json").write_text(json.dumps(rank), encoding="utf-8")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 0
    per_run = summary["axes"]["alpha"]["rank: net wins vs unstyled"]["per_run"]
    assert per_run == {"run-a": 4, "run-b": -4}


def test_a_rank_judge_mismatch_warns(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a")
    write_run(runs, "run-b", rank_model="sonnet")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        "condition mismatch on rank judge model: run-a opus, run-b sonnet",
    ]


def test_a_resolved_judge_model_mismatch_warns(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", rank_resolved="claude-opus-5")
    write_run(runs, "run-b", rank_resolved="claude-opus-6")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        "condition mismatch on rank judge model_resolved: run-a claude-opus-5, run-b claude-opus-6",
    ]


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


def test_a_run_without_a_workdir_mode_warns(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", workdir=None)
    write_run(runs, "run-b")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        "condition mismatch on workdir: run-a null, run-b temp",
    ]


def test_a_run_without_a_config_mode_warns(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", config=None, manifest_sha=None)
    write_run(runs, "run-b")
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        "condition mismatch on config: run-a null, run-b hermetic",
        f"condition mismatch on config manifest hash: run-a null, run-b {'m' * 8}",
    ]


def test_a_manifest_hash_mismatch_warns(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", manifest_sha="a" * 8)
    write_run(runs, "run-b", manifest_sha="b" * 8)
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        f"condition mismatch on config manifest hash: run-a {'a' * 8}, run-b {'b' * 8}",
    ]


SCREENING = {
    "prompts_per_type": 2,
    "seed": 0,
    "prompt_ids": ["debugging-01", "explanation-01"],
    "full_prompt_count": 20,
}


def test_a_screening_run_never_compares_with_a_full_run(tmp_path):
    runs = tmp_path / "runs"
    run_a = write_run(runs, "run-a")
    run_b = write_run(runs, "run-b", screening=SCREENING)
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_a), str(run_b)])
    assert error.value.code == 2


def test_two_screening_runs_with_the_same_subset_compare(tmp_path):
    runs = tmp_path / "runs"
    write_run(runs, "run-a", screening=SCREENING)
    write_run(runs, "run-b", screening=SCREENING)
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 0
    assert summary["warnings"] == []


def test_two_screening_runs_with_different_subsets_warn(tmp_path):
    runs = tmp_path / "runs"
    other = dict(SCREENING, prompt_ids=["debugging-02", "explanation-01"])
    write_run(runs, "run-a", screening=SCREENING)
    write_run(runs, "run-b", screening=other)
    code, summary, _ = run_cli(tmp_path, "run-a", "run-b")
    assert code == 1
    assert summary["warnings"] == [
        (
            "condition mismatch on screening: "
            f"run-a {json.dumps(SCREENING, sort_keys=True)}, "
            f"run-b {json.dumps(other, sort_keys=True)}"
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
