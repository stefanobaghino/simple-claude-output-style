"""The cross-run comparison.

One run gives one sample per verdict, and a win-loss table over 20
pairs can flip on a resample. The comparison reads several runs with
identical conditions and states, per style and axis, the spread
across the runs: the error bar of the harness.
"""

from .analysis import CompareResult, compare_runs
from .report import build_compare_report, build_compare_summary

__all__ = [
    "CompareResult",
    "build_compare_report",
    "build_compare_summary",
    "compare_runs",
]
