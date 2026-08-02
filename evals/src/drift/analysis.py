"""Score stored sessions.

The scoring is a pure function of sessions.jsonl, the rule files, and
the flags: per style, the violation-rate series over turn positions,
the mean series over the complete sessions, the slope of the mean
series, and the verdict flat or growing.
"""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from linter import Linter

Key = tuple[str, int, int]
"""(style, repeat, turn), both numbers 1-based."""


@dataclass
class DriftResult:
    styles: dict[str, dict] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def load_sessions(path: Path) -> dict[Key, dict]:
    """The stored turns, last (style, repeat, turn) wins."""
    rows: dict[Key, dict] = {}
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[(row["style"], row["repeat"], row["turn"])] = row
    return rows


def _turn_row(row: dict, linter: Linter) -> dict:
    report = linter.lint_text(
        row["answer"], file=f"{row['style']}/repeat-{row['repeat']}/turn-{row['turn']}"
    )
    return {
        "style": row["style"],
        "repeat": row["repeat"],
        "turn": row["turn"],
        "prompt_id": row["prompt_id"],
        "sentences": report.sentence_count,
        "violations": len(report.violations),
        "by_rule": dict(sorted(Counter(v.rule for v in report.violations).items())),
        "rate": round(report.rate, 2),
        "answer_sha256": hashlib.sha256(row["answer"].encode("utf-8")).hexdigest(),
    }


def score_sessions(
    *,
    rows: dict[Key, dict],
    linters: dict[str, Linter],
    turns: int,
    repeats: int,
    threshold: float,
) -> DriftResult:
    """Score every style of the linters mapping against the stored rows."""
    result = DriftResult()
    wanted = set(range(1, turns + 1))
    for style in sorted(linters):
        sessions: list[dict] = []
        turn_details: list[dict] = []
        for repeat in range(1, repeats + 1):
            present = {turn for (s, r, turn) in rows if s == style and r == repeat}
            if not present:
                result.warnings.append(f"{style}: session {repeat} has no turns")
                continue
            if present != wanted:
                missing = ", ".join(str(turn) for turn in sorted(wanted - present))
                result.warnings.append(
                    f"{style}: session {repeat} misses turn(s) {missing}, "
                    "so the session is excluded"
                )
                continue
            series = []
            for turn in sorted(wanted):
                detail = _turn_row(rows[(style, repeat, turn)], linters[style])
                if detail["sentences"] == 0:
                    result.warnings.append(
                        f"{style}: session {repeat} turn {turn} has no sentences"
                    )
                turn_details.append(detail)
                series.append(detail["rate"])
            sessions.append({"repeat": repeat, "series": series})

        if not sessions:
            result.warnings.append(f"{style}: no complete session, so the style has no verdict")
            result.styles[style] = {
                "complete_sessions": 0,
                "sessions": [],
                "mean_series": None,
                "slope": None,
                "intercept": None,
                "verdict": None,
                "turns": [],
            }
            continue

        mean_series = [
            round(statistics.fmean(session["series"][index] for session in sessions), 2)
            for index in range(turns)
        ]
        slope, intercept = statistics.linear_regression(range(1, turns + 1), mean_series)
        result.styles[style] = {
            "complete_sessions": len(sessions),
            "sessions": sessions,
            "mean_series": mean_series,
            "slope": round(slope, 3),
            "intercept": round(intercept, 3),
            "verdict": "growing" if slope > threshold else "flat",
            "turns": turn_details,
        }
    return result
