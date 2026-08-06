"""Tests for the clarity ranking. No test touches the network: the
claude subprocess is replaced with fake runners that return canned
stream-json output."""

import hashlib
import json
import threading
from collections import Counter
from pathlib import Path

import pytest

from rank import build_schedule, cli, contest_key, fit_bradley_terry, parse_pick, score_contests

ALPHA_TEXT = "The quick brown fox jumps."
BETA_TEXT = "The big red bear sleeps."
UNSTYLED_TEXT = "The slow green turtle crawls."

ANIMALS = ("fox", "bear", "turtle")

# The intransitive cycle of the fake judge: every competitor ends the
# round robin at one win and one loss, so every Bradley-Terry
# strength is exactly 1.0.
WINNER_BY_PAIR = {
    frozenset(("fox", "turtle")): "fox",
    frozenset(("bear", "fox")): "bear",
    frozenset(("turtle", "bear")): "turtle",
}


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def arm(text):
    return {"text": text, "sha256": sha(text)}


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


def animals_of(prompt):
    """The animal of Text 1 and the animal of Text 2 of a judge prompt."""
    head, _, tail = prompt.partition("Text 2:")
    (first,) = [animal for animal in ANIMALS if animal in head]
    (second,) = [animal for animal in ANIMALS if animal in tail]
    return first, second


class FakeRankRunner:
    """Picks the cycle winner of the two texts, consistent in both orders."""

    def __init__(self):
        self.calls = []
        # Parallel judge calls share the runner, so the lock covers
        # the calls list.
        self.lock = threading.Lock()

    def __call__(self, argv, cwd):
        with self.lock:
            self.calls.append(argv)
            prompt = argv[argv.index("-p") + 1]
            return stream(self.reply(prompt))

    def reply(self, prompt):
        first, second = animals_of(prompt)
        winner = WINNER_BY_PAIR[frozenset((first, second))]
        return "1" if winner == first else "2"


class SplitRunner:
    """Always picks the first position: pure position bias, all splits."""

    def __init__(self):
        self.calls = []
        self.lock = threading.Lock()

    def __call__(self, argv, cwd):
        with self.lock:
            self.calls.append(argv)
        return stream("1")


def test_build_schedule_pairs_every_competitor():
    pairs = {"alpha": ["p-01"], "beta": ["p-01"]}
    index = {
        ("p-01", "alpha"): arm(ALPHA_TEXT),
        ("p-01", "beta"): arm(BETA_TEXT),
        ("p-01", None): arm(UNSTYLED_TEXT),
    }
    competitors, contests = build_schedule(pairs, index)
    assert competitors == ["alpha", "beta", "unstyled"]
    assert [(c["a"], c["b"], c["prompt_id"]) for c in contests] == [
        ("alpha", "beta", "p-01"),
        ("alpha", "unstyled", "p-01"),
        ("beta", "unstyled", "p-01"),
    ]
    assert contests[0]["a_sha"] == sha(ALPHA_TEXT)
    assert contests[0]["b_text"] == BETA_TEXT
    assert not any(c["identical"] for c in contests)


def test_build_schedule_skips_a_prompt_missing_a_side():
    pairs = {"alpha": ["p-01"], "beta": []}
    index = {
        ("p-01", "alpha"): arm(ALPHA_TEXT),
        ("p-01", "beta"): arm(BETA_TEXT),
        ("p-01", None): arm(UNSTYLED_TEXT),
        ("p-02", None): arm("Another unstyled answer."),
    }
    competitors, contests = build_schedule(pairs, index)
    assert competitors == ["alpha", "unstyled"]
    assert [(c["a"], c["b"], c["prompt_id"]) for c in contests] == [("alpha", "unstyled", "p-01")]


def test_build_schedule_marks_identical_texts():
    pairs = {"alpha": ["p-01"]}
    index = {
        ("p-01", "alpha"): arm(UNSTYLED_TEXT),
        ("p-01", None): arm(UNSTYLED_TEXT),
    }
    _, contests = build_schedule(pairs, index)
    assert [c["identical"] for c in contests] == [True]


def test_parse_pick_accepts_only_a_position():
    assert parse_pick("1") == 1
    assert parse_pick(" 2 \n") == 2
    assert parse_pick("Text 1") == 1
    assert parse_pick("text 2") == 2
    assert parse_pick('"2"') == 2
    assert parse_pick("**1**") == 1
    assert parse_pick("3") is None
    assert parse_pick("1 or 2") is None
    assert parse_pick("the first") is None
    assert parse_pick("12") is None


def one_pair_schedule(styled_text=ALPHA_TEXT, unstyled_text=UNSTYLED_TEXT):
    pairs = {"alpha": ["p-01"]}
    index = {("p-01", "alpha"): arm(styled_text), ("p-01", None): arm(unstyled_text)}
    return build_schedule(pairs, index)


def test_scoring_a_decisive_win():
    competitors, contests = one_pair_schedule()
    rows = {
        contest_key("p-01", sha(ALPHA_TEXT), sha(UNSTYLED_TEXT)): {"output": "1"},
        contest_key("p-01", sha(UNSTYLED_TEXT), sha(ALPHA_TEXT)): {"output": "2"},
    }
    result = score_contests(competitors, contests, rows)
    assert result.matchups == [
        {
            "a": "alpha",
            "b": "unstyled",
            "contests": 1,
            "wins_a": 1,
            "wins_b": 0,
            "splits": 0,
            "unscored": 0,
            "net": 1,
        }
    ]
    assert result.win_matrix == {"alpha": {"unstyled": 1.0}, "unstyled": {"alpha": 0.0}}
    assert result.position_bias == {
        "first_pick_rate": 0.5,
        "picks": 2,
        "split_rate": 0.0,
        "contests": 1,
    }
    assert result.warnings == []
    assert result.bradley_terry["fitted"] is False


def test_scoring_a_disagreement_is_a_split():
    competitors, contests = one_pair_schedule()
    rows = {
        contest_key("p-01", sha(ALPHA_TEXT), sha(UNSTYLED_TEXT)): {"output": "1"},
        contest_key("p-01", sha(UNSTYLED_TEXT), sha(ALPHA_TEXT)): {"output": "1"},
    }
    result = score_contests(competitors, contests, rows)
    matchup = result.matchups[0]
    assert (matchup["wins_a"], matchup["wins_b"], matchup["splits"]) == (0, 0, 1)
    assert result.win_matrix == {"alpha": {"unstyled": 0.5}, "unstyled": {"alpha": 0.5}}
    assert result.position_bias["first_pick_rate"] == 1.0
    assert result.position_bias["split_rate"] == 1.0
    assert result.warnings == []


def test_scoring_a_missing_pick_is_unscored():
    competitors, contests = one_pair_schedule()
    rows = {contest_key("p-01", sha(ALPHA_TEXT), sha(UNSTYLED_TEXT)): {"output": "1"}}
    result = score_contests(competitors, contests, rows)
    matchup = result.matchups[0]
    assert (matchup["wins_a"], matchup["wins_b"], matchup["splits"], matchup["unscored"]) == (
        0,
        0,
        0,
        1,
    )
    assert result.position_bias == {
        "first_pick_rate": 1.0,
        "picks": 1,
        "split_rate": None,
        "contests": 0,
    }
    assert any("no usable pick" in w for w in result.warnings)


def test_scoring_identical_texts_splits_without_a_row():
    competitors, contests = one_pair_schedule(styled_text=UNSTYLED_TEXT)
    result = score_contests(competitors, contests, rows={})
    matchup = result.matchups[0]
    assert (matchup["splits"], matchup["unscored"]) == (1, 0)
    assert result.position_bias["picks"] == 0
    assert any("identical" in w for w in result.warnings)


def test_length_confound_orients_by_length():
    long_text = "The long answer repeats itself with many extra words in it."
    short_text = "The short answer stops."
    competitors, contests = one_pair_schedule(styled_text=long_text, unstyled_text=short_text)
    rows = {
        contest_key("p-01", sha(long_text), sha(short_text)): {"output": "2"},
        contest_key("p-01", sha(short_text), sha(long_text)): {"output": "1"},
    }
    result = score_contests(competitors, contests, rows)
    assert result.length_confound == {
        "n": 1,
        "pearson": None,
        "spearman": None,
        "longer_win_rate": 0.0,
    }


def test_equal_word_counts_contribute_no_length_sample():
    competitors, contests = one_pair_schedule()
    rows = {
        contest_key("p-01", sha(ALPHA_TEXT), sha(UNSTYLED_TEXT)): {"output": "1"},
        contest_key("p-01", sha(UNSTYLED_TEXT), sha(ALPHA_TEXT)): {"output": "2"},
    }
    result = score_contests(competitors, contests, rows)
    assert result.length_confound == {
        "n": 0,
        "pearson": None,
        "spearman": None,
        "longer_win_rate": None,
    }


def test_bradley_terry_orders_a_lopsided_matrix():
    outcomes = [
        ("alpha", "unstyled", 1),
        ("alpha", "unstyled", 1),
        ("alpha", "unstyled", 0),
        ("beta", "unstyled", 0),
        ("beta", "unstyled", 0),
        ("beta", "unstyled", 1),
        ("alpha", "beta", 1),
        ("alpha", "beta", 1),
        ("alpha", "beta", 0),
    ]
    block, warnings = fit_bradley_terry(outcomes, resamples=50)
    assert warnings == []
    assert block["fitted"] is True
    assert block["anchored_on"] == "unstyled"
    strengths = {name: entry["strength"] for name, entry in block["strengths"].items()}
    assert strengths["unstyled"] == 1.0
    assert strengths["alpha"] > strengths["unstyled"] > strengths["beta"]


def test_bradley_terry_a_shutout_strength_is_none():
    outcomes = [
        ("alpha", "unstyled", 1),
        ("alpha", "unstyled", 1),
        ("alpha", "beta", 1),
        ("alpha", "beta", 1),
        ("beta", "unstyled", 0.5),
        ("beta", "unstyled", 0.5),
    ]
    block, warnings = fit_bradley_terry(outcomes, resamples=0)
    assert block["strengths"]["alpha"] == {"strength": None, "ci_low": None, "ci_high": None}
    assert block["strengths"]["beta"]["strength"] == 1.0
    assert block["strengths"]["unstyled"]["strength"] == 1.0
    assert any(w.startswith("alpha:") for w in warnings)


def test_bradley_terry_stays_dormant_below_3_competitors():
    block, warnings = fit_bradley_terry([("alpha", "unstyled", 1)])
    assert block == {
        "fitted": False,
        "note": "the fit needs at least 3 competitors with a scored contest",
    }
    assert warnings == []


def test_bradley_terry_bootstrap_is_deterministic_and_brackets_the_strength():
    cycle = [("alpha", "beta", 0), ("alpha", "unstyled", 1), ("beta", "unstyled", 0)]
    first, _ = fit_bradley_terry(cycle)
    second, _ = fit_bradley_terry(cycle)
    assert first == second
    for name in ("alpha", "beta", "unstyled"):
        assert first["strengths"][name]["strength"] == 1.0
    assert first["strengths"]["unstyled"]["ci_low"] is None
    entry = first["strengths"]["alpha"]
    assert entry["ci_low"] <= entry["strength"] <= entry["ci_high"]
    assert first["bootstrap"] == {"resamples": 1000, "seed": 0}


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row) + "\n")


def make_project(tmp_path, styled_answers=None, prompt_ids=("explanation-01",), failures=()):
    """A gated run: unstyled turtle plus one styled answer per style."""
    styled_answers = styled_answers or {"alpha": ALPHA_TEXT, "beta": BETA_TEXT}
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    answers, fidelity = [], []
    for prompt_id in prompt_ids:
        answers.append({"prompt_id": prompt_id, "style": None, "answer": UNSTYLED_TEXT})
        fidelity.append(
            {
                "prompt_id": prompt_id,
                "style": None,
                "pass": None,
                "answer_sha256": sha(UNSTYLED_TEXT),
            }
        )
        for style, text in styled_answers.items():
            answers.append({"prompt_id": prompt_id, "style": style, "answer": text})
            fidelity.append(
                {
                    "prompt_id": prompt_id,
                    "style": style,
                    "pass": (style, prompt_id) not in failures,
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
    return cli.main([str(project / "run"), *extra], run=run or FakeRankRunner())


def test_cli_judge_writes_the_artifacts(project, capsys):
    assert run_cli(project, "--judge") == 0
    summary = json.loads((project / "run" / "rank.json").read_text())
    assert summary["design"] == "clarity-v1"
    assert summary["competitors"] == ["alpha", "beta", "unstyled"]
    assert summary["matchups"] == [
        {
            "a": "alpha",
            "b": "beta",
            "contests": 1,
            "wins_a": 0,
            "wins_b": 1,
            "splits": 0,
            "unscored": 0,
            "net": -1,
        },
        {
            "a": "alpha",
            "b": "unstyled",
            "contests": 1,
            "wins_a": 1,
            "wins_b": 0,
            "splits": 0,
            "unscored": 0,
            "net": 1,
        },
        {
            "a": "beta",
            "b": "unstyled",
            "contests": 1,
            "wins_a": 0,
            "wins_b": 1,
            "splits": 0,
            "unscored": 0,
            "net": -1,
        },
    ]
    assert summary["win_matrix"] == {
        "alpha": {"beta": 0.0, "unstyled": 1.0},
        "beta": {"alpha": 1.0, "unstyled": 0.0},
        "unstyled": {"alpha": 0.0, "beta": 1.0},
    }
    assert summary["position_bias"] == {
        "first_pick_rate": 0.5,
        "picks": 6,
        "split_rate": 0.0,
        "contests": 3,
    }
    bradley_terry = summary["bradley_terry"]
    assert bradley_terry["fitted"] is True
    assert bradley_terry["anchored_on"] == "unstyled"
    assert bradley_terry["strengths"]["alpha"] == {"strength": 1.0, "ci_low": 1.0, "ci_high": 1.0}
    assert bradley_terry["strengths"]["beta"] == {"strength": 1.0, "ci_low": 1.0, "ci_high": 1.0}
    assert bradley_terry["strengths"]["unstyled"] == {
        "strength": 1.0,
        "ci_low": None,
        "ci_high": None,
    }
    assert summary["by_task_type"] == {"explanation": summary["matchups"]}
    assert summary["length_confound"] == {
        "n": 0,
        "pearson": None,
        "spearman": None,
        "longer_win_rate": None,
    }
    assert summary["warnings"] == []
    raw_rows = [
        json.loads(line) for line in (project / "run" / "rank-raw.jsonl").read_text().splitlines()
    ]
    call_rows = [row for row in raw_rows if row.get("type") == "call"]
    assert call_rows
    assert all(isinstance(row["wall_ms"], int) for row in call_rows)
    assert all(row["input_tokens"] == 3 for row in call_rows)
    assert all(row["cache_creation_input_tokens"] == 2 for row in call_rows)
    assert all(row["cache_read_input_tokens"] == 1 for row in call_rows)
    report = (project / "run" / "rank.md").read_text()
    assert "## Call timing" in report
    assert "## Harness spend" in report
    assert "| alpha | beta | 1 | 0 | 1 | 0 | 0 | -1 |" in report
    assert "The scale is anchored on unstyled at strength 1.0." in report
    assert "| alpha | 1.0 | [1.0, 1.0] |" in report
    assert "| unstyled | 1.0 | n/a |" in report
    assert "First-pick rate: 0.5 over 6 usable picks." in report
    out = capsys.readouterr().out
    assert "alpha: 1-1-0 (win-loss-split), strength 1.0" in out
    assert "beta: 1-1-0 (win-loss-split), strength 1.0" in out
    assert "unstyled: 1-1-0 (win-loss-split), strength 1.0" in out


def test_cli_judge_prompts_are_blind(project):
    runner = FakeRankRunner()
    run_cli(project, "--judge", run=runner)
    assert runner.calls
    for argv in runner.calls:
        assert "--plugin-dir" not in argv
        settings = json.loads(argv[argv.index("--settings") + 1])
        assert settings["outputStyle"] == "default"
        prompt = argv[argv.index("-p") + 1]
        assert "alpha" not in prompt
        assert "beta" not in prompt
        assert "styled" not in prompt.lower()
        texts_shown = [t for t in (ALPHA_TEXT, BETA_TEXT, UNSTYLED_TEXT) if t in prompt]
        assert len(texts_shown) == 2


def test_cli_judge_emits_both_orders_per_contest(project):
    run_cli(project, "--judge")
    raw = (project / "run" / "rank-raw.jsonl").read_text().splitlines()
    rows = [json.loads(line) for line in raw]
    keys = {row.get("key") for row in rows}
    a, b, u = sha(ALPHA_TEXT), sha(BETA_TEXT), sha(UNSTYLED_TEXT)
    for first, second in ((a, b), (b, a), (a, u), (u, a), (b, u), (u, b)):
        assert f"clarity:explanation-01:{first}:{second}" in keys
    call = next(row for row in rows if row.get("key") == f"clarity:explanation-01:{a}:{u}")
    assert (call["first"], call["second"]) == ("alpha", "unstyled")
    assert (call["first_sha256"], call["second_sha256"]) == (a, u)


def test_cli_resume_makes_no_new_calls(project):
    run_cli(project, "--judge")
    second_runner = FakeRankRunner()
    assert run_cli(project, "--judge", run=second_runner) == 0
    assert second_runner.calls == []


def test_cli_offline_rescores_the_stored_rows(project):
    run_cli(project, "--judge")
    first = json.loads((project / "run" / "rank.json").read_text())
    assert run_cli(project) == 0
    second = json.loads((project / "run" / "rank.json").read_text())
    first.pop("date")
    second.pop("date")
    assert first == second


def test_cli_offline_without_raw_data_exits_2(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project)
    assert error.value.code == 2


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
        summary = json.loads((root / "run" / "rank.json").read_text())
        summary.pop("date")
        summary["judge"].pop("judged_date")
        summaries.append(summary)
    assert summaries[0] == summaries[1]
    rows = [
        json.loads(line)
        for line in (roots["wide"] / "run" / "rank-raw.jsonl").read_text().splitlines()
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

    class WorkdirProbe(FakeRankRunner):
        def __call__(self, argv, cwd):
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


def test_cli_judge_model_must_differ_from_the_writer(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--model", "sonnet")
    assert error.value.code == 2


def test_cli_needs_gate_data(project):
    (project / "run" / "fidelity.jsonl").unlink()
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_a_style_named_unstyled_exits_2(tmp_path):
    project = make_project(tmp_path, styled_answers={"unstyled": ALPHA_TEXT})
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_all_pairs_gate_failed_exits_2(tmp_path):
    project = make_project(
        tmp_path, failures={("alpha", "explanation-01"), ("beta", "explanation-01")}
    )
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_a_gate_failed_pair_drops_only_its_contests(tmp_path):
    project = make_project(
        tmp_path,
        prompt_ids=("explanation-01", "explanation-02"),
        failures={("beta", "explanation-02")},
    )
    assert run_cli(project, "--judge") == 1
    summary = json.loads((project / "run" / "rank.json").read_text())
    matchups = {(m["a"], m["b"]): m for m in summary["matchups"]}
    assert matchups[("alpha", "beta")]["contests"] == 1
    assert matchups[("alpha", "unstyled")]["contests"] == 2
    assert matchups[("beta", "unstyled")]["contests"] == 1
    assert any("failed the gate" in w for w in summary["warnings"])


def test_cli_an_unusable_pick_retries_then_warns_and_exits_1(project):
    class BadOrder(FakeRankRunner):
        def reply(self, prompt):
            if animals_of(prompt) == ("fox", "turtle"):
                return "no pick at all"
            return super().reply(prompt)

    runner = BadOrder()
    assert run_cli(project, "--judge", run=runner) == 1
    bad_calls = [
        argv for argv in runner.calls if animals_of(argv[argv.index("-p") + 1]) == ("fox", "turtle")
    ]
    assert len(bad_calls) == 2
    summary = json.loads((project / "run" / "rank.json").read_text())
    matchups = {(m["a"], m["b"]): m for m in summary["matchups"]}
    assert matchups[("alpha", "unstyled")]["unscored"] == 1
    assert any("no usable pick" in w for w in summary["warnings"])


def test_cli_a_split_judge_reports_the_position_bias(project):
    assert run_cli(project, "--judge", run=SplitRunner()) == 0
    summary = json.loads((project / "run" / "rank.json").read_text())
    assert summary["position_bias"] == {
        "first_pick_rate": 1.0,
        "picks": 6,
        "split_rate": 1.0,
        "contests": 3,
    }
    assert all(m["splits"] == 1 for m in summary["matchups"])
    assert summary["bradley_terry"]["strengths"]["alpha"]["strength"] == 1.0
    assert summary["warnings"] == []


def test_cli_identical_texts_split_without_calls(tmp_path):
    project = make_project(tmp_path, styled_answers={"alpha": UNSTYLED_TEXT})
    runner = FakeRankRunner()
    assert run_cli(project, "--judge", run=runner) == 1
    assert runner.calls == []
    summary = json.loads((project / "run" / "rank.json").read_text())
    matchup = summary["matchups"][0]
    assert (matchup["splits"], matchup["unscored"]) == (1, 0)
    assert any("identical" in w for w in summary["warnings"])
    assert summary["bradley_terry"]["fitted"] is False


def test_cli_groups_the_contests_by_task_type(tmp_path):
    project = make_project(tmp_path, prompt_ids=("explanation-01", "debugging-01"))
    assert run_cli(project, "--judge") == 0
    summary = json.loads((project / "run" / "rank.json").read_text())
    assert sorted(summary["by_task_type"]) == ["debugging", "explanation"]
    for matchups in summary["by_task_type"].values():
        assert [m["contests"] for m in matchups] == [1, 1, 1]
