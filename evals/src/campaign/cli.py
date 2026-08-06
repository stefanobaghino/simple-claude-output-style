"""The command-line interface of the campaign driver.

The driver produces N full runs: per run, the pair set, the gate,
and every report, under the schedule that the harness document
describes. The pair stages run one at a time, so the default-out
picker never races. The judge stages overlap, within a run and
across the runs. The value pass splits: the paraphrase check and
the round-trip check run next to the loss pass, because only the
comprehension check reads the loss data, and the comprehension pass
follows the loss pass. The two value invocations of one run never
overlap, because both append to value-raw.jsonl.

Every stage pool takes its size from one worker budget, so the live
worker total stays at or under the budget. A stopped stage runs
once more, because every tool resumes from its stored rows. The
first value invocation of a run exits 1 by construction, because
the comprehension check is not judged yet; the driver records that
exit code but does not count it.

Exit codes: 0 when every stage is done and no counted stage exited
1, 1 when every stage is done but a counted stage exited 1, 2 when
a stage failed, was skipped, or was aborted, or the campaign cannot
start.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import UTC, datetime
from functools import partial
from pathlib import Path

from cost import cli as cost_cli
from gate import cli as gate_cli
from loss import cli as loss_cli
from rank import cli as rank_cli
from runner import cli as runner_cli
from runner.generate import Runner, subprocess_runner
from value import cli as value_cli

from .schedule import DONE, Scheduler, StageKey, StageResult, StageSpec

STAGE_ORDER = ("pairs", "gate", "loss", "value-pr", "value-c", "rank", "cost")

UNCOUNTED = ("value-pr",)
"""Stages whose exit code 1 is structural and thus not counted."""


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def _label(key: StageKey) -> str:
    return f"run {key[1] + 1} {key[0]}"


def build_stages(args, chosen: list[Path | None], run: Runner) -> list[StageSpec]:
    """The stage table: 7 stages per run, wired to the tool mains.

    The chosen list holds the run directory per run index. The pairs
    action fills a missing entry through the default-out picker; the
    picker never races, because the pair stages run one at a time.
    Every downstream action reads the entry at call time, after the
    pairs stage of its run is done.
    """
    prompts = runner_cli.load_prompts(Path(args.prompts))
    styles = runner_cli.discover_styles(Path(args.rules_dir))
    if not styles:
        raise _fail(f"{args.rules_dir}: no rule files found")
    arms: list[str | None] = [None, *styles]

    def pairs_action(index: int, workers: int) -> int:
        if chosen[index] is None:
            date = datetime.now(UTC).strftime("%Y-%m-%d")
            chosen[index] = runner_cli.pick_default_out(Path("runs"), date, arms, prompts)
        argv = [
            "--prompts",
            args.prompts,
            "--rules-dir",
            args.rules_dir,
            "--plugin-dir",
            args.plugin_dir,
            "--model",
            args.model,
            "--out",
            str(chosen[index]),
            "--parallel",
            str(workers),
        ]
        return runner_cli.main(argv, run=run)

    def gate_action(index: int, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--rules-dir",
            args.rules_dir,
            "--gate-config",
            args.gate_config,
        ]
        return gate_cli.main(argv)

    def cost_action(index: int, workers: int) -> int:
        argv = [str(chosen[index]), "--probe", "--plugin-dir", args.plugin_dir]
        return cost_cli.main(argv, run=run)

    def loss_action(index: int, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--judge",
            "--model",
            args.judge_model,
            "--parallel",
            str(workers),
        ]
        return loss_cli.main(argv, run=run)

    def value_action(index: int, checks: str, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--judge",
            "--checks",
            checks,
            "--model-reader",
            args.reader_model,
            "--model-grader",
            args.judge_model,
            "--parallel",
            str(workers),
        ]
        return value_cli.main(argv, run=run)

    def rank_action(index: int, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--judge",
            "--model",
            args.judge_model,
            "--parallel",
            str(workers),
        ]
        return rank_cli.main(argv, run=run)

    pairs_cap = max(1, args.budget // 2)
    judge_cap = max(1, args.budget // 4)
    floor = max(1, min(args.budget // 8, judge_cap))
    stages: list[StageSpec] = []
    for r in range(len(chosen)):
        serial = (("pairs", r - 1),) if r else ()
        stages += [
            StageSpec(
                key=("pairs", r),
                action=partial(pairs_action, r),
                after=serial,
                priority=1,
                cap=pairs_cap,
                floor=floor,
            ),
            StageSpec(key=("gate", r), action=partial(gate_action, r), needs=(("pairs", r),)),
            StageSpec(
                key=("loss", r),
                action=partial(loss_action, r),
                needs=(("gate", r),),
                priority=2,
                cap=judge_cap,
                floor=floor,
            ),
            StageSpec(
                key=("value-pr", r),
                action=partial(value_action, r, "paraphrase,roundtrip"),
                needs=(("gate", r),),
                priority=3,
                cap=judge_cap,
                floor=floor,
            ),
            StageSpec(
                key=("value-c", r),
                action=partial(value_action, r, "comprehension"),
                needs=(("loss", r),),
                after=(("value-pr", r),),
                priority=4,
                cap=judge_cap,
                floor=floor,
            ),
            StageSpec(
                key=("rank", r),
                action=partial(rank_action, r),
                needs=(("gate", r),),
                priority=5,
                cap=judge_cap,
                floor=floor,
            ),
            StageSpec(
                key=("cost", r), action=partial(cost_action, r), needs=(("gate", r),), priority=6
            ),
        ]
    return stages


def build_table(
    results: dict[StageKey, StageResult], chosen: list[Path | None], wall: float, peak: int
) -> str:
    lines = ["run  stage     seconds  exit  attempts  workers  state"]
    for r in range(len(chosen)):
        for name in STAGE_ORDER:
            result = results[(name, r)]
            code = "-" if result.exit_code is None else str(result.exit_code)
            note = f"  {result.detail}" if result.detail else ""
            lines.append(
                f"{r + 1:>3}  {name:<9}{result.wall:>8.1f}  {code:>4}  {result.attempts:>8}"
                f"  {result.workers:>7}  {result.state}{note}"
            )
    lines.append(f"total wall {wall:.0f}s, peak workers {peak}")
    lines.append("the value-pr exit code 1 is structural and is not counted")
    return "\n".join(lines)


def main(argv: list[str] | None = None, run: Runner = subprocess_runner) -> int:
    parser = argparse.ArgumentParser(
        prog="style-campaign",
        description=(
            "Run a campaign: several full pair runs under the documented "
            "schedule, with one worker budget across every stage."
        ),
    )
    count_group = parser.add_mutually_exclusive_group()
    count_group.add_argument("--runs", type=int, default=3, help="number of full runs")
    count_group.add_argument(
        "--dirs", nargs="+", help="explicit run directories (resumes an interrupted campaign)"
    )
    parser.add_argument(
        "--budget", type=int, default=32, help="total live workers across the stages"
    )
    parser.add_argument("--model", default="sonnet", help="writer model for all answers")
    parser.add_argument("--prompts", default="prompts/prompts.yaml", help="the prompt set")
    parser.add_argument("--rules-dir", default="rules", help="directory with the rule files")
    parser.add_argument("--plugin-dir", default="../plugin", help="the plugin directory")
    parser.add_argument("--gate-config", default="rules/gate.yaml", help="the gate policy file")
    parser.add_argument(
        "--judge-model", default="opus", help="judge model for loss, rank, and value grading"
    )
    parser.add_argument(
        "--reader-model", default="haiku", help="the weak-reader model of the value checks"
    )
    args = parser.parse_args(argv)
    if args.budget < 1:
        raise _fail(f"--budget must be 1 or more, not {args.budget}")
    if not args.dirs and args.runs < 1:
        raise _fail(f"--runs must be 1 or more, not {args.runs}")

    chosen: list[Path | None] = [Path(d) for d in args.dirs] if args.dirs else [None] * args.runs

    def on_start(stage: StageSpec, workers: int) -> None:
        print(f"campaign: {_label(stage.key)}: start ({workers} worker(s))", file=sys.stderr)

    def on_end(stage: StageSpec, result: StageResult) -> None:
        if result.state == DONE:
            outcome = f"done in {result.wall:.0f}s (exit {result.exit_code}"
            outcome += f", attempts {result.attempts})" if result.attempts > 1 else ")"
        else:
            outcome = f"{result.state} after {result.attempts} attempt(s)"
            outcome += f": {result.detail}" if result.detail else ""
        print(f"campaign: {_label(stage.key)}: {outcome}", file=sys.stderr)

    stages = build_stages(args, chosen, run)
    scheduler = Scheduler(stages, args.budget, on_start=on_start, on_end=on_end)
    start = time.monotonic()
    results = scheduler.run()
    wall = time.monotonic() - start

    print(build_table(results, chosen, wall, scheduler.peak))
    if any(result.state != DONE for result in results.values()):
        return 2
    counted = [r for key, r in results.items() if key[0] not in UNCOUNTED]
    return 1 if any(result.exit_code == 1 for result in counted) else 0


if __name__ == "__main__":
    sys.exit(main())
