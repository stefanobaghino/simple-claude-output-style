"""Measure the fixed input overhead of each style with a live probe.

The overhead is not derivable from a stored run, so the probe runs a
minimal prompt through the same CLI path as the runner. One repeat is
one cycle of arms: unstyled, then one arm per style. The probe runs
several repeats, so the overhead per style is a mean with a spread,
not a point. Both arms load the plugin, so the difference between a
styled arm and the unstyled arm of the same repeat isolates the style
block alone, not plugin loading. This is the one place where an
unstyled call loads the plugin; the unstyled arm of the runner does
not.
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from statistics import fmean, stdev

from runner.generate import (
    ISOLATION_FLAGS,
    GenerationError,
    Runner,
    parse_events,
    style_reference,
    subprocess_runner,
)
from runner.provenance import claude_version, sha256_of

PROBE_PROMPT = "Reply with the word OK."

USAGE_FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")

# The price of each token kind, as a ratio against one uncached input
# token: a cache write costs 1.25 and a cache read costs 0.1. The
# weighted overhead is thus in uncached-token equivalents, so the
# number holds under any absolute price.
PRICE_WEIGHTS = {
    "input_tokens": 1.0,
    "cache_creation_input_tokens": 1.25,
    "cache_read_input_tokens": 0.1,
}

PROBE_NOTE = (
    "Both probe arms load the plugin through --plugin-dir, unlike the "
    "unstyled arm of the runner. Thus the difference between a styled "
    "arm and the unstyled arm isolates the style block."
)


def _plugin_name(plugin_dir: Path) -> str:
    manifest = json.loads(
        (plugin_dir / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    return manifest["name"]


def probe_argv(prompt: str, model: str, style: str | None, plugin_dir: Path) -> list[str]:
    """The claude invocation for one probe arm. Every arm loads the plugin."""
    settings = {
        "disableAllHooks": True,
        "outputStyle": style_reference(plugin_dir, style) if style is not None else "default",
    }
    argv = ["claude", "-p", prompt, "--model", model]
    argv += ["--plugin-dir", str(plugin_dir)]
    argv += ["--settings", json.dumps(settings)]
    argv += list(ISOLATION_FLAGS)
    return argv


def _run_arm(
    name: str,
    style: str | None,
    repeat: int,
    model: str,
    plugin_dir: Path,
    workdir: Path,
    run: Runner,
) -> dict:
    start = time.monotonic()
    stdout = run(probe_argv(PROBE_PROMPT, model, style, plugin_dir), workdir)
    wall_ms = round((time.monotonic() - start) * 1000)
    init, result = parse_events(stdout)

    expected = style_reference(plugin_dir, style) if style is not None else "default"
    active = init.get("output_style")
    if active != expected:
        raise GenerationError(
            f"{name}: expected output style {expected!r}, but {active!r} was active"
        )
    if result.get("is_error"):
        raise GenerationError(
            f"{name}: claude reported an error: {str(result.get('result', ''))[:500]}"
        )
    usage = result.get("usage") or {}
    missing = [field for field in USAGE_FIELDS if field not in usage]
    if missing:
        raise GenerationError(
            f"{name}: the usage carries no {', '.join(missing)}; present keys: {sorted(usage)}"
        )

    arm = {
        "arm": name,
        "repeat": repeat,
        "output_style_active": active,
        "model": str(init.get("model", "")),
    }
    for field in USAGE_FIELDS:
        arm[field] = int(usage[field])
    arm["total_input_tokens"] = sum(arm[field] for field in USAGE_FIELDS)
    if arm["total_input_tokens"] == 0:
        raise GenerationError(
            f"{name}: the usage reports zero input tokens, so the reading is invalid"
        )
    arm["output_tokens"] = int(usage.get("output_tokens", 0))
    arm["duration_ms"] = int(result.get("duration_ms", 0))
    arm["wall_ms"] = wall_ms
    return arm


def _stats(values: list) -> dict:
    """Min, mean, max, and sample standard deviation over the repeats."""
    return {
        "n": len(values),
        "per_repeat": values,
        "min": round(min(values), 3),
        "mean": round(fmean(values), 3),
        "max": round(max(values), 3),
        "stdev": round(stdev(values), 3) if len(values) >= 2 else None,
    }


def weighted_total(arm: dict) -> float:
    """The input total of one arm in uncached-token equivalents."""
    return round(sum(arm[field] * PRICE_WEIGHTS[field] for field in USAGE_FIELDS), 2)


def overhead_stats(arms: list[dict], styles: list[str]) -> dict:
    """The token and weighted overhead stats per style, from the arm rows.

    Each styled arm subtracts the unstyled arm of its own repeat. An
    old arm row without a repeat index reads as repeat 0, and an old
    unstyled-check arm never matches a style, so a stored old-format
    probe yields one sample per style.
    """
    unstyled = {arm.get("repeat", 0): arm for arm in arms if arm["arm"] == "unstyled"}
    result = {}
    for style in styles:
        tokens: list[int] = []
        weighted: list[float] = []
        for arm in arms:
            if arm["arm"] != style:
                continue
            baseline = unstyled.get(arm.get("repeat", 0))
            if baseline is None:
                continue
            tokens.append(arm["total_input_tokens"] - baseline["total_input_tokens"])
            weighted.append(round(weighted_total(arm) - weighted_total(baseline), 2))
        if tokens:
            result[style] = {"tokens": _stats(tokens), "weighted": _stats(weighted)}
    return result


def probe_overhead(
    *,
    styles: list[str],
    model: str,
    plugin_dir: Path,
    workdir: Path,
    run: Runner = subprocess_runner,
    repeats: int = 3,
) -> dict:
    """Run the probe and return the content of cost-probe.json."""
    sequence: list[tuple[str, str | None]] = [("unstyled", None)]
    sequence += [(style, style) for style in styles]
    arms = [
        _run_arm(name, style, repeat, model, plugin_dir, workdir, run)
        for repeat in range(repeats)
        for name, style in sequence
    ]

    unstyled_totals = [arm["total_input_tokens"] for arm in arms if arm["arm"] == "unstyled"]
    warnings: list[str] = []
    if len(set(unstyled_totals)) > 1:
        totals = ", ".join(str(total) for total in unstyled_totals)
        warnings.append(
            f"the unstyled input total moved between the probe repeats: {totals}; "
            "each overhead uses the unstyled arm of its own repeat"
        )

    style_files = {style: plugin_dir / "output-styles" / f"{style}.md" for style in sorted(styles)}
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": claude_version(),
        "model_requested": model,
        "probe_prompt": PROBE_PROMPT,
        "flags": list(ISOLATION_FLAGS),
        "note": PROBE_NOTE,
        "plugin": {"dir": str(plugin_dir), "name": _plugin_name(plugin_dir)},
        "styles": {
            style: {"file": str(path), "sha256": sha256_of(path)}
            for style, path in style_files.items()
        },
        "repeats": repeats,
        "price_weights": dict(PRICE_WEIGHTS),
        "arms": arms,
        "unstyled_totals": unstyled_totals,
        "overhead": overhead_stats(arms, styles),
        "warnings": warnings,
    }
