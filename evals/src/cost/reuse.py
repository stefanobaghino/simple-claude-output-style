"""Import stored probe arms from another run, per style.

The probe layer of the explicit reuse: with --reuse-from, style-cost
imports, per style whose text sha matches the source probe, the arms
of that style together with the per-repeat unstyled baseline arms of
the source, and probes live only the styles that the source cannot
serve. The same-repeat subtraction survives because the pairing key
carries the origin: a styled arm meets only the unstyled arm of its
own origin and repeat, and the arms of one style all come from one
origin. The probe arms carry no freshness sample, because they are
token measurements, not judge scores: a re-run-and-compare would
simply be a live probe.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from runner.generate import ISOLATION_FLAGS, plugin_name
from runner.hermetic import CONFIG_MODE, manifest_sha256
from runner.provenance import sha256_of

from .probe import PRICE_WEIGHTS, PROBE_NOTE, PROBE_PROMPT, overhead_stats


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def load_source_probe(source_dir: Path) -> dict:
    path = source_dir / "cost-probe.json"
    if not path.exists():
        raise _fail(f"{path}: the source run holds no probe; run style-cost {source_dir} --probe")
    return json.loads(path.read_text(encoding="utf-8"))


def check_source_probe(source_probe: dict, *, model: str, repeats: int, source_dir: Path) -> None:
    """Stop when the source probe cannot feed this invocation.

    The model and the probe prompt are call conditions. The repeat
    counts must be equal, so every style carries the same sample
    size; an old-format source probe reads as one repeat.
    """
    source_model = source_probe.get("model_requested")
    if source_model != model:
        raise _fail(
            f"{source_dir}: the source probe used the model {source_model!r}, not {model!r}"
        )
    if source_probe.get("probe_prompt") != PROBE_PROMPT:
        raise _fail(f"{source_dir}: the source probe used another probe prompt")
    source_repeats = source_probe.get("repeats") or 1
    if source_repeats != repeats:
        raise _fail(f"--reuse-from implies --repeats {source_repeats}, not {repeats}")


def select_imported_styles(
    source_probe: dict, plugin_dir: Path, styles: list[str]
) -> tuple[list[str], list[str]]:
    """The styles whose source arms can import, and the rest.

    A source arm substitutes for a fresh probe call only when the
    source probe measured the same style text that a fresh probe
    would measure now: the sha in the source probe must equal the
    sha of the current style file.
    """
    imported: list[str] = []
    fresh: list[str] = []
    source_styles = source_probe.get("styles") or {}
    for style in styles:
        entry = source_styles.get(style)
        current = plugin_dir / "output-styles" / f"{style}.md"
        if entry is not None and current.exists() and entry.get("sha256") == sha256_of(current):
            imported.append(style)
        else:
            fresh.append(style)
    return imported, fresh


def merge_probe(
    *,
    source_probe: dict,
    source_name: str,
    imported_styles: list[str],
    live: dict | None,
    styles: list[str],
    repeats: int,
    model: str,
    plugin_dir: Path,
) -> dict:
    """The content of cost-probe.json with imported and live arms.

    The imported arms are the source arms of the imported styles plus
    every unstyled arm of the source, marked with the origin, so the
    per-repeat baselines travel with the styled arms. The repeat
    indices keep their stored values: the pairing key of
    overhead_stats carries the origin, so the indices of the two
    origins never meet.
    """
    imported = [
        {**arm, "reused_from": source_name}
        for arm in source_probe["arms"]
        if arm["arm"] == "unstyled" or arm["arm"] in imported_styles
    ]
    live_arms = list(live["arms"]) if live else []
    arms = imported + live_arms

    warnings = list(live["warnings"]) if live else []
    imported_unstyled = [arm["total_input_tokens"] for arm in imported if arm["arm"] == "unstyled"]
    if len(set(imported_unstyled)) > 1:
        totals = ", ".join(str(total) for total in imported_unstyled)
        warnings.append(
            f"the unstyled input total moved between the probe repeats of {source_name}: "
            f"{totals}; each overhead uses the unstyled arm of its own origin and repeat"
        )

    styles_map = {style: source_probe["styles"][style] for style in sorted(imported_styles)}
    if live:
        styles_map.update(live["styles"])
    styles_map = {style: styles_map[style] for style in sorted(styles_map)}

    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "claude_version": live["claude_version"] if live else source_probe.get("claude_version"),
        "model_requested": model,
        "probe_prompt": PROBE_PROMPT,
        "flags": list(ISOLATION_FLAGS),
        "config": CONFIG_MODE,
        "config_manifest_sha256": manifest_sha256(),
        "note": PROBE_NOTE,
        "plugin": {"dir": str(plugin_dir), "name": plugin_name(plugin_dir)},
        "styles": styles_map,
        "repeats": repeats,
        "price_weights": dict(PRICE_WEIGHTS),
        "arms": arms,
        "unstyled_totals": [arm["total_input_tokens"] for arm in arms if arm["arm"] == "unstyled"],
        "overhead": overhead_stats(arms, styles),
        "warnings": warnings,
        "reuse": {
            "source": source_name,
            "source_date": source_probe.get("date"),
            "styles": sorted(imported_styles),
            "reused_arms": len(imported),
            "live_arms": len(live_arms),
        },
    }


def probe_reuse_block(probe: dict | None) -> dict | None:
    """The reuse block of the cost report, or None without markers.

    The block derives from the per-arm markers of the stored probe,
    so a rescore without the flag reproduces it.
    """
    if probe is None:
        return None
    arms = probe.get("arms") or []
    reused = [arm for arm in arms if "reused_from" in arm]
    if not reused:
        return None
    sources = sorted({arm["reused_from"] for arm in reused})
    return {
        "source": sources[0] if len(sources) == 1 else sources,
        "source_date": (probe.get("reuse") or {}).get("source_date"),
        "styles": sorted({arm["arm"] for arm in reused if arm["arm"] != "unstyled"}),
        "reused_arms": len(reused),
        "live_arms": len(arms) - len(reused),
    }
