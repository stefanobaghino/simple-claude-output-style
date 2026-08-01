"""Compute the answer-length ratios of a run.

The ratio of a pair is the output-token count of the styled answer
divided by the output-token count of the unstyled answer of the same
prompt. The analysis reads all pairs, gated or not: a token is a token
in any answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median, quantiles


@dataclass
class RatioResult:
    """The per-style ratio blocks plus the warnings of the analysis."""

    per_style: dict[str, dict]
    warnings: list[str]


def task_type(prompt_id: str) -> str:
    """The task type encoded in the prompt id, like "explanation-01"."""
    return prompt_id.rsplit("-", 1)[0]


def distribution(values: list[float]) -> dict:
    ordered = sorted(values)
    if len(ordered) == 1:
        p25 = p50 = p75 = ordered[0]
    else:
        p25, p50, p75 = quantiles(ordered, n=4, method="inclusive")
    return {
        "n": len(ordered),
        "min": round(ordered[0], 2),
        "p25": round(p25, 2),
        "median": round(p50, 2),
        "p75": round(p75, 2),
        "max": round(ordered[-1], 2),
        "mean": round(mean(ordered), 2),
    }


def _by_task_type(ratios: dict[str, float]) -> dict[str, dict]:
    grouped: dict[str, list[float]] = {}
    for prompt_id, ratio in ratios.items():
        grouped.setdefault(task_type(prompt_id), []).append(ratio)
    return {
        name: {
            "n": len(values),
            "min": round(min(values), 2),
            "median": round(median(values), 2),
            "mean": round(mean(values), 2),
            "max": round(max(values), 2),
        }
        for name, values in sorted(grouped.items())
    }


def analyze_ratios(answers: list[dict]) -> RatioResult:
    """The answer-length ratio block per style, over all complete pairs."""
    unstyled = {a["prompt_id"]: a for a in answers if a.get("style") is None}
    styles = sorted({a["style"] for a in answers if a.get("style") is not None})

    warnings: list[str] = []
    per_style: dict[str, dict] = {}
    for style in styles:
        styled = {a["prompt_id"]: a for a in answers if a.get("style") == style}
        ratios: dict[str, float] = {}
        for prompt_id in sorted(styled):
            counterpart = unstyled.get(prompt_id)
            if counterpart is None:
                warnings.append(f"{style}/{prompt_id}: no unstyled counterpart, pair skipped")
                continue
            if not counterpart["output_tokens"]:
                warnings.append(
                    f"{style}/{prompt_id}: the unstyled answer has zero output tokens, pair skipped"
                )
                continue
            ratios[prompt_id] = styled[prompt_id]["output_tokens"] / counterpart["output_tokens"]
        for prompt_id in sorted(set(unstyled) - set(styled)):
            warnings.append(f"{style}/{prompt_id}: no styled answer, pair skipped")

        styled_total = sum(styled[p]["output_tokens"] for p in ratios)
        unstyled_total = sum(unstyled[p]["output_tokens"] for p in ratios)
        per_style[style] = {
            "pairs": len(ratios),
            "styled_output_tokens_total": styled_total,
            "unstyled_output_tokens_total": unstyled_total,
            "ratio_of_totals": round(styled_total / unstyled_total, 2) if unstyled_total else None,
            "distribution": distribution(list(ratios.values())) if ratios else None,
            "by_task_type": _by_task_type(ratios),
        }
    return RatioResult(per_style=per_style, warnings=warnings)
