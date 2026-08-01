"""Run the blind judge calls of the reader-value checks.

Every judge call goes through the same CLI path as the runner, but a
judge never loads the plugin and always runs with the default output
style. A judge prompt carries one bare text: no style name, no arm
label, and never both answers of a pair. Thus a judge cannot know
which answer is styled. The caller keeps the arm bookkeeping in the
raw rows, outside every judge prompt.

Each completed call goes to the sink as one raw row, keyed by check,
role, and the sha256 of the text under test. A later run reuses every
key that the stored rows already hold, so an interrupted run resumes
without loss.
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

QUESTIONS_PROMPT = """\
You write a comprehension quiz. Below is a task that was given to a
writer. Write {n} short factual questions that any good answer to the
task must cover, each with a short reference answer. Ask about the
subject of the task, not about the wording of the task. Output only a
JSON array of objects with the keys "question" and "reference".

Task:
{task}"""

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


def build_meta(
    *,
    reader_model: str,
    grader_model: str,
    questions_n: int,
    paraphrases_k: int,
    language: str,
    answers_sha256: str,
    prompts_sha256: str | None,
) -> dict:
    return {
        "type": "meta",
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": claude_version(),
        "models": {"reader": reader_model, "grader": grader_model},
        "questions": questions_n,
        "paraphrases": paraphrases_k,
        "language": language,
        "flags": list(ISOLATION_FLAGS),
        "answers_sha256": answers_sha256,
        "prompts_sha256": prompts_sha256,
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
    texts: list[dict],
    prompts_by_id: dict[str, str],
    grader_model: str,
    reader_model: str,
    questions_n: int,
) -> None:
    questions_by_prompt: dict[str, list[dict]] = {}
    for prompt_id in sorted({text["prompt_id"] for text in texts}):
        questions = session.structured(
            validate=parse_questions,
            key=f"comprehension:questions:{prompt_id}",
            check="comprehension",
            role="questions",
            model=grader_model,
            prompt=QUESTIONS_PROMPT.format(n=questions_n, task=prompts_by_id[prompt_id]),
            prompt_id=prompt_id,
            answer_sha256=None,
        )
        if questions is None:
            session.warnings.append(
                f"{prompt_id}: the question writer returned no usable questions, "
                "so comprehension skips the prompt"
            )
            continue
        questions_by_prompt[prompt_id] = questions

    for text in texts:
        questions = questions_by_prompt.get(text["prompt_id"])
        if questions is None:
            continue
        answers = session.structured(
            validate=partial(parse_strings, n=len(questions)),
            key=f"comprehension:reader:{text['sha256']}",
            check="comprehension",
            role="reader",
            model=reader_model,
            prompt=READER_PROMPT.format(
                text=text["text"],
                questions=_numbered([question["question"] for question in questions]),
            ),
            prompt_id=text["prompt_id"],
            answer_sha256=text["sha256"],
        )
        if answers is None:
            session.warnings.append(
                f"{text['prompt_id']}: the reader returned no usable answers for the text "
                f"{text['sha256'][:12]}, so comprehension skips the text"
            )
            continue
        grades = session.structured(
            validate=partial(parse_bools, n=len(questions)),
            key=f"comprehension:grades:{text['sha256']}",
            check="comprehension",
            role="grades",
            model=grader_model,
            prompt=GRADES_PROMPT.format(items=_grade_items(questions, answers)),
            prompt_id=text["prompt_id"],
            answer_sha256=text["sha256"],
        )
        if grades is None:
            session.warnings.append(
                f"{text['prompt_id']}: the grader returned no usable grades for the text "
                f"{text['sha256'][:12]}, so comprehension skips the text"
            )


def run_judges(
    *,
    texts: list[dict],
    prompts_by_id: dict[str, str] | None,
    checks: list[str],
    reader_model: str,
    grader_model: str,
    questions_n: int,
    paraphrases_k: int,
    language: str,
    rows: dict[str, dict],
    sink: RowSink,
    workdir: Path,
    run: Runner = subprocess_runner,
) -> list[str]:
    """Run the judge calls for every text and return the warnings.

    Each text is one dict with prompt_id, sha256, and text. The rows
    mapping is read for reuse and extended in place; every new row
    also goes to the sink.
    """
    session = JudgeSession(rows=rows, sink=sink, workdir=workdir, run=run)

    if "comprehension" in checks:
        if prompts_by_id is None:
            raise ValueError("the comprehension check needs the prompt texts")
        _judge_comprehension(session, texts, prompts_by_id, grader_model, reader_model, questions_n)

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
