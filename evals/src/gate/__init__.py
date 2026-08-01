"""The fidelity gate.

A non-compliant answer does not represent its style. The gate checks
each styled answer of a run with the rules of its style and marks the
pair as pass or fail against the threshold of the style. The judged
measurements read only the passing pairs.
"""

from .config import GateConfig, load_gate_config
from .score import GateResult, score_run

__all__ = ["GateConfig", "GateResult", "load_gate_config", "score_run"]
