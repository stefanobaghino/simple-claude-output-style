"""Run the blind judge calls of the content-loss checks.

Each check has two call shapes. An extraction call sees only the
unstyled text and lists its facts or its uncertain claims. A check
call sees only the styled text plus the extracted list. The extracted
items travel between the calls, never the source text, so no call
sees both answers of a pair. No prompt names a style or an arm.

The extraction is keyed by the sha256 of the unstyled text, so two
styles that share an unstyled answer share the extraction. The rows
go to the same sink design as the reader-value checks, and a later
run reuses every stored key.
"""

from __future__ import annotations

from datetime import UTC, datetime
from functools import partial
from pathlib import Path

from runner.generate import ISOLATION_FLAGS, Runner, subprocess_runner
from runner.provenance import claude_version
from value.judges import JudgeSession, RowSink, extract_json, parse_bools

CHECKS = ("completeness", "hedging")
VERDICTS = ("hedged", "certain", "absent")

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


def _extract(
    session: JudgeSession,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    *,
    check: str,
    role: str,
    prompt_template: str,
    model: str,
    noun: str,
) -> dict[str, list[str]]:
    """One extraction call per unique unstyled text. Returns lists by sha."""
    lists: dict[str, list[str]] = {}
    for prompt_id, arm in _unstyled_arms(pairs, answers):
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
                f"{arm['sha256'][:12]}, so {check} skips its pairs"
            )
            continue
        lists[arm["sha256"]] = items
    return lists


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
) -> None:
    """One check call per pair whose unstyled arm has a non-empty list."""
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            items = lists.get(answers[(prompt_id, None)]["sha256"])
            if not items:
                continue
            styled = answers[(prompt_id, style)]
            marks = session.structured(
                validate=validate_factory(len(items)),
                key=f"{check}:check:{styled['sha256']}",
                check=check,
                role="check",
                model=model,
                prompt=prompt_template.format(text=styled["text"], claims=_numbered(items)),
                prompt_id=prompt_id,
                answer_sha256=styled["sha256"],
            )
            if marks is None:
                session.warnings.append(
                    f"{prompt_id}: the {noun} check returned no usable marks for the text "
                    f"{styled['sha256'][:12]}, so the pair is unscored"
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
) -> list[str]:
    """Run the judge calls for every pair and return the warnings.

    The answers mapping goes from (prompt_id, style or None) to a dict
    with text and sha256. The rows mapping is read for reuse and
    extended in place; every new row also goes to the sink.
    """
    session = JudgeSession(rows=rows, sink=sink, workdir=workdir, run=run)

    if "completeness" in checks:
        facts = _extract(
            session,
            pairs,
            answers,
            check="completeness",
            role="facts",
            prompt_template=FACTS_PROMPT,
            model=model,
            noun="fact",
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
        )

    if "hedging" in checks:
        claims = _extract(
            session,
            pairs,
            answers,
            check="hedging",
            role="claims",
            prompt_template=CLAIMS_PROMPT,
            model=model,
            noun="claim",
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
        )

    return session.warnings
