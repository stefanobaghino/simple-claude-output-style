"""Summarize the token spend of the stored rows.

Every live call stores four token counts: the uncached input tokens,
the cache-write input tokens, the cache-read input tokens, and the
output tokens. The totals per tool show what the harness itself
spends, and the cache-read share shows how much of the input comes
from the prompt cache. The summary lands in the md reports only,
because the raw rows already hold the machine-readable counts. Old
rows predate the token fields, so the summary counts only the
measured rows and states when none exist.
"""

from __future__ import annotations

from collections.abc import Iterable

TOKEN_FIELDS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)


def spend_summary(rows: Iterable[dict]) -> dict | None:
    """The token spend of the rows, or None when no row exists.

    A row is measured when it holds an integer input_tokens. The
    totals run over the measured rows only, and the totals are None
    when no row is measured.
    """
    calls = 0
    measured: list[dict] = []
    for row in rows:
        calls += 1
        if isinstance(row.get("input_tokens"), int):
            measured.append(row)
    if calls == 0:
        return None
    if not measured:
        totals: dict[str, int | float | None] = dict.fromkeys((*TOKEN_FIELDS, "cache_read_share"))
    else:
        counts = {field: sum(int(row.get(field, 0)) for row in measured) for field in TOKEN_FIELDS}
        input_total = (
            counts["input_tokens"]
            + counts["cache_creation_input_tokens"]
            + counts["cache_read_input_tokens"]
        )
        share = round(counts["cache_read_input_tokens"] / input_total, 3) if input_total else None
        totals = {**counts, "cache_read_share": share}
    return {"calls": calls, "measured": len(measured), **totals}


def spend_section(spend: dict | None) -> list[str]:
    """The md lines of the harness-spend section of a report."""
    lines = [
        "## Harness spend",
        "",
        "A stored call row holds the token counts of its call: the",
        "uncached input, cache-write input, cache-read input, and",
        "output tokens. The cache-read share is the cache-read total",
        "over the whole input total.",
        "",
    ]
    if spend is None or spend["measured"] == 0:
        lines += ["The spend is not measured: the stored rows predate the token fields.", ""]
        return lines
    share = spend["cache_read_share"]
    lines += [
        f"Calls: {spend['calls']}, measured: {spend['measured']}.",
        (
            f"Input tokens: {spend['input_tokens']} uncached, "
            f"{spend['cache_creation_input_tokens']} cache write, "
            f"{spend['cache_read_input_tokens']} cache read. "
            f"Output tokens: {spend['output_tokens']}."
        ),
        f"Cache-read share: {'not computable' if share is None else share}.",
        "",
    ]
    return lines
