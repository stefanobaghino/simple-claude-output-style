"""Write the run report.

The report states pair completeness, answer volume, the observed
environment, and warnings. Deeper measurements read the answers file
directly; the report is for a human who opens the run directory.
"""

from __future__ import annotations

from .screening import screening_section
from .spend import spend_section, spend_summary
from .timing import timing_section, timing_summary

UNSTYLED = "unstyled"


def arm_name(style: str | None) -> str:
    return style if style is not None else UNSTYLED


def build_report(
    prompts: list[dict],
    styles: list[str],
    answers: list[dict],
    provenance: dict,
    failures: list[str],
) -> str:
    prompt_ids = [p["id"] for p in prompts]
    arms = [None, *styles]
    by_arm: dict[str, list[dict]] = {arm_name(a): [] for a in arms}
    for answer in answers:
        by_arm.setdefault(arm_name(answer.get("style")), []).append(answer)

    lines = ["# Run report", ""]
    lines += screening_section(provenance)
    lines += [
        f"- Date: {provenance['date']}",
        f"- Model requested: {provenance['conditions']['model_requested']}",
        f"- Prompts: {len(prompt_ids)}",
        f"- Styles: {', '.join(styles)}",
        "",
    ]

    lines += ["## Completeness", "", "| Arm | Answers | Missing |", "|---|---|---|"]
    complete = True
    for arm in arms:
        name = arm_name(arm)
        have = {a["prompt_id"] for a in by_arm[name]}
        missing = [pid for pid in prompt_ids if pid not in have]
        if missing:
            complete = False
        missing_text = ", ".join(missing) if missing else "none"
        lines.append(f"| {name} | {len(have)}/{len(prompt_ids)} | {missing_text} |")
    lines.append("")

    lines += ["## Volume", "", "| Arm | Output tokens | Mean words per answer |", "|---|---|---|"]
    for arm in arms:
        name = arm_name(arm)
        arm_answers = by_arm[name]
        tokens = sum(a.get("output_tokens", 0) for a in arm_answers)
        words = [len(str(a.get("answer", "")).split()) for a in arm_answers]
        mean_words = round(sum(words) / len(words)) if words else 0
        lines.append(f"| {name} | {tokens} | {mean_words} |")
    lines.append("")

    lines += timing_section(timing_summary(answers))
    lines += spend_section(spend_summary(answers))

    versions = sorted({a.get("claude_code_version", "") for a in answers} - {""})
    models = sorted({m for a in answers for m in a.get("models_used", [])})
    plugin_sets = sorted({", ".join(a.get("plugins", [])) for a in answers})
    lines += ["## Environment", ""]
    lines.append(f"- Claude Code versions observed: {', '.join(versions) or 'none'}")
    lines.append(f"- Models observed: {', '.join(models) or 'none'}")
    lines.append("- Plugin sets observed:")
    lines += [f"  - {plugins or 'none'}" for plugins in plugin_sets]
    lines.append("")

    warnings: list[str] = []
    if provenance["repo"].get("dirty"):
        warnings.append(
            "The repository was dirty during the run. The style hashes in the "
            "provenance are authoritative, the commit is not."
        )
    if provenance["repo"].get("commit") is None:
        warnings.append("The repository state was not available.")
    if len(versions) > 1:
        warnings.append("The answers come from more than one Claude Code version.")
    if len(plugin_sets) > 1:
        warnings.append("The answers come from more than one plugin environment.")
    if not complete:
        warnings.append("The pair set is incomplete. Run the same invocation again to resume.")
    warnings += [f"Failed call: {failure}" for failure in failures]

    lines += ["## Warnings", ""]
    lines += [f"- {w}" for w in warnings] or ["- none"]
    lines.append("")
    return "\n".join(lines)
