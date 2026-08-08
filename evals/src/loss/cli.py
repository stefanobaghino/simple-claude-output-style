"""The command-line interface of the content-loss checks.

Exit codes: 0 when the checks are scored and no warnings exist, 1
when the checks are scored but warnings exist (an excluded pair, a
check without judge data, an unusable judge output), 2 when the run
cannot be scored at all.
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
from value.judges import parse_bools
from value.reuse import (
    check_source_meta,
    check_source_pins,
    freshness_block,
    import_judge_rows,
    read_raw_calls,
    reuse_summary,
    sample_forced_keys,
)

from .analysis import score_checks
from .judges import CHECKS, build_meta, parse_string_list, parse_verdicts, run_judges
from .report import build_loss_report, build_loss_summary

META_MATCH_KEYS = ("model", "answers_sha256")

# The keys that entered the meta row after the first stored runs:
# the two-way fact mine and the judge-prompt hash. A stored meta row
# without a key gets an upgraded meta row appended; a stored value
# that differs is a hard mismatch. The backfill stamps the current
# value, so a prompt-edit PR must not rely on it.
META_UPGRADE_KEYS = ("fact_mine", "judge_prompts_sha256")


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


def _judge(args, run_dir: Path, pairs, index, meta_stored, rows, run: Runner) -> tuple[dict, list]:
    """Run the live judge calls. Returns the meta row and the warnings."""
    warnings = _check_writer_constraint(run_dir, args.model)

    raw_path = run_dir / "loss-raw.jsonl"
    with hermetic_call("judge-loss") as hermetic:
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
                filename="loss-raw.jsonl",
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
                    pairs=pairs,
                    answers=index,
                    checks=args.check_list,
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


def _row_valid(
    current_shas: set[str],
    checks: list[str],
    source_index: dict[tuple[str, str | None], dict],
):
    """The import test for a loss row.

    Every loss key ends in the sha of the text that the row speaks
    about, so a key hit is a content hit. A reverse row checks the
    unstyled text against the styled facts, so both texts must be
    current. A forward check row grades marks against the facts of
    the source pair, so the unstyled text of that source pair must
    be current as well, else the marks answer another fact list.
    Only the rows of the invoked checks import.
    """

    def valid(row: dict) -> bool:
        if row.get("check") not in checks:
            return False
        key = str(row.get("key", ""))
        if key.rsplit(":", 1)[-1] not in current_shas:
            return False
        if key.startswith("completeness:reverse:"):
            return row.get("answer_sha256") in current_shas
        if key.startswith(("completeness:check:", "hedging:check:")):
            unstyled = source_index.get((str(row.get("prompt_id")), None))
            return unstyled is not None and unstyled["sha256"] in current_shas
        return True

    return valid


def _freshness_parser(
    pairs: dict[str, list[str]],
    index: dict[tuple[str, str | None], dict],
    rows: dict[str, dict],
):
    """The verdict parser for a sampled loss row.

    A check row grades a numbered item list, so the parse needs the
    item count of the extraction row behind the pair. The join goes
    from the check key to the extraction key through the pair arms.
    """
    items_key: dict[str, str] = {}
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            styled = index[(prompt_id, style)]["sha256"]
            unstyled = index[(prompt_id, None)]["sha256"]
            items_key[f"completeness:check:{styled}"] = f"completeness:facts:{unstyled}"
            items_key[f"completeness:reverse:{styled}"] = f"completeness:facts:{styled}"
            items_key[f"hedging:check:{styled}"] = f"hedging:claims:{unstyled}"

    def parse(row: dict) -> object:
        source = rows.get(items_key.get(str(row.get("key")), ""))
        items = parse_string_list(source["output"]) if source else None
        if not items:
            return None
        if str(row.get("check")) == "hedging":
            return parse_verdicts(row["output"], len(items))
        return parse_bools(row["output"], len(items))

    return parse


def _import_source_rows(args, meta, index, rows, sink, warnings) -> set[str]:
    """Import the reusable source rows; returns the freshness sample keys."""
    source_dir = Path(args.reuse_from)
    source_raw = source_dir / "loss-raw.jsonl"
    source_answers_path = source_dir / "answers.jsonl"
    if not source_answers_path.exists():
        raise _fail(f"{source_answers_path}: no answers, so the source directory is not a run")
    source_meta, source_rows = load_raw(source_raw)
    check_source_meta(
        source_meta,
        meta,
        match_keys=("model",),
        upgrade_keys=META_UPGRADE_KEYS,
        source_raw=source_raw,
    )
    check_source_pins(source_rows, source_raw)
    source_index = answer_index(load_answers(source_answers_path))
    current_shas = {arm["sha256"] for arm in index.values()}
    candidates = any(key not in rows for key in source_rows)
    imported = import_judge_rows(
        source_rows=source_rows,
        source_name=source_dir.name,
        rows=rows,
        sink=sink,
        valid=_row_valid(current_shas, args.check_list, source_index),
    )
    if candidates and not imported and not any("reused_from" in row for row in rows.values()):
        warnings.append(
            f"{source_dir}: no stored judge row was reusable for this run; every call runs live"
        )
    return sample_forced_keys(imported, "loss")


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-loss",
        description=(
            "Check what the styled answer loses relative to the unstyled "
            "answer, per gated pair: the fraction of the facts that "
            "survive, and each uncertain claim that lost its uncertainty. "
            "The judge never sees a style name and differs from the "
            "writer of the answers."
        ),
    )
    parser.add_argument("run_dir", help="the run directory with answers.jsonl and fidelity.jsonl")
    parser.add_argument("--judge", action="store_true", help="run the live judge calls first")
    parser.add_argument("--model", default="opus", help="the extraction and check model")
    parser.add_argument(
        "--checks",
        default=",".join(CHECKS),
        help="comma-separated subset of the checks to judge",
    )
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

    args.check_list = [check for check in args.checks.split(",") if check]
    unknown = sorted(set(args.check_list) - set(CHECKS))
    if unknown:
        raise _fail(f"unknown check(s): {', '.join(unknown)}; the checks are {', '.join(CHECKS)}")
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
    if not any(pairs.values()):
        raise _fail(f"{run_dir}: no pair passes the gate, so there is nothing to judge")

    raw_path = run_dir / "loss-raw.jsonl"
    meta, rows = load_raw(raw_path)
    judge_warnings: list[str] = []
    if args.judge:
        meta, judge_warnings = _judge(args, run_dir, pairs, index, meta, rows, run)
    elif meta is None:
        raise _fail(f"{raw_path}: no judge data; run style-loss {run_dir} --judge")

    result = score_checks(pairs=pairs, answers=index, rows=rows, fact_mine=meta.get("fact_mine"))
    raw_calls = read_raw_calls(raw_path)
    freshness, fresh_warnings = freshness_block(raw_calls, _freshness_parser(pairs, index, rows))
    warnings = pair_warnings + judge_warnings + result.warnings + fresh_warnings
    summary = build_loss_summary(
        run_name=run_dir.name,
        meta=meta,
        pairs=pairs,
        checks=result.checks,
        warnings=warnings,
        model_resolved=resolved_models(rows).get(meta["model"]),
        reuse=reuse_summary(rows, raw_calls, freshness),
    )
    (run_dir / "loss.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    own_rows = [row for row in rows.values() if "reused_from" not in row]
    timing = timing_summary(own_rows)
    spend = spend_summary(own_rows)
    report = build_loss_report(
        summary, timing, spend, screening=screening_section(run_provenance(run_dir))
    )
    (run_dir / "loss.md").write_text(report, encoding="utf-8")

    for style in sorted(pairs):
        parts = []
        for check in CHECKS:
            stats = result.checks[check]
            if not stats["judged"]:
                parts.append(f"{check} not judged")
                continue
            score = stats["per_style"][style]["median"]
            parts.append(
                f"{check} median {score}" if score is not None else f"{check} without a scored pair"
            )
        print(f"{style}: " + ", ".join(parts))
    return 0 if not warnings else 1


if __name__ == "__main__":
    sys.exit(main())
