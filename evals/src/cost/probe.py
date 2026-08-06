"""Measure the fixed input overhead of each style with a live probe.

The overhead is not derivable from a stored run, so the probe runs a
minimal prompt through the same CLI path as the runner, once per arm:
unstyled, one arm per style, then unstyled again as a stability check.
Both arms load the plugin, so the difference between a styled arm and
the unstyled arm isolates the style block alone, not plugin loading.
This is the one place where an unstyled call loads the plugin; the
unstyled arm of the runner does not.
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path

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

    arm = {"arm": name, "output_style_active": active, "model": str(init.get("model", ""))}
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


def probe_overhead(
    *,
    styles: list[str],
    model: str,
    plugin_dir: Path,
    workdir: Path,
    run: Runner = subprocess_runner,
) -> dict:
    """Run the probe and return the content of cost-probe.json."""
    sequence: list[tuple[str, str | None]] = [("unstyled", None)]
    sequence += [(style, style) for style in styles]
    sequence.append(("unstyled-check", None))
    arms = [_run_arm(name, style, model, plugin_dir, workdir, run) for name, style in sequence]

    baseline = arms[0]["total_input_tokens"]
    check = arms[-1]["total_input_tokens"]
    warnings: list[str] = []
    if check != baseline:
        warnings.append(
            "the unstyled input total moved between the probe calls: "
            f"{baseline} then {check}; the overhead uses the first"
        )

    by_name = {arm["arm"]: arm for arm in arms}
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
        "arms": arms,
        "unstyled_totals": [baseline, check],
        "overhead": {style: by_name[style]["total_input_tokens"] - baseline for style in styles},
        "warnings": warnings,
    }
