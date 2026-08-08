"""Run the blind judge calls of the reader-value checks.

Every judge call goes through the same CLI path as the runner, but a
judge never loads the plugin and always runs with the default output
style. A judge prompt carries one bare text: no style name, no arm
label, and never both answers of a pair. Thus a judge cannot know
which answer is styled. The comprehension questions come from the
shared facts of the pair, in the wordings of both answers, and only
the fact strings travel between the calls, never a second answer
text. The caller keeps the arm bookkeeping in the raw rows, outside
every judge prompt.

Each completed call goes to the sink as one raw row. A later run
reuses every key that the stored rows already hold, so an interrupted
run resumes without loss. With parallel judge calls, the session lock
serializes the row writes, and the rows land in completion order, not
in call order. The loaders read the rows by key, so the row order in
the raw file carries no meaning.

One task pool spans the checks of a pass. A call that depends on an
earlier call stays behind that call in one task, and every other call
goes to the pool as its own task, so a call runs as soon as its
inputs exist.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import partial
from pathlib import Path

from runner.generate import (
    ISOLATION_FLAGS,
    GenerationError,
    PluginLeakError,
    Runner,
    assert_declared_plugins,
    parse_events,
    subprocess_runner,
)
from runner.hermetic import CONFIG_MODE, manifest_sha256

CHECKS = ("comprehension", "paraphrase", "roundtrip")

JUDGE_MODEL_PINS = {
    "opus": "claude-opus-5",
    "haiku": "claude-haiku-4-5-20251001",
}
"""The exact model ID that each judge alias must resolve to.

Every live judge call checks the resolved ID of its init event
against this table. An alias outside the table must resolve to
itself, so an exact ID passes and an unpinned alias fails loudly.
A pin change opens a new comparability era for the judged passes,
like WORKDIR_MODE does for the generation calls.
"""


class JudgePinError(GenerationError):
    """The resolved judge model differs from the pinned model.

    The mismatch is deterministic, so the caller must not retry the
    call. The subclass keeps the GenerationError handler of every
    CLI intact, and the CLI exits with code 2.
    """


COMPREHENSION_DESIGNS = (None, "shared-facts-v2", "balanced-facts-v3")
"""Every comprehension design, oldest first.

The first design wrote questions from the task prompt alone, one
reader call per text. The shared-facts design writes the questions
from the facts that both answers hold, worded by the unstyled answer.
The balanced design takes the fact wording from both answers, half of
the cap per side. The scorer reads the stored tag to pick the matched
scoring path, so every stored run stays rescoreable.
"""

COMPREHENSION_DESIGN = COMPREHENSION_DESIGNS[-1]
"""The design tag of the current comprehension check, stored in the meta row."""

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


def judge_prompts_sha256(prompts: dict[str, str]) -> str:
    """One hash over the judge prompt templates of a tool.

    Canonical JSON over the name-to-template mapping, like
    manifest_sha256 in runner.hermetic, so a change to any template or
    template name changes the hash and opens a visible era. Only the
    meta row, the resume check, and the cross-run comparison read the
    hash; the scorer never does, so every stored run stays rescoreable.
    """
    payload = json.dumps(prompts, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


JUDGE_PROMPTS_SHA256 = judge_prompts_sha256(
    {
        "questions_from_facts": QUESTIONS_FROM_FACTS_PROMPT,
        "reader": READER_PROMPT,
        "grades": GRADES_PROMPT,
        "paraphrase": PARAPHRASE_PROMPT,
        "translate": TRANSLATE_PROMPT,
        "back": BACK_PROMPT,
    }
)
"""The hash of the reader-value judge prompts, stored in the meta row."""


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


def select_balanced(
    unstyled_facts: list[str], styled_facts: list[str], cap: int
) -> tuple[list[str], dict[str, int]]:
    """At most cap facts, half of the cap per wording source.

    The unstyled facts come first. A short side yields its remainder
    to the other side, and an odd cap gives the unstyled side the
    extra slot. Returns the facts and the count taken per source.
    """
    half = cap // 2
    take_unstyled = min(len(unstyled_facts), cap - min(len(styled_facts), half))
    take_styled = min(len(styled_facts), cap - take_unstyled)
    facts = select_facts(unstyled_facts, take_unstyled) + select_facts(styled_facts, take_styled)
    return facts, {"unstyled": take_unstyled, "styled": take_styled}


def build_meta(
    *,
    reader_model: str,
    grader_model: str,
    questions_n: int,
    paraphrases_k: int,
    replicates: int,
    language: str,
    answers_sha256: str,
    cli_version: str | None = None,
) -> dict:
    return {
        "type": "meta",
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": cli_version,
        "config": CONFIG_MODE,
        "config_manifest_sha256": manifest_sha256(),
        "models": {"reader": reader_model, "grader": grader_model},
        "questions": questions_n,
        "paraphrases": paraphrases_k,
        "replicates": replicates,
        "comprehension_design": COMPREHENSION_DESIGN,
        "language": language,
        "judge_prompts_sha256": JUDGE_PROMPTS_SHA256,
        "flags": list(ISOLATION_FLAGS),
        "answers_sha256": answers_sha256,
    }


class TaskPool:
    """Runs tasks, at most workers at a time; a task can submit more tasks.

    With workers at 1 or below, the tasks run in order in the thread
    of the caller, like a plain loop over a queue that can grow, and
    the first error stops the loop. Else the tasks run on a thread
    pool. An error cancels every task that did not start, a later
    submit becomes a no-op, and drain waits for the live tasks, then
    re-raises the error. Thus no task is live after drain, and the
    caller can close a shared file directly after drain. A submit or
    a drain after drain raises, because a late task would write past
    a closed sink.

    A task must submit and return, never wait on a submitted task:
    a wait would starve the workers. Thus submit returns None, not
    a handle.
    """

    def __init__(self, workers: int) -> None:
        self._lock = threading.Lock()
        self._failed = False
        self._closed = False
        self._queue: list[Callable[[], None]] = []
        self._futures: list = []
        self._pool = ThreadPoolExecutor(max_workers=workers) if workers > 1 else None

    def submit(self, task: Callable[[], None]) -> None:
        with self._lock:
            if self._closed:
                raise RuntimeError("the pool is drained")
            if self._failed:
                return
            if self._pool is None:
                self._queue.append(task)
            else:
                self._futures.append(self._pool.submit(task))

    def drain(self) -> None:
        with self._lock:
            if self._closed:
                raise RuntimeError("the pool is drained")
        if self._pool is None:
            self._drain_serial()
        else:
            self._drain_parallel()

    def _drain_serial(self) -> None:
        index = 0
        try:
            while index < len(self._queue):
                task = self._queue[index]
                index += 1
                task()
        except BaseException:
            with self._lock:
                self._failed = True
            raise
        finally:
            with self._lock:
                self._closed = True

    def _drain_parallel(self) -> None:
        # A child future lands in the list before the future of its
        # parent resolves, so when the length check under the lock
        # finds no new future, no task runs and the length is final.
        index = 0
        try:
            while True:
                with self._lock:
                    if index == len(self._futures):
                        break
                    future = self._futures[index]
                index += 1
                future.result()
        except BaseException:
            # A KeyboardInterrupt must also cancel the queue, so the
            # catch takes BaseException, not Exception. The failed
            # flag goes first, under the lock, so no parent submits
            # into the shutdown.
            with self._lock:
                self._failed = True
            self._pool.shutdown(wait=True, cancel_futures=True)
            raise
        finally:
            self._pool.shutdown(wait=True)
            with self._lock:
                self._closed = True


RowSink = Callable[[dict], None]


@dataclass
class JudgeSession:
    """Runs judge calls with reuse of the stored rows.

    Parallel tasks share one session. The lock serializes the row
    fast path and the row writes, so the sink never interleaves two
    rows. The subprocess runs outside the lock. A call that raises
    a GenerationError runs once more before the error propagates,
    because one transient failure must not abort a whole pass; the
    retry becomes a warning. A pin mismatch is deterministic and
    never retries. A key in force_keys skips the row fast path once:
    the freshness sample of a reuse pass re-runs that stored key
    live, and the fresh row lands under the same key.
    """

    rows: dict[str, dict]
    sink: RowSink
    workdir: Path
    run: Runner
    env: dict[str, str] | None = None
    warnings: list[str] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)
    force_keys: set[str] = field(default_factory=set)

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
        extra: dict | None = None,
        force: bool = False,
    ) -> dict:
        if not force:
            with self.lock:
                if key in self.force_keys:
                    self.force_keys.discard(key)
                elif key in self.rows:
                    return self.rows[key]
        try:
            init, result, wall_ms = self._attempt(key, model, prompt)
        except (JudgePinError, PluginLeakError):
            raise
        except GenerationError as error:
            init, result, wall_ms = self._attempt(key, model, prompt)
            self.warnings.append(f"{key}: the first call failed and the retry succeeded: {error}")
        usage = result.get("usage") or {}
        row = {
            "type": "call",
            "date": datetime.now(UTC).isoformat(timespec="seconds"),
            "key": key,
            "check": check,
            "role": role,
            "prompt_id": prompt_id,
            "answer_sha256": answer_sha256,
            "index": index,
            "model_requested": model,
            "model_resolved": str(init.get("model", "")),
            "output": str(result.get("result", "")),
            "output_tokens": int(usage.get("output_tokens", 0)),
            "input_tokens": int(usage.get("input_tokens", 0)),
            "cache_creation_input_tokens": int(usage.get("cache_creation_input_tokens", 0)),
            "cache_read_input_tokens": int(usage.get("cache_read_input_tokens", 0)),
            "duration_ms": int(result.get("duration_ms", 0)),
            "wall_ms": wall_ms,
        }
        if extra:
            row.update(extra)
        with self.lock:
            self.rows[key] = row
            self.sink(row)
        return row

    def _attempt(self, key: str, model: str, prompt: str) -> tuple[dict, dict, int]:
        """One live judge call: the subprocess, then the sanity checks."""
        start = time.monotonic()
        stdout = self.run(judge_argv(prompt, model), self.workdir, self.env)
        wall_ms = round((time.monotonic() - start) * 1000)
        init, result = parse_events(stdout)
        # A judge call declares no plugin at all.
        assert_declared_plugins(init, (), key)
        active = init.get("output_style")
        if active != "default":
            raise GenerationError(
                f"{key}: expected the default output style, but {active!r} was active"
            )
        if result.get("is_error"):
            raise GenerationError(
                f"{key}: claude reported an error: {str(result.get('result', ''))[:500]}"
            )
        expected = JUDGE_MODEL_PINS.get(model, model)
        resolved = str(init.get("model", ""))
        if resolved != expected:
            raise JudgePinError(
                f"{key}: the judge model {model!r} must resolve to {expected!r}, "
                f"but the CLI resolved it to {resolved!r}"
            )
        return init, result, wall_ms

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
    pool: TaskPool,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    facts_by_pair: dict[tuple[str, str], dict[str, list[str]]],
    grader_model: str,
    reader_model: str,
    questions_cap: int,
    replicates: int,
) -> None:
    """One quiz per pair, from the shared facts, read by both answers.

    A pair without an entry in facts_by_pair was warned about by the
    caller and is skipped here. Each remaining pair is one task that
    writes the questions, and the task submits one reader-and-grade
    task per arm and replicate.
    """
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            survivors = facts_by_pair.get((style, prompt_id))
            if survivors is None:
                continue
            pool.submit(
                partial(
                    _judge_comprehension_pair,
                    session,
                    pool,
                    answers,
                    survivors,
                    grader_model=grader_model,
                    reader_model=reader_model,
                    questions_cap=questions_cap,
                    replicates=replicates,
                    style=style,
                    prompt_id=prompt_id,
                )
            )


def _judge_comprehension_pair(
    session: JudgeSession,
    pool: TaskPool,
    answers: dict[tuple[str, str | None], dict],
    survivors: dict[str, list[str]],
    *,
    grader_model: str,
    reader_model: str,
    questions_cap: int,
    replicates: int,
    style: str,
    prompt_id: str,
) -> None:
    """The question call of one pair, then one task per replicate.

    The facts of a pair come in the two wordings of the answers, and
    the quiz takes half of its cap from each wording. The reference
    answer of a question is the fact that produced the question. Both
    arms answer the same question list, so the question order carries
    no arm bias. Every reader replicate depends only on the questions,
    so each (arm, replicate) goes to the pool as its own task.
    """
    total = len(survivors["unstyled"]) + len(survivors["styled"])
    if total < FACTS_FLOOR:
        session.warnings.append(
            f"{style}/{prompt_id}: the pair has {total} shared facts, "
            f"fewer than the floor of {FACTS_FLOOR}, so comprehension skips the pair"
        )
        return
    facts, sources = select_balanced(survivors["unstyled"], survivors["styled"], questions_cap)
    questions = session.structured(
        validate=partial(parse_strings, n=len(facts)),
        key=f"comprehension:v3:questions:{style}:{prompt_id}",
        check="comprehension",
        role="questions",
        model=grader_model,
        prompt=QUESTIONS_FROM_FACTS_PROMPT.format(facts=_numbered(facts)),
        prompt_id=prompt_id,
        answer_sha256=None,
        extra={"sources": sources},
    )
    if questions is None:
        session.warnings.append(
            f"{style}/{prompt_id}: the question writer returned no usable "
            "questions, so comprehension skips the pair"
        )
        return
    references = [
        {"question": question, "reference": fact}
        for question, fact in zip(questions, facts, strict=True)
    ]
    for arm, arm_key in (("styled", (prompt_id, style)), ("unstyled", (prompt_id, None))):
        text = answers[arm_key]
        for replicate in range(replicates):
            pool.submit(
                partial(
                    _read_and_grade,
                    session,
                    questions,
                    references,
                    text,
                    grader_model=grader_model,
                    reader_model=reader_model,
                    style=style,
                    prompt_id=prompt_id,
                    arm=arm,
                    replicate=replicate,
                )
            )


def _read_and_grade(
    session: JudgeSession,
    questions: list[str],
    references: list[dict],
    text: dict,
    *,
    grader_model: str,
    reader_model: str,
    style: str,
    prompt_id: str,
    arm: str,
    replicate: int,
) -> None:
    """The reader call and the grade call of one replicate, one task.

    The grade call consumes the replies of the reader call, so the
    two calls stay in one task.
    """
    replies = session.structured(
        validate=partial(parse_strings, n=len(questions)),
        key=f"comprehension:v3:reader:{style}:{prompt_id}:{arm}:{replicate}",
        check="comprehension",
        role="reader",
        model=reader_model,
        prompt=READER_PROMPT.format(text=text["text"], questions=_numbered(questions)),
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
        return
    grades = session.structured(
        validate=partial(parse_bools, n=len(questions)),
        key=f"comprehension:v3:grades:{style}:{prompt_id}:{arm}:{replicate}",
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


def _paraphrase_call(session: JudgeSession, model: str, text: dict, index: int) -> None:
    """One restatement call, one task."""
    session.call(
        key=f"paraphrase:reader:{text['sha256']}:{index}",
        check="paraphrase",
        role="paraphrase",
        model=model,
        prompt=PARAPHRASE_PROMPT.format(text=text["text"]),
        prompt_id=text["prompt_id"],
        answer_sha256=text["sha256"],
        index=index,
    )


def _roundtrip_chain(session: JudgeSession, model: str, language: str, text: dict) -> None:
    """The translate call and the back call of one text, one task.

    The back call consumes the output of the translate call, so the
    two calls stay in one task.
    """
    translated = session.call(
        key=f"roundtrip:translate:{text['sha256']}",
        check="roundtrip",
        role="translate",
        model=model,
        prompt=TRANSLATE_PROMPT.format(language=language, text=text["text"]),
        prompt_id=text["prompt_id"],
        answer_sha256=text["sha256"],
    )
    session.call(
        key=f"roundtrip:back:{text['sha256']}",
        check="roundtrip",
        role="back",
        model=model,
        prompt=BACK_PROMPT.format(text=translated["output"]),
        prompt_id=text["prompt_id"],
        answer_sha256=text["sha256"],
    )


def run_judges(
    *,
    texts: list[dict],
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    facts_by_pair: dict[tuple[str, str], dict[str, list[str]]],
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
    env: dict[str, str] | None = None,
    parallel: int = 1,
    force_keys: set[str] | None = None,
) -> list[str]:
    """Run the judge calls for every pair and return the warnings.

    The texts list holds the unique texts for the per-text checks:
    one dict with prompt_id, sha256, and text per unique sha256. The
    comprehension check works per pair instead, with the shared facts
    from facts_by_pair. The rows mapping is read for reuse and
    extended in place; every new row also goes to the sink. One pool
    spans the checks, the parallel count sets how many tasks run at
    a time, and a call runs as soon as its inputs exist. Each key in
    force_keys runs live once, past the stored row: the freshness
    sample of a reuse pass.
    """
    session = JudgeSession(
        rows=rows, sink=sink, workdir=workdir, run=run, env=env, force_keys=force_keys or set()
    )
    pool = TaskPool(parallel)

    if "comprehension" in checks:
        _judge_comprehension(
            session,
            pool,
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
                pool.submit(partial(_paraphrase_call, session, reader_model, text, index))

    if "roundtrip" in checks:
        for text in texts:
            pool.submit(partial(_roundtrip_chain, session, reader_model, language, text))

    pool.drain()
    return session.warnings
