"""Compare the stored artifacts of several runs.

The comparison is a pure function of the loaded artifacts. Per style
and axis, the spread across the runs states how much a verdict moves
on a resample. A condition mismatch between the runs becomes a
warning, because the reader must see how far apart the conditions
are.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from statistics import fmean, stdev

VALUE_CHECKS = ("comprehension", "paraphrase", "roundtrip")

AXIS_ORDER = (
    "fidelity: styled violation rate",
    "fidelity: gated pairs passed",
    "cost: output-token ratio",
    "value: net wins (comprehension)",
    "value: net wins (paraphrase)",
    "value: net wins (roundtrip)",
    "loss: fact survival median",
    "loss: hedge survival median",
    "rank: Bradley-Terry strength",
    "rank: net wins vs unstyled",
)

ARTIFACTS = ("fidelity", "cost", "value", "loss", "rank")

VALUE_JUDGE_KEYS = (
    "models",
    "models_resolved",
    "questions",
    "paraphrases",
    "replicates",
    "comprehension_design",
    "language",
)


@dataclass
class CompareResult:
    styles: dict[str, dict[str, dict]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def _condition_entries(run: dict) -> dict[str, object]:
    """The condition values of one run, keyed by a readable name."""
    entries: dict[str, object] = {}
    provenance = run["provenance"]
    entries["prompt-set hash"] = provenance.get("prompt_set", {}).get("sha256")
    for style, info in (provenance.get("styles") or {}).items():
        entries[f"style hash ({style})"] = info.get("sha256")
    conditions = provenance.get("conditions", {})
    entries["writer model"] = conditions.get("model_requested")
    entries["claude version"] = conditions.get("claude_version")
    # A run before the temp-workdir change has no key here, so the
    # entry is None there, and an old-versus-new comparison warns:
    # the workdir mode marks a comparability era.
    entries["workdir"] = conditions.get("workdir")
    entries["linter toolchain"] = provenance.get("linter_toolchain")
    # A full run and an old run both read None here, so the entry
    # stays silent for them. The CLI already rejects a mix of
    # screening and full runs; this entry makes two screening runs
    # with different subsets warn.
    entries["screening"] = provenance.get("screening")
    fidelity = run["fidelity"]
    if fidelity is not None:
        for style, info in (fidelity.get("rules") or {}).items():
            entries[f"rule-file hash ({style})"] = info.get("sha256")
        entries["gate-config hash"] = fidelity.get("gate_config", {}).get("sha256")
    value = run["value"]
    if value is not None:
        judges = value.get("judges", {})
        for key in VALUE_JUDGE_KEYS:
            entries[f"value judges {key}"] = judges.get(key)
    loss = run["loss"]
    if loss is not None:
        entries["loss judge model"] = loss.get("judge", {}).get("model")
        entries["loss judge model_resolved"] = loss.get("judge", {}).get("model_resolved")
    rank = run["rank"]
    if rank is not None:
        entries["rank judge model"] = rank.get("judge", {}).get("model")
        entries["rank judge model_resolved"] = rank.get("judge", {}).get("model_resolved")
        entries["rank design"] = rank.get("design")
    return entries


def _rendered(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def _condition_mismatches(runs: list[dict]) -> list[str]:
    entries = {run["name"]: _condition_entries(run) for run in runs}
    keys: list[str] = []
    for run_entries in entries.values():
        keys += [key for key in run_entries if key not in keys]
    warnings = []
    for key in keys:
        values = {name: e[key] for name, e in entries.items() if key in e}
        if len(values) < 2:
            continue
        if len({_rendered(value) for value in values.values()}) == 1:
            continue
        rendered = ", ".join(f"{name} {_rendered(value)}" for name, value in values.items())
        warnings.append(f"condition mismatch on {key}: {rendered}")
    return warnings


def _styles(runs: list[dict]) -> list[str]:
    styles: set[str] = set()
    for run in runs:
        styles.update(run["provenance"].get("styles") or {})
        if run["fidelity"] is not None:
            styles.update(run["fidelity"].get("summary") or {})
    return sorted(styles)


def _axis_values(run: dict, style: str) -> dict[str, float | int | None]:
    """The axis scalars of one (run, style). A missing artifact gives no entry."""
    values: dict[str, float | int | None] = {}
    fidelity = run["fidelity"]
    if fidelity is not None:
        summary = fidelity.get("summary", {}).get(style)
        if summary is not None:
            values["fidelity: styled violation rate"] = summary.get("styled_rate")
            values["fidelity: gated pairs passed"] = summary.get("passed")
    cost = run["cost"]
    if cost is not None:
        stats = cost.get("answer_ratio", {}).get("per_style", {}).get(style)
        if stats is not None:
            values["cost: output-token ratio"] = stats.get("ratio_of_totals")
    value = run["value"]
    if value is not None:
        for check in VALUE_CHECKS:
            stats = value.get("checks", {}).get(check, {}).get("per_style", {}).get(style)
            if stats is not None and "wins" in stats:
                values[f"value: net wins ({check})"] = stats["wins"] - stats["losses"]
    loss = run["loss"]
    if loss is not None:
        checks = loss.get("checks", {})
        completeness = checks.get("completeness", {}).get("per_style", {}).get(style)
        if completeness is not None:
            values["loss: fact survival median"] = completeness.get("median")
        hedging = checks.get("hedging", {}).get("per_style", {}).get(style)
        if hedging is not None:
            values["loss: hedge survival median"] = hedging.get("median")
    rank = run["rank"]
    if rank is not None:
        strengths = rank.get("bradley_terry", {}).get("strengths") or {}
        info = strengths.get(style)
        if info is not None:
            values["rank: Bradley-Terry strength"] = info.get("strength")
        for matchup in rank.get("matchups") or []:
            if {matchup.get("a"), matchup.get("b")} != {style, "unstyled"}:
                continue
            # The stored net is wins_a - wins_b, so the sign flips
            # when the style sits on the b side of the matchup.
            net = matchup.get("net")
            if matchup.get("b") == style and net is not None:
                net = -net
            values["rank: net wins vs unstyled"] = net
    return values


def _spread(samples: dict[str, float]) -> dict:
    """Min, mean, max, and sample standard deviation over the run values."""
    values = list(samples.values())
    return {
        "n": len(values),
        "per_run": samples,
        "min": round(min(values), 3),
        "mean": round(fmean(values), 3),
        "max": round(max(values), 3),
        "stdev": round(stdev(values), 3) if len(values) >= 2 else None,
    }


def compare_runs(runs: list[dict]) -> CompareResult:
    """Compare loaded runs: each a dict with name, provenance, and artifacts.

    The provenance is required per run. A missing artifact drops the
    axes of that artifact for that run, with a warning. A null axis
    value drops that sample, and n shows the drop.
    """
    result = CompareResult()
    for run in runs:
        for artifact in ARTIFACTS:
            if run[artifact] is None:
                result.warnings.append(
                    f"{run['name']}: no {artifact}.json, so the {artifact} axes miss this run"
                )
    result.warnings += _condition_mismatches(runs)
    for style in _styles(runs):
        per_axis: dict[str, dict[str, float]] = {}
        for run in runs:
            for axis, value in _axis_values(run, style).items():
                if value is None:
                    continue
                per_axis.setdefault(axis, {})[run["name"]] = value
        axes = {axis: _spread(per_axis[axis]) for axis in AXIS_ORDER if axis in per_axis}
        if axes:
            result.styles[style] = axes
    return result
