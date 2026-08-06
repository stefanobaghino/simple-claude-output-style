"""Render the cost artifacts of a run.

cost.json holds the machine-readable summary. cost.md is for a human
who opens the run directory. Both are a pure function of the answers
and the stored probe data.
"""

from __future__ import annotations

from datetime import UTC, datetime
from statistics import fmean

from runner.spend import spend_section

from .probe import PRICE_WEIGHTS, overhead_stats

SHORTNESS_WARNING = (
    "A lower ratio is not by itself a win: fewer tokens with less "
    "content is a loss. Issue #7 measures whether the content survives."
)


def _overhead_block(probe: dict | None, styles: list[str]) -> dict:
    if probe is None:
        return {
            "measured": False,
            "per_style": None,
            "probe_date": None,
            "probe_model": None,
            "repeats": None,
            "price_weights": None,
        }
    arms = probe["arms"]
    unstyled_totals = [arm["total_input_tokens"] for arm in arms if arm["arm"] == "unstyled"]
    per_style = {}
    for style, stats in overhead_stats(arms, styles).items():
        styled_totals = [arm["total_input_tokens"] for arm in arms if arm["arm"] == style]
        per_style[style] = {
            "tokens": stats["tokens"],
            "weighted": stats["weighted"],
            "styled_input_total_mean": round(fmean(styled_totals), 3),
            "unstyled_input_total_mean": round(fmean(unstyled_totals), 3),
        }
    return {
        "measured": True,
        "per_style": per_style,
        "probe_date": probe["date"],
        "probe_model": probe["model_requested"],
        "repeats": probe.get("repeats") or len(unstyled_totals),
        "price_weights": dict(PRICE_WEIGHTS),
    }


def build_cost_summary(
    *,
    run_name: str,
    per_style: dict[str, dict],
    probe: dict | None,
    warnings: list[str],
) -> dict:
    styles = sorted(per_style)
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "run": run_name,
        "answer_ratio": {"per_style": per_style},
        "input_overhead": _overhead_block(probe, styles),
        "warnings": warnings,
    }


def _mean_spread(stats: dict) -> str:
    if stats["stdev"] is None:
        return f"{stats['mean']} (n = {stats['n']})"
    return f"{stats['mean']} ± {stats['stdev']}"


def build_cost_report(summary: dict, spend: dict | None = None) -> str:
    per_style = summary["answer_ratio"]["per_style"]
    overhead = summary["input_overhead"]
    styles = sorted(per_style)

    lines = [
        "# Token cost report",
        "",
        "A style costs tokens in two ways: the style block adds a fixed",
        "quantity of input tokens to every request, and the style changes",
        "the answer length. The report states both numbers per style. The",
        "report reads all pairs of the run, gated or not.",
        "",
        "## Input overhead per request",
        "",
    ]

    if overhead["measured"]:
        weights = overhead["price_weights"]
        lines += [
            "The overhead is the difference in input context tokens between",
            "a styled probe call and an unstyled probe call of the same",
            "repeat. Both probe arms load the plugin, so the difference",
            "isolates the style block. The weighted overhead multiplies each",
            "token count by its price ratio against one uncached input token",
            (
                f"(uncached {weights['input_tokens']}, cache write "
                f"{weights['cache_creation_input_tokens']}, cache read "
                f"{weights['cache_read_input_tokens']}), so the unit is"
            ),
            "uncached-token equivalents.",
            "",
            "| Style | Overhead tokens (mean ± stdev) | Weighted overhead (mean ± stdev) |",
            "|---|---|---|",
        ]
        lines += [
            f"| {style} | {_mean_spread(stats['tokens'])} | {_mean_spread(stats['weighted'])} |"
            for style, stats in overhead["per_style"].items()
        ]
        lines += [
            "",
            (
                f"Probe: {overhead['probe_date']}, model {overhead['probe_model']}, "
                f"repeats {overhead['repeats']}."
            ),
            "",
        ]
    else:
        lines += [
            "The overhead is not measured. Run `style-cost <run> --probe`",
            "to measure it with live probe calls.",
            "",
        ]

    if spend is not None:
        lines += spend_section(spend)

    lines += [
        "## Answer-length ratio",
        "",
        "The ratio of a pair is the output-token count of the styled",
        "answer divided by the output-token count of the unstyled answer",
        "of the same prompt. A ratio below 1 means a shorter styled",
        "answer.",
        "",
    ]

    for style in styles:
        stats = per_style[style]
        lines += [f"### {style}", ""]
        if stats["distribution"] is None:
            lines += ["No complete pair exists for this style.", ""]
            continue
        lines += [
            f"- Pairs: {stats['pairs']}",
            (
                f"- Output tokens: styled {stats['styled_output_tokens_total']}, "
                f"unstyled {stats['unstyled_output_tokens_total']}, "
                f"ratio of totals {stats['ratio_of_totals']}"
            ),
            "",
            "| n | min | p25 | median | p75 | max | mean |",
            "|---|---|---|---|---|---|---|",
        ]
        d = stats["distribution"]
        lines += [
            (
                f"| {d['n']} | {d['min']} | {d['p25']} | {d['median']} "
                f"| {d['p75']} | {d['max']} | {d['mean']} |"
            ),
            "",
            "| Task type | n | min | median | mean | max |",
            "|---|---|---|---|---|---|",
        ]
        lines += [
            f"| {name} | {t['n']} | {t['min']} | {t['median']} | {t['mean']} | {t['max']} |"
            for name, t in stats["by_task_type"].items()
        ]
        lines.append("")

    lines += [
        "## Reading the ratio",
        "",
        SHORTNESS_WARNING,
        "",
        "## Warnings",
        "",
    ]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- none"]
    lines.append("")
    return "\n".join(lines)
