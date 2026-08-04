"""Tests for the reader-value checks. No test touches the network:
the claude subprocess is replaced with fake runners that return
canned stream-json output."""

import hashlib
import json
import re
from functools import partial
from pathlib import Path

import pytest

from runner.provenance import sha256_of
from value import cli, extract_json, judge_argv, score_checks, select_pairs
from value.analysis import shared_facts
from value.judges import JudgeSession, parse_bools, select_balanced, select_facts
from value.report import build_value_report, build_value_summary
from value.similarity import mean_pairwise_f1, unigram_f1

STYLED_TEXT = "The quick brown fox jumps."
UNSTYLED_TEXT = "The slow green turtle crawls."
BETA_TEXT = "The big red bear sleeps."


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stream(result_text, output_style="default"):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": "claude-haiku-4-5",
    }
    result = {
        "type": "result",
        "is_error": False,
        "result": result_text,
        "usage": {"output_tokens": 5},
        "duration_ms": 10,
    }
    return "\n".join(json.dumps(event) for event in (init, result))


class FakeJudgeRunner:
    """Routes each judge prompt to a canned reply.

    The unstyled turtle text plays the weaker arm: its reader misses
    the last question, its restatements differ, and its round-trip
    loses words. Every other text is judged faithful, so its styled
    pair wins. The quiz replies match the item count of the prompt.
    """

    def __init__(self):
        self.calls = []
        self.turtle_restatements = 0

    def __call__(self, argv, cwd):
        self.calls.append(argv)
        prompt = argv[argv.index("-p") + 1]
        return stream(self.reply(prompt))

    @staticmethod
    def _numbered_count(prompt):
        return len(re.findall(r"(?m)^\d+\. ", prompt))

    def reply(self, prompt):
        if prompt.startswith("You write a quiz from an answer key"):
            n = self._numbered_count(prompt)
            return json.dumps([f"Q{number}" for number in range(1, n + 1)])
        if prompt.startswith("Answer the questions"):
            n = self._numbered_count(prompt)
            answers = [f"A{number}" for number in range(1, n + 1)]
            if "turtle" in prompt:
                answers[-1] = "NOT IN TEXT"
            return json.dumps(answers)
        if prompt.startswith("Grade the quiz answers"):
            grades = [True] * prompt.count("Question:")
            if "Answer: NOT IN TEXT" in prompt:
                grades[-1] = False
            return json.dumps(grades)
        if prompt.startswith("Restate the text"):
            if "turtle" in prompt:
                self.turtle_restatements += 1
                return f"turtle restatement {self.turtle_restatements}"
            return "one same restatement"
        if prompt.startswith("Translate the text below to Italian"):
            if "turtle" in prompt:
                return "tartaruga lenta"
            return "volpe rapida" if "fox" in prompt else "orso grande"
        if prompt.startswith("Translate the text below to English"):
            if "tartaruga" in prompt:
                return "a slow turtle crawled"
            return STYLED_TEXT if "volpe" in prompt else BETA_TEXT
        raise AssertionError(f"unrouted judge prompt: {prompt[:60]}")


def test_unigram_f1_on_known_texts():
    assert unigram_f1("a b b", "a b b") == 1.0
    assert unigram_f1("a b", "c d") == 0.0
    assert unigram_f1("", "") == 1.0
    assert unigram_f1("a b b", "a b c") == pytest.approx(2 / 3)


def test_mean_pairwise_f1_averages_every_pair():
    assert mean_pairwise_f1(["a b", "a b", "a c"]) == pytest.approx((1.0 + 0.5 + 0.5) / 3)
    with pytest.raises(ValueError):
        mean_pairwise_f1(["alone"])


def test_select_pairs_takes_only_passing_pairs():
    shas = {
        ("p-01", None): "u1",
        ("p-01", "alpha"): "s1",
        ("p-02", None): "u2",
        ("p-02", "alpha"): "s2",
        ("p-03", "alpha"): "s3",
        ("p-04", None): "u4",
        ("p-04", "alpha"): "changed",
    }
    rows = [
        {"prompt_id": "p-01", "style": None, "pass": None, "answer_sha256": "u1"},
        {"prompt_id": "p-01", "style": "alpha", "pass": True, "answer_sha256": "s1"},
        {"prompt_id": "p-02", "style": "alpha", "pass": False, "answer_sha256": "s2"},
        {"prompt_id": "p-03", "style": "alpha", "pass": True, "answer_sha256": "s3"},
        {"prompt_id": "p-04", "style": "alpha", "pass": True, "answer_sha256": "s4"},
    ]
    pairs, warnings = select_pairs(rows, shas)
    assert pairs == {"alpha": ["p-01"]}
    assert any("p-02: the pair failed the gate" in w for w in warnings)
    assert any("p-03: no unstyled counterpart" in w for w in warnings)
    assert any("p-04: the answer changed after the gate" in w for w in warnings)


def test_judge_argv_is_blind():
    argv = judge_argv("the prompt", "haiku")
    assert "--plugin-dir" not in argv
    settings = json.loads(argv[argv.index("--settings") + 1])
    assert settings["outputStyle"] == "default"
    assert "--disallowedTools" in argv
    assert "--exclude-dynamic-system-prompt-sections" in argv


def test_extract_json_is_lenient():
    assert extract_json("[1, 2]") == [1, 2]
    assert extract_json("Sure!\n```json\n[true]\n```\nDone.") == [True]
    assert extract_json('The answers are ["a", "b"] as requested.') == ["a", "b"]
    assert extract_json("no json here") is None


def test_select_facts_spaces_evenly_and_keeps_the_order():
    facts = [str(number) for number in range(13)]
    assert select_facts(facts, 5) == ["0", "2", "5", "7", "10"]
    assert select_facts(["a", "b"], 5) == ["a", "b"]


def test_select_balanced_splits_the_cap_between_the_sources():
    unstyled = [f"U{number}" for number in range(10)]
    styled = [f"S{number}" for number in range(10)]
    facts, sources = select_balanced(unstyled, styled, 6)
    assert sources == {"unstyled": 3, "styled": 3}
    assert facts == select_facts(unstyled, 3) + select_facts(styled, 3)


def test_select_balanced_gives_an_odd_cap_extra_to_the_unstyled_side():
    unstyled = [f"U{number}" for number in range(10)]
    styled = [f"S{number}" for number in range(10)]
    _, sources = select_balanced(unstyled, styled, 5)
    assert sources == {"unstyled": 3, "styled": 2}


def test_select_balanced_lets_a_short_side_yield_its_remainder():
    ten = [f"X{number}" for number in range(10)]
    _, sources = select_balanced(ten, ["S0"], 6)
    assert sources == {"unstyled": 5, "styled": 1}
    _, sources = select_balanced(["U0"], ten, 6)
    assert sources == {"unstyled": 1, "styled": 5}
    facts, sources = select_balanced(["U0"], [], 6)
    assert facts == ["U0"]
    assert sources == {"unstyled": 1, "styled": 0}


def test_shared_facts_takes_the_survivors_of_both_directions():
    pairs = {"alpha": ["p-01"]}
    answers = {
        ("p-01", "alpha"): {"text": "s", "sha256": "S"},
        ("p-01", None): {"text": "u", "sha256": "U"},
    }
    loss_rows = {
        "completeness:facts:U": {"output": '["F1", "F2", "F3"]'},
        "completeness:check:S": {"output": "[true, false, true]"},
        "completeness:facts:S": {"output": '["G1", "G2"]'},
        "completeness:reverse:S": {"output": "[false, true]"},
    }
    facts, warnings = shared_facts(pairs, answers, loss_rows)
    assert facts == {("alpha", "p-01"): {"unstyled": ["F1", "F3"], "styled": ["G2"]}}
    assert warnings == []


def test_shared_facts_accepts_an_empty_fact_list_without_a_check_row():
    pairs = {"alpha": ["p-01"]}
    answers = {
        ("p-01", "alpha"): {"text": "s", "sha256": "S"},
        ("p-01", None): {"text": "u", "sha256": "U"},
    }
    loss_rows = {
        "completeness:facts:U": {"output": '["F1"]'},
        "completeness:check:S": {"output": "[true]"},
        "completeness:facts:S": {"output": "[]"},
    }
    facts, warnings = shared_facts(pairs, answers, loss_rows)
    assert facts == {("alpha", "p-01"): {"unstyled": ["F1"], "styled": []}}
    assert warnings == []


def test_shared_facts_warns_on_missing_and_unparsable_rows():
    pairs = {"alpha": ["p-01", "p-02", "p-03"]}
    answers = {
        ("p-01", "alpha"): {"text": "s1", "sha256": "S1"},
        ("p-01", None): {"text": "u1", "sha256": "U1"},
        ("p-02", "alpha"): {"text": "s2", "sha256": "S2"},
        ("p-02", None): {"text": "u2", "sha256": "U2"},
        ("p-03", "alpha"): {"text": "s3", "sha256": "S3"},
        ("p-03", None): {"text": "u3", "sha256": "U3"},
    }
    loss_rows = {
        "completeness:facts:U2": {"output": '["F1"]'},
        "completeness:check:S2": {"output": "no json here"},
        "completeness:facts:U3": {"output": '["F1"]'},
        "completeness:check:S3": {"output": "[true]"},
    }
    facts, warnings = shared_facts(pairs, answers, loss_rows)
    assert facts == {}
    assert any(
        "alpha/p-01: loss-raw.jsonl holds no completeness rows for the unstyled facts" in w
        for w in warnings
    )
    assert any(
        "alpha/p-02: the completeness rows for the unstyled facts do not parse" in w
        for w in warnings
    )
    assert any(
        "alpha/p-03: loss-raw.jsonl holds no completeness rows for the styled facts" in w
        for w in warnings
    )


def pair_fixture(styled_score_rows):
    """A one-pair scoring input with hand-built raw rows."""
    answers = {
        ("p-01", "alpha"): {"text": "styled text", "sha256": "S"},
        ("p-01", None): {"text": "unstyled text", "sha256": "U"},
    }
    rows = {
        "comprehension:questions:p-01": {
            "check": "comprehension",
            "output": json.dumps(
                [
                    {"question": "Q1", "reference": "R1"},
                    {"question": "Q2", "reference": "R2"},
                ]
            ),
        }
    }
    rows.update(styled_score_rows)
    return {"alpha": ["p-01"]}, answers, rows


def grades_row(grades):
    return {"check": "comprehension", "output": json.dumps(grades)}


def test_comprehension_scoring_marks_win_loss_and_tie():
    for styled, unstyled, expected in (
        ([True, True], [True, False], "win"),
        ([True, False], [True, False], "tie"),
        ([False, False], [True, False], "loss"),
    ):
        pairs, answers, rows = pair_fixture(
            {
                "comprehension:grades:S": grades_row(styled),
                "comprehension:grades:U": grades_row(unstyled),
            }
        )
        result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
        stats = result.checks["comprehension"]["per_style"]["alpha"]
        assert stats["pairs"]["p-01"]["result"] == expected
    assert any(
        "scores worse than the unstyled answer on comprehension" in w for w in result.warnings
    )


def test_a_missing_grade_leaves_the_pair_unscored():
    pairs, answers, rows = pair_fixture({"comprehension:grades:S": grades_row([True, True])})
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    assert result.checks["comprehension"]["per_style"]["alpha"]["pairs"] == {}
    assert any("no usable score for the unstyled answer" in w for w in result.warnings)


def v2_fixture(styled_reps, unstyled_reps, styled_replies=()):
    """A one-pair scoring input with hand-built shared-facts rows."""
    rows = {
        "comprehension:v2:questions:alpha:p-01": {
            "check": "comprehension",
            "output": '["Q1", "Q2"]',
        }
    }
    for replicate, grades in enumerate(styled_reps):
        rows[f"comprehension:v2:grades:alpha:p-01:styled:{replicate}"] = grades_row(grades)
    for replicate, grades in enumerate(unstyled_reps):
        rows[f"comprehension:v2:grades:alpha:p-01:unstyled:{replicate}"] = grades_row(grades)
    for replicate, replies in enumerate(styled_replies):
        rows[f"comprehension:v2:reader:alpha:p-01:styled:{replicate}"] = {
            "check": "comprehension",
            "output": json.dumps(replies),
        }
    answers = {
        ("p-01", "alpha"): {"text": "styled text", "sha256": "S"},
        ("p-01", None): {"text": "unstyled text", "sha256": "U"},
    }
    return {"alpha": ["p-01"]}, answers, rows


def score_v2(pairs, answers, rows):
    return score_checks(
        pairs=pairs,
        answers=answers,
        rows=rows,
        paraphrases_k=3,
        comprehension_design="shared-facts-v2",
        replicates=3,
    )


def test_v2_scoring_takes_the_plurality_of_the_replicate_outcomes():
    pairs, answers, rows = v2_fixture(
        styled_reps=([True, True], [True, True], [True, False]),
        unstyled_reps=([True, False], [True, False], [True, False]),
    )
    result = score_v2(pairs, answers, rows)
    stats = result.checks["comprehension"]["per_style"]["alpha"]
    pair = stats["pairs"]["p-01"]
    assert pair["result"] == "win"
    assert pair["agreement"] == 0.667
    assert pair["questions"] == 2
    assert pair["styled"] == 0.833
    assert pair["unstyled"] == 0.5
    assert stats["mean_delta"] == 0.333
    assert stats["mean_agreement"] == 0.667
    assert result.checks["comprehension"]["design"] == "shared-facts-v2"


def test_v2_scoring_without_a_strict_plurality_is_a_tie():
    pairs, answers, rows = v2_fixture(
        styled_reps=([True, True], [True, False], [False, False]),
        unstyled_reps=([True, False], [True, False], [True, False]),
    )
    result = score_v2(pairs, answers, rows)
    pair = result.checks["comprehension"]["per_style"]["alpha"]["pairs"]["p-01"]
    assert pair["result"] == "tie"
    assert pair["agreement"] == 0.333


def test_v2_scoring_counts_the_buried_facts():
    reps = ([True, True], [True, True], [True, True])
    pairs, answers, rows = v2_fixture(
        styled_reps=reps,
        unstyled_reps=reps,
        styled_replies=(["A1", "NOT IN TEXT"], ["A1", "A2"], ["NOT IN TEXT", "NOT IN TEXT"]),
    )
    result = score_v2(pairs, answers, rows)
    stats = result.checks["comprehension"]["per_style"]["alpha"]
    assert stats["buried_fact_rate"] == 0.5


def test_v2_scoring_without_a_replicate_side_leaves_the_pair_unscored():
    pairs, answers, rows = v2_fixture(styled_reps=([True, True],), unstyled_reps=())
    result = score_v2(pairs, answers, rows)
    assert result.checks["comprehension"]["per_style"]["alpha"]["pairs"] == {}
    assert any("no usable score for the unstyled answer" in w for w in result.warnings)


def v3_fixture(styled_reps, unstyled_reps, styled_replies=(), unstyled_replies=()):
    """A one-pair scoring input with hand-built balanced-facts rows."""
    rows = {
        "comprehension:v3:questions:alpha:p-01": {
            "check": "comprehension",
            "output": '["Q1", "Q2"]',
            "sources": {"unstyled": 1, "styled": 1},
        }
    }
    for replicate, grades in enumerate(styled_reps):
        rows[f"comprehension:v3:grades:alpha:p-01:styled:{replicate}"] = grades_row(grades)
    for replicate, grades in enumerate(unstyled_reps):
        rows[f"comprehension:v3:grades:alpha:p-01:unstyled:{replicate}"] = grades_row(grades)
    for arm, replies_per_replicate in (("styled", styled_replies), ("unstyled", unstyled_replies)):
        for replicate, replies in enumerate(replies_per_replicate):
            rows[f"comprehension:v3:reader:alpha:p-01:{arm}:{replicate}"] = {
                "check": "comprehension",
                "output": json.dumps(replies),
            }
    answers = {
        ("p-01", "alpha"): {"text": "styled text", "sha256": "S"},
        ("p-01", None): {"text": "unstyled text", "sha256": "U"},
    }
    return {"alpha": ["p-01"]}, answers, rows


def score_v3(pairs, answers, rows):
    return score_checks(
        pairs=pairs,
        answers=answers,
        rows=rows,
        paraphrases_k=3,
        comprehension_design="balanced-facts-v3",
        replicates=3,
    )


def test_v3_scoring_records_the_sources_and_the_design():
    pairs, answers, rows = v3_fixture(
        styled_reps=([True, True], [True, True], [True, False]),
        unstyled_reps=([True, False], [True, False], [True, False]),
    )
    result = score_v3(pairs, answers, rows)
    check = result.checks["comprehension"]
    assert check["design"] == "balanced-facts-v3"
    pair = check["per_style"]["alpha"]["pairs"]["p-01"]
    assert pair["result"] == "win"
    assert pair["agreement"] == 0.667
    assert pair["sources"] == {"unstyled": 1, "styled": 1}


def test_v3_scoring_counts_the_buried_facts_per_arm():
    reps = ([True, True], [True, True], [True, True])
    pairs, answers, rows = v3_fixture(
        styled_reps=reps,
        unstyled_reps=reps,
        styled_replies=(["A1", "NOT IN TEXT"], ["A1", "A2"], ["A1", "A2"]),
        unstyled_replies=(["NOT IN TEXT", "NOT IN TEXT"], ["NOT IN TEXT", "A2"], ["A1", "A2"]),
    )
    result = score_v3(pairs, answers, rows)
    stats = result.checks["comprehension"]["per_style"]["alpha"]
    assert stats["buried_fact_rate"] == 0.167
    assert stats["buried_fact_rate_unstyled"] == 0.5


def paraphrase_rows(sha_key, texts):
    return {
        f"paraphrase:reader:{sha_key}:{index}": {"check": "paraphrase", "output": text}
        for index, text in enumerate(texts)
    }


def test_paraphrase_agreement_and_the_tie_threshold():
    pairs, answers, rows = pair_fixture({})
    rows.update(paraphrase_rows("S", ["same words here", "same words here", "same words here"]))
    rows.update(paraphrase_rows("U", ["same words here", "same words here", "same words also"]))
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    stats = result.checks["paraphrase"]["per_style"]["alpha"]["pairs"]["p-01"]
    assert stats["styled"] == 1.0
    assert stats["unstyled"] == pytest.approx((1.0 + 2 / 3 + 2 / 3) / 3, abs=0.001)
    assert stats["result"] == "win"

    rows.update(paraphrase_rows("U", ["same words here", "same words here", "same words here"]))
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    assert result.checks["paraphrase"]["per_style"]["alpha"]["pairs"]["p-01"]["result"] == "tie"


def test_roundtrip_loss_arithmetic():
    pairs, answers, rows = pair_fixture({})
    rows["roundtrip:back:S"] = {"check": "roundtrip", "output": "styled text"}
    rows["roundtrip:back:U"] = {"check": "roundtrip", "output": "different words entirely"}
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    stats = result.checks["roundtrip"]["per_style"]["alpha"]["pairs"]["p-01"]
    assert stats["styled"] == 0.0
    assert stats["unstyled"] == 1.0
    assert stats["result"] == "win"


def test_an_unjudged_check_warns():
    pairs, answers, rows = pair_fixture({})
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    assert result.checks["paraphrase"] == {"judged": False, "per_style": None}
    assert any("the paraphrase check has no judge data" in w for w in result.warnings)


def test_structured_calls_retry_once(tmp_path):
    outputs = iter(["garbage", "[true, false]"])

    def run(argv, cwd):
        return stream(next(outputs))

    session = JudgeSession(rows={}, sink=lambda row: None, workdir=tmp_path, run=run)
    value = session.structured(
        validate=partial(parse_bools, n=2),
        key="comprehension:grades:S",
        check="comprehension",
        role="grades",
        model="opus",
        prompt="Grade the quiz answers below.",
        prompt_id="p-01",
        answer_sha256="S",
    )
    assert value == [True, False]
    assert session.rows["comprehension:grades:S"]["output"] == "[true, false]"


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row) + "\n")


def make_project(tmp_path, styled_answers=None):
    """A gated run with one prompt and one styled answer per style."""
    styled_answers = styled_answers or {"alpha": STYLED_TEXT}
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    prompts_path = tmp_path / "prompts.yaml"
    prompts_path.write_text(
        "prompts:\n  - id: explanation-01\n    type: explanation\n    text: Explain the fox.\n"
    )
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
    loss_rows = [
        {
            "type": "meta",
            "model": "opus",
            "fact_mine": "two-way",
            "answers_sha256": sha256_of(run_dir / "answers.jsonl"),
        },
        {
            "type": "call",
            "key": f"completeness:facts:{sha(UNSTYLED_TEXT)}",
            "check": "completeness",
            "output": '["F1", "F2", "F3"]',
        },
    ]
    for text in styled_answers.values():
        loss_rows += [
            {
                "type": "call",
                "key": f"completeness:check:{sha(text)}",
                "check": "completeness",
                "output": "[true, true, true]",
            },
            {
                "type": "call",
                "key": f"completeness:facts:{sha(text)}",
                "check": "completeness",
                "output": '["G1", "G2", "G3"]',
            },
            {
                "type": "call",
                "key": f"completeness:reverse:{sha(text)}",
                "check": "completeness",
                "output": "[true, true, true]",
            },
        ]
    write_jsonl(run_dir / "loss-raw.jsonl", loss_rows)
    provenance = {
        "conditions": {"model_requested": "sonnet"},
        "prompt_set": {"sha256": sha256_of(prompts_path)},
    }
    (run_dir / "provenance.json").write_text(json.dumps(provenance))
    return tmp_path


@pytest.fixture
def project(tmp_path):
    return make_project(tmp_path)


def run_cli(project, *extra, run=None):
    argv = [str(project / "run"), *extra]
    return cli.main(argv, run=run or FakeJudgeRunner())


def test_cli_judge_writes_the_artifacts(project, capsys):
    assert run_cli(project, "--judge") == 0
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["pairs"] == {"alpha": ["explanation-01"]}
    assert summary["judges"]["replicates"] == 3
    assert summary["judges"]["comprehension_design"] == "balanced-facts-v3"
    for check in ("comprehension", "paraphrase", "roundtrip"):
        stats = summary["checks"][check]["per_style"]["alpha"]
        assert (stats["wins"], stats["losses"], stats["ties"]) == (1, 0, 0)
    assert summary["checks"]["comprehension"]["per_style"]["alpha"]["pairs"]["explanation-01"] == {
        "styled": 1.0,
        "unstyled": 0.833,
        "questions": 6,
        "agreement": 1.0,
        "result": "win",
        "sources": {"unstyled": 3, "styled": 3},
    }
    assert summary["checks"]["comprehension"]["per_style"]["alpha"]["buried_fact_rate"] == 0.0
    assert (
        summary["checks"]["comprehension"]["per_style"]["alpha"]["buried_fact_rate_unstyled"]
        == 0.167
    )
    assert summary["warnings"] == []
    report = (project / "run" / "value.md").read_text()
    assert report.count("| alpha | 1 | 0 | 0 |\n") == 2
    assert "worded by both answers in balance" in report
    assert "| alpha | 1 | 0 | 0 | 0.167 | 1.0 | 0.0 | 0.167 |" in report
    assert "- alpha: the styled answer holds (1 wins, 0 losses, 0 ties)." in report
    assert "| explanation-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |" in report
    out = capsys.readouterr().out
    assert "alpha: comprehension 1-0-0, paraphrase 1-0-0, roundtrip 1-0-0 (win-loss-tie)" in out


def test_cli_judge_prompts_are_blind(project):
    runner = FakeJudgeRunner()
    run_cli(project, "--judge", run=runner)
    assert runner.calls
    for argv in runner.calls:
        assert "--plugin-dir" not in argv
        prompt = argv[argv.index("-p") + 1]
        assert "alpha" not in prompt
        assert "styled" not in prompt.lower()


def test_cli_offline_without_raw_data_exits_2(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project)
    assert error.value.code == 2


def test_cli_offline_rescores_the_stored_rows(project):
    run_cli(project, "--judge")
    first = json.loads((project / "run" / "value.json").read_text())
    assert run_cli(project) == 0
    second = json.loads((project / "run" / "value.json").read_text())
    first.pop("date")
    second.pop("date")
    assert first == second


def test_cli_resume_makes_no_new_calls(project):
    run_cli(project, "--judge")
    second_runner = FakeJudgeRunner()
    assert run_cli(project, "--judge", run=second_runner) == 0
    assert second_runner.calls == []


def test_cli_meta_mismatch_exits_2(project):
    run_cli(project, "--judge")
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--questions", "7")
    assert error.value.code == 2
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--replicates", "5")
    assert error.value.code == 2


def test_cli_a_first_design_file_transitions_to_the_current_design(project):
    run_dir = project / "run"
    old_meta = {
        "type": "meta",
        "date": "2026-01-01T00:00:00+00:00",
        "claude_version": "1.0.0",
        "models": {"reader": "haiku", "grader": "opus"},
        "questions": 5,
        "paraphrases": 3,
        "language": "Italian",
        "flags": [],
        "answers_sha256": sha256_of(run_dir / "answers.jsonl"),
        "prompts_sha256": "abc",
    }
    write_jsonl(run_dir / "value-raw.jsonl", [old_meta])
    assert run_cli(project, "--judge") == 0
    metas = [
        row
        for line in (run_dir / "value-raw.jsonl").read_text().splitlines()
        if (row := json.loads(line)).get("type") == "meta"
    ]
    assert len(metas) == 2
    assert "comprehension_design" not in metas[0]
    assert metas[1]["comprehension_design"] == "balanced-facts-v3"
    assert metas[1]["questions"] == 6
    assert metas[1]["replicates"] == 3
    assert metas[1]["date"] == "2026-01-01T00:00:00+00:00"


def test_cli_a_v2_file_transitions_and_re_judges_comprehension_only(project):
    run_dir = project / "run"
    v2_rows = [
        {
            "type": "meta",
            "date": "2026-01-01T00:00:00+00:00",
            "claude_version": "1.0.0",
            "models": {"reader": "haiku", "grader": "opus"},
            "questions": 5,
            "paraphrases": 3,
            "replicates": 3,
            "comprehension_design": "shared-facts-v2",
            "language": "Italian",
            "flags": [],
            "answers_sha256": sha256_of(run_dir / "answers.jsonl"),
        },
        {
            "type": "call",
            "key": "comprehension:v2:questions:alpha:explanation-01",
            "check": "comprehension",
            "output": '["Q1", "Q2", "Q3"]',
        },
    ]
    for text in (STYLED_TEXT, UNSTYLED_TEXT):
        v2_rows += [
            {
                "type": "call",
                "key": f"paraphrase:reader:{sha(text)}:{index}",
                "check": "paraphrase",
                "output": "one same restatement",
            }
            for index in range(3)
        ]
        v2_rows += [
            {
                "type": "call",
                "key": f"roundtrip:translate:{sha(text)}",
                "check": "roundtrip",
                "output": "testo tradotto",
            },
            {
                "type": "call",
                "key": f"roundtrip:back:{sha(text)}",
                "check": "roundtrip",
                "output": "text translated back",
            },
        ]
    write_jsonl(run_dir / "value-raw.jsonl", v2_rows)
    runner = FakeJudgeRunner()
    assert run_cli(project, "--judge", run=runner) == 0
    prompts = [argv[argv.index("-p") + 1] for argv in runner.calls]
    assert not any(
        prompt.startswith(("Restate the text", "Translate the text")) for prompt in prompts
    )
    # One questions call, then a reader and a grades call per arm and
    # replicate: the transition re-judges only the comprehension rows.
    assert len(prompts) == 1 + 2 * 3 * 2
    metas = [
        row
        for line in (run_dir / "value-raw.jsonl").read_text().splitlines()
        if (row := json.loads(line)).get("type") == "meta"
    ]
    assert len(metas) == 2
    assert metas[0]["comprehension_design"] == "shared-facts-v2"
    assert metas[1]["comprehension_design"] == "balanced-facts-v3"
    assert metas[1]["questions"] == 6
    assert metas[1]["date"] == "2026-01-01T00:00:00+00:00"
    summary = json.loads((run_dir / "value.json").read_text())
    assert summary["judges"]["comprehension_design"] == "balanced-facts-v3"
    assert summary["checks"]["comprehension"]["design"] == "balanced-facts-v3"


def test_cli_an_unknown_stored_design_exits_2(project):
    run_dir = project / "run"
    meta = {
        "type": "meta",
        "date": "2026-01-01T00:00:00+00:00",
        "models": {"reader": "haiku", "grader": "opus"},
        "questions": 6,
        "paraphrases": 3,
        "replicates": 3,
        "comprehension_design": "balanced-facts-v9",
        "language": "Italian",
        "answers_sha256": sha256_of(run_dir / "answers.jsonl"),
    }
    write_jsonl(run_dir / "value-raw.jsonl", [meta])
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_without_loss_data_skips_comprehension(project):
    (project / "run" / "loss-raw.jsonl").unlink()
    assert run_cli(project, "--judge") == 1
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["checks"]["comprehension"]["judged"] is False
    assert summary["checks"]["paraphrase"]["judged"] is True
    assert any("run style-loss" in w for w in summary["warnings"])


def test_cli_stale_loss_data_skips_comprehension(project):
    loss_path = project / "run" / "loss-raw.jsonl"
    rows = [json.loads(line) for line in loss_path.read_text().splitlines()]
    rows[0]["answers_sha256"] = "stale"
    write_jsonl(loss_path, rows)
    assert run_cli(project, "--judge") == 1
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["checks"]["comprehension"]["judged"] is False
    assert any("comes from other answers" in w for w in summary["warnings"])


def test_cli_one_way_loss_data_skips_comprehension(project):
    loss_path = project / "run" / "loss-raw.jsonl"
    rows = [json.loads(line) for line in loss_path.read_text().splitlines()]
    del rows[0]["fact_mine"]
    write_jsonl(loss_path, rows)
    assert run_cli(project, "--judge") == 1
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["checks"]["comprehension"]["judged"] is False
    assert summary["checks"]["paraphrase"]["judged"] is True
    assert any("one-way fact mine" in w for w in summary["warnings"])


def test_cli_a_pair_below_the_facts_floor_is_skipped(project):
    loss_path = project / "run" / "loss-raw.jsonl"
    rows = [json.loads(line) for line in loss_path.read_text().splitlines()]
    for row in rows:
        if row.get("type") == "call":
            is_facts = row["key"].startswith("completeness:facts:")
            row["output"] = '["F1"]' if is_facts else "[true]"
    write_jsonl(loss_path, rows)
    assert run_cli(project, "--judge") == 1
    summary = json.loads((project / "run" / "value.json").read_text())
    assert any("fewer than the floor of 3" in w for w in summary["warnings"])
    assert summary["checks"]["comprehension"]["judged"] is False


def test_cli_judge_model_must_differ_from_the_writer(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--model-reader", "sonnet")
    assert error.value.code == 2


def test_cli_rejects_an_unknown_check(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--checks", "comprehension,vibes")
    assert error.value.code == 2


def test_cli_needs_gate_data(project):
    (project / "run" / "fidelity.jsonl").unlink()
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
    assert error.value.code == 2


def test_cli_shares_the_unstyled_arm_between_styles(tmp_path):
    project = make_project(tmp_path, styled_answers={"alpha": STYLED_TEXT, "beta": BETA_TEXT})
    runner = FakeJudgeRunner()
    assert run_cli(project, "--judge", run=runner) == 0
    turtle_calls = [argv for argv in runner.calls if "turtle" in argv[argv.index("-p") + 1]]
    # Three restatements and one translation judge the turtle once, not
    # per style. The comprehension readers read it per pair: two styles
    # times three replicates.
    assert len(turtle_calls) == 4 + 2 * 3
    summary = json.loads((project / "run" / "value.json").read_text())
    assert sorted(summary["pairs"]) == ["alpha", "beta"]


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
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["pairs"] == {"alpha": ["explanation-01"]}
    assert any("explanation-02: the pair failed the gate" in w for w in summary["warnings"])


def test_cli_a_checks_subset_marks_the_rest_unjudged(project):
    assert run_cli(project, "--judge", "--checks", "paraphrase") == 1
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["checks"]["paraphrase"]["judged"] is True
    assert summary["checks"]["comprehension"]["judged"] is False
    report = (project / "run" / "value.md").read_text()
    assert "The check is not judged." in report
    assert any("comprehension check has no judge data" in w for w in summary["warnings"])


def test_cli_unparseable_grades_warn_and_exit_1(project):
    class BadGrader(FakeJudgeRunner):
        def reply(self, prompt):
            if prompt.startswith("Grade the quiz answers"):
                return "no json at all"
            return super().reply(prompt)

    assert run_cli(project, "--judge", run=BadGrader()) == 1
    summary = json.loads((project / "run" / "value.json").read_text())
    assert any("no usable grades" in w for w in summary["warnings"])
    assert any("comprehension check has no usable score" in w for w in summary["warnings"])


def test_report_keeps_the_v2_rendering_for_a_stored_v2_run():
    pairs, answers, rows = v2_fixture(
        styled_reps=([True, True], [True, True], [True, False]),
        unstyled_reps=([True, False], [True, False], [True, False]),
    )
    result = score_v2(pairs, answers, rows)
    meta = {
        "date": "2026-01-01T00:00:00+00:00",
        "models": {"reader": "haiku", "grader": "opus"},
        "questions": 5,
        "paraphrases": 3,
        "replicates": 3,
        "comprehension_design": "shared-facts-v2",
        "language": "Italian",
    }
    summary = build_value_summary(
        run_name="run", meta=meta, pairs=pairs, checks=result.checks, warnings=[]
    )
    report = build_value_report(summary)
    assert "Comprehension asks up to 5 questions per pair, with 3 reader replicates" in report
    assert "| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried-fact rate |" in report
    assert "| Pair | Questions | Styled | Unstyled | Agreement | Result |" in report
    assert "Sources" not in report


def test_load_raw_takes_the_last_row_per_key(tmp_path):
    path = tmp_path / "value-raw.jsonl"
    write_jsonl(
        path,
        [
            {"type": "meta", "models": {}},
            {"type": "call", "key": "k", "output": "old"},
            {"type": "call", "key": "k", "output": "new"},
        ],
    )
    meta, rows = cli.load_raw(Path(path))
    assert meta["type"] == "meta"
    assert rows["k"]["output"] == "new"
