"""Tests for the content-loss checks. No test touches the network:
the claude subprocess is replaced with fake runners that return
canned stream-json output."""

import hashlib
import json
import threading
from collections import Counter
from pathlib import Path

import pytest

from loss import cli, parse_string_list, parse_verdicts, score_checks
from loss.judges import run_judges
from runner.provenance import sha256_of

STYLED_TEXT = "The quick brown fox jumps."
UNSTYLED_TEXT = "The slow green turtle crawls."
BETA_TEXT = "The big red bear sleeps."

FACTS = '["the animal crawls", "the animal is green"]'
STYLED_FACTS = '["the animal jumps", "the animal is brown"]'
BETA_FACTS = '["the animal sleeps", "the animal is red"]'
CLAIMS = '["the animal probably sleeps", "the animal may swim"]'


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stream(result_text, output_style="default"):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": "claude-opus-5",
    }
    result = {
        "type": "result",
        "is_error": False,
        "result": result_text,
        "usage": {
            "output_tokens": 5,
            "input_tokens": 3,
            "cache_creation_input_tokens": 2,
            "cache_read_input_tokens": 1,
        },
        "duration_ms": 10,
    }
    return "\n".join(json.dumps(event) for event in (init, result))


class FakeLossRunner:
    """Routes each judge prompt to a canned reply.

    The unstyled turtle text yields two facts and two uncertain
    claims. The styled fox text loses one fact and turns one claim
    certain; the beta bear text keeps every fact and drops one claim.
    In reverse, the fox text yields two facts of which one is an
    addition, and the bear text adds no fact. A reverse check carries
    the turtle text, and its claims name the styled facts.
    """

    def __init__(self):
        self.calls = []
        # Parallel judge calls share the runner, so the lock covers
        # the calls list and the counters of the reply methods.
        self.lock = threading.Lock()

    def __call__(self, argv, cwd, env=None):
        with self.lock:
            self.calls.append(argv)
            prompt = argv[argv.index("-p") + 1]
            return stream(self.reply(prompt))

    def reply(self, prompt):
        if prompt.startswith("List the distinct factual claims"):
            if "fox" in prompt:
                return STYLED_FACTS
            if "bear" in prompt:
                return BETA_FACTS
            return FACTS
        if prompt.startswith("Check each claim"):
            if "turtle" in prompt:
                return "[false, true]" if "jumps" in prompt else "[true, true]"
            return "[true, false]" if "fox" in prompt else "[true, true]"
        if prompt.startswith("List the claims"):
            return CLAIMS
        if prompt.startswith("For each uncertain claim"):
            return '["hedged", "certain"]' if "fox" in prompt else '["hedged", "absent"]'
        raise AssertionError(f"unrouted judge prompt: {prompt[:60]}")


def test_a_hedging_extraction_runs_before_a_completeness_check(tmp_path):
    # At one worker the order is breadth-first: every extraction of
    # every check goes to the pool first, and each check call lands
    # behind its own extraction only. The old phase structure ran the
    # whole completeness check before the first hedging call.
    keys = []
    warnings = run_judges(
        pairs={"alpha": ["p-01"]},
        answers={
            ("p-01", "alpha"): {"text": STYLED_TEXT, "sha256": sha(STYLED_TEXT)},
            ("p-01", None): {"text": UNSTYLED_TEXT, "sha256": sha(UNSTYLED_TEXT)},
        },
        checks=["completeness", "hedging"],
        model="opus",
        rows={},
        sink=lambda row: keys.append(row["key"]),
        workdir=tmp_path,
        run=FakeLossRunner(),
        parallel=1,
    )
    assert warnings == []
    assert len(keys) == 6
    assert keys.index(f"hedging:claims:{sha(UNSTYLED_TEXT)}") < keys.index(
        f"completeness:check:{sha(STYLED_TEXT)}"
    )


def test_parse_string_list_accepts_any_length():
    assert parse_string_list('["a", "b"]') == ["a", "b"]
    assert parse_string_list("[]") == []
    assert parse_string_list("[1, 2]") == ["1", "2"]
    assert parse_string_list('"just a string"') is None
    assert parse_string_list("no json here") is None


def test_parse_verdicts_needs_exact_verdicts():
    assert parse_verdicts('["hedged", "certain", "absent"]', 3) == ["hedged", "certain", "absent"]
    assert parse_verdicts('["hedged"]', 2) is None
    assert parse_verdicts('["hedged", "maybe"]', 2) is None
    assert parse_verdicts("no json here", 1) is None


def pair_fixture(rows):
    answers = {
        ("p-01", "alpha"): {"text": "styled text", "sha256": "S"},
        ("p-01", None): {"text": "unstyled text", "sha256": "U"},
    }
    return {"alpha": ["p-01"]}, answers, rows


def loss_row(check, output):
    return {"check": check, "output": output}


def test_completeness_scoring_counts_the_lost_facts():
    pairs, answers, rows = pair_fixture(
        {
            "completeness:facts:U": loss_row("completeness", '["f1", "f2", "f3"]'),
            "completeness:check:S": loss_row("completeness", "[true, false, false]"),
        }
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows)
    stats = result.checks["completeness"]["per_style"]["alpha"]
    assert stats["pairs"]["p-01"] == {
        "facts": 3,
        "survived": 1,
        "fraction": 0.333,
        "lost": ["f2", "f3"],
    }
    assert stats["median"] == 0.333


def test_two_way_scoring_counts_the_additions():
    pairs, answers, rows = pair_fixture(
        {
            "completeness:facts:U": loss_row("completeness", '["f1", "f2", "f3"]'),
            "completeness:check:S": loss_row("completeness", "[true, false, false]"),
            "completeness:facts:S": loss_row("completeness", '["g1", "g2"]'),
            "completeness:reverse:S": loss_row("completeness", "[false, true]"),
        }
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows, fact_mine="two-way")
    stats = result.checks["completeness"]["per_style"]["alpha"]
    assert stats["pairs"]["p-01"] == {
        "facts": 3,
        "survived": 1,
        "fraction": 0.333,
        "lost": ["f2", "f3"],
        "styled_facts": 2,
        "additions": 1,
        "added": ["g1"],
    }
    assert stats["additions_median"] == 1
    assert not any("completeness" in w for w in result.warnings)


def test_two_way_scoring_without_reverse_marks_keeps_the_fraction():
    pairs, answers, rows = pair_fixture(
        {
            "completeness:facts:U": loss_row("completeness", '["f1", "f2", "f3"]'),
            "completeness:check:S": loss_row("completeness", "[true, false, false]"),
            "completeness:facts:S": loss_row("completeness", '["g1", "g2"]'),
        }
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows, fact_mine="two-way")
    stats = result.checks["completeness"]["per_style"]["alpha"]
    entry = stats["pairs"]["p-01"]
    assert entry["fraction"] == 0.333
    assert entry["styled_facts"] == 2
    assert entry["additions"] is None
    assert entry["added"] == []
    assert stats["additions_median"] is None
    assert any("no usable reverse marks" in w for w in result.warnings)


def test_two_way_scoring_without_a_styled_fact_list_warns():
    pairs, answers, rows = pair_fixture(
        {
            "completeness:facts:U": loss_row("completeness", '["f1"]'),
            "completeness:check:S": loss_row("completeness", "[true]"),
        }
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows, fact_mine="two-way")
    entry = result.checks["completeness"]["per_style"]["alpha"]["pairs"]["p-01"]
    assert entry["styled_facts"] is None
    assert entry["additions"] is None
    assert any("no usable styled fact list" in w for w in result.warnings)


def test_scoring_without_the_two_way_tag_adds_no_addition_fields():
    pairs, answers, rows = pair_fixture(
        {
            "completeness:facts:U": loss_row("completeness", '["f1", "f2", "f3"]'),
            "completeness:check:S": loss_row("completeness", "[true, false, false]"),
            "completeness:facts:S": loss_row("completeness", '["g1", "g2"]'),
            "completeness:reverse:S": loss_row("completeness", "[false, true]"),
        }
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows)
    stats = result.checks["completeness"]["per_style"]["alpha"]
    assert stats["pairs"]["p-01"] == {
        "facts": 3,
        "survived": 1,
        "fraction": 0.333,
        "lost": ["f2", "f3"],
    }
    assert "additions_median" not in stats


def test_hedging_scoring_counts_the_three_verdicts():
    pairs, answers, rows = pair_fixture(
        {
            "hedging:claims:U": loss_row("hedging", '["c1", "c2", "c3"]'),
            "hedging:check:S": loss_row("hedging", '["certain", "hedged", "absent"]'),
        }
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows)
    stats = result.checks["hedging"]["per_style"]["alpha"]
    assert stats["pairs"]["p-01"] == {
        "claims": 3,
        "hedged": 1,
        "certain": 1,
        "absent": 1,
        "survival": 0.5,
        "lost": ["c1"],
    }
    assert stats["median"] == 0.5


def test_an_empty_claim_list_leaves_the_pair_without_a_score():
    pairs, answers, rows = pair_fixture({"hedging:claims:U": loss_row("hedging", "[]")})
    result = score_checks(pairs=pairs, answers=answers, rows=rows)
    stats = result.checks["hedging"]["per_style"]["alpha"]
    assert stats["pairs"]["p-01"] == {
        "claims": 0,
        "hedged": 0,
        "certain": 0,
        "absent": 0,
        "survival": None,
        "lost": [],
    }
    assert stats["median"] is None
    assert not any("hedging" in w for w in result.warnings)


def test_missing_check_marks_leave_the_pair_unscored():
    pairs, answers, rows = pair_fixture(
        {"completeness:facts:U": loss_row("completeness", '["f1"]')}
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows)
    assert result.checks["completeness"]["per_style"]["alpha"]["pairs"] == {}
    assert any("no usable survival marks" in w for w in result.warnings)


def test_an_unjudged_check_warns():
    pairs, answers, rows = pair_fixture(
        {"completeness:facts:U": loss_row("completeness", '["f1"]')}
    )
    result = score_checks(pairs=pairs, answers=answers, rows=rows)
    assert result.checks["hedging"] == {"judged": False, "per_style": None}
    assert any("the hedging check has no judge data" in w for w in result.warnings)


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row) + "\n")


def make_project(tmp_path, styled_answers=None):
    """A gated run with one prompt and one styled answer per style."""
    styled_answers = styled_answers or {"alpha": STYLED_TEXT}
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    answers = [
        {"prompt_id": "explanation-01", "style": None, "answer": UNSTYLED_TEXT},
    ]
    fidelity = [
        {
            "prompt_id": "explanation-01",
            "style": None,
            "pass": None,
            "answer_sha256": sha(UNSTYLED_TEXT),
        },
    ]
    for style, text in styled_answers.items():
        answers.append({"prompt_id": "explanation-01", "style": style, "answer": text})
        fidelity.append(
            {
                "prompt_id": "explanation-01",
                "style": style,
                "pass": True,
                "answer_sha256": sha(text),
            }
        )
    write_jsonl(run_dir / "answers.jsonl", answers)
    write_jsonl(run_dir / "fidelity.jsonl", fidelity)
    provenance = {"conditions": {"model_requested": "sonnet"}}
    (run_dir / "provenance.json").write_text(json.dumps(provenance))
    return tmp_path


@pytest.fixture
def project(tmp_path):
    return make_project(tmp_path)


def run_cli(project, *extra, run=None):
    return cli.main([str(project / "run"), *extra], run=run or FakeLossRunner())


def test_cli_judge_writes_the_artifacts(project, capsys):
    assert run_cli(project, "--judge") == 0
    summary = json.loads((project / "run" / "loss.json").read_text())
    assert summary["pairs"] == {"alpha": ["explanation-01"]}
    assert summary["judge"]["model_resolved"] == "claude-opus-5"
    completeness = summary["checks"]["completeness"]["per_style"]["alpha"]
    assert completeness["median"] == 0.5
    assert completeness["additions_median"] == 1
    assert completeness["pairs"]["explanation-01"] == {
        "facts": 2,
        "survived": 1,
        "fraction": 0.5,
        "lost": ["the animal is green"],
        "styled_facts": 2,
        "additions": 1,
        "added": ["the animal jumps"],
    }
    hedging = summary["checks"]["hedging"]["per_style"]["alpha"]
    assert hedging["median"] == 0.5
    assert hedging["pairs"]["explanation-01"]["lost"] == ["the animal may swim"]
    assert summary["warnings"] == []
    raw_rows = [
        json.loads(line) for line in (project / "run" / "loss-raw.jsonl").read_text().splitlines()
    ]
    call_rows = [row for row in raw_rows if row.get("type") == "call"]
    assert call_rows
    assert all(isinstance(row["wall_ms"], int) for row in call_rows)
    assert all(row["input_tokens"] == 3 for row in call_rows)
    assert all(row["cache_creation_input_tokens"] == 2 for row in call_rows)
    assert all(row["cache_read_input_tokens"] == 1 for row in call_rows)
    report = (project / "run" / "loss.md").read_text()
    assert "## Call timing" in report
    assert "## Harness spend" in report
    assert "| explanation-01 | 2 | 1 | 0.5 | 2 | 1 |" in report
    assert "Median fraction: 0.5 over 1 scored pairs." in report
    assert "Median additions: 1 over 1 scored pairs." in report
    assert "- explanation-01: the animal is green" in report
    assert "Added facts (styled only):" in report
    assert "- explanation-01: the animal jumps" in report
    assert "| explanation-01 | 2 | 1 | 1 | 0 | 0.5 |" in report
    assert "Median survival: 0.5 over 1 scored pairs." in report
    assert "- explanation-01: the animal may swim" in report
    out = capsys.readouterr().out
    assert "alpha: completeness median 0.5, hedging median 0.5" in out


def test_cli_judge_emits_the_reverse_keys(project):
    run_cli(project, "--judge")
    raw = (project / "run" / "loss-raw.jsonl").read_text().splitlines()
    keys = {json.loads(line).get("key") for line in raw}
    assert f"completeness:facts:{sha(UNSTYLED_TEXT)}" in keys
    assert f"completeness:check:{sha(STYLED_TEXT)}" in keys
    assert f"completeness:facts:{sha(STYLED_TEXT)}" in keys
    assert f"completeness:reverse:{sha(STYLED_TEXT)}" in keys


def test_cli_judge_prompts_are_blind(project):
    runner = FakeLossRunner()
    run_cli(project, "--judge", run=runner)
    assert runner.calls
    for argv in runner.calls:
        assert "--plugin-dir" not in argv
        settings = json.loads(argv[argv.index("--settings") + 1])
        assert settings["outputStyle"] == "default"
        prompt = argv[argv.index("-p") + 1]
        assert "alpha" not in prompt
        assert "styled" not in prompt.lower()
        assert not (STYLED_TEXT in prompt and UNSTYLED_TEXT in prompt)


def test_cli_shares_the_extraction_between_styles(tmp_path):
    project = make_project(tmp_path, styled_answers={"alpha": STYLED_TEXT, "beta": BETA_TEXT})
    runner = FakeLossRunner()
    assert run_cli(project, "--judge", run=runner) == 0
    turtle_calls = [argv for argv in runner.calls if "turtle" in argv[argv.index("-p") + 1]]
    # One fact extraction, one claim extraction, and one reverse check
    # per style: the extractions are judged once, not per style.
    assert len(turtle_calls) == 4
    summary = json.loads((project / "run" / "loss.json").read_text())
    beta = summary["checks"]["completeness"]["per_style"]["beta"]
    assert beta["pairs"]["explanation-01"]["fraction"] == 1.0
    assert beta["pairs"]["explanation-01"]["additions"] == 0
    assert summary["checks"]["hedging"]["per_style"]["beta"]["pairs"]["explanation-01"] == {
        "claims": 2,
        "hedged": 1,
        "certain": 0,
        "absent": 1,
        "survival": 1.0,
        "lost": [],
    }


def test_cli_an_empty_claim_list_makes_no_check_call(project, capsys):
    class NoHedges(FakeLossRunner):
        def reply(self, prompt):
            if prompt.startswith("List the claims"):
                return "[]"
            return super().reply(prompt)

    assert run_cli(project, "--judge", run=NoHedges()) == 0
    summary = json.loads((project / "run" / "loss.json").read_text())
    stats = summary["checks"]["hedging"]["per_style"]["alpha"]
    assert stats["pairs"]["explanation-01"]["claims"] == 0
    assert stats["median"] is None
    out = capsys.readouterr().out
    assert "alpha: completeness median 0.5, hedging without a scored pair" in out


def test_cli_offline_without_raw_data_exits_2(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project)
    assert error.value.code == 2


def test_cli_offline_rescores_the_stored_rows(project):
    run_cli(project, "--judge")
    first = json.loads((project / "run" / "loss.json").read_text())
    assert run_cli(project) == 0
    second = json.loads((project / "run" / "loss.json").read_text())
    first.pop("date")
    second.pop("date")
    assert first == second


def test_cli_resume_makes_no_new_calls(project):
    run_cli(project, "--judge")
    second_runner = FakeLossRunner()
    assert run_cli(project, "--judge", run=second_runner) == 0
    assert second_runner.calls == []


def test_cli_parallel_judge_matches_the_serial_artifacts(tmp_path):
    roots = {}
    for name, width in (("serial", "1"), ("wide", "3")):
        root = tmp_path / name
        root.mkdir()
        make_project(root)
        assert run_cli(root, "--judge", "--parallel", width) == 0
        roots[name] = root
    summaries = []
    for root in roots.values():
        summary = json.loads((root / "run" / "loss.json").read_text())
        summary.pop("date")
        summary["judge"].pop("judged_date")
        summaries.append(summary)
    assert summaries[0] == summaries[1]
    rows = [
        json.loads(line)
        for line in (roots["wide"] / "run" / "loss-raw.jsonl").read_text().splitlines()
    ]
    keys = Counter(row["key"] for row in rows if row.get("type") == "call")
    assert keys
    assert max(keys.values()) == 1


def test_cli_parallel_below_1_exits_2(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--parallel", "0")
    assert error.value.code == 2


def test_cli_judge_works_in_a_workdir_outside_the_run(project):
    seen = []

    class WorkdirProbe(FakeLossRunner):
        def __call__(self, argv, cwd, env=None):
            seen.append((Path(cwd), Path(cwd).is_dir()))
            return super().__call__(argv, cwd)

    assert run_cli(project, "--judge", run=WorkdirProbe()) == 0
    assert seen
    workdirs = {cwd for cwd, _ in seen}
    assert len(workdirs) == 1
    assert all(existed for _, existed in seen)
    workdir = workdirs.pop()
    assert project.resolve() not in workdir.resolve().parents
    assert not workdir.exists()


def test_cli_meta_mismatch_exits_2(project):
    run_cli(project, "--judge")
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--model", "haiku")
    assert error.value.code == 2


def test_cli_meta_upgrade_appends_a_row(project):
    run_dir = project / "run"
    old_meta = {
        "type": "meta",
        "date": "2026-01-01T00:00:00+00:00",
        "claude_version": "1.0.0",
        "model": "opus",
        "flags": [],
        "answers_sha256": sha256_of(run_dir / "answers.jsonl"),
    }
    write_jsonl(run_dir / "loss-raw.jsonl", [old_meta])
    assert run_cli(project, "--judge") == 0
    metas = [
        row
        for line in (run_dir / "loss-raw.jsonl").read_text().splitlines()
        if (row := json.loads(line)).get("type") == "meta"
    ]
    assert len(metas) == 2
    assert "fact_mine" not in metas[0]
    assert metas[1]["fact_mine"] == "two-way"
    assert metas[1]["date"] == "2026-01-01T00:00:00+00:00"


def test_cli_a_fact_mine_mismatch_exits_2(project):
    run_dir = project / "run"
    old_meta = {
        "type": "meta",
        "date": "2026-01-01T00:00:00+00:00",
        "model": "opus",
        "fact_mine": "three-way",
        "answers_sha256": sha256_of(run_dir / "answers.jsonl"),
    }
    write_jsonl(run_dir / "loss-raw.jsonl", [old_meta])
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_judge_model_must_differ_from_the_writer(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--model", "sonnet")
    assert error.value.code == 2


def test_cli_rejects_an_unknown_check(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--checks", "completeness,vibes")
    assert error.value.code == 2


def test_cli_needs_gate_data(project):
    (project / "run" / "fidelity.jsonl").unlink()
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_a_failing_pair_warns_and_exits_1(project):
    fidelity_path = project / "run" / "fidelity.jsonl"
    rows = [json.loads(line) for line in fidelity_path.read_text().splitlines()]
    rows.append(
        {
            "prompt_id": "explanation-02",
            "style": "alpha",
            "pass": False,
            "answer_sha256": "irrelevant",
        }
    )
    write_jsonl(fidelity_path, rows)
    assert run_cli(project, "--judge") == 1
    summary = json.loads((project / "run" / "loss.json").read_text())
    assert summary["pairs"] == {"alpha": ["explanation-01"]}
    assert any("explanation-02: the pair failed the gate" in w for w in summary["warnings"])


def test_cli_a_checks_subset_marks_the_rest_unjudged(project):
    assert run_cli(project, "--judge", "--checks", "completeness") == 1
    summary = json.loads((project / "run" / "loss.json").read_text())
    assert summary["checks"]["completeness"]["judged"] is True
    assert summary["checks"]["hedging"]["judged"] is False
    report = (project / "run" / "loss.md").read_text()
    assert "The check is not judged." in report
    assert any("hedging check has no judge data" in w for w in summary["warnings"])


def test_cli_unparseable_marks_retry_then_warn_and_exit_1(project):
    class BadChecker(FakeLossRunner):
        def __init__(self):
            super().__init__()
            self.check_calls = 0

        def reply(self, prompt):
            if prompt.startswith("Check each claim"):
                self.check_calls += 1
                return "no json at all"
            return super().reply(prompt)

    runner = BadChecker()
    assert run_cli(project, "--judge", run=runner) == 1
    # Two attempts per direction: the forward check and the reverse check.
    assert runner.check_calls == 4
    summary = json.loads((project / "run" / "loss.json").read_text())
    assert any("the fact check returned no usable marks" in w for w in summary["warnings"])
    assert any("the fact reverse check returned no usable marks" in w for w in summary["warnings"])
    assert any("no usable survival marks" in w for w in summary["warnings"])
