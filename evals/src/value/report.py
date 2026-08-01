"""Render the value artifacts of a run.

value.json holds the machine-readable summary. value.md is for a
human who opens the run directory. Both are a pure function of the
answers, the gate rows, and the stored judge rows.
"""

from __future__ import annotations

from datetime import UTC, datetime

from .judges import CHECKS

COMPREHENSION_VERDICT = "The styled answer must not score worse than the unstyled answer."

CHECK_TITLES = {
    "comprehension": "Comprehension (weak reader)",
    "paraphrase": "Ambiguity (paraphrase agreement)",
    "roundtrip": "Translation round-trip",
}

CHECK_INTROS = {
    "comprehension": (
        "The grader model writes questions with reference answers from the "
        "task prompt alone, so the questions cannot favor an arm. The weak "
        "reader answers the questions from one answer text only, and the "
        "grader marks each reader answer against the reference. The score "
        "is the fraction of questions correct: an answer that drops "
        "content loses questions, so a short answer wins only when the "
        "content survives. Higher is better."
    ),
    "paraphrase": (
        "Independent reader calls restate one answer text in their own "
        "words. The score is the mean pairwise lexical similarity between "
        "the restatements: when the readers agree on what the text says, "
        "the text is less ambiguous. Higher is better."
    ),
    "roundtrip": (
        "One call translates the answer to another language, and a second "
        "call translates the result back to English. The score is the "
        "lexical loss between the original and the round-trip: simpler "
        "text survives the round-trip with less loss. Lower is better."
    ),
}


def build_value_summary(
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
        "judges": {
            "models": meta["models"],
            "questions": meta["questions"],
            "paraphrases": meta["paraphrases"],
            "language": meta["language"],
            "judged_date": meta["date"],
            "claude_version": meta.get("claude_version"),
        },
        "pairs": pairs,
        "checks": checks,
        "warnings": warnings,
    }


def _check_section(name: str, check: dict, run_name: str) -> list[str]:
    lines = [f"## {CHECK_TITLES[name]}", "", CHECK_INTROS[name], ""]
    if not check["judged"]:
        lines += [f"The check is not judged. Run `style-value {run_name} --judge`.", ""]
        return lines

    lines += ["| Style | Wins | Losses | Ties |", "|---|---|---|---|"]
    for style, stats in check["per_style"].items():
        lines.append(f"| {style} | {stats['wins']} | {stats['losses']} | {stats['ties']} |")
    lines.append("")

    if name == "comprehension":
        lines += [COMPREHENSION_VERDICT]
        for style, stats in check["per_style"].items():
            held = stats["losses"] <= stats["wins"]
            verdict = "holds" if held else "scores worse"
            lines.append(
                f"- {style}: the styled answer {verdict} "
                f"({stats['wins']} wins, {stats['losses']} losses, {stats['ties']} ties)."
            )
        lines.append("")

    for style, stats in check["per_style"].items():
        lines += [
            f"### {style}",
            "",
            "| Pair | Styled | Unstyled | Result |",
            "|---|---|---|---|",
        ]
        lines += [
            f"| {prompt_id} | {scores['styled']} | {scores['unstyled']} | {scores['result']} |"
            for prompt_id, scores in stats["pairs"].items()
        ]
        lines.append("")
    return lines


def build_value_report(summary: dict) -> str:
    judges = summary["judges"]
    lines = [
        "# Reader-value report",
        "",
        "The checks compare the styled answer with the unstyled answer of",
        "the same prompt, pair by pair, as win, loss, or tie. Only pairs",
        "whose styled answer passes the fidelity gate enter the checks.",
        "Each judge call sees one bare text: no style name, no arm label,",
        "and never both answers. Thus a judge cannot know which answer is",
        "styled. The judge models differ from the writer of the answers.",
        "",
        (
            f"Judges: reader {judges['models']['reader']}, "
            f"grader {judges['models']['grader']}. "
            f"Comprehension uses {judges['questions']} questions per prompt, "
            f"ambiguity uses {judges['paraphrases']} restatements per answer, "
            f"and the round-trip goes through {judges['language']}. "
            f"Judged on {judges['judged_date']}."
        ),
        "",
    ]

    for name in CHECKS:
        lines += _check_section(name, summary["checks"][name], summary["run"])

    lines += ["## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
