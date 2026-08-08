"""The command-line interface of the clarity ranking.

Exit codes: 0 when the contests are scored and no warnings exist, 1
when the contests are scored but warnings exist (an excluded pair,
an unscored contest, a degenerate strength), 2 when the run cannot
be ranked at all.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from gate.cli import load_answers, run_provenance
from runner.generate import GenerationError, Runner, subprocess_runner
from runner.hermetic import hermetic_call
from runner.provenance import claude_version, sha256_of
from runner.screening import screening_section
from runner.spend import spend_summary
from runner.timing import timing_summary
from value.analysis import select_pairs
from value.cli import answer_index, load_fidelity, load_raw, reconcile_meta, resolved_models
from value.reuse import (
    check_source_meta,
    check_source_pins,
    freshness_block,
    import_judge_rows,
    read_raw_calls,
    reuse_summary,
    sample_forced_keys,
)

from .analysis import UNSTYLED, build_schedule, score_contests
from .judges import build_meta, parse_pick, run_judges
from .report import build_rank_report, build_rank_summary

META_MATCH_KEYS = ("model", "design", "orders", "replicates", "answers_sha256")

# The judge-prompt hash entered the meta row after the first stored
# runs. A stored meta row without it gets an upgraded meta row
# appended; a stored value that differs is a hard mismatch. The
# backfill stamps the current value, so a prompt-edit PR must not
# rely on it.
META_UPGRADE_KEYS = ("judge_prompts_sha256",)


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def _check_writer_constraint(run_dir: Path, model: str) -> list[str]:
    path = run_dir / "provenance.json"
    provenance = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    writer = (provenance or {}).get("conditions", {}).get("model_requested")
    if writer is None:
        return ["no provenance.json with a model: the judge-differs-from-writer rule is unchecked"]
    if model == writer:
        raise _fail(
            f"the judge model {model!r} equals the writer model of the run; "
            "the judge must differ from the writer"
        )
    return []


def _judge(
    args, run_dir: Path, contests, index, meta_stored, rows, run: Runner
) -> tuple[dict, list]:
    """Run the live judge calls. Returns the meta row and the warnings."""
    warnings = _check_writer_constraint(run_dir, args.model)

    raw_path = run_dir / "rank-raw.jsonl"
    with hermetic_call("judge-rank") as hermetic:
        meta = build_meta(
            model=args.model,
            answers_sha256=sha256_of(run_dir / "answers.jsonl"),
            cli_version=claude_version(hermetic.binary, hermetic.env),
        )
        meta_upgraded = False
        if meta_stored is not None:
            meta, meta_upgraded = reconcile_meta(
                meta,
                meta_stored,
                match_keys=META_MATCH_KEYS,
                upgrade_keys=META_UPGRADE_KEYS,
                filename="rank-raw.jsonl",
            )

        with raw_path.open("a", encoding="utf-8") as raw_file:
            if meta_stored is None or meta_upgraded:
                raw_file.write(json.dumps(meta, ensure_ascii=False) + "\n")
                raw_file.flush()

            def sink(row: dict) -> None:
                raw_file.write(json.dumps(row, ensure_ascii=False) + "\n")
                raw_file.flush()

            forced: set[str] = set()
            if args.reuse_from:
                forced = _import_source_rows(args, meta, index, rows, sink, warnings)

            try:
                warnings += run_judges(
                    contests=contests,
                    model=meta["model"],
                    rows=rows,
                    sink=sink,
                    workdir=hermetic.workdir,
                    run=run,
                    env=hermetic.env,
                    parallel=args.parallel,
                    force_keys=forced,
                )
            except GenerationError as error:
                raise _fail(f"a judge call failed: {error}") from error
    return meta, warnings


def _row_valid(current_shas: set[str]):
    """The import test for a rank row: both shown texts are current."""

    def valid(row: dict) -> bool:
        return row.get("first_sha256") in current_shas and row.get("second_sha256") in current_shas

    return valid


def _freshness_parser():
    """The verdict parser for a sampled contest row."""

    def parse(row: dict) -> object:
        return parse_pick(row["output"])

    return parse


def _import_source_rows(args, meta, index, rows, sink, warnings) -> set[str]:
    """Import the reusable source rows; returns the freshness sample keys."""
    source_dir = Path(args.reuse_from)
    source_raw = source_dir / "rank-raw.jsonl"
    source_meta, source_rows = load_raw(source_raw)
    check_source_meta(
        source_meta,
        meta,
        match_keys=("model", "design", "orders", "replicates"),
        upgrade_keys=META_UPGRADE_KEYS,
        source_raw=source_raw,
    )
    check_source_pins(source_rows, source_raw)
    current_shas = {arm["sha256"] for arm in index.values()}
    candidates = any(key not in rows for key in source_rows)
    imported = import_judge_rows(
        source_rows=source_rows,
        source_name=source_dir.name,
        rows=rows,
        sink=sink,
        valid=_row_valid(current_shas),
    )
    if candidates and not imported and not any("reused_from" in row for row in rows.values()):
        warnings.append(
            f"{source_dir}: no stored judge row was reusable for this run; every call runs live"
        )
    return sample_forced_keys(imported, "rank")


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-rank",
        description=(
            "Rank the answers of a run by clarity, through blind "
            "head-to-head contests: per prompt and per competitor pair, "
            "a judge sees the two texts side by side, in both orders, "
            "and picks the clearer text. The unstyled answer competes "
            "as its own arm and anchors the Bradley-Terry scale. The "
            "judge never sees a style name and differs from the writer "
            "of the answers."
        ),
    )
    parser.add_argument("run_dir", help="the run directory with answers.jsonl and fidelity.jsonl")
    parser.add_argument("--judge", action="store_true", help="run the live judge calls first")
    parser.add_argument("--model", default="opus", help="the contest judge model")
    parser.add_argument(
        "--parallel",
        type=int,
        default=8,
        help="concurrent judge calls (1 runs one call at a time)",
    )
    parser.add_argument(
        "--reuse-from",
        metavar="RUN_DIR",
        help=(
            "import the stored judge rows of another run whose conditions "
            "match; a small fixed sample of the imported verdicts re-runs live"
        ),
    )
    args = parser.parse_args(argv)

    if args.parallel < 1:
        raise _fail(f"--parallel must be 1 or more, not {args.parallel}")
    if args.reuse_from and not args.judge:
        raise _fail("--reuse-from implies --judge")

    run_dir = Path(args.run_dir)
    if args.reuse_from and Path(args.reuse_from).resolve() == run_dir.resolve():
        raise _fail(f"{args.reuse_from}: the reuse source is the run itself; pass another run")
    answers = load_answers(run_dir / "answers.jsonl")
    index = answer_index(answers)
    answer_shas = {key: arm["sha256"] for key, arm in index.items()}

    fidelity_rows = load_fidelity(run_dir / "fidelity.jsonl")
    pairs, pair_warnings = select_pairs(fidelity_rows, answer_shas)
    if UNSTYLED in pairs:
        raise _fail(
            f'a style named "{UNSTYLED}" collides with the reserved name of the unstyled competitor'
        )
    if not any(pairs.values()):
        raise _fail(f"{run_dir}: no pair passes the gate, so there is nothing to rank")

    competitors, contests = build_schedule(pairs, index)
    if not contests:
        raise _fail(f"{run_dir}: no contest exists, so there is nothing to rank")

    raw_path = run_dir / "rank-raw.jsonl"
    meta, rows = load_raw(raw_path)
    judge_warnings: list[str] = []
    if args.judge:
        meta, judge_warnings = _judge(args, run_dir, contests, index, meta, rows, run)
    elif meta is None:
        raise _fail(f"{raw_path}: no judge data; run style-rank {run_dir} --judge")

    result = score_contests(competitors, contests, rows)
    raw_calls = read_raw_calls(raw_path)
    freshness, fresh_warnings = freshness_block(raw_calls, _freshness_parser())
    warnings = pair_warnings + judge_warnings + result.warnings + fresh_warnings
    summary = build_rank_summary(
        run_name=run_dir.name,
        meta=meta,
        result=result,
        warnings=warnings,
        model_resolved=resolved_models(rows).get(meta["model"]),
        reuse=reuse_summary(rows, raw_calls, freshness),
    )
    (run_dir / "rank.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    own_rows = [row for row in rows.values() if "reused_from" not in row]
    timing = timing_summary(own_rows)
    spend = spend_summary(own_rows)
    report = build_rank_report(
        summary, timing, spend, screening=screening_section(run_provenance(run_dir))
    )
    (run_dir / "rank.md").write_text(report, encoding="utf-8")

    totals = {name: {"wins": 0, "losses": 0, "splits": 0} for name in result.competitors}
    for matchup in result.matchups:
        totals[matchup["a"]]["wins"] += matchup["wins_a"]
        totals[matchup["a"]]["losses"] += matchup["wins_b"]
        totals[matchup["b"]]["wins"] += matchup["wins_b"]
        totals[matchup["b"]]["losses"] += matchup["wins_a"]
        for side in ("a", "b"):
            totals[matchup[side]]["splits"] += matchup["splits"]
    strengths = result.bradley_terry.get("strengths", {})
    # The lines follow the fitted order. A competitor outside the
    # fit comes last, in name order.
    ordered = [*strengths, *(name for name in result.competitors if name not in strengths)]
    for name in ordered:
        tally = totals[name]
        strength = (strengths.get(name) or {}).get("strength")
        strength_part = f"strength {strength}" if strength is not None else "strength n/a"
        print(
            f"{name}: {tally['wins']}-{tally['losses']}-{tally['splits']} "
            f"(win-loss-split), {strength_part}"
        )
    return 0 if not warnings else 1


if __name__ == "__main__":
    sys.exit(main())
