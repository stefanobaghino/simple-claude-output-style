"""Render the compare artifacts.

compare.json holds the machine-readable summary. compare.md is for a
human who opens the compare directory. Both are a pure function of
the stored run artifacts.
"""

from __future__ import annotations

from datetime import UTC, datetime

COMPARE_INTRO = (
    "The comparison reads the stored artifacts of several runs with "
    "identical conditions. Per style and axis, the table states one "
    "value per run and the spread: minimum, mean, maximum, and the "
    "sample standard deviation. The spread is the error bar of the "
    "harness: it shows how much a verdict moves on a resample. Net "
    "wins is wins minus losses, and n counts the runs that hold a "
    "value for the axis."
)


def build_compare_summary(
    *,
    run_names: list[str],
    styles: dict[str, dict[str, dict]],
    warnings: list[str],
) -> dict:
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "runs": run_names,
        "axes": styles,
        "warnings": warnings,
    }


def _cell(value: object) -> str:
    return "n/a" if value is None else str(value)


def build_compare_report(summary: dict) -> str:
    runs = summary["runs"]
    lines = [
        "# Cross-run comparison",
        "",
        COMPARE_INTRO,
        "",
        f"Runs: {', '.join(runs)}.",
        "",
    ]
    for style, axes in summary["axes"].items():
        lines += [
            f"## {style}",
            "",
            "| Axis | " + " | ".join(runs) + " | n | Min | Mean | Max | Stdev |",
            "|---|" + "---|" * (len(runs) + 5),
        ]
        for axis, spread in axes.items():
            cells = [_cell(spread["per_run"].get(run)) for run in runs]
            cells += [
                str(spread["n"]),
                _cell(spread["min"]),
                _cell(spread["mean"]),
                _cell(spread["max"]),
                _cell(spread["stdev"]),
            ]
            lines.append(f"| {axis} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
