"""Tests for the reader-value checks. No test touches the network:
the claude subprocess is replaced with fake runners that return
canned stream-json output."""

import hashlib
import json
import re
import threading
from collections import Counter
from functools import partial
from pathlib import Path

import pytest

from runner.generate import GenerationError
from runner.provenance import sha256_of
from value import cli, extract_json, judge_argv, score_checks, select_pairs
from value.analysis import shared_facts
from value.judges import (
    JUDGE_PROMPTS_SHA256,
    JudgePinError,
    JudgeSession,
    TaskPool,
    judge_prompts_sha256,
    parse_bools,
    run_judges,
    select_balanced,
    select_facts,
)
from value.report import build_value_report, build_value_summary
from value.similarity import mean_pairwise_f1, unigram_f1

STYLED_TEXT = "The quick brown fox jumps."
UNSTYLED_TEXT = "The slow green turtle crawls."
BETA_TEXT = "The big red bear sleeps."

# Hardcoded on purpose, apart from JUDGE_MODEL_PINS: a silent pin
# change must break these tests.
RESOLVED = {"haiku": "claude-haiku-4-5-20251001", "opus": "claude-opus-5"}


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stream(result_text, output_style="default", model="claude-haiku-4-5-20251001", plugins=()):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": model,
        "plugins": [{"name": name} for name in plugins],
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
        # Parallel judge calls share the runner, so the lock covers
        # the calls list and the counters of the reply methods.
        self.lock = threading.Lock()

    def __call__(self, argv, cwd, env=None):
        with self.lock:
            self.calls.append(argv)
            prompt = argv[argv.index("-p") + 1]
            model = argv[argv.index("--model") + 1]
            return stream(self.reply(prompt), model=RESOLVED[model])

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


def test_judge_prompts_sha256_changes_with_any_template():
    prompts = {"reader": "Answer the questions.", "grades": "Grade the answers."}
    assert judge_prompts_sha256(prompts) == judge_prompts_sha256(dict(prompts))
    edited = {**prompts, "reader": "Answer the questions!"}
    assert judge_prompts_sha256(edited) != judge_prompts_sha256(prompts)
    renamed = {"read": prompts["reader"], "grades": prompts["grades"]}
    assert judge_prompts_sha256(renamed) != judge_prompts_sha256(prompts)


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


def length_fixture(arms):
    """A multi-pair scoring input: one (prompt_id, styled, unstyled) per arm."""
    pairs = {"alpha": []}
    answers = {}
    for index, (prompt_id, styled_text, unstyled_text) in enumerate(arms):
        pairs["alpha"].append(prompt_id)
        answers[(prompt_id, "alpha")] = {"text": styled_text, "sha256": f"S{index}"}
        answers[(prompt_id, None)] = {"text": unstyled_text, "sha256": f"U{index}"}
    return pairs, answers


def test_length_correlation_tracks_the_length_ratio():
    # Ratios 0.25, 0.5, 0.75; the styled loss is 0 everywhere, and the
    # unstyled loss is 0.75, 0.5, 0.25. The advantage is thus exactly
    # 1 - ratio, so both statistics are exactly -1.
    pairs, answers = length_fixture(
        [
            ("p-01", "one", "one two three four"),
            ("p-02", "one two", "one two three four"),
            ("p-03", "one two three", "one two three four"),
        ]
    )
    backs = {
        "S0": "one",
        "S1": "one two",
        "S2": "one two three",
        "U0": "one aa bb cc",
        "U1": "one two bb cc",
        "U2": "one two three cc",
    }
    rows = {
        f"roundtrip:back:{sha}": {"check": "roundtrip", "output": output}
        for sha, output in backs.items()
    }
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    stats = result.checks["roundtrip"]["per_style"]["alpha"]
    assert (stats["wins"], stats["losses"], stats["ties"]) == (3, 0, 0)
    assert stats["length_correlation"] == {"n": 3, "pearson": -1.0, "spearman": -1.0}


def test_length_correlation_uses_the_styled_advantage_sign():
    # Paraphrase scores win high, so the advantage is styled minus
    # unstyled: (ratio 0.5, advantage 1/3) and (ratio 1.0, advantage
    # -1/3) give -1. An inverted sign gives +1 and fails.
    pairs, answers = length_fixture([("p-01", "one", "one two"), ("p-02", "one two", "one two")])
    rows = {}
    rows.update(paraphrase_rows("S0", ["same words here", "same words here"]))
    rows.update(paraphrase_rows("U0", ["same words here", "same words also"]))
    rows.update(paraphrase_rows("S1", ["same words here", "same words also"]))
    rows.update(paraphrase_rows("U1", ["same words here", "same words here"]))
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    stats = result.checks["paraphrase"]["per_style"]["alpha"]
    assert stats["length_correlation"] == {"n": 2, "pearson": -1.0, "spearman": -1.0}


def test_length_correlation_is_none_on_a_constant_ratio():
    # Both ratios are 0.5, so statistics.correlation raises and each
    # statistic becomes None. The third pair has no unstyled words, so
    # the sample count stays 2.
    pairs, answers = length_fixture(
        [
            ("p-01", "one two", "one two three four"),
            ("p-02", "three four", "one two three four"),
            ("p-03", "one", "?!"),
        ]
    )
    backs = {"S0": "one two", "S1": "three four", "S2": "one", "U0": "aa", "U1": "bb", "U2": "?!"}
    rows = {
        f"roundtrip:back:{sha}": {"check": "roundtrip", "output": output}
        for sha, output in backs.items()
    }
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    stats = result.checks["roundtrip"]["per_style"]["alpha"]
    assert stats["length_correlation"] == {"n": 2, "pearson": None, "spearman": None}


def test_length_correlation_is_none_for_a_single_pair():
    pairs, answers, rows = pair_fixture({})
    rows["roundtrip:back:S"] = {"check": "roundtrip", "output": "styled text"}
    rows["roundtrip:back:U"] = {"check": "roundtrip", "output": "unstyled text"}
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    stats = result.checks["roundtrip"]["per_style"]["alpha"]
    assert stats["length_correlation"] == {"n": 1, "pearson": None, "spearman": None}


def test_an_unjudged_check_warns():
    pairs, answers, rows = pair_fixture({})
    result = score_checks(pairs=pairs, answers=answers, rows=rows, paraphrases_k=3)
    assert result.checks["paraphrase"] == {"judged": False, "per_style": None}
    assert any("the paraphrase check has no judge data" in w for w in result.warnings)


def test_structured_calls_retry_once(tmp_path):
    outputs = iter(["garbage", "[true, false]"])

    def run(argv, cwd, env=None):
        return stream(next(outputs), model="claude-opus-5")

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


def test_a_call_retries_a_transient_failure_once(tmp_path):
    attempts = []

    def run(argv, cwd, env=None):
        attempts.append(argv)
        if len(attempts) == 1:
            raise GenerationError("claude exited with code 1: transient")
        return stream("[true, false]", model="claude-opus-5")

    session = JudgeSession(rows={}, sink=lambda row: None, workdir=tmp_path, run=run)
    row = session.call(
        key="comprehension:grades:S",
        check="comprehension",
        role="grades",
        model="opus",
        prompt="Grade the quiz answers below.",
        prompt_id="p-01",
        answer_sha256="S",
    )
    assert len(attempts) == 2
    assert row["output"] == "[true, false]"
    assert session.rows["comprehension:grades:S"] is row
    assert session.warnings == [
        (
            "comprehension:grades:S: the first call failed and the retry "
            "succeeded: claude exited with code 1: transient"
        )
    ]


def test_a_second_call_failure_propagates(tmp_path):
    attempts = []

    def run(argv, cwd, env=None):
        attempts.append(argv)
        raise GenerationError("claude exited with code 1: persistent")

    session = JudgeSession(rows={}, sink=lambda row: None, workdir=tmp_path, run=run)
    with pytest.raises(GenerationError):
        session.call(
            key="comprehension:grades:S",
            check="comprehension",
            role="grades",
            model="opus",
            prompt="Grade the quiz answers below.",
            prompt_id="p-01",
            answer_sha256="S",
        )
    assert len(attempts) == 2
    assert session.rows == {}


def test_a_pin_mismatch_raises_without_a_retry(tmp_path):
    attempts = []

    def run(argv, cwd, env=None):
        attempts.append(argv)
        return stream("[true]", model="claude-opus-4-1")

    session = JudgeSession(rows={}, sink=lambda row: None, workdir=tmp_path, run=run)
    with pytest.raises(JudgePinError):
        session.call(
            key="comprehension:grades:S",
            check="comprehension",
            role="grades",
            model="opus",
            prompt="Grade the quiz answers below.",
            prompt_id="p-01",
            answer_sha256="S",
        )
    assert len(attempts) == 1
    assert session.rows == {}


def test_an_exact_id_passes_and_an_unpinned_alias_fails(tmp_path):
    def run(argv, cwd, env=None):
        model = argv[argv.index("--model") + 1]
        resolved = "claude-sonnet-5" if model == "sonnet" else model
        return stream("[true]", model=resolved)

    session = JudgeSession(rows={}, sink=lambda row: None, workdir=tmp_path, run=run)
    row = session.call(
        key="comprehension:grades:S",
        check="comprehension",
        role="grades",
        model="claude-opus-5",
        prompt="Grade the quiz answers below.",
        prompt_id="p-01",
        answer_sha256="S",
    )
    assert row["model_resolved"] == "claude-opus-5"
    with pytest.raises(JudgePinError):
        session.call(
            key="comprehension:grades:U",
            check="comprehension",
            role="grades",
            model="sonnet",
            prompt="Grade the quiz answers below.",
            prompt_id="p-01",
            answer_sha256="U",
        )


def test_the_pool_runs_every_task():
    lock = threading.Lock()
    done = []

    def record(number):
        with lock:
            done.append(number)

    pool = TaskPool(3)
    for number in range(10):
        pool.submit(partial(record, number))
    pool.drain()
    assert sorted(done) == list(range(10))


def test_the_serial_pool_keeps_the_order_and_stops_at_the_first_error():
    done = []

    def record(number):
        done.append(number)

    def boom():
        raise ValueError("boom")

    pool = TaskPool(1)
    for task in (partial(record, 0), partial(record, 1), boom, partial(record, 2)):
        pool.submit(task)
    with pytest.raises(ValueError):
        pool.drain()
    assert done == [0, 1]


def test_the_pool_propagates_a_base_exception_and_joins_the_live_tasks():
    lock = threading.Lock()
    state = {"entered": 0, "exited": 0}

    class Cancel(BaseException):
        pass

    def task():
        with lock:
            state["entered"] += 1
        with lock:
            state["exited"] += 1

    def boom():
        raise Cancel("stop")

    pool = TaskPool(3)
    pool.submit(boom)
    for _ in range(30):
        pool.submit(task)
    with pytest.raises(Cancel):
        pool.drain()
    assert state["entered"] == state["exited"]


def test_a_serial_task_can_submit_a_task_and_the_order_is_breadth_first():
    done = []
    pool = TaskPool(1)

    def child():
        done.append("child")

    def parent():
        done.append("parent")
        pool.submit(child)

    pool.submit(parent)
    pool.submit(partial(done.append, "sibling"))
    pool.drain()
    assert done == ["parent", "sibling", "child"]


def test_the_drain_waits_for_a_task_submitted_during_the_drain():
    # A snapshot of the futures at the start of the drain would never
    # call result() on the child, and the error of the child would be
    # lost. The growing list must surface the error.
    pool = TaskPool(2)

    def child():
        raise ValueError("late boom")

    def parent():
        pool.submit(child)

    pool.submit(parent)
    with pytest.raises(ValueError):
        pool.drain()


def test_a_live_parent_can_submit_during_an_abort_without_an_error():
    # The boom task releases the parent and then raises. The parent
    # then submits while the pool fails or aborts. A raise from that
    # submit would surface as the error of the parent instead of the
    # ValueError of the boom task.
    release = threading.Event()
    pool = TaskPool(2)

    def parent():
        release.wait(timeout=10)
        pool.submit(lambda: None)

    def boom():
        release.set()
        raise ValueError("boom")

    pool.submit(parent)
    pool.submit(boom)
    with pytest.raises(ValueError):
        pool.drain()


def test_a_drained_pool_rejects_a_submit_and_a_second_drain():
    pool = TaskPool(1)
    pool.drain()
    with pytest.raises(RuntimeError):
        pool.submit(lambda: None)
    with pytest.raises(RuntimeError):
        pool.drain()


def test_the_comprehension_grain_is_smaller_than_a_pair(tmp_path):
    # At one worker the order is breadth-first, so the questions call
    # of the second pair must land before the grade call of the first
    # pair. The old per-pair task ran all thirteen calls of a pair
    # before the next pair started.
    def run(argv, cwd, env=None):
        prompt = argv[2]
        model = RESOLVED[argv[argv.index("--model") + 1]]
        if prompt.startswith("You write a quiz"):
            return stream('["q1", "q2", "q3"]', model=model)
        if prompt.startswith("Answer the questions"):
            return stream('["a1", "a2", "a3"]', model=model)
        return stream("[true, true, true]", model=model)

    facts = {"unstyled": ["f1", "f2", "f3"], "styled": []}
    keys = []
    warnings = run_judges(
        texts=[],
        pairs={"alpha": ["p-01", "p-02"]},
        answers={
            ("p-01", "alpha"): {"text": STYLED_TEXT, "sha256": sha(STYLED_TEXT)},
            ("p-01", None): {"text": UNSTYLED_TEXT, "sha256": sha(UNSTYLED_TEXT)},
            ("p-02", "alpha"): {"text": STYLED_TEXT, "sha256": sha(STYLED_TEXT)},
            ("p-02", None): {"text": UNSTYLED_TEXT, "sha256": sha(UNSTYLED_TEXT)},
        },
        facts_by_pair={("alpha", "p-01"): facts, ("alpha", "p-02"): facts},
        checks=["comprehension"],
        reader_model="haiku",
        grader_model="opus",
        questions_n=6,
        paraphrases_k=0,
        replicates=1,
        language="Italian",
        rows={},
        sink=lambda row: keys.append(row["key"]),
        workdir=tmp_path,
        run=run,
        parallel=1,
    )
    assert warnings == []
    assert len(keys) == 10
    assert keys.index("comprehension:v3:questions:alpha:p-02") < keys.index(
        "comprehension:v3:grades:alpha:p-01:styled:0"
    )


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
    assert summary["judges"]["models_resolved"] == {
        "reader": "claude-haiku-4-5-20251001",
        "grader": "claude-opus-5",
    }
    for check in ("comprehension", "paraphrase", "roundtrip"):
        stats = summary["checks"][check]["per_style"]["alpha"]
        assert (stats["wins"], stats["losses"], stats["ties"]) == (1, 0, 0)
    for check in ("paraphrase", "roundtrip"):
        assert summary["checks"][check]["per_style"]["alpha"]["length_correlation"] == {
            "n": 1,
            "pearson": None,
            "spearman": None,
        }
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
    raw_rows = [
        json.loads(line) for line in (project / "run" / "value-raw.jsonl").read_text().splitlines()
    ]
    call_rows = [row for row in raw_rows if row.get("type") == "call"]
    assert call_rows
    assert all(isinstance(row["wall_ms"], int) for row in call_rows)
    assert all(row["input_tokens"] == 3 for row in call_rows)
    assert all(row["cache_creation_input_tokens"] == 2 for row in call_rows)
    assert all(row["cache_read_input_tokens"] == 1 for row in call_rows)
    report = (project / "run" / "value.md").read_text()
    assert "## Call timing" in report
    assert "## Harness spend" in report
    assert report.count("| alpha | 1 | 0 | 0 |\n") == 2
    assert "worded by both answers in balance" in report
    assert "| alpha | 1 | 0 | 0 | 0.167 | 1.0 | 0.0 | 0.167 |" in report
    assert "- alpha: the styled answer holds (1 wins, 0 losses, 0 ties)." in report
    assert "| explanation-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |" in report
    assert report.count("The length confound is the correlation") == 2
    assert (
        report.count("- alpha: Pearson not computable, Spearman not computable, over 1 pair.") == 2
    )
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


def test_cli_offline_rescore_without_wall_states_not_measured(project):
    run_cli(project, "--judge")
    raw_path = project / "run" / "value-raw.jsonl"
    rows = [json.loads(line) for line in raw_path.read_text().splitlines()]
    for row in rows:
        row.pop("wall_ms", None)
    write_jsonl(raw_path, rows)
    assert run_cli(project) == 0
    assert "The wall is not measured" in (project / "run" / "value.md").read_text()


def test_cli_offline_rescore_without_tokens_states_not_measured(project):
    run_cli(project, "--judge")
    raw_path = project / "run" / "value-raw.jsonl"
    rows = [json.loads(line) for line in raw_path.read_text().splitlines()]
    for row in rows:
        row.pop("input_tokens", None)
        row.pop("cache_creation_input_tokens", None)
        row.pop("cache_read_input_tokens", None)
    write_jsonl(raw_path, rows)
    assert run_cli(project) == 0
    assert "The spend is not measured" in (project / "run" / "value.md").read_text()


def test_cli_resume_makes_no_new_calls(project):
    run_cli(project, "--judge")
    second_runner = FakeJudgeRunner()
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
        summary = json.loads((root / "run" / "value.json").read_text())
        summary.pop("date")
        summary["judges"].pop("judged_date")
        summaries.append(summary)
    assert summaries[0] == summaries[1]
    rows = [
        json.loads(line)
        for line in (roots["wide"] / "run" / "value-raw.jsonl").read_text().splitlines()
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

    class WorkdirProbe(FakeJudgeRunner):
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
        run_cli(project, "--judge", "--questions", "7")
    assert error.value.code == 2
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--replicates", "5")
    assert error.value.code == 2


def test_cli_meta_holds_the_judge_prompt_hash(project):
    assert run_cli(project, "--judge") == 0
    meta = json.loads((project / "run" / "value-raw.jsonl").read_text().splitlines()[0])
    assert meta["judge_prompts_sha256"] == JUDGE_PROMPTS_SHA256
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["judges"]["judge_prompts_sha256"] == JUDGE_PROMPTS_SHA256


def test_cli_a_stored_file_without_the_prompt_hash_upgrades_and_resumes(project):
    run_cli(project, "--judge")
    raw_path = project / "run" / "value-raw.jsonl"
    rows = [json.loads(line) for line in raw_path.read_text().splitlines()]
    del rows[0]["judge_prompts_sha256"]
    write_jsonl(raw_path, rows)
    second_runner = FakeJudgeRunner()
    assert run_cli(project, "--judge", run=second_runner) == 0
    assert second_runner.calls == []
    metas = [
        row
        for line in raw_path.read_text().splitlines()
        if (row := json.loads(line)).get("type") == "meta"
    ]
    assert len(metas) == 2
    assert "judge_prompts_sha256" not in metas[0]
    assert metas[1]["judge_prompts_sha256"] == JUDGE_PROMPTS_SHA256
    assert metas[1]["date"] == metas[0]["date"]


def test_cli_a_prompt_hash_mismatch_exits_2(project):
    run_cli(project, "--judge")
    raw_path = project / "run" / "value-raw.jsonl"
    rows = [json.loads(line) for line in raw_path.read_text().splitlines()]
    rows[0]["judge_prompts_sha256"] = "stale"
    write_jsonl(raw_path, rows)
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge")
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
    # The transition row backfills the judge-prompt hash, and the
    # historical task-prompt-set key never blocks a resume.
    assert metas[1]["judge_prompts_sha256"] == JUDGE_PROMPTS_SHA256
    assert metas[1]["prompts_sha256"] == "abc"


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


def test_judge_call_with_a_plugin_fails_without_retry(project):
    class LeakedPlugin(FakeJudgeRunner):
        def __call__(self, argv, cwd, env=None):
            with self.lock:
                self.calls.append(argv)
                prompt = argv[argv.index("-p") + 1]
                return stream(self.reply(prompt), plugins=("user-plugin",))

    runner = LeakedPlugin()
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--parallel", "1", run=runner)
    assert error.value.code == 2
    assert len(runner.calls) == 1


def test_cli_a_pin_mismatch_exits_2_without_a_retry(project):
    class WrongModel(FakeJudgeRunner):
        def __call__(self, argv, cwd, env=None):
            with self.lock:
                self.calls.append(argv)
                prompt = argv[argv.index("-p") + 1]
                return stream(self.reply(prompt), model="claude-haiku-4-0")

    runner = WrongModel()
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--judge", "--parallel", "1", run=runner)
    assert error.value.code == 2
    assert len(runner.calls) == 1


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
