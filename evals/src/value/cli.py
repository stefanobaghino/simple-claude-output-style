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
import shutil
import sys
from pathlib import Path

import yaml

from gate.cli import load_answers
from runner.generate import GenerationError, Runner, subprocess_runner
from runner.provenance import sha256_of

from .analysis import score_checks, select_pairs
from .judges import CHECKS, build_meta, run_judges
from .report import build_value_report, build_value_summary

META_MATCH_KEYS = ("models", "questions", "paraphrases", "language", "answers_sha256")


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


def load_prompts(path: Path) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {prompt["id"]: prompt["text"] for prompt in data["prompts"]}


def _answer_index(answers: list[dict]) -> dict[tuple[str, str | None], dict]:
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
    checks = args.check_list

    prompts_by_id = None
    prompts_sha = None
    if "comprehension" in checks:
        prompts_path = Path(args.prompts)
        if not prompts_path.exists():
            raise _fail(f"{prompts_path}: no prompt file; the comprehension check needs it")
        prompts_by_id = load_prompts(prompts_path)
        prompts_sha = sha256_of(prompts_path)
        recorded = (_provenance(run_dir) or {}).get("prompt_set", {}).get("sha256")
        if recorded and recorded != prompts_sha:
            warnings.append("the prompt file differs from the prompt file of the run")
        needed = {prompt_id for ids in pairs.values() for prompt_id in ids}
        missing = sorted(needed - set(prompts_by_id))
        if missing:
            raise _fail(f"{prompts_path}: no prompt text for {', '.join(missing)}")

    meta = build_meta(
        reader_model=args.model_reader,
        grader_model=args.model_grader,
        questions_n=args.questions,
        paraphrases_k=args.paraphrases,
        language=args.language,
        answers_sha256=sha256_of(run_dir / "answers.jsonl"),
        prompts_sha256=prompts_sha,
    )
    if meta_stored is not None:
        mismatched = [key for key in META_MATCH_KEYS if meta_stored.get(key) != meta[key]]
        if mismatched:
            raise _fail(
                f"value-raw.jsonl does not match this invocation on {', '.join(mismatched)}; "
                "remove the file to judge again from scratch"
            )
        meta = meta_stored

    raw_path = run_dir / "value-raw.jsonl"
    workdir = run_dir / ".judge-workdir"
    workdir.mkdir(exist_ok=True)
    with raw_path.open("a", encoding="utf-8") as raw_file:
        if meta_stored is None:
            raw_file.write(json.dumps(meta, ensure_ascii=False) + "\n")
            raw_file.flush()

        def sink(row: dict) -> None:
            raw_file.write(json.dumps(row, ensure_ascii=False) + "\n")
            raw_file.flush()

        try:
            warnings += run_judges(
                texts=_texts(pairs, index),
                prompts_by_id=prompts_by_id,
                checks=checks,
                reader_model=meta["models"]["reader"],
                grader_model=meta["models"]["grader"],
                questions_n=meta["questions"],
                paraphrases_k=meta["paraphrases"],
                language=meta["language"],
                rows=rows,
                sink=sink,
                workdir=workdir,
                run=run,
            )
        except GenerationError as error:
            raise _fail(f"a judge call failed: {error}") from error
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
    return meta, warnings


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-value",
        description=(
            "Check whether the styled answer beats the unstyled answer for "
            "a reader, as win, loss, or tie per gated pair: weak-reader "
            "comprehension, ambiguity through paraphrase, and translation "
            "round-trip. The judges never see a style name and differ from "
            "the writer of the answers."
        ),
    )
    parser.add_argument("run_dir", help="the run directory with answers.jsonl and fidelity.jsonl")
    parser.add_argument("--judge", action="store_true", help="run the live judge calls first")
    parser.add_argument("--model-reader", default="haiku", help="the weak-reader model")
    parser.add_argument("--model-grader", default="opus", help="the question and grading model")
    parser.add_argument("--questions", type=int, default=5, help="questions per prompt")
    parser.add_argument("--paraphrases", type=int, default=3, help="restatements per answer")
    parser.add_argument("--language", default="Italian", help="the round-trip language")
    parser.add_argument(
        "--checks",
        default=",".join(CHECKS),
        help="comma-separated subset of the checks to judge",
    )
    parser.add_argument("--prompts", default="prompts/prompts.yaml", help="the prompt file")
    args = parser.parse_args(argv)

    args.check_list = [check for check in args.checks.split(",") if check]
    unknown = sorted(set(args.check_list) - set(CHECKS))
    if unknown:
        raise _fail(f"unknown check(s): {', '.join(unknown)}; the checks are {', '.join(CHECKS)}")

    run_dir = Path(args.run_dir)
    answers = load_answers(run_dir / "answers.jsonl")
    index = _answer_index(answers)
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

    result = score_checks(pairs=pairs, answers=index, rows=rows, paraphrases_k=meta["paraphrases"])
    warnings = pair_warnings + judge_warnings + result.warnings
    summary = build_value_summary(
        run_name=run_dir.name, meta=meta, pairs=pairs, checks=result.checks, warnings=warnings
    )
    (run_dir / "value.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (run_dir / "value.md").write_text(build_value_report(summary), encoding="utf-8")

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
