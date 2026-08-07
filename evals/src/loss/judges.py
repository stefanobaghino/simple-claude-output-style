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
from runner.hermetic import CONFIG_MODE, manifest_sha256
from value.judges import (
    JudgeSession,
    RowSink,
    TaskPool,
    extract_json,
    judge_prompts_sha256,
    parse_bools,
)

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

JUDGE_PROMPTS_SHA256 = judge_prompts_sha256(
    {
        "facts": FACTS_PROMPT,
        "facts_check": FACTS_CHECK_PROMPT,
        "claims": CLAIMS_PROMPT,
        "claims_check": CLAIMS_CHECK_PROMPT,
    }
)
"""The hash of the content-loss judge prompts, stored in the meta row."""


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


def build_meta(*, model: str, answers_sha256: str, cli_version: str | None = None) -> dict:
    return {
        "type": "meta",
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": cli_version,
        "config": CONFIG_MODE,
        "config_manifest_sha256": manifest_sha256(),
        "model": model,
        "fact_mine": FACT_MINE,
        "judge_prompts_sha256": JUDGE_PROMPTS_SHA256,
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


def _dependents(
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    *,
    reverse: bool,
) -> dict[str, list[tuple[str, dict, dict]]]:
    """The pairs behind each source sha: (prompt_id, styled, checked).

    Forward, the styled text is checked against the facts of the
    unstyled answer. In reverse, the unstyled text is checked against
    the facts of the styled answer. The check key carries the styled
    sha in both directions, so two styles that share one unstyled
    answer never share a check row. Two pairs with byte-identical
    styled texts do share a key, and each pair keeps its own entry
    here, so both tasks run and can both miss the row fast path. The
    key gets two rows, the last row wins at load, and the marks
    agree, so the duplicate is harmless.
    """
    grouped: dict[str, list[tuple[str, dict, dict]]] = {}
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            styled = answers[(prompt_id, style)]
            unstyled = answers[(prompt_id, None)]
            source, checked = (styled, unstyled) if reverse else (unstyled, styled)
            grouped.setdefault(source["sha256"], []).append((prompt_id, styled, checked))
    return grouped


def _submit_extractions(
    session: JudgeSession,
    pool: TaskPool,
    arms: list[tuple[str, dict]],
    dependents: dict[str, list[tuple[str, dict, dict]]],
    *,
    check: str,
    role: str,
    check_role: str,
    prompt_template: str,
    check_template: str,
    validate_factory,
    model: str,
    noun: str,
    reverse: bool,
    consequence: str | None = None,
) -> None:
    """One extraction task per unique text; each submits its check tasks."""
    consequence = consequence or f"{check} skips its pairs"
    for prompt_id, arm in arms:
        pool.submit(
            partial(
                _extract_one,
                session,
                pool,
                prompt_id,
                arm,
                dependents.get(arm["sha256"], []),
                check=check,
                role=role,
                check_role=check_role,
                prompt_template=prompt_template,
                check_template=check_template,
                validate_factory=validate_factory,
                model=model,
                noun=noun,
                reverse=reverse,
                consequence=consequence,
            )
        )


def _extract_one(
    session: JudgeSession,
    pool: TaskPool,
    prompt_id: str,
    arm: dict,
    dependents: list[tuple[str, dict, dict]],
    *,
    check: str,
    role: str,
    check_role: str,
    prompt_template: str,
    check_template: str,
    validate_factory,
    model: str,
    noun: str,
    reverse: bool,
    consequence: str,
) -> None:
    """One extraction call; a non-empty list submits the dependent checks.

    The arms carry unique shas, so one extraction serves every pair
    with the same source text. An empty list is a valid extraction
    (routine for hedging), and the pairs behind it get no check call
    and no warning, as before.
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
    if not items:
        return
    for pair_prompt_id, styled, checked in dependents:
        pool.submit(
            partial(
                _check_pair,
                session,
                items,
                styled,
                checked,
                pair_prompt_id,
                check=check,
                role=check_role,
                prompt_template=check_template,
                validate_factory=validate_factory,
                model=model,
                noun=noun,
                reverse=reverse,
            )
        )


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
    env: dict[str, str] | None = None,
    parallel: int = 1,
) -> list[str]:
    """Run the judge calls for every pair and return the warnings.

    The answers mapping goes from (prompt_id, style or None) to a dict
    with text and sha256. The rows mapping is read for reuse and
    extended in place; every new row also goes to the sink. One pool
    spans the checks, the parallel count sets how many tasks run at
    a time, and a check call starts as soon as its own extraction is
    complete.
    """
    session = JudgeSession(rows=rows, sink=sink, workdir=workdir, run=run, env=env)
    pool = TaskPool(parallel)

    if "completeness" in checks:
        _submit_extractions(
            session,
            pool,
            _unstyled_arms(pairs, answers),
            _dependents(pairs, answers, reverse=False),
            check="completeness",
            role="facts",
            check_role="check",
            prompt_template=FACTS_PROMPT,
            check_template=FACTS_CHECK_PROMPT,
            validate_factory=lambda n: partial(parse_bools, n=n),
            model=model,
            noun="fact",
            reverse=False,
        )
        _submit_extractions(
            session,
            pool,
            _styled_arms(pairs, answers),
            _dependents(pairs, answers, reverse=True),
            check="completeness",
            role="facts",
            check_role="reverse",
            prompt_template=FACTS_PROMPT,
            check_template=FACTS_CHECK_PROMPT,
            validate_factory=lambda n: partial(parse_bools, n=n),
            model=model,
            noun="fact",
            reverse=True,
            consequence="the additions of its pairs are unscored",
        )

    if "hedging" in checks:
        _submit_extractions(
            session,
            pool,
            _unstyled_arms(pairs, answers),
            _dependents(pairs, answers, reverse=False),
            check="hedging",
            role="claims",
            check_role="check",
            prompt_template=CLAIMS_PROMPT,
            check_template=CLAIMS_CHECK_PROMPT,
            validate_factory=lambda n: partial(parse_verdicts, n=n),
            model=model,
            noun="claim",
            reverse=False,
        )

    pool.drain()
    return session.warnings
