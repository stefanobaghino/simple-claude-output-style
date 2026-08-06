"""Summarize the call timing of the stored rows.

Every live call stores two times: duration_ms is the model time that
the CLI reports, and wall_ms is the wall clock of the subprocess. The
difference is the startup cost of one CLI call: the subprocess loads
its configuration and plugins before the API call starts. The summary
lands in the md reports only, because the raw rows already hold the
machine-readable times. Old rows predate the wall_ms field, so the
summary counts only the measured rows and states when none exist.
"""

from __future__ import annotations

from collections.abc import Iterable
from statistics import fmean


def timing_summary(rows: Iterable[dict]) -> dict | None:
    """The call timing of the rows, or None when no row exists.

    A row is measured when it holds an integer wall_ms. The means run
    over the measured rows only, and the three means are None when no
    row is measured.
    """
    calls = 0
    measured: list[dict] = []
    for row in rows:
        calls += 1
        if isinstance(row.get("wall_ms"), int):
            measured.append(row)
    if calls == 0:
        return None
    if not measured:
        means = {"mean_duration_ms": None, "mean_wall_ms": None, "mean_startup_ms": None}
    else:
        durations = [int(row.get("duration_ms", 0)) for row in measured]
        walls = [int(row["wall_ms"]) for row in measured]
        means = {
            "mean_duration_ms": round(fmean(durations)),
            "mean_wall_ms": round(fmean(walls)),
            "mean_startup_ms": round(fmean([w - d for w, d in zip(walls, durations)])),
        }
    return {"calls": calls, "measured": len(measured), **means}


def timing_section(timing: dict | None) -> list[str]:
    """The md lines of the call-timing section of a report."""
    lines = [
        "## Call timing",
        "",
        "A stored call row holds two times: duration_ms is the model",
        "time that the CLI reports, and wall_ms is the wall clock of",
        "the subprocess. The difference is the startup cost of one CLI",
        "call.",
        "",
    ]
    if timing is None or timing["measured"] == 0:
        lines += ["The wall is not measured: the stored rows predate the wall_ms field.", ""]
        return lines
    lines += [
        f"Calls: {timing['calls']}, measured: {timing['measured']}.",
        (
            f"Mean duration: {timing['mean_duration_ms']} ms. "
            f"Mean wall: {timing['mean_wall_ms']} ms. "
            f"Mean startup: {timing['mean_startup_ms']} ms."
        ),
        "",
    ]
    return lines
