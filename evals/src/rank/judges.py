"""Run the blind clarity contests of a run.

This tool relaxes one harness invariant on purpose: a clarity
contest is a choice, so a judge call sees both answers of a prompt
side by side. Blindness holds through the absence of labels. The
texts appear only as "Text 1" and "Text 2", no prompt names a style
or an arm, and the position mapping lives only in the raw rows.
Each contest runs in both orders, and the scorer scores a contest
only with two usable picks, so a position preference cancels
instead of counting.

The rows go to the same sink design as the reader-value checks, and
a later run reuses every stored key. A key carries the prompt id
plus the sha256 of both texts in their shown order, so a changed
answer invalidates its stale rows, and the two orders of a contest
never share a row.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from functools import partial
from pathlib import Path

from runner.generate import ISOLATION_FLAGS, Runner, subprocess_runner
from runner.hermetic import CONFIG_MODE, manifest_sha256
from value.judges import JudgeSession, RowSink, TaskPool, judge_prompts_sha256

DESIGN = "clarity-v1"
"""The design tag of the contest prompt, stored in the meta row."""

ORDERS = 2
"""Both orders of every contest run, so a position preference cancels."""

REPLICATES = 1
"""One judge call per order."""

CLARITY_PROMPT = """\
Two texts below answer the same request. Judge which text is clearer
for a reader: easier to understand and easier to act on. You must
pick one, even when the difference is small. Output only the single
character "1" or "2".

Text 1:
{first}

Text 2:
{second}"""

JUDGE_PROMPTS_SHA256 = judge_prompts_sha256({"clarity": CLARITY_PROMPT})
"""The hash of the clarity contest prompt, stored in the meta row."""

_PICK = re.compile(r"(?:text\s*)?([12])", re.IGNORECASE)


def parse_pick(output: str) -> int | None:
    """The picked position of a judge output, 1 or 2, or None."""
    stripped = output.strip().strip("\"'`*").strip()
    match = _PICK.fullmatch(stripped)
    return int(match.group(1)) if match else None


def contest_key(prompt_id: str, first_sha256: str, second_sha256: str) -> str:
    """The row key of one order: the texts in their shown order."""
    return f"clarity:{prompt_id}:{first_sha256}:{second_sha256}"


def build_meta(*, model: str, answers_sha256: str, cli_version: str | None = None) -> dict:
    return {
        "type": "meta",
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": cli_version,
        "config": CONFIG_MODE,
        "config_manifest_sha256": manifest_sha256(),
        "model": model,
        "design": DESIGN,
        "orders": ORDERS,
        "replicates": REPLICATES,
        "judge_prompts_sha256": JUDGE_PROMPTS_SHA256,
        "flags": list(ISOLATION_FLAGS),
        "answers_sha256": answers_sha256,
    }


def _judge_order(
    session: JudgeSession,
    *,
    contest: dict,
    first: tuple[str, str, str],
    second: tuple[str, str, str],
    model: str,
) -> None:
    """One order of one contest, one task.

    A side is (competitor, sha256, text). The competitor names go
    only into the raw row, never into the judge prompt.
    """
    first_name, first_sha, first_text = first
    second_name, second_sha, second_text = second
    pick = session.structured(
        validate=parse_pick,
        key=contest_key(contest["prompt_id"], first_sha, second_sha),
        check="clarity",
        role="pick",
        model=model,
        prompt=CLARITY_PROMPT.format(first=first_text, second=second_text),
        prompt_id=contest["prompt_id"],
        answer_sha256=None,
        extra={
            "first": first_name,
            "second": second_name,
            "first_sha256": first_sha,
            "second_sha256": second_sha,
        },
    )
    if pick is None:
        session.warnings.append(
            f"{contest['a']} vs {contest['b']} on {contest['prompt_id']}: the judge "
            f"gave no usable pick for the order with {first_name} first, so the "
            "contest is unscored"
        )


def run_judges(
    *,
    contests: list[dict],
    model: str,
    rows: dict[str, dict],
    sink: RowSink,
    workdir: Path,
    run: Runner = subprocess_runner,
    env: dict[str, str] | None = None,
    parallel: int = 1,
) -> list[str]:
    """Run both orders of every contest and return the warnings.

    An identical contest (both texts equal) gets no call: the scorer
    marks the split. The rows mapping is read for reuse and extended
    in place; every new row also goes to the sink. Every order is
    its own task, so the orders run several at a time.
    """
    session = JudgeSession(rows=rows, sink=sink, workdir=workdir, run=run, env=env)
    pool = TaskPool(parallel)
    for contest in contests:
        if contest["identical"]:
            continue
        side_a = (contest["a"], contest["a_sha"], contest["a_text"])
        side_b = (contest["b"], contest["b_sha"], contest["b_text"])
        for first, second in ((side_a, side_b), (side_b, side_a)):
            pool.submit(
                partial(
                    _judge_order, session, contest=contest, first=first, second=second, model=model
                )
            )
    pool.drain()
    return session.warnings
