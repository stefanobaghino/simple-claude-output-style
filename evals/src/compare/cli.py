"""The command-line interface of the cross-run comparison.

Exit codes: 0 when the comparison ran and no warnings exist, 1 when
warnings exist (for example, a condition mismatch or a missing
artifact), 2 when the comparison cannot run.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from .analysis import ARTIFACTS, compare_runs
from .report import build_compare_report, build_compare_summary


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_runs(run_dirs: list[Path]) -> list[dict]:
    runs = []
    names: set[str] = set()
    for run_dir in run_dirs:
        if run_dir.name in names:
            raise _fail(f"{run_dir.name}: the run name appears twice")
        names.add(run_dir.name)
        provenance = _load_json(run_dir / "provenance.json")
        if provenance is None:
            raise _fail(f"{run_dir}: no provenance.json, so the directory is not a run")
        run = {"name": run_dir.name, "provenance": provenance}
        for artifact in ARTIFACTS:
            run[artifact] = _load_json(run_dir / f"{artifact}.json")
        runs.append(run)
    return runs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="style-compare",
        description=(
            "Compare several runs with identical conditions and state, "
            "per style and axis, the spread across the runs. The "
            "comparison reads only the stored artifacts of the runs."
        ),
    )
    parser.add_argument("run_dirs", nargs="+", help="the run directories to compare")
    parser.add_argument("--out", help="output directory (default: runs/<date>-compare)")
    args = parser.parse_args(argv)

    if len(args.run_dirs) < 2:
        raise _fail("style-compare needs at least 2 run directories")
    runs = load_runs([Path(run_dir) for run_dir in args.run_dirs])

    result = compare_runs(runs)
    summary = build_compare_summary(
        run_names=[run["name"] for run in runs],
        styles=result.styles,
        warnings=result.warnings,
    )
    out = (
        Path(args.out)
        if args.out
        else Path("runs") / f"{datetime.now(UTC).strftime('%Y-%m-%d')}-compare"
    )
    out.mkdir(parents=True, exist_ok=True)
    (out / "compare.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out / "compare.md").write_text(build_compare_report(summary), encoding="utf-8")

    for style, axes in result.styles.items():
        print(f"{style}: {len(axes)} axes across {len(runs)} runs")
    return 0 if not result.warnings else 1


if __name__ == "__main__":
    sys.exit(main())
