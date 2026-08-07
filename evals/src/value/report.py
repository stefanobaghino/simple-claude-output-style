"""Render the value artifacts of a run.

value.json holds the machine-readable summary. value.md is for a
human who opens the run directory. Both are a pure function of the
answers, the gate rows, and the stored judge rows.
"""

from __future__ import annotations

from datetime import UTC, datetime

from runner.spend import spend_section
from runner.timing import timing_section

from .judges import CHECKS

COMPREHENSION_VERDICT = "The styled answer must not score worse than the unstyled answer."

CHECK_TITLES = {
    "comprehension": "Comprehension (weak reader)",
    "paraphrase": "Ambiguity (paraphrase agreement)",
    "roundtrip": "Translation round-trip",
}

COMPREHENSION_V2_INTRO = (
    "The questions come from the shared facts of the pair: the facts "
    "that the loss judge extracted from the unstyled answer and found "
    "present in the styled answer. A grader call turns each fact into "
    "one question, and the fact is the reference answer. The weak "
    "reader answers the questions from one answer text, once per "
    "replicate, and the grader marks every reply. Each styled "
    "replicate meets each unstyled replicate as a win, a loss, or a "
    "tie, and the pair outcome is the strict plurality, else a tie. "
    "The agreement is the plurality share, and the buried-fact rate "
    'counts styled "NOT IN TEXT" replies to a shared fact. The check '
    "measures extraction over shared material. Absence belongs to the "
    "content-loss report. Higher is better."
)

COMPREHENSION_V3_INTRO = (
    "The questions come from the shared facts of the pair, mined in "
    "both directions: the facts of the unstyled answer that survive "
    "in the styled answer, and the facts of the styled answer that "
    "the unstyled answer also states. The quiz takes half of its "
    "questions from each wording, so neither answer sets the phrasing "
    "alone, and the Sources column counts the questions per wording "
    "(unstyled/styled). A grader call turns each fact into one "
    "question, and the fact is the reference answer. The weak reader "
    "answers the questions from one answer text, once per replicate, "
    "and the grader marks every reply. Each styled replicate meets "
    "each unstyled replicate as a win, a loss, or a tie, and the pair "
    "outcome is the strict plurality, else a tie. The agreement is "
    "the plurality share, and the buried-fact rate counts "
    '"NOT IN TEXT" replies to a shared fact, per arm. The check '
    "measures extraction over shared material. Absence belongs to the "
    "content-loss report. Higher is better."
)

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

LENGTH_CONFOUND_NOTE = (
    "The length confound is the correlation between the length ratio of "
    "a pair (styled words over unstyled words) and the styled advantage "
    "(the score gain of the styled arm). A negative value means that "
    "the shorter styled answers score better."
)


def build_value_summary(
    *,
    run_name: str,
    meta: dict,
    pairs: dict[str, list[str]],
    checks: dict[str, dict],
    warnings: list[str],
    models_resolved: dict | None = None,
) -> dict:
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "run": run_name,
        "judges": {
            "models": meta["models"],
            "models_resolved": models_resolved,
            "questions": meta["questions"],
            "paraphrases": meta["paraphrases"],
            "replicates": meta.get("replicates"),
            "comprehension_design": meta.get("comprehension_design"),
            "language": meta["language"],
            "judged_date": meta["date"],
            "claude_version": meta.get("claude_version"),
        },
        "pairs": pairs,
        "checks": checks,
        "warnings": warnings,
    }


def _sources(scores: dict) -> str:
    sources = scores.get("sources")
    if not sources:
        return "n/a"
    return f"{sources['unstyled']}/{sources['styled']}"


def _correlation_value(value: float | None) -> str:
    return "not computable" if value is None else str(value)


def _check_section(name: str, check: dict, run_name: str) -> list[str]:
    design = check.get("design")
    v3 = design == "balanced-facts-v3"
    if v3:
        intro = COMPREHENSION_V3_INTRO
    elif design is not None:
        intro = COMPREHENSION_V2_INTRO
    else:
        intro = CHECK_INTROS[name]
    lines = [f"## {CHECK_TITLES[name]}", "", intro, ""]
    if not check["judged"]:
        lines += [f"The check is not judged. Run `style-value {run_name} --judge`.", ""]
        return lines

    if v3:
        lines += [
            (
                "| Style | Wins | Losses | Ties | Mean delta | Agreement "
                "| Buried (styled) | Buried (unstyled) |"
            ),
            "|---|---|---|---|---|---|---|---|",
        ]
        for style, stats in check["per_style"].items():
            lines.append(
                f"| {style} | {stats['wins']} | {stats['losses']} | {stats['ties']} | "
                f"{stats['mean_delta']} | {stats['mean_agreement']} | "
                f"{stats['buried_fact_rate']} | {stats['buried_fact_rate_unstyled']} |"
            )
    elif design is not None:
        lines += [
            "| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried-fact rate |",
            "|---|---|---|---|---|---|---|",
        ]
        for style, stats in check["per_style"].items():
            lines.append(
                f"| {style} | {stats['wins']} | {stats['losses']} | {stats['ties']} | "
                f"{stats['mean_delta']} | {stats['mean_agreement']} | "
                f"{stats['buried_fact_rate']} |"
            )
    else:
        lines += ["| Style | Wins | Losses | Ties |", "|---|---|---|---|"]
        for style, stats in check["per_style"].items():
            lines.append(f"| {style} | {stats['wins']} | {stats['losses']} | {stats['ties']} |")
        lines += ["", LENGTH_CONFOUND_NOTE]
        for style, stats in check["per_style"].items():
            corr = stats.get("length_correlation")
            if corr is None:
                continue
            noun = "pair" if corr["n"] == 1 else "pairs"
            lines.append(
                f"- {style}: Pearson {_correlation_value(corr['pearson'])}, "
                f"Spearman {_correlation_value(corr['spearman'])}, over {corr['n']} {noun}."
            )
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
        lines += [f"### {style}", ""]
        if v3:
            lines += [
                "| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |",
                "|---|---|---|---|---|---|---|",
            ]
            lines += [
                f"| {prompt_id} | {scores['questions']} | {_sources(scores)} | "
                f"{scores['styled']} | {scores['unstyled']} | {scores['agreement']} | "
                f"{scores['result']} |"
                for prompt_id, scores in stats["pairs"].items()
            ]
        elif design is not None:
            lines += [
                "| Pair | Questions | Styled | Unstyled | Agreement | Result |",
                "|---|---|---|---|---|---|",
            ]
            lines += [
                f"| {prompt_id} | {scores['questions']} | {scores['styled']} | "
                f"{scores['unstyled']} | {scores['agreement']} | {scores['result']} |"
                for prompt_id, scores in stats["pairs"].items()
            ]
        else:
            lines += [
                "| Pair | Styled | Unstyled | Result |",
                "|---|---|---|---|",
            ]
            lines += [
                f"| {prompt_id} | {scores['styled']} | {scores['unstyled']} | {scores['result']} |"
                for prompt_id, scores in stats["pairs"].items()
            ]
        lines.append("")
    return lines


def _comprehension_header(judges: dict) -> str:
    design = judges.get("comprehension_design")
    if design == "balanced-facts-v3":
        return (
            f"Comprehension asks up to {judges['questions']} questions per pair, "
            "worded by both answers in balance, "
            f"with {judges['replicates']} reader replicates per answer, "
        )
    if design:
        return (
            f"Comprehension asks up to {judges['questions']} questions per pair, "
            f"with {judges['replicates']} reader replicates per answer, "
        )
    return f"Comprehension uses {judges['questions']} questions per prompt, "


def build_value_report(
    summary: dict,
    timing: dict | None = None,
    spend: dict | None = None,
    screening: list[str] | None = None,
) -> str:
    judges = summary["judges"]
    lines = [
        "# Reader-value report",
        "",
        *(screening or []),
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
            + _comprehension_header(judges)
            + f"ambiguity uses {judges['paraphrases']} restatements per answer, "
            f"and the round-trip goes through {judges['language']}. "
            f"Judged on {judges['judged_date']}."
        ),
        "",
    ]

    for name in CHECKS:
        lines += _check_section(name, summary["checks"][name], summary["run"])

    lines += timing_section(timing)
    lines += spend_section(spend)
    lines += ["## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
