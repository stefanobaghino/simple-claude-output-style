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
from loss.judges import FACT_MINE
from runner.generate import GenerationError, Runner, subprocess_runner
from runner.hermetic import hermetic_call
from runner.provenance import claude_version, sha256_of
from runner.screening import screening_section
from runner.spend import spend_summary
from runner.timing import timing_summary

from .analysis import score_checks, select_pairs, shared_facts
from .judges import CHECKS, COMPREHENSION_DESIGN, COMPREHENSION_DESIGNS, build_meta, run_judges
from .report import build_value_report, build_value_summary

META_MATCH_KEYS = ("models", "questions", "paraphrases", "language", "answers_sha256")

# On a design transition (a stored design earlier than the current
# one), the comprehension rows rebuild fully under new keys, so the
# questions and the replicates can change. The reuse of the
# paraphrase and roundtrip rows depends only on these keys.
TRANSITION_MATCH_KEYS = ("models", "paraphrases", "language", "answers_sha256")


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


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
            if stored_design != COMPREHENSION_DESIGN:
                match_keys = TRANSITION_MATCH_KEYS
            else:
                match_keys = (*META_MATCH_KEYS, "replicates")
            mismatched = [key for key in match_keys if meta_stored.get(key) != meta[key]]
            if mismatched:
                raise _fail(
                    f"value-raw.jsonl does not match this invocation on {', '.join(mismatched)}; "
                    "remove the file to judge again from scratch"
                )
            if stored_design != COMPREHENSION_DESIGN:
                meta = {
                    **meta_stored,
                    "comprehension_design": COMPREHENSION_DESIGN,
                    "questions": meta["questions"],
                    "replicates": meta["replicates"],
                }
                meta_upgraded = True
            else:
                meta = meta_stored

        with raw_path.open("a", encoding="utf-8") as raw_file:
            if meta_stored is None or meta_upgraded:
                raw_file.write(json.dumps(meta, ensure_ascii=False) + "\n")
                raw_file.flush()

            def sink(row: dict) -> None:
                raw_file.write(json.dumps(row, ensure_ascii=False) + "\n")
                raw_file.flush()

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
                )
            except GenerationError as error:
                raise _fail(f"a judge call failed: {error}") from error
    return meta, warnings


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
    args = parser.parse_args(argv)

    args.check_list = [check for check in args.checks.split(",") if check]
    unknown = sorted(set(args.check_list) - set(CHECKS))
    if unknown:
        raise _fail(f"unknown check(s): {', '.join(unknown)}; the checks are {', '.join(CHECKS)}")
    if args.parallel < 1:
        raise _fail(f"--parallel must be 1 or more, not {args.parallel}")

    run_dir = Path(args.run_dir)
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
    warnings = pair_warnings + judge_warnings + result.warnings
    resolved = resolved_models(rows)
    summary = build_value_summary(
        run_name=run_dir.name,
        meta=meta,
        pairs=pairs,
        checks=result.checks,
        warnings=warnings,
        models_resolved={role: resolved.get(alias) for role, alias in meta["models"].items()},
    )
    (run_dir / "value.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    timing = timing_summary(rows.values())
    spend = spend_summary(rows.values())
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
