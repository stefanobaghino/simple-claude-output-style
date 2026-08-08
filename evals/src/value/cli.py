"""The command-line interface of the reader-value checks.

Exit codes: 0 when the checks are scored and no warnings exist, 1
when the checks are scored but warnings exist (an excluded pair, a
check without judge data, a style that scores worse on
comprehension), 2 when the run cannot be scored at all.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from gate.cli import load_answers
from loss.judges import FACT_MINE, parse_string_list
from runner.generate import GenerationError, Runner, subprocess_runner
from runner.hermetic import hermetic_call
from runner.provenance import claude_version, sha256_of
from runner.screening import screening_section
from runner.spend import spend_summary
from runner.timing import timing_summary

from .analysis import score_checks, select_pairs, shared_facts
from .judges import (
    CHECKS,
    COMPREHENSION_DESIGN,
    COMPREHENSION_DESIGNS,
    build_meta,
    parse_bools,
    run_judges,
)
from .report import build_value_report, build_value_summary
from .reuse import (
    check_source_meta,
    check_source_pins,
    freshness_block,
    import_judge_rows,
    read_raw_calls,
    reuse_summary,
    sample_forced_keys,
)

META_MATCH_KEYS = ("models", "questions", "paraphrases", "language", "answers_sha256")

# On a design transition (a stored design earlier than the current
# one), the comprehension rows rebuild fully under new keys, so the
# questions and the replicates can change. The reuse of the
# paraphrase and roundtrip rows depends only on these keys.
TRANSITION_MATCH_KEYS = ("models", "paraphrases", "language", "answers_sha256")

# The judge-prompt hash entered the meta row after the first stored
# runs. A stored meta row without an upgrade key gets an upgraded
# meta row appended; a stored value that differs is a hard mismatch.
# The backfill stamps the current value, so a prompt-edit PR must
# not rely on it: a pre-hash file carries rows from the old prompts.
META_UPGRADE_KEYS = ("judge_prompts_sha256",)


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def reconcile_meta(
    meta: dict,
    meta_stored: dict,
    *,
    match_keys: tuple[str, ...],
    upgrade_keys: tuple[str, ...],
    filename: str,
) -> tuple[dict, bool]:
    """The stored meta row, backfilled with the absent upgrade keys.

    A match key or a stored upgrade key whose value differs is a hard
    mismatch. Returns the meta row to use and whether the caller must
    append it as an upgraded row.
    """
    mismatched = [key for key in match_keys if meta_stored.get(key) != meta[key]]
    mismatched += [
        key for key in upgrade_keys if key in meta_stored and meta_stored[key] != meta[key]
    ]
    if mismatched:
        raise _fail(
            f"{filename} does not match this invocation on {', '.join(mismatched)}; "
            "remove the file to judge again from scratch"
        )
    absent = [key for key in upgrade_keys if key not in meta_stored]
    if absent:
        return {**meta_stored, **{key: meta[key] for key in absent}}, True
    return meta_stored, False


def _provenance(run_dir: Path) -> dict | None:
    path = run_dir / "provenance.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_fidelity(path: Path) -> list[dict]:
    if not path.exists():
        raise _fail(f"{path}: the run holds no gate data; run style-gate first")
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def load_raw(path: Path) -> tuple[dict | None, dict[str, dict]]:
    """The meta row and the call rows of value-raw.jsonl, last key wins."""
    if not path.exists():
        return None, {}
    meta = None
    rows: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("type") == "meta":
            meta = row
        else:
            rows[row["key"]] = row
    return meta, rows


def resolved_models(rows: dict[str, dict]) -> dict[str, object]:
    """The resolved model IDs of the stored call rows, per requested model.

    The value is one string when the rows agree and a sorted list when
    the rows differ. A row without a resolved ID contributes nothing,
    so a run from before the model_resolved field yields an empty
    mapping.
    """
    by_request: dict[str, set[str]] = {}
    for row in rows.values():
        requested = row.get("model_requested")
        resolved = row.get("model_resolved")
        if requested and resolved:
            by_request.setdefault(requested, set()).add(resolved)
    return {
        requested: min(values) if len(values) == 1 else sorted(values)
        for requested, values in by_request.items()
    }


def answer_index(answers: list[dict]) -> dict[tuple[str, str | None], dict]:
    return {
        (answer["prompt_id"], answer.get("style")): {
            "text": answer["answer"],
            "sha256": hashlib.sha256(answer["answer"].encode("utf-8")).hexdigest(),
        }
        for answer in answers
    }


def _texts(pairs: dict[str, list[str]], index: dict[tuple[str, str | None], dict]) -> list[dict]:
    """The unique texts to judge: both arms of every pair, once per sha256."""
    texts: list[dict] = []
    seen: set[str] = set()
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            for key in ((prompt_id, None), (prompt_id, style)):
                arm = index[key]
                if arm["sha256"] not in seen:
                    seen.add(arm["sha256"])
                    texts.append(
                        {"prompt_id": prompt_id, "sha256": arm["sha256"], "text": arm["text"]}
                    )
    return texts


def _check_writer_constraint(
    provenance: dict | None, reader_model: str, grader_model: str
) -> list[str]:
    writer = (provenance or {}).get("conditions", {}).get("model_requested")
    if writer is None:
        return ["no provenance.json with a model: the judge-differs-from-writer rule is unchecked"]
    for role, model in (("reader", reader_model), ("grader", grader_model)):
        if model == writer:
            raise _fail(
                f"the {role} model {model!r} equals the writer model of the run; "
                "the judges must differ from the writer"
            )
    return []


def _judge(args, run_dir: Path, pairs, index, meta_stored, rows, run: Runner) -> tuple[dict, list]:
    """Run the live judge calls. Returns the meta row and the warnings."""
    warnings = _check_writer_constraint(_provenance(run_dir), args.model_reader, args.model_grader)
    checks = list(args.check_list)
    answers_sha256 = sha256_of(run_dir / "answers.jsonl")

    facts_by_pair: dict[tuple[str, str], dict[str, list[str]]] = {}
    if "comprehension" in checks:
        loss_meta, loss_rows = load_raw(run_dir / "loss-raw.jsonl")
        if loss_meta is None:
            warnings.append(
                "no loss data for the comprehension questions, so comprehension is "
                f"not judged; run style-loss {run_dir} --judge first"
            )
            checks.remove("comprehension")
        elif loss_meta.get("answers_sha256") != answers_sha256:
            warnings.append(
                "loss-raw.jsonl comes from other answers, so comprehension is not "
                f"judged; run style-loss {run_dir} --judge again"
            )
            checks.remove("comprehension")
        elif loss_meta.get("fact_mine") != FACT_MINE:
            warnings.append(
                "loss-raw.jsonl holds a one-way fact mine, so comprehension is not "
                f"judged; run style-loss {run_dir} --judge again"
            )
            checks.remove("comprehension")
        else:
            facts_by_pair, fact_warnings = shared_facts(pairs, index, loss_rows)
            warnings += fact_warnings

    raw_path = run_dir / "value-raw.jsonl"
    with hermetic_call("judge-value") as hermetic:
        meta = build_meta(
            reader_model=args.model_reader,
            grader_model=args.model_grader,
            questions_n=args.questions,
            paraphrases_k=args.paraphrases,
            replicates=args.replicates,
            language=args.language,
            answers_sha256=answers_sha256,
            cli_version=claude_version(hermetic.binary, hermetic.env),
        )
        meta_upgraded = False
        if meta_stored is not None:
            stored_design = meta_stored.get("comprehension_design")
            if stored_design not in COMPREHENSION_DESIGNS:
                raise _fail(
                    f"value-raw.jsonl holds the comprehension design {stored_design!r}, "
                    "which this tool does not know; use a newer tool or remove the file"
                )
            transition = stored_design != COMPREHENSION_DESIGN
            match_keys = TRANSITION_MATCH_KEYS if transition else (*META_MATCH_KEYS, "replicates")
            merged, meta_upgraded = reconcile_meta(
                meta,
                meta_stored,
                match_keys=match_keys,
                upgrade_keys=META_UPGRADE_KEYS,
                filename="value-raw.jsonl",
            )
            if transition:
                meta = {
                    **merged,
                    "comprehension_design": COMPREHENSION_DESIGN,
                    "questions": meta["questions"],
                    "replicates": meta["replicates"],
                }
                meta_upgraded = True
            else:
                meta = merged

        with raw_path.open("a", encoding="utf-8") as raw_file:
            if meta_stored is None or meta_upgraded:
                raw_file.write(json.dumps(meta, ensure_ascii=False) + "\n")
                raw_file.flush()

            def sink(row: dict) -> None:
                raw_file.write(json.dumps(row, ensure_ascii=False) + "\n")
                raw_file.flush()

            forced: set[str] = set()
            if args.reuse_from:
                forced = _import_source_rows(args, checks, meta, index, rows, sink, warnings)

            try:
                warnings += run_judges(
                    texts=_texts(pairs, index),
                    pairs=pairs,
                    answers=index,
                    facts_by_pair=facts_by_pair,
                    checks=checks,
                    reader_model=meta["models"]["reader"],
                    grader_model=meta["models"]["grader"],
                    questions_n=meta["questions"],
                    paraphrases_k=meta["paraphrases"],
                    replicates=meta["replicates"],
                    language=meta["language"],
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
    current_index: dict[tuple[str, str | None], dict],
    source_index: dict[tuple[str, str | None], dict],
):
    """The import test for a reader-value row.

    The paraphrase and roundtrip keys carry the text sha. The
    comprehension keys carry the style and the prompt id, so their
    import requires that both arms of the pair hold the same text in
    the source run and in the current run. Only the rows of the
    invoked checks import, so each invocation observes its own
    import and runs its own freshness sample.
    """

    def pair_matches(style: str, prompt_id: str) -> bool:
        for arm_key in ((prompt_id, style), (prompt_id, None)):
            current = current_index.get(arm_key)
            source = source_index.get(arm_key)
            if current is None or source is None or current["sha256"] != source["sha256"]:
                return False
        return True

    def valid(row: dict) -> bool:
        parts = str(row.get("key", "")).split(":")
        if parts[0] in ("paraphrase", "roundtrip"):
            return parts[0] in checks and len(parts) > 2 and parts[2] in current_shas
        if parts[0] == "comprehension":
            if "comprehension" not in checks or len(parts) < 5 or parts[1] != "v3":
                return False
            return pair_matches(parts[3], parts[4])
        return False

    return valid


def _freshness_parser(rows: dict[str, dict]):
    """The verdict parser for a sampled grades row."""

    def parse(row: dict) -> object:
        parts = str(row.get("key", "")).split(":")
        if len(parts) < 5:
            return None
        questions_row = rows.get(f"comprehension:v3:questions:{parts[3]}:{parts[4]}")
        questions = parse_string_list(questions_row["output"]) if questions_row else None
        if not questions:
            return None
        return parse_bools(row["output"], len(questions))

    return parse


def _import_source_rows(args, checks, meta, index, rows, sink, warnings) -> set[str]:
    """Import the reusable source rows; returns the freshness sample keys."""
    source_dir = Path(args.reuse_from)
    source_raw = source_dir / "value-raw.jsonl"
    source_answers_path = source_dir / "answers.jsonl"
    if not source_answers_path.exists():
        raise _fail(f"{source_answers_path}: no answers, so the source directory is not a run")
    source_meta, source_rows = load_raw(source_raw)
    match_keys = ("models", "paraphrases", "language")
    if "comprehension" in checks:
        match_keys += ("questions", "replicates")
    source_meta = check_source_meta(
        source_meta,
        meta,
        match_keys=match_keys,
        upgrade_keys=META_UPGRADE_KEYS,
        source_raw=source_raw,
    )
    if (
        "comprehension" in checks
        and source_meta.get("comprehension_design") != COMPREHENSION_DESIGN
    ):
        raise _fail(
            f"{source_raw} holds the comprehension design "
            f"{source_meta.get('comprehension_design')!r}, not {COMPREHENSION_DESIGN!r}; "
            "reuse needs a source with the same judge conditions"
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
        valid=_row_valid(current_shas, checks, index, source_index),
    )
    if candidates and not imported and not any("reused_from" in row for row in rows.values()):
        warnings.append(
            f"{source_dir}: no stored judge row was reusable for this run; every call runs live"
        )
    return sample_forced_keys(imported, "value")


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-value",
        description=(
            "Check whether the styled answer beats the unstyled answer for "
            "a reader, as win, loss, or tie per gated pair: weak-reader "
            "comprehension, ambiguity through paraphrase, and translation "
            "round-trip. The comprehension questions come from the facts "
            "that both answers share, stored in loss-raw.jsonl, so run "
            "style-loss --judge first. The judges never see a style name "
            "and differ from the writer of the answers."
        ),
    )
    parser.add_argument("run_dir", help="the run directory with answers.jsonl and fidelity.jsonl")
    parser.add_argument("--judge", action="store_true", help="run the live judge calls first")
    parser.add_argument("--model-reader", default="haiku", help="the weak-reader model")
    parser.add_argument("--model-grader", default="opus", help="the question and grading model")
    parser.add_argument(
        "--questions",
        type=int,
        default=6,
        help="questions per pair (cap, split between the fact sources)",
    )
    parser.add_argument("--paraphrases", type=int, default=3, help="restatements per answer")
    parser.add_argument("--replicates", type=int, default=3, help="reader calls per answer")
    parser.add_argument("--language", default="Italian", help="the round-trip language")
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

    raw_path = run_dir / "value-raw.jsonl"
    meta, rows = load_raw(raw_path)
    judge_warnings: list[str] = []
    if args.judge:
        meta, judge_warnings = _judge(args, run_dir, pairs, index, meta, rows, run)
    elif meta is None:
        raise _fail(f"{raw_path}: no judge data; run style-value {run_dir} --judge")

    result = score_checks(
        pairs=pairs,
        answers=index,
        rows=rows,
        paraphrases_k=meta["paraphrases"],
        comprehension_design=meta.get("comprehension_design"),
        replicates=meta.get("replicates", 1),
    )
    raw_calls = read_raw_calls(raw_path)
    freshness, fresh_warnings = freshness_block(raw_calls, _freshness_parser(rows))
    warnings = pair_warnings + judge_warnings + result.warnings + fresh_warnings
    resolved = resolved_models(rows)
    summary = build_value_summary(
        run_name=run_dir.name,
        meta=meta,
        pairs=pairs,
        checks=result.checks,
        warnings=warnings,
        models_resolved={role: resolved.get(alias) for role, alias in meta["models"].items()},
        reuse=reuse_summary(rows, raw_calls, freshness),
    )
    (run_dir / "value.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    own_rows = [row for row in rows.values() if "reused_from" not in row]
    timing = timing_summary(own_rows)
    spend = spend_summary(own_rows)
    report = build_value_report(
        summary, timing, spend, screening=screening_section(_provenance(run_dir))
    )
    (run_dir / "value.md").write_text(report, encoding="utf-8")

    for style in sorted(pairs):
        parts = []
        for check in CHECKS:
            stats = result.checks[check]
            if not stats["judged"]:
                parts.append(f"{check} not judged")
                continue
            per_style = stats["per_style"][style]
            parts.append(f"{check} {per_style['wins']}-{per_style['losses']}-{per_style['ties']}")
        print(f"{style}: " + ", ".join(parts) + " (win-loss-tie)")
    return 0 if not warnings else 1


if __name__ == "__main__":
    sys.exit(main())
