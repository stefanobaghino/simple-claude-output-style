"""Render the fidelity artifacts of a gated run.

fidelity.json holds the machine-readable summary and the gate
provenance. fidelity.md is for a human who opens the run directory.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime


def _mean_rate(rows: list[dict]) -> float:
    sentences = sum(r["sentences"] for r in rows)
    violations = sum(r["violations"] for r in rows)
    return round(100.0 * violations / sentences, 2) if sentences else 0.0


def _by_rule(rows: list[dict]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        counts.update(row["by_rule"])
    return dict(sorted(counts.items()))


def build_summary(
    *,
    rows: list[dict],
    styles: list[str],
    run_name: str,
    thresholds: dict[str, float],
    rule_hashes: dict[str, dict],
    gate_config_hash: dict,
    toolchain: dict,
    run_toolchain: dict | None,
    warnings: list[str],
) -> dict:
    per_style = {}
    for style in styles:
        styled = [r for r in rows if r["style"] == style]
        baseline = [r for r in rows if r["style"] is None and r["rule_set"] == style]
        per_style[style] = {
            "gated": len(styled),
            "passed": sum(1 for r in styled if r["pass"]),
            "failed": sum(1 for r in styled if not r["pass"]),
            "styled_rate": _mean_rate(styled),
            "baseline_rate": _mean_rate(baseline),
        }
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "run": run_name,
        "thresholds": thresholds,
        "summary": per_style,
        "linter_toolchain": toolchain,
        "run_linter_toolchain": run_toolchain,
        "rules": rule_hashes,
        "gate_config": gate_config_hash,
        "warnings": warnings,
    }


def build_fidelity_report(
    rows: list[dict],
    styles: list[str],
    summary: dict,
    failing: dict[tuple[str, str], list],
) -> str:
    lines = [
        "# Fidelity report",
        "",
        "A pair passes the gate when its styled answer has at least one",
        "sentence and a violation rate at or below the threshold of its",
        "style. The baseline columns check the unstyled answers with the",
        "same rules; the baseline carries no mark, because the unstyled",
        "answers are not supposed to obey a style. The judged measurements",
        "read only the passing pairs.",
        "",
    ]

    for style in styles:
        styled = [r for r in rows if r["style"] == style]
        baseline = [r for r in rows if r["style"] is None and r["rule_set"] == style]
        stats = summary["summary"][style]

        lines += [f"## {style}", ""]
        lines += [
            f"- Threshold: {summary['thresholds'][style]} violations per 100 sentences",
            f"- Passing pairs: {stats['passed']}/{stats['gated']}",
            f"- Styled rate: {stats['styled_rate']} per 100 sentences",
            f"- Baseline rate: {stats['baseline_rate']} per 100 sentences",
            "",
        ]

        lines += ["| Rule | Styled | Baseline |", "|---|---|---|"]
        styled_by_rule = _by_rule(styled)
        baseline_by_rule = _by_rule(baseline)
        rules = sorted(set(styled_by_rule) | set(baseline_by_rule))
        if not rules:
            lines.append("| none | 0 | 0 |")
        lines += [
            f"| {rule} | {styled_by_rule.get(rule, 0)} | {baseline_by_rule.get(rule, 0)} |"
            for rule in rules
        ]
        lines.append("")

        failing_rows = [r for r in styled if not r["pass"]]
        if failing_rows:
            lines += ["### Failing pairs", ""]
            for row in failing_rows:
                lines.append(f"- {row['prompt_id']} (rate {row['rate']}):")
                for violation in failing.get((row["prompt_id"], style), []):
                    lines.append(
                        f"  - [{violation.rule}] {violation.match!r}: {violation.sentence}"
                    )
            lines.append("")

    lines += ["## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
