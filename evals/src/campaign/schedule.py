"""Run stages with dependencies under one worker budget.

A stage wraps one tool invocation. The scheduler launches a stage
when its dependencies are met and the budget holds enough free
workers, and the worker assignment stays fixed for the life of the
stage. Thus the live worker total never rises above the budget, by
construction, and the peak is a measured number, not a hope.

Two dependency kinds exist. A "needs" dependency is a data
dependency: the stage consumes the output of the other stage, so the
other stage must end in the done state. An "after" dependency is an
ordering dependency: the stage must not overlap the other stage, but
any terminal state of the other stage satisfies it, even a failure.

A stage whose action returns exit code 0 or 1 is done: a warning is
a result, not a stop. A stage whose action raises, or exits with
code 2 or above, failed for this attempt, and the scheduler retries
it once, because every tool resumes from its stored rows. A stage
whose "needs" dependency did not end done is skipped. On a keyboard
interrupt the scheduler stops every launch and retry, waits for the
live stages, and marks the rest aborted; the tools resume on the
next invocation, so an abort loses no data.

The action of a stage runs in a thread. A SystemExit inside a thread
is silently swallowed by the interpreter, so the stage wrapper
catches it and turns its payload into an exit code: an integer
payload is the exit code, and any other payload is a failure.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass

StageKey = tuple[str, int]
"""The stage name plus the run index."""

PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"
SKIPPED = "skipped"
ABORTED = "aborted"

TERMINAL = (DONE, FAILED, SKIPPED, ABORTED)


@dataclass(frozen=True)
class StageSpec:
    """One stage: an action plus its dependencies and its worker needs.

    The action receives the assigned worker count and returns an exit
    code. The cap is the most workers the stage can use, and the
    floor is the fewest free workers at which a launch makes sense;
    the assignment at launch is the free count, clamped to the cap.
    """

    key: StageKey
    action: Callable[[int], int]
    needs: tuple[StageKey, ...] = ()
    after: tuple[StageKey, ...] = ()
    priority: int = 0
    cap: int = 1
    floor: int = 1


@dataclass
class StageResult:
    state: str = PENDING
    exit_code: int | None = None
    attempts: int = 0
    workers: int = 0
    wall: float = 0.0
    detail: str = ""


StartHook = Callable[[StageSpec, int], None]
EndHook = Callable[[StageSpec, StageResult], None]


class Scheduler:
    """Runs a fixed stage set to completion under the budget."""

    def __init__(
        self,
        stages: list[StageSpec],
        budget: int,
        on_start: StartHook | None = None,
        on_end: EndHook | None = None,
    ) -> None:
        keys = [stage.key for stage in stages]
        if len(set(keys)) != len(keys):
            raise ValueError("duplicate stage keys")
        known = set(keys)
        for stage in stages:
            for dep in (*stage.needs, *stage.after):
                if dep not in known:
                    raise ValueError(f"{stage.key}: unknown dependency {dep}")
            if not 1 <= stage.floor <= stage.cap:
                raise ValueError(f"{stage.key}: the floor must be within [1, cap]")
            if stage.floor > budget:
                raise ValueError(f"{stage.key}: the floor is above the budget {budget}")
        self._stages = {stage.key: stage for stage in stages}
        self._results = {stage.key: StageResult() for stage in stages}
        self._budget = budget
        self._free = budget
        self.peak = 0
        self._cond = threading.Condition()
        self._aborted = False
        self._on_start = on_start
        self._on_end = on_end

    def run(self) -> dict[StageKey, StageResult]:
        """Run every stage to a terminal state and return the results."""
        threads: list[threading.Thread] = []
        try:
            with self._cond:
                while True:
                    self._skip_blocked()
                    self._launch_ready(threads)
                    states = [result.state for result in self._results.values()]
                    if all(state in TERMINAL for state in states):
                        break
                    if RUNNING not in states and PENDING in states:
                        pending = [k for k, r in self._results.items() if r.state == PENDING]
                        raise RuntimeError(f"no stage can launch, but {pending} are pending")
                    self._cond.wait()
        except KeyboardInterrupt:
            with self._cond:
                self._aborted = True
            for thread in threads:
                thread.join()
            with self._cond:
                for result in self._results.values():
                    if result.state == PENDING:
                        result.state = ABORTED
        for thread in threads:
            thread.join()
        return dict(self._results)

    def _skip_blocked(self) -> None:
        # Runs until no new skip appears, because a skip can block a
        # dependent of the skipped stage in the same pass.
        changed = True
        while changed:
            changed = False
            for key, stage in self._stages.items():
                result = self._results[key]
                if result.state != PENDING:
                    continue
                dep_states = [self._results[dep].state for dep in stage.needs]
                if any(state in (FAILED, SKIPPED, ABORTED) for state in dep_states):
                    result.state = SKIPPED
                    changed = True

    def _launch_ready(self, threads: list[threading.Thread]) -> None:
        if self._aborted:
            return
        ready = [
            stage
            for key, stage in self._stages.items()
            if self._results[key].state == PENDING
            and all(self._results[dep].state == DONE for dep in stage.needs)
            and all(self._results[dep].state in TERMINAL for dep in stage.after)
        ]
        ready.sort(key=lambda stage: (stage.priority, stage.key[1]))
        for stage in ready:
            if self._free < stage.floor:
                continue
            workers = min(stage.cap, self._free)
            self._free -= workers
            self.peak = max(self.peak, self._budget - self._free)
            result = self._results[stage.key]
            result.state = RUNNING
            result.workers = workers
            thread = threading.Thread(
                target=self._run_stage, args=(stage, workers), name=f"stage-{stage.key}"
            )
            threads.append(thread)
            thread.start()

    def _run_stage(self, stage: StageSpec, workers: int) -> None:
        if self._on_start is not None:
            self._on_start(stage, workers)
        result = self._results[stage.key]
        start = time.monotonic()
        state = FAILED
        code: int | None = None
        for attempt in (1, 2):
            result.attempts = attempt
            code, detail = self._attempt(stage, workers)
            if code is not None and code <= 1:
                state = DONE
                result.detail = ""
                break
            result.detail = detail
            with self._cond:
                if self._aborted:
                    break
        result.wall = time.monotonic() - start
        result.exit_code = code
        with self._cond:
            result.state = state
            self._free += workers
            self._cond.notify_all()
        if self._on_end is not None:
            self._on_end(stage, result)

    def _attempt(self, stage: StageSpec, workers: int) -> tuple[int | None, str]:
        try:
            return stage.action(workers), ""
        except SystemExit as error:
            if isinstance(error.code, int):
                return error.code, ""
            return None, str(error.code or "")[:200]
        except Exception as error:  # noqa: BLE001 -- a stage must never kill the campaign
            return None, f"{type(error).__name__}: {error}"[:200]
