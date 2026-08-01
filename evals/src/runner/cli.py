"""The command-line interface of the pair runner."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

from .generate import GenerationError, Runner, generate, subprocess_runner
from .provenance import build_provenance, claude_version
from .report import arm_name, build_report


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
    parser.add_argument("--out", help="run directory (default: runs/<date>)")
    args = parser.parse_args(argv)

    prompts_path = Path(args.prompts)
    plugin_dir = Path(args.plugin_dir).resolve()
    prompts = load_prompts(prompts_path)
    styles = args.styles or discover_styles(Path(args.rules_dir))
    if not styles:
        raise SystemExit(f"{args.rules_dir}: no rule files found")
    for style in styles:
        style_file = plugin_dir / "output-styles" / f"{style}.md"
        if not style_file.exists():
            raise SystemExit(f"{style_file}: the style file does not exist")

    out = Path(args.out) if args.out else Path("runs") / datetime.now(UTC).strftime("%Y-%m-%d")
    out.mkdir(parents=True, exist_ok=True)
    answers_path = out / "answers.jsonl"
    existing = load_existing(answers_path)
    workdir = out / ".workdir"
    workdir.mkdir(exist_ok=True)

    arms: list[str | None] = [None, *styles]
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
    with answers_path.open("a", encoding="utf-8") as answers_file:
        for index, (style, prompt) in enumerate(todo, start=1):
            name = arm_name(style)
            print(f"[{index}/{len(todo)}] {name}: {prompt['id']}", file=sys.stderr)
            try:
                result = generate(prompt["text"], args.model, style, plugin_dir, workdir, run=run)
            except GenerationError as error:
                failures.append(f"{name}/{prompt['id']}: {error}")
                print(f"  failed: {error}", file=sys.stderr)
                continue
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
            }
            answers_file.write(json.dumps(line, ensure_ascii=False) + "\n")
            answers_file.flush()
    shutil.rmtree(workdir, ignore_errors=True)

    provenance = build_provenance(
        model=args.model,
        prompts_path=prompts_path,
        styles=styles,
        plugin_dir=plugin_dir,
        cli_version=claude_version(),
    )
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
