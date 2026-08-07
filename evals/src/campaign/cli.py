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

One worker gate meters every CLI call, so the live call total stays
at or under the budget, and a stage that runs alone can use the
whole budget. A stopped stage runs
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
from runner.screening import select_screening_prompts
from value import cli as value_cli

from .budget import WorkerGate, WorkerLease
from .schedule import DONE, Scheduler, StageKey, StageResult, StageSpec

STAGE_ORDER = ("pairs", "gate", "loss", "value-pr", "value-c", "rank", "cost")

UNCOUNTED = ("value-pr",)
"""Stages whose exit code 1 is structural and thus not counted."""


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def _label(key: StageKey) -> str:
    return f"run {key[1] + 1} {key[0]}"


def build_stages(
    args, chosen: list[Path | None], run: Runner, gate: WorkerGate
) -> tuple[list[StageSpec], dict[StageKey, WorkerLease]]:
    """The stage table: 7 stages per run, wired to the tool mains.

    The chosen list holds the run directory per run index. The pairs
    action fills a missing entry through the default-out picker; the
    picker never races, because the pair stages run one at a time.
    Every downstream action reads the entry at call time, after the
    pairs stage of its run is done.

    Every stage that makes CLI calls gets one lease on the gate, at
    the priority of the stage, and its action runs the tool with the
    gated runner of that lease. The threads value is the pool size
    inside the tool: the judge stages get the whole budget, so a
    lone stage can grow to the budget, and the pairs stage gets half
    the budget, so the top-priority pairs calls never crowd out the
    judge stages of the earlier runs.
    """
    prompts = runner_cli.load_prompts(Path(args.prompts))
    if args.screening:
        prompts = select_screening_prompts(prompts)
    styles = runner_cli.discover_styles(Path(args.rules_dir))
    if not styles:
        raise _fail(f"{args.rules_dir}: no rule files found")
    arms: list[str | None] = [None, *styles]
    suffix = "-screening" if args.screening else ""

    def pairs_action(index: int, run: Runner, workers: int) -> int:
        if chosen[index] is None:
            date = datetime.now(UTC).strftime("%Y-%m-%d")
            chosen[index] = runner_cli.pick_default_out(
                Path("runs"), date, arms, prompts, suffix=suffix
            )
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
        if args.screening:
            argv.append("--screening")
        return runner_cli.main(argv, run=run)

    def gate_action(index: int, _run: Runner, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--rules-dir",
            args.rules_dir,
            "--gate-config",
            args.gate_config,
        ]
        return gate_cli.main(argv)

    def cost_action(index: int, run: Runner, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--probe",
            "--plugin-dir",
            args.plugin_dir,
            "--repeats",
            str(args.probe_repeats),
        ]
        return cost_cli.main(argv, run=run)

    def loss_action(index: int, run: Runner, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--judge",
            "--model",
            args.judge_model,
            "--parallel",
            str(workers),
        ]
        return loss_cli.main(argv, run=run)

    def value_action(index: int, run: Runner, workers: int, *, checks: str) -> int:
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

    def rank_action(index: int, run: Runner, workers: int) -> int:
        argv = [
            str(chosen[index]),
            "--judge",
            "--model",
            args.judge_model,
            "--parallel",
            str(workers),
        ]
        return rank_cli.main(argv, run=run)

    pairs_threads = max(1, args.budget // 2)
    actions = {
        "pairs": pairs_action,
        "gate": gate_action,
        "loss": loss_action,
        "value-pr": partial(value_action, checks="paraphrase,roundtrip"),
        "value-c": partial(value_action, checks="comprehension"),
        "rank": rank_action,
        "cost": cost_action,
    }
    priorities = {
        "pairs": 1,
        "gate": 0,
        "loss": 2,
        "value-pr": 3,
        "value-c": 4,
        "rank": 5,
        "cost": 6,
    }
    budget = args.budget
    threads = {
        "pairs": pairs_threads,
        "gate": 1,
        "loss": budget,
        "value-pr": budget,
        "value-c": budget,
        "rank": budget,
        "cost": 1,
    }

    stages: list[StageSpec] = []
    leases: dict[StageKey, WorkerLease] = {}
    for r in range(len(chosen)):
        deps: dict[str, dict] = {
            "pairs": {"after": (("pairs", r - 1),) if r else ()},
            "gate": {"needs": (("pairs", r),)},
            "loss": {"needs": (("gate", r),)},
            "value-pr": {"needs": (("gate", r),)},
            "value-c": {"needs": (("loss", r),), "after": (("value-pr", r),)},
            "rank": {"needs": (("gate", r),)},
            "cost": {"needs": (("gate", r),)},
        }
        for name in STAGE_ORDER:
            key = (name, r)
            if name == "gate":
                gated_run = run
            else:
                leases[key] = gate.lease(_label(key), priorities[name])
                gated_run = leases[key].wrap(run)
            stages.append(
                StageSpec(
                    key=key,
                    action=partial(actions[name], r, gated_run),
                    priority=priorities[name],
                    threads=threads[name],
                    **deps[name],
                )
            )
    return stages, leases


def build_table(
    results: dict[StageKey, StageResult],
    chosen: list[Path | None],
    leases: dict[StageKey, WorkerLease],
    wall: float,
    peak: int,
) -> str:
    lines = ["run  stage     seconds  exit  attempts  workers  state"]
    for r in range(len(chosen)):
        for name in STAGE_ORDER:
            key = (name, r)
            result = results[key]
            code = "-" if result.exit_code is None else str(result.exit_code)
            note = f"  {result.detail}" if result.detail else ""
            held = leases[key].peak if key in leases else 0
            lines.append(
                f"{r + 1:>3}  {name:<9}{result.wall:>8.1f}  {code:>4}  {result.attempts:>8}"
                f"  {held:>7}  {result.state}{note}"
            )
    lines.append(f"total wall {wall:.0f}s, peak workers {peak}")
    lines.append("the workers column is the observed peak of live calls per stage")
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
    count_group.add_argument(
        "--runs", type=int, help="number of runs (default 3, or 1 with --screening)"
    )
    count_group.add_argument(
        "--dirs",
        nargs="+",
        help=(
            "explicit run directories (resumes an interrupted campaign; "
            "resume a screening campaign with --screening as well)"
        ),
    )
    parser.add_argument(
        "--screening",
        action="store_true",
        help=(
            "screen a candidate style: one reduced run over the fixed "
            "prompt subset (implies --runs 1)"
        ),
    )
    parser.add_argument(
        "--budget", type=int, default=32, help="total live workers across the stages"
    )
    parser.add_argument(
        "--probe-repeats",
        type=int,
        default=3,
        help="probe calls per arm in the cost stage (forwarded to style-cost --repeats)",
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
    if args.probe_repeats < 1:
        raise _fail(f"--probe-repeats must be 1 or more, not {args.probe_repeats}")
    if args.screening and args.runs not in (None, 1):
        raise _fail(f"--screening implies --runs 1, not {args.runs}")
    if args.runs is None:
        args.runs = 1 if args.screening else 3
    if not args.dirs and args.runs < 1:
        raise _fail(f"--runs must be 1 or more, not {args.runs}")

    chosen: list[Path | None] = [Path(d) for d in args.dirs] if args.dirs else [None] * args.runs

    def on_start(stage: StageSpec) -> None:
        print(f"campaign: {_label(stage.key)}: start ({stage.threads} thread(s))", file=sys.stderr)

    def on_end(stage: StageSpec, result: StageResult) -> None:
        if result.state == DONE:
            outcome = f"done in {result.wall:.0f}s (exit {result.exit_code}"
            outcome += f", attempts {result.attempts})" if result.attempts > 1 else ")"
        else:
            outcome = f"{result.state} after {result.attempts} attempt(s)"
            outcome += f": {result.detail}" if result.detail else ""
        print(f"campaign: {_label(stage.key)}: {outcome}", file=sys.stderr)

    gate = WorkerGate(args.budget)
    stages, leases = build_stages(args, chosen, run, gate)
    scheduler = Scheduler(stages, on_start=on_start, on_end=on_end)
    start = time.monotonic()
    results = scheduler.run()
    wall = time.monotonic() - start

    print(build_table(results, chosen, leases, wall, gate.peak))
    if any(result.state != DONE for result in results.values()):
        return 2
    counted = [r for key, r in results.items() if key[0] not in UNCOUNTED]
    return 1 if any(result.exit_code == 1 for result in counted) else 0


if __name__ == "__main__":
    sys.exit(main())
