"""Score stored sessions.

The scoring is a pure function of sessions.jsonl, the rule files, and
the flags: per style, the violation-rate series over turn positions,
the pooled series over the complete sessions, the slope of the pooled
series, and the verdict flat or growing. The verdict threshold comes
from a per-style permutation null: the turn order of each session
shuffles, the pooled slope refits, and the threshold is the 0.95
nearest-rank quantile of the shuffled slopes.
"""

from __future__ import annotations

import hashlib
import json
import random
import statistics
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from linter import Linter
from runner.stats import nearest_rank

Key = tuple[str, int, int]
"""(style, repeat, turn), both numbers 1-based."""

PERMUTATIONS = 1000
"""Shuffles per style for the permutation null."""

SEED = 0
"""Seed of the permutation null, so a rescore repeats the threshold."""

QUANTILE = 0.95
"""The one-sided null quantile that becomes the derived threshold."""


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


def _pooled_series(session_pairs: list[list[tuple[int, int]]], turns: int) -> list[float]:
    """Per turn, 100 times the violations over the sentences, pooled.

    The pool spans the complete sessions at that turn position, so a
    short answer weighs by its sentence count. A zero sentence sum
    gives 0.0, the mirror of the linter rate.
    """
    series = []
    for index in range(turns):
        violations = sum(pairs[index][0] for pairs in session_pairs)
        sentences = sum(pairs[index][1] for pairs in session_pairs)
        series.append(round(100 * violations / sentences, 2) if sentences else 0.0)
    return series


def _derived_threshold(
    session_pairs: list[list[tuple[int, int]]],
    turns: int,
    permutations: int,
    seed: int,
) -> float:
    """The 0.95 nearest-rank quantile of the shuffled pooled slopes.

    Each permutation shuffles the turn order within each session, so
    the null keeps the rates and breaks only the turn positions.
    """
    rng = random.Random(seed)
    null = []
    for _ in range(permutations):
        shuffled = []
        for pairs in session_pairs:
            copy = list(pairs)
            rng.shuffle(copy)
            shuffled.append(copy)
        slope, _ = statistics.linear_regression(
            range(1, turns + 1), _pooled_series(shuffled, turns)
        )
        null.append(slope)
    return nearest_rank(sorted(null), QUANTILE * 100)


def score_sessions(
    *,
    rows: dict[Key, dict],
    linters: dict[str, Linter],
    turns: int,
    repeats: int,
    threshold: float | None = None,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
) -> DriftResult:
    """Score every style of the linters mapping against the stored rows."""
    result = DriftResult()
    wanted = set(range(1, turns + 1))
    for style in sorted(linters):
        sessions: list[dict] = []
        session_pairs: list[list[tuple[int, int]]] = []
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
            pairs = []
            for turn in sorted(wanted):
                detail = _turn_row(rows[(style, repeat, turn)], linters[style])
                if detail["sentences"] == 0:
                    result.warnings.append(
                        f"{style}: session {repeat} turn {turn} has no sentences"
                    )
                turn_details.append(detail)
                series.append(detail["rate"])
                pairs.append((detail["violations"], detail["sentences"]))
            sessions.append({"repeat": repeat, "series": series})
            session_pairs.append(pairs)

        if not sessions:
            result.warnings.append(f"{style}: no complete session, so the style has no verdict")
            result.styles[style] = {
                "complete_sessions": 0,
                "sessions": [],
                "pooled_series": None,
                "slope": None,
                "intercept": None,
                "threshold": None,
                "threshold_source": None,
                "null": None,
                "verdict": None,
                "turns": [],
            }
            continue

        pooled_series = _pooled_series(session_pairs, turns)
        slope, intercept = statistics.linear_regression(range(1, turns + 1), pooled_series)
        derived = _derived_threshold(session_pairs, turns, permutations, seed)
        effective = derived if threshold is None else threshold
        result.styles[style] = {
            "complete_sessions": len(sessions),
            "sessions": sessions,
            "pooled_series": pooled_series,
            "slope": round(slope, 3),
            "intercept": round(intercept, 3),
            "threshold": round(effective, 3),
            "threshold_source": "derived" if threshold is None else "override",
            "null": {
                "permutations": permutations,
                "seed": seed,
                "quantile": QUANTILE,
                "threshold": round(derived, 3),
            },
            "verdict": "growing" if slope > effective else "flat",
            "turns": turn_details,
        }
    return result
