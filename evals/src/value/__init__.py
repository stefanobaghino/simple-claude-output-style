"""Reader-value checks: does the styled answer beat the unstyled
answer for a reader, per gated pair, as win, loss, or tie?"""

from .analysis import CHECK_RULES, TIE_EPSILON, ValueResult, score_checks, select_pairs
from .judges import CHECKS, extract_json, judge_argv, run_judges
from .report import build_value_report, build_value_summary
from .similarity import mean_pairwise_f1, unigram_f1

__all__ = [
    "CHECKS",
    "CHECK_RULES",
    "TIE_EPSILON",
    "ValueResult",
    "build_value_report",
    "build_value_summary",
    "extract_json",
    "judge_argv",
    "mean_pairwise_f1",
    "run_judges",
    "score_checks",
    "select_pairs",
    "unigram_f1",
]
