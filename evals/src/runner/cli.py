"""The command-line interface of the pair runner."""

from __future__ import annotations

import argparse
import json
import sys
import threading
from datetime import UTC, datetime
from functools import partial
from pathlib import Path
from string import ascii_lowercase

import yaml

from value.judges import TaskPool

from .generate import GenerationError, Runner, generate, subprocess_runner
from .hermetic import hermetic_call
from .provenance import build_provenance, claude_version
from .report import arm_name, build_report
from .screening import screening_provenance, select_screening_prompts


def load_prompts(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    prompts = data.get("prompts") if isinstance(data, dict) else None
    if not prompts:
        raise SystemExit(f"{path}: no prompts found")
    seen: set[str] = set()
    for prompt in prompts:
        for field in ("id", "type", "text"):
            if not prompt.get(field):
                raise SystemExit(f"{path}: a prompt misses the field {field!r}")
        if prompt["id"] in seen:
            raise SystemExit(f"{path}: duplicate prompt id {prompt['id']!r}")
        seen.add(prompt["id"])
    return prompts


def discover_styles(rules_dir: Path) -> list[str]:
    return sorted(f.name.removesuffix(".rules.yaml") for f in rules_dir.glob("*.rules.yaml"))


def load_existing(answers_path: Path) -> dict[tuple[str, str], dict]:
    existing: dict[tuple[str, str], dict] = {}
    if not answers_path.exists():
        return existing
    for line in answers_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        answer = json.loads(line)
        existing[(answer["prompt_id"], arm_name(answer.get("style")))] = answer
    return existing


def _is_complete(answers_path: Path, arms: list[str | None], prompts: list[dict]) -> bool:
    existing = load_existing(answers_path)
    return all((p["id"], arm_name(s)) in existing for s in arms for p in prompts)


def pick_default_out(
    runs_dir: Path, date: str, arms: list[str | None], prompts: list[dict], suffix: str = ""
) -> Path:
    """The first date-named directory that is not a complete run.

    The bare date counts as the first slot, then the letter suffixes
    b through z. A missing directory and an incomplete run both stop
    the search, so an interrupted run still resumes. Only a complete
    run pushes the runner to the next slot, because a silent reuse of
    a complete run produces no new sample. The suffix names a
    directory family of its own, after the letter: a screening run
    lives under runs/<date>-screening, so the screening picker and
    the full-run picker never meet.
    """
    for letter in ("", *ascii_lowercase[1:]):
        candidate = runs_dir / f"{date}{letter}{suffix}"
        if not _is_complete(candidate / "answers.jsonl", arms, prompts):
            return candidate
    message = f"{runs_dir / (date + suffix)}: every letter suffix holds a complete run; pass --out"
    raise SystemExit(message)


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-pairs",
        description=(
            "Produce, per prompt, one answer per style and one shared unstyled "
            "answer, through the Claude Code CLI. An interrupted run resumes "
            "when the same invocation runs again."
        ),
    )
    parser.add_argument("--prompts", default="prompts/prompts.yaml", help="the prompt set")
    parser.add_argument("--rules-dir", default="rules", help="directory with the rule files")
    parser.add_argument("--plugin-dir", default="../plugin", help="the plugin directory")
    parser.add_argument("--model", default="sonnet", help="model for all answers")
    parser.add_argument("--styles", nargs="*", help="styles to run (default: all rule files)")
    parser.add_argument(
        "--screening",
        action="store_true",
        help=(
            "one reduced run over the fixed prompt subset (2 per type, "
            "seed 0); the run carries a screening mark and never "
            "compares with a full run"
        ),
    )
    parser.add_argument(
        "--out",
        help="run directory (default: runs/<date>, next letter suffix on a same-day repeat)",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=8,
        help="concurrent generation calls (1 runs one call at a time)",
    )
    args = parser.parse_args(argv)
    if args.parallel < 1:
        raise SystemExit(f"--parallel must be 1 or more, not {args.parallel}")

    prompts_path = Path(args.prompts)
    plugin_dir = Path(args.plugin_dir).resolve()
    prompts = load_prompts(prompts_path)
    full_count = len(prompts)
    if args.screening:
        prompts = select_screening_prompts(prompts)
    styles = args.styles or discover_styles(Path(args.rules_dir))
    if not styles:
        raise SystemExit(f"{args.rules_dir}: no rule files found")
    for style in styles:
        style_file = plugin_dir / "output-styles" / f"{style}.md"
        if not style_file.exists():
            raise SystemExit(f"{style_file}: the style file does not exist")

    arms: list[str | None] = [None, *styles]
    suffix = "-screening" if args.screening else ""
    if args.out:
        out = Path(args.out)
    else:
        date = datetime.now(UTC).strftime("%Y-%m-%d")
        out = pick_default_out(Path("runs"), date, arms, prompts, suffix=suffix)
        if out.name != f"{date}{suffix}":
            print(f"runs/{date}{suffix} is complete; starting {out}", file=sys.stderr)

    # The guard classifies a resumed directory by its provenance. A
    # run interrupted before the provenance write has no mark yet;
    # the -screening name family confines that gap to an explicit
    # --out that points a full run at a screening directory, or the
    # reverse. The subset check below closes most of that gap.
    provenance_path = out / "provenance.json"
    if provenance_path.exists():
        stored = json.loads(provenance_path.read_text(encoding="utf-8"))
        if ("screening" in stored) != args.screening:
            mode = "a screening run" if "screening" in stored else "a full run"
            flag = "with" if "screening" in stored else "without"
            raise SystemExit(
                f"{out}: the directory holds {mode}; "
                f"run again {flag} --screening, or pass another --out"
            )

    out.mkdir(parents=True, exist_ok=True)
    answers_path = out / "answers.jsonl"
    existing = load_existing(answers_path)
    if args.screening:
        subset_ids = {prompt["id"] for prompt in prompts}
        stray = sorted({pid for pid, _ in existing if pid not in subset_ids})
        if stray:
            raise SystemExit(
                f"{out}: the answers hold prompts outside the screening subset: {', '.join(stray)}"
            )

    todo = [
        (style, prompt)
        for style in arms
        for prompt in prompts
        if (prompt["id"], arm_name(style)) not in existing
    ]
    skipped = len(arms) * len(prompts) - len(todo)
    if skipped:
        print(f"resuming: {skipped} answer(s) already present", file=sys.stderr)

    failures: list[str] = []
    done = 0
    lock = threading.Lock()
    with (
        answers_path.open("a", encoding="utf-8") as answers_file,
        hermetic_call("pairs") as hermetic,
    ):
        # The calls do not interact: each call is an isolated
        # subprocess, and the workdir stays read-only for the CLI. The
        # lock serializes the append, the progress line, and the
        # failure list, so two rows never interleave. The rows land in
        # completion order, and the loaders read the rows by key, so
        # the row order carries no meaning.
        def generate_one(style: str | None, prompt: dict) -> None:
            nonlocal done
            name = arm_name(style)
            try:
                result = generate(
                    prompt["text"],
                    args.model,
                    style,
                    plugin_dir,
                    hermetic.workdir,
                    run=run,
                    env=hermetic.env,
                )
            except GenerationError as error:
                with lock:
                    done += 1
                    failures.append(f"{name}/{prompt['id']}: {error}")
                    print(
                        f"[{done}/{len(todo)}] {name}: {prompt['id']} failed: {error}",
                        file=sys.stderr,
                    )
                return
            line = {
                "prompt_id": prompt["id"],
                "style": style,
                "answer": result.answer,
                "model": result.resolved_model,
                "models_used": list(result.models_used),
                "plugins": list(result.plugins),
                "claude_code_version": result.claude_code_version,
                "output_tokens": result.output_tokens,
                "input_tokens": result.input_tokens,
                "cache_creation_input_tokens": result.cache_creation_input_tokens,
                "cache_read_input_tokens": result.cache_read_input_tokens,
                "duration_ms": result.duration_ms,
                "wall_ms": result.wall_ms,
            }
            with lock:
                done += 1
                print(f"[{done}/{len(todo)}] {name}: {prompt['id']}", file=sys.stderr)
                answers_file.write(json.dumps(line, ensure_ascii=False) + "\n")
                answers_file.flush()

        pool = TaskPool(args.parallel)
        for style, prompt in todo:
            pool.submit(partial(generate_one, style, prompt))
        pool.drain()
        # The version call needs the live hermetic directory, so it
        # runs before the context closes.
        cli_version = claude_version(hermetic.binary, hermetic.env)

    provenance = build_provenance(
        model=args.model,
        prompts_path=prompts_path,
        styles=styles,
        plugin_dir=plugin_dir,
        cli_version=cli_version,
        claude_binary=hermetic.binary,
        config_manifest_sha256=hermetic.manifest_sha256,
    )
    if args.screening:
        provenance["screening"] = screening_provenance(prompts, full_count)
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    answers = list(load_existing(answers_path).values())
    report = build_report(prompts, styles, answers, provenance, failures)
    (out / "report.md").write_text(report, encoding="utf-8")

    complete = len(answers) == len(arms) * len(prompts)
    status = "complete" if complete else "incomplete"
    print(f"{out}: {len(answers)} answer(s), {len(failures)} failure(s), {status}")
    return 0 if complete and not failures else 1


if __name__ == "__main__":
    sys.exit(main())
