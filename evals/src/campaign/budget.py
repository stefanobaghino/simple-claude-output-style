"""One worker gate across every stage of a campaign.

The bounded resource is the concurrent CLI call. Every live call of
every tool flows through one injected runner, so the gate wraps the
runner: a wrapped call takes a permit before the subprocess starts
and returns the permit when the subprocess ends. Thus the live call
total never rises above the budget, by construction, and an idle
permit is free for any live stage, not only for the stage that held
it earlier. A stage that runs alone in the campaign tail can thus
use the whole budget.

The arbitration is strict priority. When a permit becomes free, the
waiter with the lowest priority number takes it, and waiters with
equal priority proceed in arrival order. Strict priority keeps the
critical path fast and starves only the stages whose work is small.
The starvation is safe: the work is finite, and no waiter holds a
permit, so no cycle can form and every call runs.
"""

from __future__ import annotations

import heapq
import threading

from runner.generate import Runner


class WorkerGate:
    """Meters the live calls of every lease against one budget."""

    def __init__(self, budget: int) -> None:
        self._budget = budget
        self._free = budget
        self._cond = threading.Condition()
        self._waiters: list[tuple[int, int]] = []
        self._ticket = 0
        self.peak = 0

    @property
    def free(self) -> int:
        with self._cond:
            return self._free

    @property
    def waiting(self) -> int:
        with self._cond:
            return len(self._waiters)

    def lease(self, name: str, priority: int = 0) -> WorkerLease:
        return WorkerLease(self, name, priority)

    def acquire(self, priority: int) -> None:
        with self._cond:
            entry = (priority, self._ticket)
            self._ticket += 1
            heapq.heappush(self._waiters, entry)
            while self._free < 1 or self._waiters[0] != entry:
                self._cond.wait()
            heapq.heappop(self._waiters)
            self._free -= 1
            self.peak = max(self.peak, self._budget - self._free)
            # The next waiter can also be eligible when permits remain.
            self._cond.notify_all()

    def release(self) -> None:
        with self._cond:
            self._free += 1
            self._cond.notify_all()


class WorkerLease:
    """The handle of one stage on the gate.

    The lease carries the priority of its stage and counts its own
    live calls, so the campaign report can state the peak that each
    stage held.
    """

    def __init__(self, gate: WorkerGate, name: str, priority: int) -> None:
        self._gate = gate
        self._priority = priority
        self._lock = threading.Lock()
        self.name = name
        self.live = 0
        self.peak = 0

    def wrap(self, run: Runner) -> Runner:
        """Return a runner whose every call holds one gate permit."""

        def gated(argv: list[str], cwd, env=None) -> str:
            self._gate.acquire(self._priority)
            with self._lock:
                self.live += 1
                self.peak = max(self.peak, self.live)
            try:
                return run(argv, cwd, env)
            finally:
                with self._lock:
                    self.live -= 1
                self._gate.release()

        return gated
