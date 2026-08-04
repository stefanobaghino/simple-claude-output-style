"""Render the content-loss artifacts of a run.

loss.json holds the machine-readable summary. loss.md is for a human
who opens the run directory. Both are a pure function of the answers,
the gate rows, and the stored judge rows.
"""

from __future__ import annotations

from datetime import UTC, datetime

from .judges import CHECKS

CHECK_TITLES = {
    "completeness": "Completeness (fact survival)",
    "hedging": "Hedging survival",
}

CHECK_INTROS = {
    "completeness": (
        "The judge lists the facts of the unstyled answer, then checks "
        "each fact against the styled answer. The fraction is the share "
        "of the facts that survive. The judge also lists the facts of "
        "the styled answer and checks each fact against the unstyled "
        "answer: a styled fact that the unstyled answer does not state "
        "is an addition. The lost facts and the added facts appear "
        "verbatim below the table."
    ),
    "hedging": (
        "The judge lists the claims that the unstyled answer presents "
        "with uncertainty, then judges each claim in the styled answer: "
        "hedged (the uncertainty survives in some form), certain (the "
        "claim survives but reads as a fact — the failure this check "
        "targets), or absent (the claim is gone, a completeness loss). "
        "Survival is hedged / (hedged + certain). The claims that became "
        "certain appear verbatim below the table."
    ),
}


def build_loss_summary(
    *,
    run_name: str,
    meta: dict,
    pairs: dict[str, list[str]],
    checks: dict[str, dict],
    warnings: list[str],
) -> dict:
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "run": run_name,
        "judge": {
            "model": meta["model"],
            "judged_date": meta["date"],
            "claude_version": meta.get("claude_version"),
        },
        "pairs": pairs,
        "checks": checks,
        "warnings": warnings,
    }


def _fraction(value: float | None) -> str:
    return "n/a" if value is None else str(value)


def _completeness_section(stats: dict) -> list[str]:
    two_way = any("additions" in entry for entry in stats["pairs"].values())
    if two_way:
        lines = [
            "| Pair | Facts | Survived | Fraction | Styled facts | Additions |",
            "|---|---|---|---|---|---|",
        ]
        lines += [
            f"| {prompt_id} | {entry['facts']} | {entry['survived']} "
            f"| {_fraction(entry['fraction'])} | {_fraction(entry['styled_facts'])} "
            f"| {_fraction(entry['additions'])} |"
            for prompt_id, entry in stats["pairs"].items()
        ]
    else:
        lines = ["| Pair | Facts | Survived | Fraction |", "|---|---|---|---|"]
        lines += [
            f"| {prompt_id} | {entry['facts']} | {entry['survived']} "
            f"| {_fraction(entry['fraction'])} |"
            for prompt_id, entry in stats["pairs"].items()
        ]
    lines.append("")
    lines += _median_line(stats, "fraction")
    if two_way:
        lines += _additions_median_line(stats)
    lines += _lost_lines(stats, "lost", "Lost facts:", "No pair lost a fact.")
    if two_way:
        lines += _lost_lines(
            stats, "added", "Added facts (styled only):", "No styled answer adds a fact."
        )
    return lines


def _hedging_section(stats: dict) -> list[str]:
    lines = [
        "| Pair | Claims | Hedged | Certain | Absent | Survival |",
        "|---|---|---|---|---|---|",
    ]
    lines += [
        f"| {prompt_id} | {entry['claims']} | {entry['hedged']} | {entry['certain']} "
        f"| {entry['absent']} | {_fraction(entry['survival'])} |"
        for prompt_id, entry in stats["pairs"].items()
    ]
    lines.append("")
    lines += _median_line(stats, "survival")
    lines += _lost_lines(stats, "lost", "Claims that became certain:", "No claim became certain.")
    return lines


def _median_line(stats: dict, score_key: str) -> list[str]:
    if stats["median"] is None:
        return [f"No pair has a {score_key} score.", ""]
    scored = sum(1 for entry in stats["pairs"].values() if entry[score_key] is not None)
    return [f"Median {score_key}: {stats['median']} over {scored} scored pairs.", ""]


def _additions_median_line(stats: dict) -> list[str]:
    if stats["additions_median"] is None:
        return ["No pair has an additions count.", ""]
    scored = sum(1 for entry in stats["pairs"].values() if entry["additions"] is not None)
    return [f"Median additions: {stats['additions_median']} over {scored} scored pairs.", ""]


def _lost_lines(stats: dict, key: str, title: str, empty: str) -> list[str]:
    items = [
        f"- {prompt_id}: {item}"
        for prompt_id, entry in stats["pairs"].items()
        for item in entry.get(key, [])
    ]
    if not items:
        return [empty, ""]
    return [title, "", *items, ""]


def _check_section(name: str, check: dict, run_name: str) -> list[str]:
    lines = [f"## {CHECK_TITLES[name]}", "", CHECK_INTROS[name], ""]
    if not check["judged"]:
        lines += [f"The check is not judged. Run `style-loss {run_name} --judge`.", ""]
        return lines
    sections = {"completeness": _completeness_section, "hedging": _hedging_section}
    for style, stats in check["per_style"].items():
        lines += [f"### {style}", ""]
        lines += sections[name](stats)
    return lines


def build_loss_report(summary: dict) -> str:
    judge = summary["judge"]
    lines = [
        "# Content-loss report",
        "",
        "The checks measure what a rewrite loses relative to the unstyled",
        "answer of the same prompt, per gated pair. The judge extracts the",
        "facts and the uncertain claims from the unstyled answer, then",
        "checks each item against the styled answer. No judge call sees",
        "both answers of a pair: the extracted items travel between the",
        "calls, never the source text. No prompt names a style or an arm,",
        "and the judge model differs from the writer of the answers.",
        "",
        "The unstyled answer is the reference, not a gold standard. A fact",
        "that the unstyled answer omits is invisible to these checks, and",
        "survival measures loss against that baseline, not correctness.",
        "",
        f"Judge: {judge['model']}. Judged on {judge['judged_date']}.",
        "",
    ]

    for name in CHECKS:
        lines += _check_section(name, summary["checks"][name], summary["run"])

    lines += ["## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
