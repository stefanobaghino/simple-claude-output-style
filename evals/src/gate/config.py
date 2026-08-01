"""Load the gate policy.

The policy lives in its own file, apart from the rule files: a threshold
edit changes only the pass mark, never the measured rate, and thus must
not change the rule-file hashes in the provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class GateConfig:
    path: Path
    thresholds: dict[str, float]
    """The highest passing violation rate per 100 sentences, per style."""


def load_gate_config(path: str | Path) -> GateConfig:
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    thresholds = raw.get("thresholds") if isinstance(raw, dict) else None
    if not isinstance(thresholds, dict) or not thresholds:
        raise ValueError(f"{path}: no thresholds defined")
    return GateConfig(
        path=path,
        thresholds={str(style): float(entry["max_rate"]) for style, entry in thresholds.items()},
    )
