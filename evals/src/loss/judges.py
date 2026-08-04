"""Run the blind judge calls of the content-loss checks.

Each check has two call shapes. An extraction call sees one answer
text and lists its facts or its uncertain claims. A check call sees
the other answer text plus the extracted list. The extracted items
travel between the calls, never the source text, so no call sees
both answers of a pair. No prompt names a style or an arm.

The completeness check mines both directions: the facts of the
unstyled answer are checked against the styled answer, and the facts
of the styled answer are checked against the unstyled answer. The
hedging check mines one direction only. An extraction is keyed by the
sha256 of its source text, and both check directions are keyed by the
sha256 of the styled text, so two styles that share an unstyled
answer share the extraction but never a check row. The rows go to the
same sink design as the reader-value checks, and a later run reuses
every stored key.
"""

from __future__ import annotations

from datetime import UTC, datetime
from functools import partial
from pathlib import Path

from runner.generate import ISOLATION_FLAGS, Runner, subprocess_runner
from runner.provenance import claude_version
from value.judges import JudgeSession, RowSink, extract_json, parse_bools, run_parallel

CHECKS = ("completeness", "hedging")
VERDICTS = ("hedged", "certain", "absent")

FACT_MINE = "two-way"
"""The design tag of the fact mine, stored in the meta row.

A raw file without the tag holds a one-way mine: the facts of the
unstyled answer only. The two-way mine adds the facts of the styled
answer plus a reverse check against the unstyled answer, so the
scorer can count the additions of a pair.
"""

FACTS_PROMPT = """\
List the distinct factual claims that the text below states. Keep
each claim short and self-contained. Output only a JSON array of
strings, one claim per item.

Text:
{text}"""

FACTS_CHECK_PROMPT = """\
Check each claim below against the text. A claim survives when the
text states it or clearly implies it; the wording is free. Output
only a JSON array of booleans, one per claim, in order.

Text:
{text}

Claims:
{claims}"""

CLAIMS_PROMPT = """\
List the claims that the text below presents as uncertain, with a
hedge such as "may", "probably", "likely", or "I think". Keep the
uncertainty in each item. When the text presents no claim as
uncertain, output an empty array. Output only a JSON array of
strings.

Text:
{text}"""

CLAIMS_CHECK_PROMPT = """\
For each uncertain claim below, judge how the text treats the claim.
Reply "hedged" when the text keeps the claim with its uncertainty in
some form, "certain" when the text states the claim as a fact without
uncertainty, and "absent" when the text does not contain the claim.
Output only a JSON array of these strings, one per claim, in order.

Text:
{text}

Claims:
{claims}"""


def parse_string_list(output: str) -> list[str] | None:
    """A JSON array of strings, any length including zero, or None."""
    value = extract_json(output)
    if not isinstance(value, list):
        return None
    return [str(item) for item in value]


def parse_verdicts(output: str, n: int) -> list[str] | None:
    """A JSON array of exactly n verdict strings, or None."""
    value = extract_json(output)
    if not isinstance(value, list) or len(value) != n:
        return None
    if not all(item in VERDICTS for item in value):
        return None
    return value


def build_meta(*, model: str, answers_sha256: str) -> dict:
    return {
        "type": "meta",
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": claude_version(),
        "model": model,
        "fact_mine": FACT_MINE,
        "flags": list(ISOLATION_FLAGS),
        "answers_sha256": answers_sha256,
    }


def _numbered(items: list[str]) -> str:
    return "\n".join(f"{number}. {item}" for number, item in enumerate(items, start=1))


def _unstyled_arms(
    pairs: dict[str, list[str]], answers: dict[tuple[str, str | None], dict]
) -> list[tuple[str, dict]]:
    """The unique unstyled arms of the pairs, one per sha256."""
    arms: dict[str, tuple[str, dict]] = {}
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            arm = answers[(prompt_id, None)]
            arms.setdefault(arm["sha256"], (prompt_id, arm))
    return sorted(arms.values())


def _styled_arms(
    pairs: dict[str, list[str]], answers: dict[tuple[str, str | None], dict]
) -> list[tuple[str, dict]]:
    """The unique styled arms of the pairs, one per sha256."""
    arms: dict[str, tuple[str, dict]] = {}
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            arm = answers[(prompt_id, style)]
            arms.setdefault(arm["sha256"], (prompt_id, arm))
    return [arms[sha] for sha in sorted(arms)]


def _extract(
    session: JudgeSession,
    arms: list[tuple[str, dict]],
    *,
    check: str,
    role: str,
    prompt_template: str,
    model: str,
    noun: str,
    parallel: int,
    consequence: str | None = None,
) -> dict[str, list[str]]:
    """One extraction call per unique text, one task each. Returns lists by sha."""
    lists: dict[str, list[str]] = {}
    consequence = consequence or f"{check} skips its pairs"
    tasks = [
        partial(
            _extract_one,
            session,
            lists,
            prompt_id,
            arm,
            check=check,
            role=role,
            prompt_template=prompt_template,
            model=model,
            noun=noun,
            consequence=consequence,
        )
        for prompt_id, arm in arms
    ]
    run_parallel(tasks, parallel)
    return lists


def _extract_one(
    session: JudgeSession,
    lists: dict[str, list[str]],
    prompt_id: str,
    arm: dict,
    *,
    check: str,
    role: str,
    prompt_template: str,
    model: str,
    noun: str,
    consequence: str,
) -> None:
    """One extraction call.

    The arms carry unique shas, so parallel tasks never write one
    lists entry twice.
    """
    items = session.structured(
        validate=parse_string_list,
        key=f"{check}:{role}:{arm['sha256']}",
        check=check,
        role=role,
        model=model,
        prompt=prompt_template.format(text=arm["text"]),
        prompt_id=prompt_id,
        answer_sha256=arm["sha256"],
    )
    if items is None:
        session.warnings.append(
            f"{prompt_id}: the {noun} extraction returned no usable list for the text "
            f"{arm['sha256'][:12]}, so {consequence}"
        )
        return
    lists[arm["sha256"]] = items


def _check_pairs(
    session: JudgeSession,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    lists: dict[str, list[str]],
    *,
    check: str,
    prompt_template: str,
    validate_factory,
    model: str,
    noun: str,
    parallel: int,
    reverse: bool = False,
) -> None:
    """One check call per pair whose source arm has a non-empty list.

    Forward, the styled text is checked against the facts of the
    unstyled answer. In reverse, the unstyled text is checked against
    the facts of the styled answer. The key carries the styled sha in
    both directions, so two styles that share one unstyled answer
    never share a check row. Two pairs with byte-identical styled
    texts do share a key, and parallel tasks can then both miss the
    row fast path. The key gets two rows, the last row wins at load,
    and the marks agree, so the duplicate is harmless.
    """
    role = "reverse" if reverse else "check"
    tasks = []
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            styled = answers[(prompt_id, style)]
            unstyled = answers[(prompt_id, None)]
            source, checked = (styled, unstyled) if reverse else (unstyled, styled)
            items = lists.get(source["sha256"])
            if not items:
                continue
            tasks.append(
                partial(
                    _check_pair,
                    session,
                    items,
                    styled,
                    checked,
                    prompt_id,
                    check=check,
                    role=role,
                    prompt_template=prompt_template,
                    validate_factory=validate_factory,
                    model=model,
                    noun=noun,
                    reverse=reverse,
                )
            )
    run_parallel(tasks, parallel)


def _check_pair(
    session: JudgeSession,
    items: list[str],
    styled: dict,
    checked: dict,
    prompt_id: str,
    *,
    check: str,
    role: str,
    prompt_template: str,
    validate_factory,
    model: str,
    noun: str,
    reverse: bool,
) -> None:
    """One check call, one task."""
    marks = session.structured(
        validate=validate_factory(len(items)),
        key=f"{check}:{role}:{styled['sha256']}",
        check=check,
        role=role,
        model=model,
        prompt=prompt_template.format(text=checked["text"], claims=_numbered(items)),
        prompt_id=prompt_id,
        answer_sha256=checked["sha256"],
    )
    if marks is None:
        what = f"the {noun} reverse check" if reverse else f"the {noun} check"
        outcome = "the additions of the pair are" if reverse else "the pair is"
        session.warnings.append(
            f"{prompt_id}: {what} returned no usable marks for the text "
            f"{checked['sha256'][:12]}, so {outcome} unscored"
        )


def run_judges(
    *,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    checks: list[str],
    model: str,
    rows: dict[str, dict],
    sink: RowSink,
    workdir: Path,
    run: Runner = subprocess_runner,
    parallel: int = 1,
) -> list[str]:
    """Run the judge calls for every pair and return the warnings.

    The answers mapping goes from (prompt_id, style or None) to a dict
    with text and sha256. The rows mapping is read for reuse and
    extended in place; every new row also goes to the sink. The
    parallel count sets how many tasks run at a time, per phase, and
    a check phase starts only when its extraction phase is complete.
    """
    session = JudgeSession(rows=rows, sink=sink, workdir=workdir, run=run)

    if "completeness" in checks:
        facts = _extract(
            session,
            _unstyled_arms(pairs, answers),
            check="completeness",
            role="facts",
            prompt_template=FACTS_PROMPT,
            model=model,
            noun="fact",
            parallel=parallel,
        )
        _check_pairs(
            session,
            pairs,
            answers,
            facts,
            check="completeness",
            prompt_template=FACTS_CHECK_PROMPT,
            validate_factory=lambda n: partial(parse_bools, n=n),
            model=model,
            noun="fact",
            parallel=parallel,
        )
        styled_facts = _extract(
            session,
            _styled_arms(pairs, answers),
            check="completeness",
            role="facts",
            prompt_template=FACTS_PROMPT,
            model=model,
            noun="fact",
            parallel=parallel,
            consequence="the additions of its pairs are unscored",
        )
        _check_pairs(
            session,
            pairs,
            answers,
            styled_facts,
            check="completeness",
            prompt_template=FACTS_CHECK_PROMPT,
            validate_factory=lambda n: partial(parse_bools, n=n),
            model=model,
            noun="fact",
            parallel=parallel,
            reverse=True,
        )

    if "hedging" in checks:
        claims = _extract(
            session,
            _unstyled_arms(pairs, answers),
            check="hedging",
            role="claims",
            prompt_template=CLAIMS_PROMPT,
            model=model,
            noun="claim",
            parallel=parallel,
        )
        _check_pairs(
            session,
            pairs,
            answers,
            claims,
            check="hedging",
            prompt_template=CLAIMS_CHECK_PROMPT,
            validate_factory=lambda n: partial(parse_verdicts, n=n),
            model=model,
            noun="claim",
            parallel=parallel,
        )

    return session.warnings
