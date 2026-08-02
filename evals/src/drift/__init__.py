"""Drift measurement: does rule obedience decay as a session grows?

A scripted session runs per style, several times, and the linter
checks every turn. The report shows the violation-rate series over
turn positions and a verdict per style: flat or growing.
"""

from .analysis import DriftResult, load_sessions, score_sessions
from .report import build_drift_report, build_drift_summary
from .session import (
    SESSION_FLAGS,
    SessionTurn,
    build_session_argv,
    generate_turn,
    run_session,
    session_script,
)

__all__ = [
    "SESSION_FLAGS",
    "DriftResult",
    "SessionTurn",
    "build_drift_report",
    "build_drift_summary",
    "build_session_argv",
    "generate_turn",
    "load_sessions",
    "run_session",
    "score_sessions",
    "session_script",
]
