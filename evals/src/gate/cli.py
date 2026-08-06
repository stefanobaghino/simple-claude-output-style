"""The command-line interface of the fidelity gate.

Exit codes: 0 when every pair passes and no warnings exist, 1 when the
gate ran but pairs fail or warnings exist, 2 when the run cannot be
gated at all.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from linter import Linter, load_rules
from runner.provenance import linter_toolchain, sha256_of
from runner.screening import screening_section

from .config import load_gate_config
from .report import build_fidelity_report, build_summary
from .score import score_run


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def load_answers(path: Path) -> list[dict]:
    """The deduplicated answers, last line wins per (prompt, arm)."""
    if not path.exists():
        raise _fail(f"{path}: the run holds no answers file")
    deduplicated: dict[tuple[str, str | None], dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            answer = json.loads(line)
            deduplicated[(answer["prompt_id"], answer.get("style"))] = answer
    if not deduplicated:
        raise _fail(f"{path}: the answers file is empty")
    return list(deduplicated.values())


def run_provenance(run_dir: Path) -> dict | None:
    provenance_path = run_dir / "provenance.json"
    if not provenance_path.exists():
        return None
    return json.loads(provenance_path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="style-gate",
        description=(
            "Check each styled answer of a run with the rules of its style, "
            "mark each pair as pass or fail against the threshold of the "
            "style, and check the unstyled answers as a baseline."
        ),
    )
    parser.add_argument("run_dir", help="the run directory with answers.jsonl")
    parser.add_argument("--rules-dir", default="rules", help="directory with the rule files")
    parser.add_argument("--gate-config", default="rules/gate.yaml", help="the gate policy file")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir)
    answers = load_answers(run_dir / "answers.jsonl")
    styles = sorted({a["style"] for a in answers if a.get("style") is not None})
    if not styles:
        raise _fail(f"{run_dir}: the run holds no styled answers")

    config = load_gate_config(args.gate_config)
    rule_files = {style: Path(args.rules_dir) / f"{style}.rules.yaml" for style in styles}
    for style, rule_file in rule_files.items():
        if not rule_file.exists():
            raise _fail(f"{style}: no rule file at {rule_file}")
        if style not in config.thresholds:
            raise _fail(f"{style}: no threshold in {config.path}")

    linters = {style: Linter(load_rules(rule_file)) for style, rule_file in rule_files.items()}
    result = score_run(answers, linters, config)

    toolchain = linter_toolchain()
    provenance = run_provenance(run_dir)
    run_toolchain = (provenance or {}).get("linter_toolchain")
    if run_toolchain is not None and run_toolchain != toolchain:
        result.warnings.append(
            f"the linter toolchain differs from the run: gate {toolchain}, run {run_toolchain}"
        )

    summary = build_summary(
        rows=result.rows,
        styles=styles,
        run_name=run_dir.name,
        thresholds={style: config.thresholds[style] for style in styles},
        rule_hashes={
            style: {"file": str(path), "sha256": sha256_of(path)}
            for style, path in rule_files.items()
        },
        gate_config_hash={"file": str(config.path), "sha256": sha256_of(config.path)},
        toolchain=toolchain,
        run_toolchain=run_toolchain,
        warnings=result.warnings,
    )

    with (run_dir / "fidelity.jsonl").open("w", encoding="utf-8") as fidelity_file:
        for row in result.rows:
            fidelity_file.write(json.dumps(row, ensure_ascii=False) + "\n")
    (run_dir / "fidelity.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    report = build_fidelity_report(
        result.rows, styles, summary, result.failing, screening=screening_section(provenance)
    )
    (run_dir / "fidelity.md").write_text(report, encoding="utf-8")

    for style in styles:
        stats = summary["summary"][style]
        print(f"{style}: {stats['passed']}/{stats['gated']} pair(s) pass the gate")
    all_pass = all(stats["failed"] == 0 for stats in summary["summary"].values())
    return 0 if all_pass and not result.warnings else 1


if __name__ == "__main__":
    sys.exit(main())
