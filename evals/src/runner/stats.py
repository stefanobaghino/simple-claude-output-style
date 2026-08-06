"""Shared order statistics for the harness tools."""

from __future__ import annotations

from math import ceil


def nearest_rank(ordered: list[float], percentile: float) -> float:
    """The nearest-rank percentile of an ascending list."""
    rank = ceil(percentile / 100 * len(ordered))
    return ordered[max(rank, 1) - 1]
