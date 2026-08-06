"""The command-line interface of the token-cost report.

Exit codes: 0 when both numbers are computed and no warnings exist, 1
when the report ran but warnings exist (for example, the overhead is
not measured), 2 when the run cannot be reported at all.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from gate.cli import load_answers
from runner.generate import GenerationError, Runner, isolated_workdir, subprocess_runner
from runner.spend import spend_summary

from .analysis import analyze_ratios
from .probe import probe_overhead
from .report import build_cost_report, build_cost_summary


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def _provenance(run_dir: Path) -> dict | None:
    path = run_dir / "provenance.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _run_probe(styles: list[str], model: str, plugin_dir: Path, run: Runner, repeats: int) -> dict:
    try:
        with isolated_workdir("probe") as workdir:
            return probe_overhead(
                styles=styles,
                model=model,
                plugin_dir=plugin_dir,
                workdir=workdir,
                run=run,
                repeats=repeats,
            )
    except GenerationError as error:
        raise _fail(f"the probe failed: {error}") from error


def _probe_warnings(probe: dict, styles: list[str], provenance: dict | None) -> list[str]:
    warnings = list(probe.get("warnings", []))
    for style in styles:
        if style not in probe.get("overhead", {}):
            warnings.append(f"{style}: the probe holds no overhead for this style")
    run_styles = (provenance or {}).get("styles", {})
    for style, info in probe.get("styles", {}).items():
        recorded = run_styles.get(style)
        if recorded and recorded.get("sha256") != info.get("sha256"):
            warnings.append(
                f"{style}: the style file of the probe differs from the style file of the run"
            )
    return warnings


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-cost",
        description=(
            "Report the token cost of each style: the fixed input overhead "
            "of the style block per request, and the distribution of the "
            "ratio of styled answer length to unstyled answer length. The "
            "report reads all pairs of a run, gated or not."
        ),
    )
    parser.add_argument("run_dir", help="the run directory with answers.jsonl")
    parser.add_argument(
        "--probe",
        action="store_true",
        help="measure the input overhead with live probe calls",
    )
    parser.add_argument("--plugin-dir", default="../plugin", help="the plugin directory")
    parser.add_argument("--model", help="model for the probe (default: the model of the run)")
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="probe calls per arm (with --probe)",
    )
    args = parser.parse_args(argv)
    if args.repeats < 1:
        raise _fail("--repeats must be at least 1")

    run_dir = Path(args.run_dir)
    answers = load_answers(run_dir / "answers.jsonl")
    styles = sorted({a["style"] for a in answers if a.get("style") is not None})
    if not styles:
        raise _fail(f"{run_dir}: the run holds no styled answers")
    provenance = _provenance(run_dir)

    probe_path = run_dir / "cost-probe.json"
    warnings: list[str] = []
    if args.probe:
        model = args.model or (provenance or {}).get("conditions", {}).get("model_requested")
        if not model:
            raise _fail(f"{run_dir}: no provenance.json with a model; pass --model")
        probe = _run_probe(styles, model, Path(args.plugin_dir).resolve(), run, args.repeats)
        probe_path.write_text(json.dumps(probe, indent=2) + "\n", encoding="utf-8")
    elif probe_path.exists():
        probe = json.loads(probe_path.read_text(encoding="utf-8"))
    else:
        probe = None
        warnings.append(
            "the input overhead is not measured: run style-cost with --probe to measure it"
        )
    if probe is not None:
        warnings += _probe_warnings(probe, styles, provenance)

    ratios = analyze_ratios(answers)
    warnings = ratios.warnings + warnings
    summary = build_cost_summary(
        run_name=run_dir.name, per_style=ratios.per_style, probe=probe, warnings=warnings
    )
    (run_dir / "cost.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    spend = spend_summary(probe["arms"]) if probe is not None else None
    (run_dir / "cost.md").write_text(build_cost_report(summary, spend), encoding="utf-8")

    overhead = summary["input_overhead"]
    for style in styles:
        stats = ratios.per_style[style]
        measured = (overhead["per_style"] or {}).get(style)
        overhead_text = (
            f"mean {measured['tokens']['mean']} input tokens, "
            f"weighted mean {measured['weighted']['mean']}"
            if measured
            else "not measured"
        )
        print(f"{style}: ratio of totals {stats['ratio_of_totals']}, overhead {overhead_text}")
    return 0 if not warnings else 1


if __name__ == "__main__":
    sys.exit(main())
