"""The token-cost report.

A style costs tokens in two ways: the style block adds a fixed quantity
of input tokens to every request, and the style changes the answer
length. The report states both numbers per style, over all pairs of a
run, gated or not.
"""

from .analysis import RatioResult, analyze_ratios
from .probe import probe_argv, probe_overhead
from .report import build_cost_report, build_cost_summary

__all__ = [
    "RatioResult",
    "analyze_ratios",
    "build_cost_report",
    "build_cost_summary",
    "probe_argv",
    "probe_overhead",
]
