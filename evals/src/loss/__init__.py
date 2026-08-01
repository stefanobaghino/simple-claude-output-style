"""Content-loss checks: which facts and which hedges of the unstyled
answer survive in the styled answer, per gated pair?"""

from .analysis import LossResult, score_checks
from .judges import CHECKS, VERDICTS, parse_string_list, parse_verdicts, run_judges
from .report import build_loss_report, build_loss_summary

__all__ = [
    "CHECKS",
    "VERDICTS",
    "LossResult",
    "build_loss_report",
    "build_loss_summary",
    "parse_string_list",
    "parse_verdicts",
    "run_judges",
    "score_checks",
]
