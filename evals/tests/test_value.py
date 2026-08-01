"""Tests for the reader-value checks. No test touches the network:
the claude subprocess is replaced with fake runners that return
canned stream-json output."""

import hashlib
import json
from functools import partial
from pathlib import Path

import pytest

from runner.provenance import sha256_of
from value import cli, extract_json, judge_argv, score_checks, select_pairs
from value.judges import JudgeSession, parse_bools
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

    The unstyled turtle text plays the weaker arm: its reader misses a
    question, its restatements differ, and its round-trip loses words.
    Every other text is judged faithful, so its styled pair wins.
    """

    def __init__(self):
        self.calls = []
        self.turtle_restatements = 0

    def __call__(self, argv, cwd):
        self.calls.append(argv)
        prompt = argv[argv.index("-p") + 1]
        return stream(self.reply(prompt))

    def reply(self, prompt):
        if prompt.startswith("You write a comprehension quiz"):
            return json.dumps(
                [
                    {"question": "Q1", "reference": "R1"},
                    {"question": "Q2", "reference": "R2"},
                ]
            )
        if prompt.startswith("Answer the questions"):
            return '["A1", "NOT IN TEXT"]' if "turtle" in prompt else '["A1", "A2"]'
        if prompt.startswith("Grade the quiz answers"):
            return "[true, false]" if "Answer: NOT IN TEXT" in prompt else "[true, true]"
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
    argv = [str(project / "run"), "--prompts", str(project / "prompts.yaml"), *extra]
    return cli.main(argv, run=run or FakeJudgeRunner())


def test_cli_judge_writes_the_artifacts(project, capsys):
    assert run_cli(project, "--judge") == 0
    summary = json.loads((project / "run" / "value.json").read_text())
    assert summary["pairs"] == {"alpha": ["explanation-01"]}
    for check in ("comprehension", "paraphrase", "roundtrip"):
        stats = summary["checks"][check]["per_style"]["alpha"]
        assert (stats["wins"], stats["losses"], stats["ties"]) == (1, 0, 0)
    assert summary["checks"]["comprehension"]["per_style"]["alpha"]["pairs"]["explanation-01"] == {
        "styled": 1.0,
        "unstyled": 0.5,
        "result": "win",
    }
    assert summary["warnings"] == []
    report = (project / "run" / "value.md").read_text()
    assert report.count("| alpha | 1 | 0 | 0 |") == 3
    assert "- alpha: the styled answer holds (1 wins, 0 losses, 0 ties)." in report
    assert "| explanation-01 | 1.0 | 0.5 | win |" in report
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
    # One reader, three restatements, one translation: judged once, not per style.
    assert len(turtle_calls) == 5
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
