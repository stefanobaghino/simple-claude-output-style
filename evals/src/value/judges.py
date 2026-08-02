"""Run the blind judge calls of the reader-value checks.

Every judge call goes through the same CLI path as the runner, but a
judge never loads the plugin and always runs with the default output
style. A judge prompt carries one bare text: no style name, no arm
label, and never both answers of a pair. Thus a judge cannot know
which answer is styled. The comprehension questions come from the
shared facts of the pair, and only the fact strings travel between
the calls, never a second answer text. The caller keeps the arm
bookkeeping in the raw rows, outside every judge prompt.

Each completed call goes to the sink as one raw row. A later run
reuses every key that the stored rows already hold, so an interrupted
run resumes without loss.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import partial
from pathlib import Path

from runner.generate import (
    ISOLATION_FLAGS,
    GenerationError,
    Runner,
    parse_events,
    subprocess_runner,
)
from runner.provenance import claude_version

CHECKS = ("comprehension", "paraphrase", "roundtrip")

COMPREHENSION_DESIGN = "shared-facts-v2"
"""The design tag of the comprehension check, stored in the meta row.

A raw file without the tag holds first-design rows: questions written
from the task prompt alone, one reader call per text. The scorer
reads the tag to pick the matched scoring path.
"""

FACTS_FLOOR = 3
"""A pair with fewer shared facts is skipped: too few for a quiz."""

QUESTIONS_FROM_FACTS_PROMPT = """\
You write a quiz from an answer key. Below is a numbered list of
facts. For each fact, write one short question whose correct answer
is that fact. The question must not contain its answer. Output only
a JSON array of strings, one question per fact, in order.

Facts:
{facts}"""

READER_PROMPT = """\
Answer the questions below with only the text as your source. Do not
use outside knowledge. When the text does not contain the answer,
reply exactly "NOT IN TEXT" for that question. Output only a JSON
array of strings, one answer per question, in order.

Text:
{text}

Questions:
{questions}"""

GRADES_PROMPT = """\
Grade the quiz answers below. An answer is correct when it states the
substance of the reference answer; the wording is free. The answer
"NOT IN TEXT" is incorrect. Output only a JSON array of booleans, one
per item, in order.

{items}"""

PARAPHRASE_PROMPT = """\
Restate the text below in your own words. Keep every point and every
qualification. Output only the restatement.

Text:
{text}"""

TRANSLATE_PROMPT = """\
Translate the text below to {language}. Output only the translation.

Text:
{text}"""

BACK_PROMPT = """\
Translate the text below to English. Output only the translation.

Text:
{text}"""


def judge_argv(prompt: str, model: str) -> list[str]:
    """The claude invocation for one judge call: no plugin, default style."""
    settings = {"disableAllHooks": True, "outputStyle": "default"}
    argv = ["claude", "-p", prompt, "--model", model]
    argv += ["--settings", json.dumps(settings)]
    argv += list(ISOLATION_FLAGS)
    return argv


def extract_json(text: str) -> object | None:
    """The first JSON value in a judge output, or None.

    A judge is asked for bare JSON, but a model can wrap the JSON in a
    code fence or in prose. The parser tries the full text, then every
    fenced block, then the widest bracketed span.
    """
    candidates = [text.strip()]
    candidates += [
        match.group(1).strip() for match in re.finditer(r"```(?:json)?\n(.*?)```", text, re.DOTALL)
    ]
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        candidates.append(text[start : end + 1])
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def parse_questions(output: str) -> list[dict] | None:
    """The question list of a question-writer output, or None."""
    value = extract_json(output)
    if not isinstance(value, list) or not value:
        return None
    questions = []
    for item in value:
        if not isinstance(item, dict) or "question" not in item or "reference" not in item:
            return None
        questions.append({"question": str(item["question"]), "reference": str(item["reference"])})
    return questions


def parse_strings(output: str, n: int) -> list[str] | None:
    """A JSON array of exactly n strings, or None."""
    value = extract_json(output)
    if not isinstance(value, list) or len(value) != n:
        return None
    return [str(item) for item in value]


def parse_bools(output: str, n: int) -> list[bool] | None:
    """A JSON array of exactly n booleans, or None."""
    value = extract_json(output)
    if not isinstance(value, list) or len(value) != n:
        return None
    if not all(isinstance(item, bool) for item in value):
        return None
    return value


def select_facts(facts: list[str], cap: int) -> list[str]:
    """At most cap facts, spaced evenly over the list, in stored order."""
    if len(facts) <= cap:
        return list(facts)
    step = len(facts) / cap
    return [facts[int(index * step)] for index in range(cap)]


def build_meta(
    *,
    reader_model: str,
    grader_model: str,
    questions_n: int,
    paraphrases_k: int,
    replicates: int,
    language: str,
    answers_sha256: str,
) -> dict:
    return {
        "type": "meta",
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": claude_version(),
        "models": {"reader": reader_model, "grader": grader_model},
        "questions": questions_n,
        "paraphrases": paraphrases_k,
        "replicates": replicates,
        "comprehension_design": COMPREHENSION_DESIGN,
        "language": language,
        "flags": list(ISOLATION_FLAGS),
        "answers_sha256": answers_sha256,
    }


RowSink = Callable[[dict], None]


@dataclass
class JudgeSession:
    """Runs judge calls with reuse of the stored rows."""

    rows: dict[str, dict]
    sink: RowSink
    workdir: Path
    run: Runner
    warnings: list[str] = field(default_factory=list)

    def call(
        self,
        *,
        key: str,
        check: str,
        role: str,
        model: str,
        prompt: str,
        prompt_id: str,
        answer_sha256: str | None,
        index: int | None = None,
        force: bool = False,
    ) -> dict:
        if not force and key in self.rows:
            return self.rows[key]
        stdout = self.run(judge_argv(prompt, model), self.workdir)
        init, result = parse_events(stdout)
        active = init.get("output_style")
        if active != "default":
            raise GenerationError(
                f"{key}: expected the default output style, but {active!r} was active"
            )
        if result.get("is_error"):
            raise GenerationError(
                f"{key}: claude reported an error: {str(result.get('result', ''))[:500]}"
            )
        row = {
            "type": "call",
            "key": key,
            "check": check,
            "role": role,
            "prompt_id": prompt_id,
            "answer_sha256": answer_sha256,
            "index": index,
            "model_requested": model,
            "model_resolved": str(init.get("model", "")),
            "output": str(result.get("result", "")),
            "output_tokens": int((result.get("usage") or {}).get("output_tokens", 0)),
            "duration_ms": int(result.get("duration_ms", 0)),
        }
        self.rows[key] = row
        self.sink(row)
        return row

    def structured(self, *, validate: Callable[[str], object | None], **call_kwargs) -> object:
        """A call whose output must pass the validator; one retry on failure."""
        row = self.call(**call_kwargs)
        value = validate(row["output"])
        if value is None:
            row = self.call(force=True, **call_kwargs)
            value = validate(row["output"])
        return value


def _numbered(items: list[str]) -> str:
    return "\n".join(f"{number}. {item}" for number, item in enumerate(items, start=1))


def _grade_items(questions: list[dict], answers: list[str]) -> str:
    blocks = []
    for number, (question, answer) in enumerate(zip(questions, answers, strict=True), start=1):
        blocks.append(
            f"{number}. Question: {question['question']}\n"
            f"   Reference: {question['reference']}\n"
            f"   Answer: {answer}"
        )
    return "\n".join(blocks)


def _judge_comprehension(
    session: JudgeSession,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    facts_by_pair: dict[tuple[str, str], list[str]],
    grader_model: str,
    reader_model: str,
    questions_cap: int,
    replicates: int,
) -> None:
    """One quiz per pair, from the shared facts, read by both answers.

    A pair without an entry in facts_by_pair was warned about by the
    caller and is skipped here. The reference answer of a question is
    the fact that produced the question.
    """
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            survivors = facts_by_pair.get((style, prompt_id))
            if survivors is None:
                continue
            if len(survivors) < FACTS_FLOOR:
                session.warnings.append(
                    f"{style}/{prompt_id}: the pair has {len(survivors)} shared facts, "
                    f"fewer than the floor of {FACTS_FLOOR}, so comprehension skips the pair"
                )
                continue
            facts = select_facts(survivors, questions_cap)
            questions = session.structured(
                validate=partial(parse_strings, n=len(facts)),
                key=f"comprehension:v2:questions:{style}:{prompt_id}",
                check="comprehension",
                role="questions",
                model=grader_model,
                prompt=QUESTIONS_FROM_FACTS_PROMPT.format(facts=_numbered(facts)),
                prompt_id=prompt_id,
                answer_sha256=None,
            )
            if questions is None:
                session.warnings.append(
                    f"{style}/{prompt_id}: the question writer returned no usable "
                    "questions, so comprehension skips the pair"
                )
                continue
            references = [
                {"question": question, "reference": fact}
                for question, fact in zip(questions, facts, strict=True)
            ]
            for arm, arm_key in (("styled", (prompt_id, style)), ("unstyled", (prompt_id, None))):
                text = answers[arm_key]
                for replicate in range(replicates):
                    replies = session.structured(
                        validate=partial(parse_strings, n=len(facts)),
                        key=f"comprehension:v2:reader:{style}:{prompt_id}:{arm}:{replicate}",
                        check="comprehension",
                        role="reader",
                        model=reader_model,
                        prompt=READER_PROMPT.format(
                            text=text["text"], questions=_numbered(questions)
                        ),
                        prompt_id=prompt_id,
                        answer_sha256=text["sha256"],
                        index=replicate,
                    )
                    if replies is None:
                        session.warnings.append(
                            f"{prompt_id}: the reader returned no usable answers for the "
                            f"text {text['sha256'][:12]}, so comprehension skips the "
                            "replicate"
                        )
                        continue
                    grades = session.structured(
                        validate=partial(parse_bools, n=len(facts)),
                        key=f"comprehension:v2:grades:{style}:{prompt_id}:{arm}:{replicate}",
                        check="comprehension",
                        role="grades",
                        model=grader_model,
                        prompt=GRADES_PROMPT.format(items=_grade_items(references, replies)),
                        prompt_id=prompt_id,
                        answer_sha256=text["sha256"],
                        index=replicate,
                    )
                    if grades is None:
                        session.warnings.append(
                            f"{prompt_id}: the grader returned no usable grades for the "
                            f"text {text['sha256'][:12]}, so comprehension skips the "
                            "replicate"
                        )


def run_judges(
    *,
    texts: list[dict],
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    facts_by_pair: dict[tuple[str, str], list[str]],
    checks: list[str],
    reader_model: str,
    grader_model: str,
    questions_n: int,
    paraphrases_k: int,
    replicates: int,
    language: str,
    rows: dict[str, dict],
    sink: RowSink,
    workdir: Path,
    run: Runner = subprocess_runner,
) -> list[str]:
    """Run the judge calls for every pair and return the warnings.

    The texts list holds the unique texts for the per-text checks:
    one dict with prompt_id, sha256, and text per unique sha256. The
    comprehension check works per pair instead, with the shared facts
    from facts_by_pair. The rows mapping is read for reuse and
    extended in place; every new row also goes to the sink.
    """
    session = JudgeSession(rows=rows, sink=sink, workdir=workdir, run=run)

    if "comprehension" in checks:
        _judge_comprehension(
            session,
            pairs,
            answers,
            facts_by_pair,
            grader_model,
            reader_model,
            questions_n,
            replicates,
        )

    if "paraphrase" in checks:
        for text in texts:
            for index in range(paraphrases_k):
                session.call(
                    key=f"paraphrase:reader:{text['sha256']}:{index}",
                    check="paraphrase",
                    role="paraphrase",
                    model=reader_model,
                    prompt=PARAPHRASE_PROMPT.format(text=text["text"]),
                    prompt_id=text["prompt_id"],
                    answer_sha256=text["sha256"],
                    index=index,
                )

    if "roundtrip" in checks:
        for text in texts:
            translated = session.call(
                key=f"roundtrip:translate:{text['sha256']}",
                check="roundtrip",
                role="translate",
                model=reader_model,
                prompt=TRANSLATE_PROMPT.format(language=language, text=text["text"]),
                prompt_id=text["prompt_id"],
                answer_sha256=text["sha256"],
            )
            session.call(
                key=f"roundtrip:back:{text['sha256']}",
                check="roundtrip",
                role="back",
                model=reader_model,
                prompt=BACK_PROMPT.format(text=translated["output"]),
                prompt_id=text["prompt_id"],
                answer_sha256=text["sha256"],
            )

    return session.warnings
