"""The command-line interface of the drift measurement.

Exit codes: 0 when every session is complete, every verdict is flat,
and no warnings exist; 1 when the run is scored but a session failed
or is incomplete, a warning exists, or a verdict is "growing"; 2 when
the run cannot run or cannot be scored at all.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from linter import Linter, load_rules
from runner.cli import discover_styles, load_prompts
from runner.generate import GenerationError, Runner, subprocess_runner
from runner.hermetic import hermetic_call
from runner.provenance import build_provenance, claude_version, linter_toolchain, sha256_of
from runner.spend import spend_summary

from .analysis import load_sessions, score_sessions
from .report import build_drift_report, build_drift_summary
from .session import SESSION_FLAGS, deep_script, load_session_script, run_session, session_script


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def _generate(
    args,
    out: Path,
    sessions_path: Path,
    styles: list[str],
    run: Runner,
    scripts: list[dict] | None,
) -> list[str]:
    """Run the missing sessions and write the provenance. Returns the failures."""
    prompts_path: Path | None = None
    prompts: list[dict] = []
    if scripts is None:
        prompts_path = Path(args.prompts)
        if not prompts_path.exists():
            raise _fail(f"{prompts_path}: no prompt file")
        prompts = load_prompts(prompts_path)
        if args.turns > len(prompts):
            raise _fail(
                f"{prompts_path}: {args.turns} turns need {args.turns} prompts, "
                f"but the set holds {len(prompts)}"
            )
    plugin_dir = Path(args.plugin_dir).resolve()
    for style in styles:
        style_file = plugin_dir / "output-styles" / f"{style}.md"
        if not style_file.exists():
            raise _fail(f"{style_file}: the style file does not exist")

    out.mkdir(parents=True, exist_ok=True)
    existing = load_sessions(sessions_path)
    wanted = set(range(1, args.turns + 1))

    failures: list[str] = []
    with (
        sessions_path.open("a", encoding="utf-8") as sessions_file,
        hermetic_call("drift") as hermetic,
    ):
        for style in styles:
            for repeat in range(1, args.repeats + 1):
                present = {turn for (s, r, turn) in existing if s == style and r == repeat}
                if present >= wanted:
                    print(f"skipping {style} session {repeat}: complete", file=sys.stderr)
                    continue
                # An incomplete session restarts from turn 1 with a fresh
                # session id: nothing depends on stored session state
                # across invocations.
                if scripts is None:
                    script = session_script(prompts, args.turns, repeat, args.repeats)
                else:
                    script = deep_script(scripts, repeat)
                print(
                    f"{style} session {repeat}/{args.repeats}: {args.turns} turn(s)",
                    file=sys.stderr,
                )

                def record(turn_number, prompt, turn, style=style, repeat=repeat):
                    row = {
                        "style": style,
                        "repeat": repeat,
                        "turn": turn_number,
                        "prompt_id": prompt["id"],
                        "session_id": turn.session_id,
                        "resume_from": turn.resume_from,
                        "answer": turn.answer,
                        "model": turn.resolved_model,
                        "claude_code_version": turn.claude_code_version,
                        "output_tokens": turn.output_tokens,
                        "input_tokens": turn.input_tokens,
                        "cache_creation_input_tokens": turn.cache_creation_input_tokens,
                        "cache_read_input_tokens": turn.cache_read_input_tokens,
                        "duration_ms": turn.duration_ms,
                        "wall_ms": turn.wall_ms,
                    }
                    sessions_file.write(json.dumps(row, ensure_ascii=False) + "\n")
                    sessions_file.flush()
                    print(f"  [{turn_number}/{args.turns}] {prompt['id']}", file=sys.stderr)

                try:
                    run_session(
                        script,
                        args.model,
                        style,
                        plugin_dir,
                        hermetic.workdir,
                        run,
                        record,
                        env=hermetic.env,
                    )
                except GenerationError as error:
                    failures.append(f"{style}: session {repeat} failed: {error}")
                    print(f"  failed: {error}", file=sys.stderr)
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
    provenance["conditions"]["flags"] = list(SESSION_FLAGS)
    provenance["conditions"]["settings"] = {
        "base": {"disableAllHooks": True},
        "styled_arm": {"outputStyle": "<style>", "extra_flag": "--plugin-dir"},
    }
    repeat_range = range(1, args.repeats + 1)
    if scripts is None:
        # The shallow block stays byte-identical to the pre-script era:
        # the absence of a mode key marks a shallow (or old) run.
        provenance["drift"] = {
            "turns": args.turns,
            "repeats": args.repeats,
            "resume": True,
            "script": {
                str(repeat): [
                    p["id"] for p in session_script(prompts, args.turns, repeat, args.repeats)
                ]
                for repeat in repeat_range
            },
        }
    else:
        provenance["drift"] = {
            "turns": args.turns,
            "repeats": args.repeats,
            "resume": True,
            "mode": "deep",
            "scripts": {
                s["id"]: {"path": s["path"], "sha256": sha256_of(Path(s["path"]))} for s in scripts
            },
            "repeat_scripts": {
                str(repeat): scripts[(repeat - 1) % len(scripts)]["id"] for repeat in repeat_range
            },
            "script": {
                str(repeat): [p["id"] for p in deep_script(scripts, repeat)]
                for repeat in repeat_range
            },
        }
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return failures


def run_toolchain_of(run_dir: Path) -> dict | None:
    provenance_path = run_dir / "provenance.json"
    if not provenance_path.exists():
        return None
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    return provenance.get("linter_toolchain")


def run_mode_of(run_dir: Path) -> str | None:
    """The drift mode of a stored run, or None without a provenance.

    A run from before the deep scripts has no mode key and reads as
    shallow.
    """
    provenance_path = run_dir / "provenance.json"
    if not provenance_path.exists():
        return None
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    return provenance.get("drift", {}).get("mode", "shallow")


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-drift",
        description=(
            "Measure rule obedience across long sessions: run a scripted "
            "session per style several times, lint every turn with the rule "
            "set of the style, and report the violation-rate series over "
            "turn positions with a verdict per style, flat or growing."
        ),
    )
    parser.add_argument("--generate", action="store_true", help="run the missing sessions first")
    parser.add_argument("--prompts", default="prompts/prompts.yaml", help="the prompt set")
    parser.add_argument(
        "--scripts",
        nargs="+",
        help="coherent session scripts for a deep run (default: the shallow rotated prompt set)",
    )
    parser.add_argument("--rules-dir", default="rules", help="directory with the rule files")
    parser.add_argument("--plugin-dir", default="../plugin", help="the plugin directory")
    parser.add_argument("--model", default="sonnet", help="model for all answers")
    parser.add_argument("--styles", nargs="*", help="styles to run (default: all rule files)")
    parser.add_argument("--repeats", type=int, default=3, help="sessions per style")
    parser.add_argument(
        "--turns",
        type=int,
        default=None,
        help="turns per session (default: 15; a deep run takes the script length)",
    )
    parser.add_argument(
        "--slope-threshold",
        type=float,
        default=None,
        help="override the derived per-style threshold, in violations "
        "per 100 sentences per turn (default: the 0.95 quantile of a "
        "per-style permutation null)",
    )
    parser.add_argument("--out", help="run directory (default: runs/<date>-drift)")
    args = parser.parse_args(argv)

    scripts: list[dict] | None = None
    if args.scripts:
        if args.turns is not None:
            raise _fail("--turns does not combine with --scripts: the scripts fix the turn count")
        scripts = []
        for raw in args.scripts:
            path = Path(raw)
            if not path.exists():
                raise _fail(f"{path}: no script file")
            try:
                scripts.append(load_session_script(path))
            except ValueError as error:
                raise _fail(str(error)) from error
        lengths = {script["id"]: len(script["turns"]) for script in scripts}
        if len(set(lengths)) < len(scripts):
            raise _fail("duplicate script ids: every script needs its own id")
        if len(set(lengths.values())) > 1:
            raise _fail(
                "the scripts must share one turn count, because the analysis pools "
                f"by turn position; got {lengths}"
            )
        if args.repeats % len(scripts) != 0:
            raise _fail(
                f"{args.repeats} repeat(s) do not spread evenly over "
                f"{len(scripts)} script(s), so the position-content coupling "
                "would not average cleanly"
            )
        args.turns = len(scripts[0]["turns"])
    elif args.turns is None:
        args.turns = 15

    if args.turns < 2:
        raise _fail("the series needs at least 2 turns")
    rules_dir = Path(args.rules_dir)
    styles = args.styles or discover_styles(rules_dir)
    if not styles:
        raise _fail(f"{rules_dir}: no rule files found")
    rule_files = {style: rules_dir / f"{style}.rules.yaml" for style in styles}
    for style, rule_file in rule_files.items():
        if not rule_file.exists():
            raise _fail(f"{style}: no rule file at {rule_file}")

    suffix = "-drift-deep" if scripts is not None else "-drift"
    out = (
        Path(args.out)
        if args.out
        else Path("runs") / f"{datetime.now(UTC).strftime('%Y-%m-%d')}{suffix}"
    )
    sessions_path = out / "sessions.jsonl"

    run_mode = run_mode_of(out)
    mode = "deep" if scripts is not None else "shallow"
    if run_mode is not None and run_mode != mode:
        raise _fail(f"{out}: the run directory holds a {run_mode} run, but this is a {mode} run")

    failures: list[str] = []
    if args.generate:
        failures = _generate(args, out, sessions_path, styles, run, scripts)

    rows = load_sessions(sessions_path)
    if not rows:
        raise _fail(f"{sessions_path}: no session data; run style-drift --generate")

    linters = {style: Linter(load_rules(rule_file)) for style, rule_file in rule_files.items()}
    result = score_sessions(
        rows=rows,
        linters=linters,
        turns=args.turns,
        repeats=args.repeats,
        threshold=args.slope_threshold,
    )
    if all(stats["complete_sessions"] == 0 for stats in result.styles.values()):
        raise _fail(f"{sessions_path}: no style has a complete session")

    toolchain = linter_toolchain()
    run_toolchain = run_toolchain_of(out)
    warnings = failures + result.warnings
    if run_toolchain is not None and run_toolchain != toolchain:
        warnings.append(
            f"the linter toolchain differs from the run: drift {toolchain}, run {run_toolchain}"
        )

    summary = build_drift_summary(
        run_name=out.name,
        turns=args.turns,
        repeats=args.repeats,
        slope_threshold=args.slope_threshold,
        mode="deep" if scripts is not None else None,
        scripts={
            str(repeat): scripts[(repeat - 1) % len(scripts)]["id"]
            for repeat in range(1, args.repeats + 1)
        }
        if scripts is not None
        else None,
        styles=result.styles,
        rules={
            style: {"file": str(path), "sha256": sha256_of(path)}
            for style, path in rule_files.items()
        },
        toolchain=toolchain,
        run_toolchain=run_toolchain,
        warnings=warnings,
    )
    (out / "drift.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out / "drift.md").write_text(
        build_drift_report(summary, spend_summary(rows.values())), encoding="utf-8"
    )

    growing = False
    for style in sorted(result.styles):
        stats = result.styles[style]
        if stats["complete_sessions"] == 0:
            print(f"{style}: no complete session")
            continue
        growing = growing or stats["verdict"] == "growing"
        print(
            f"{style}: slope {stats['slope']}, threshold {stats['threshold']} "
            f"({stats['threshold_source']}), verdict {stats['verdict']} "
            f"({stats['complete_sessions']}/{args.repeats} session(s))"
        )
    return 0 if not warnings and not growing else 1


if __name__ == "__main__":
    sys.exit(main())
