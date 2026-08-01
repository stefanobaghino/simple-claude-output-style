"""Score the answers of a run and mark each pair.

A styled answer is checked with the rule set of its style and gets a
pass or fail mark. An unstyled answer is checked with the rule set of
every style in the run, as a baseline, and gets no mark: the baseline
shows how much rule obedience exists without a style. A styled answer
is never checked against the rules of another style, because the
styles conflict on purpose.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass, field

from linter import Linter
from linter.engine import Violation

from .config import GateConfig


@dataclass
class GateResult:
    rows: list[dict] = field(default_factory=list)
    failing: dict[tuple[str, str], list[Violation]] = field(default_factory=dict)
    """The violation detail per failing (prompt_id, style), for the report."""
    warnings: list[str] = field(default_factory=list)


def _row(
    answer: dict, rule_set: str, linter: Linter, threshold: float | None
) -> tuple[dict, list[Violation]]:
    report = linter.lint_text(answer["answer"], file=answer["prompt_id"])
    styled = answer.get("style") is not None
    passed = None
    if styled:
        passed = report.sentence_count > 0 and report.rate <= threshold
    row = {
        "prompt_id": answer["prompt_id"],
        "style": answer.get("style"),
        "rule_set": rule_set,
        "sentences": report.sentence_count,
        "violations": len(report.violations),
        "by_rule": dict(sorted(Counter(v.rule for v in report.violations).items())),
        "rate": round(report.rate, 2),
        "threshold": threshold if styled else None,
        "pass": passed,
        "answer_sha256": hashlib.sha256(answer["answer"].encode("utf-8")).hexdigest(),
    }
    return row, list(report.violations)


def score_run(answers: list[dict], linters: dict[str, Linter], config: GateConfig) -> GateResult:
    """Score a deduplicated answer set. The styles come from the answers."""
    styles = sorted({a["style"] for a in answers if a.get("style") is not None})
    result = GateResult()

    for answer in answers:
        style = answer.get("style")
        rule_sets = [style] if style is not None else styles
        for rule_set in rule_sets:
            threshold = config.thresholds.get(rule_set)
            row, violations = _row(answer, rule_set, linters[rule_set], threshold)
            result.rows.append(row)
            if row["pass"] is False:
                result.failing[(row["prompt_id"], style)] = violations
            if style is not None and row["sentences"] == 0:
                result.warnings.append(
                    f"{style}/{answer['prompt_id']}: the answer has no sentences and fails the gate"
                )

    unstyled_ids = {a["prompt_id"] for a in answers if a.get("style") is None}
    for style in styles:
        styled_ids = {a["prompt_id"] for a in answers if a.get("style") == style}
        for prompt_id in sorted(styled_ids - unstyled_ids):
            result.warnings.append(
                f"{style}/{prompt_id}: the unstyled counterpart is missing, so the pair is "
                "unusable downstream"
            )
        for prompt_id in sorted(unstyled_ids - styled_ids):
            result.warnings.append(f"{style}/{prompt_id}: the styled answer is missing")
    return result
