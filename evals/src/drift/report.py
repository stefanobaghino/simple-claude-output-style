"""Build the drift summary and the drift report."""

from __future__ import annotations

from datetime import UTC, datetime

HEADER = """\
# Drift report

Run: {run}

The report measures rule obedience across long sessions. A session is
{turns} scripted turns in one Claude Code session, with the style
active. Each turn resumes the session of the previous turn, so the
context grows. Each session runs {repeats} time(s), and each repeat
rotates the prompt order, so a hard prompt does not always sit at the
same turn position. The linter checks each answer with the rule set
of the style. The verdict compares the slope of the mean rate series
against the threshold: "growing" when the slope is more than
{threshold} violations per 100 sentences per turn, else "flat".
"""


def build_drift_summary(
    *,
    run_name: str,
    turns: int,
    repeats: int,
    slope_threshold: float,
    styles: dict[str, dict],
    rules: dict[str, dict],
    toolchain: dict,
    run_toolchain: dict | None,
    warnings: list[str],
) -> dict:
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "run": run_name,
        "turns": turns,
        "repeats": repeats,
        "slope_threshold": slope_threshold,
        "styles": styles,
        "rules": rules,
        "linter_toolchain": toolchain,
        "run_linter_toolchain": run_toolchain,
        "warnings": warnings,
    }


def _rate(value: float | None) -> str:
    return "-" if value is None else f"{value:.2f}"


def _style_section(style: str, stats: dict, summary: dict) -> list[str]:
    lines = [f"## {style}", ""]
    repeats = summary["repeats"]
    if stats["complete_sessions"] == 0:
        lines += ["The style has no complete session, so the style has no verdict.", ""]
        return lines
    lines += [
        f"- Sessions: {stats['complete_sessions']}/{repeats} complete",
        f"- Slope of the mean series: {stats['slope']} violations per 100 sentences per turn",
        f"- Slope threshold: {summary['slope_threshold']}",
        f"- Verdict: {stats['verdict']}",
        "",
    ]
    by_repeat = {session["repeat"]: session["series"] for session in stats["sessions"]}
    header = ["Turn", "Mean rate"] + [f"Repeat {repeat}" for repeat in range(1, repeats + 1)]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "---|" * len(header))
    for index in range(summary["turns"]):
        cells = [str(index + 1), _rate(stats["mean_series"][index])]
        for repeat in range(1, repeats + 1):
            series = by_repeat.get(repeat)
            cells.append(_rate(series[index]) if series is not None else "-")
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return lines


def build_drift_report(summary: dict) -> str:
    lines = [
        HEADER.format(
            run=summary["run"],
            turns=summary["turns"],
            repeats=summary["repeats"],
            threshold=summary["slope_threshold"],
        )
    ]
    for style in sorted(summary["styles"]):
        lines += _style_section(style, summary["styles"][style], summary)
    lines.append("## Warnings")
    lines.append("")
    if summary["warnings"]:
        lines += [f"- {warning}" for warning in summary["warnings"]]
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)
