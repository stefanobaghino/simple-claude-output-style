"""Blind clarity ranking: which answer of a prompt reads clearer, per
head-to-head contest, with the unstyled answer as a competitor?"""

from .analysis import UNSTYLED, RankResult, build_schedule, fit_bradley_terry, score_contests
from .judges import DESIGN, build_meta, contest_key, parse_pick, run_judges
from .report import build_rank_report, build_rank_summary

__all__ = [
    "DESIGN",
    "UNSTYLED",
    "RankResult",
    "build_meta",
    "build_rank_report",
    "build_rank_summary",
    "build_schedule",
    "contest_key",
    "fit_bradley_terry",
    "parse_pick",
    "run_judges",
    "score_contests",
]
