"""Render the clarity-ranking artifacts of a run.

rank.json holds the machine-readable summary. rank.md is for a human
who opens the run directory. Both are a pure function of the schedule
and the stored judge rows.
"""

from __future__ import annotations

from datetime import UTC, datetime

from runner.spend import spend_section
from runner.timing import timing_section

PROXY_NOTE = (
    "The judge is a proxy reader: the picks state a model preference "
    "for clarity, not a measured human outcome."
)

UNGATED_NOTE = (
    "The unstyled competitor is ungated: every styled competitor "
    "passed its rule gate, and the unstyled answer has no gate."
)

LENGTH_NOTE = (
    "A clarity pick can reward the shorter text. The length-confound "
    "section states the correlation."
)


def build_rank_summary(
    *,
    run_name: str,
    meta: dict,
    result,
    warnings: list[str],
    model_resolved: object = None,
) -> dict:
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "run": run_name,
        "judge": {
            "model": meta["model"],
            "model_resolved": model_resolved,
            "judged_date": meta["date"],
            "claude_version": meta.get("claude_version"),
        },
        "design": meta["design"],
        "competitors": result.competitors,
        "matchups": result.matchups,
        "win_matrix": result.win_matrix,
        "position_bias": result.position_bias,
        "bradley_terry": result.bradley_terry,
        "by_task_type": result.by_task_type,
        "length_confound": result.length_confound,
        "warnings": warnings,
    }


def _value(value) -> str:
    return "n/a" if value is None else str(value)


def _matchup_table(matchups: list[dict]) -> list[str]:
    lines = [
        "| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    lines += [
        f"| {m['a']} | {m['b']} | {m['contests']} | {m['wins_a']} | {m['wins_b']} "
        f"| {m['splits']} | {m['unscored']} | {m['net']} |"
        for m in matchups
    ]
    return lines


def _win_matrix_section(competitors: list[str], matrix: dict[str, dict[str, float]]) -> list[str]:
    lines = [
        "## Win matrix",
        "",
        "A cell holds the points of the row competitor against the column",
        "competitor: 1 per decisive win plus 0.5 per split.",
        "",
        "| | " + " | ".join(competitors) + " |",
        "|---|" + "---|" * len(competitors),
    ]
    for name in competitors:
        cells = ["-" if other == name else _value(matrix[name][other]) for other in competitors]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines.append("")
    return lines


def _bradley_terry_section(block: dict) -> list[str]:
    lines = ["## Bradley-Terry strengths", ""]
    if not block["fitted"]:
        lines += [f"The layer is dormant: {block['note']}.", ""]
        return lines
    if block["anchored_on"] is None:
        lines += [
            "No competitor anchors the scale; the strengths are scaled by",
            "their geometric mean.",
            "",
        ]
    else:
        lines += [f"The scale is anchored on {block['anchored_on']} at strength 1.0.", ""]
    lines += ["| Competitor | Strength | 95% CI |", "|---|---|---|"]
    for name, entry in block["strengths"].items():
        if entry["ci_low"] is None:
            interval = "n/a"
        else:
            interval = f"[{entry['ci_low']}, {entry['ci_high']}]"
        lines.append(f"| {name} | {_value(entry['strength'])} | {interval} |")
    bootstrap = block["bootstrap"]
    lines += [
        "",
        (
            f"The interval comes from {bootstrap['resamples']} bootstrap resamples "
            f"of the scored contests (seed {bootstrap['seed']})."
        ),
        "",
    ]
    return lines


def _position_bias_section(bias: dict) -> list[str]:
    return [
        "## Position bias",
        "",
        f"First-pick rate: {_value(bias['first_pick_rate'])} over {bias['picks']} usable picks.",
        f"Split rate: {_value(bias['split_rate'])} over {bias['contests']} judged contests.",
        "",
    ]


def _task_type_section(by_task_type: dict[str, list[dict]]) -> list[str]:
    lines = ["## Per task type", ""]
    if not by_task_type:
        lines += ["No contest is scheduled.", ""]
        return lines
    for name, matchups in by_task_type.items():
        lines += [f"### {name}", "", *_matchup_table(matchups), ""]
    return lines


def _length_section(confound: dict) -> list[str]:
    return [
        "## Length confound",
        "",
        f"Samples: {confound['n']} contests with unequal word counts.",
        f"Pearson: {_value(confound['pearson'])}. Spearman: {_value(confound['spearman'])}.",
        f"Longer-text win rate: {_value(confound['longer_win_rate'])}.",
        "",
    ]


def build_rank_report(
    summary: dict,
    timing: dict | None = None,
    spend: dict | None = None,
    screening: list[str] | None = None,
) -> str:
    judge = summary["judge"]
    lines = [
        "# Clarity-ranking report",
        "",
        *(screening or []),
        "Every contest shows a blind judge the two answers of one prompt,",
        "in both orders, and the judge picks the clearer text. This tool",
        "relaxes one harness invariant on purpose: a clarity contest is a",
        "choice, so a judge call sees both answers of a prompt side by",
        "side. Blindness holds through the absence of labels: no prompt",
        "names a style or an arm, and the position mapping lives only in",
        "the raw rows. The judge model differs from the writer of the",
        "answers. The unstyled answer competes as its own arm and anchors",
        "the strength scale.",
        "",
        "Caveats:",
        "",
        f"- {PROXY_NOTE}",
        f"- {UNGATED_NOTE}",
        f"- {LENGTH_NOTE}",
        "",
        f"Judge: {judge['model']}. Judged on {judge['judged_date']}.",
        "",
        "## Matchups",
        "",
        *_matchup_table(summary["matchups"]),
        "",
    ]
    lines += _win_matrix_section(summary["competitors"], summary["win_matrix"])
    lines += _bradley_terry_section(summary["bradley_terry"])
    lines += _position_bias_section(summary["position_bias"])
    lines += _task_type_section(summary["by_task_type"])
    lines += _length_section(summary["length_confound"])
    lines += timing_section(timing)
    lines += spend_section(spend)
    lines += ["## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
