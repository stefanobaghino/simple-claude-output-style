"""Tests for the campaign driver. No test touches the network: one
composite fake runner dispatches every CLI call of a campaign to the
fake of the matching tool, and the scheduler tests use stub actions."""

import json
import re
import threading
import time
from datetime import UTC, datetime

import pytest
import yaml
from test_cost import FakeProbeRunner
from test_loss import FakeLossRunner
from test_pairs import make_plugin, stream_output
from test_rank import FakeRankRunner
from test_value import FakeJudgeRunner

from campaign import Scheduler, StageSpec, WorkerGate
from campaign import cli as campaign_cli
from runner import cli as runner_cli
from runner.generate import GenerationError

PROBE_PROMPT = "Reply with the word OK."

VALUE_C_PREFIXES = ("You write a quiz from an answer key", "Answer the questions", "Grade the quiz")
VALUE_PR_PREFIXES = ("Restate the text", "Translate the text below")
LOSS_PREFIXES = (
    "List the distinct factual claims",
    "Check each claim",
    "List the claims",
    "For each uncertain claim",
)
RANK_PREFIX = "Two texts below answer the same request"

CALLS_PER_PAIR_SET = 4  # 2 prompts x (unstyled + alpha)


def style_of(argv):
    settings = json.loads(argv[argv.index("--settings") + 1])
    return settings.get("outputStyle")


class RichLossRunner(FakeLossRunner):
    """Mines 3 facts per direction, and every fact survives.

    The comprehension check skips a pair below 3 shared facts, so the
    campaign fake must mine more than the stock loss fake does.
    """

    def reply(self, prompt):
        if prompt.startswith("List the distinct factual claims"):
            if "fox" in prompt:
                return '["the animal jumps", "the animal is brown", "the animal is quick"]'
            return '["the animal crawls", "the animal is green", "the animal is slow"]'
        if prompt.startswith("Check each claim"):
            return "[true, true, true]"
        return super().reply(prompt)


class CampaignRunner:
    """Dispatches every CLI call of a campaign to the matching fake.

    The generation answers carry a "Run N." marker, so a judge prompt
    that embeds an answer text is attributable to its run. The events
    list holds one (tag, run, start, end) row per call, with run None
    when no marker is present, and the peak counter holds the highest
    number of live calls.
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.value = FakeJudgeRunner()
        self.loss = RichLossRunner()
        self.rank = FakeRankRunner()
        self.probe = FakeProbeRunner()
        self.events = []
        self.generation_calls = 0
        self.live = 0
        self.peak = 0

    def __call__(self, argv, cwd):
        prompt = argv[argv.index("-p") + 1]
        with self.lock:
            self.live += 1
            self.peak = max(self.peak, self.live)
        start = time.monotonic()
        try:
            tag, run_index, reply = self.dispatch(prompt, argv, cwd)
            return reply
        finally:
            end = time.monotonic()
            with self.lock:
                self.live -= 1
                self.events.append((tag, run_index, start, end))

    def dispatch(self, prompt, argv, cwd):
        marker = re.search(r"Run (\d+)\.", prompt)
        run_index = int(marker.group(1)) if marker else None
        if prompt == PROBE_PROMPT:
            return "probe", run_index, self.probe(argv, cwd)
        if prompt.startswith(VALUE_C_PREFIXES):
            return "value-c", run_index, self.value(argv, cwd)
        if prompt.startswith(VALUE_PR_PREFIXES):
            return "value-pr", run_index, self.value(argv, cwd)
        if prompt.startswith(LOSS_PREFIXES):
            return "loss", run_index, self.loss(argv, cwd)
        if prompt.startswith(RANK_PREFIX):
            return "rank", run_index, self.rank(argv, cwd)
        return "pairs", *self.generate(prompt, argv)

    def generate(self, prompt, argv):
        with self.lock:
            run_index = self.generation_calls // CALLS_PER_PAIR_SET
            self.generation_calls += 1
        style = style_of(argv)
        animal = (
            "The slow green turtle crawls" if style == "default" else "The quick brown fox jumps"
        )
        return run_index, stream_output(
            output_style=style or "default", answer=f"{animal}. Run {run_index}."
        )

    def spans(self, tag, run_index):
        return [
            (start, end)
            for row_tag, row_run, start, end in self.events
            if row_tag == tag and row_run == run_index
        ]


@pytest.fixture
def project(tmp_path, monkeypatch):
    """A minimal campaign project: 2 prompts, 1 style, a permissive gate."""
    prompts = {
        "prompts": [
            {"id": "explanation-01", "type": "explanation", "text": "Explain A."},
            {"id": "debugging-01", "type": "debugging", "text": "Debug B."},
        ]
    }
    (tmp_path / "prompts.yaml").write_text(yaml.safe_dump(prompts))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "alpha.rules.yaml").write_text("style: alpha\n")
    (rules / "gate.yaml").write_text(yaml.safe_dump({"thresholds": {"alpha": {"max_rate": 100}}}))
    make_plugin(tmp_path / "plugin")
    monkeypatch.setattr(runner_cli, "claude_version", lambda: "0.0.0 (test)")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def run_campaign(project, runner, *extra):
    return campaign_cli.main(
        [
            "--prompts",
            str(project / "prompts.yaml"),
            "--rules-dir",
            str(project / "rules"),
            "--plugin-dir",
            str(project / "plugin"),
            "--gate-config",
            str(project / "rules" / "gate.yaml"),
            *extra,
        ],
        run=runner,
    )


ARTIFACTS = (
    "answers.jsonl",
    "provenance.json",
    "report.md",
    "fidelity.jsonl",
    "fidelity.json",
    "fidelity.md",
    "cost-probe.json",
    "cost.json",
    "cost.md",
    "loss-raw.jsonl",
    "loss.json",
    "loss.md",
    "value-raw.jsonl",
    "value.json",
    "value.md",
    "rank-raw.jsonl",
    "rank.json",
    "rank.md",
)


def run_dirs(project, count):
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    suffixes = ("", "b", "c")[:count]
    return [project / "runs" / f"{date}{suffix}" for suffix in suffixes]


def test_campaign_produces_two_complete_runs(project):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--runs", "2", "--budget", "8") == 0
    for run_dir in run_dirs(project, 2):
        for artifact in ARTIFACTS:
            assert (run_dir / artifact).exists(), f"{run_dir / artifact} is missing"
        value = json.loads((run_dir / "value.json").read_text())
        assert all(value["checks"][check]["judged"] for check in value["checks"])


def test_campaign_serializes_the_pair_stages(project):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--runs", "2", "--budget", "8") == 0
    first = runner.spans("pairs", 0)
    second = runner.spans("pairs", 1)
    assert len(first) == CALLS_PER_PAIR_SET
    assert len(second) == CALLS_PER_PAIR_SET
    assert max(end for _, end in first) <= min(start for start, _ in second)


def test_campaign_splits_the_value_stage(project):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--runs", "2", "--budget", "8") == 0
    for run_index in (0, 1):
        loss = runner.spans("loss", run_index)
        pr = runner.spans("value-pr", run_index)
        comp = runner.spans("value-c", run_index)
        assert loss and pr and comp
        # The comprehension pass follows the loss pass of its run,
        # and the two value invocations of one run never overlap.
        assert max(end for _, end in loss) <= min(start for start, _ in comp)
        assert max(end for _, end in pr) <= min(start for start, _ in comp)


def test_campaign_holds_the_worker_budget(project):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--runs", "2", "--budget", "4") == 0
    assert runner.peak <= 4


def test_campaign_tail_stage_uses_the_whole_budget(project):
    class TailRunner(CampaignRunner):
        """Blocks every reader call until 3 reader calls are live.

        The fixture produces 12 reader calls, a multiple of 3, so
        every barrier group fills. Under a fixed per-stage share of
        budget // 4 = 1 worker, the barrier can never fill and the
        campaign fails; with the shared gate, the lone comprehension
        stage grows into the idle budget and the barrier releases.
        """

        def __init__(self):
            super().__init__()
            self.barrier = threading.Barrier(3, timeout=30)

        def dispatch(self, prompt, argv, cwd):
            if prompt.startswith("Answer the questions"):
                self.barrier.wait()
            return super().dispatch(prompt, argv, cwd)

    runner = TailRunner()
    assert run_campaign(project, runner, "--runs", "1", "--budget", "4") == 0
    assert runner.peak >= 3


def test_campaign_retries_a_stopped_stage_once(project, capsys):
    class StoppingRunner(CampaignRunner):
        """Fails the first loss extraction twice, past the in-tool retry."""

        def __init__(self):
            super().__init__()
            self.failures_left = 2

        def dispatch(self, prompt, argv, cwd):
            if prompt.startswith("List the distinct factual claims"):
                with self.lock:
                    inject = self.failures_left > 0
                    if inject:
                        self.failures_left -= 1
                if inject:
                    raise GenerationError("injected failure")
            return super().dispatch(prompt, argv, cwd)

    runner = StoppingRunner()
    assert run_campaign(project, runner, "--runs", "1", "--budget", "8") == 0
    assert runner.failures_left == 0
    err = capsys.readouterr().err
    assert re.search(r"run 1 loss: done in \d+s \(exit \d, attempts 2\)", err)


def test_campaign_reports_the_stage_walls(project, capsys):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--runs", "1", "--budget", "8") == 0
    out = capsys.readouterr().out
    assert "run  stage     seconds  exit  attempts  workers  state" in out
    for name in ("pairs", "gate", "loss", "value-pr", "value-c", "rank", "cost"):
        assert re.search(rf"(?m)^  1  {re.escape(name)}\s", out), f"no table row for {name}"
    assert "peak workers" in out
    assert "value-pr exit code 1 is structural" in out


def test_campaign_exit_code_is_one_when_a_stage_warns(project):
    class OneFailedGeneration(CampaignRunner):
        """The first styled generation call comes back unstyled."""

        def __init__(self):
            super().__init__()
            self.failed = False

        def generate(self, prompt, argv):
            if style_of(argv) != "default" and not self.failed:
                self.failed = True
                with self.lock:
                    run_index = self.generation_calls // CALLS_PER_PAIR_SET
                    self.generation_calls += 1
                return run_index, stream_output(output_style="default", answer="unstyled")
            return super().generate(prompt, argv)

    runner = OneFailedGeneration()
    assert run_campaign(project, runner, "--runs", "1", "--budget", "8") == 1
    (run_dir,) = run_dirs(project, 1)
    assert (run_dir / "fidelity.json").exists()
    assert (run_dir / "value.json").exists()


def test_campaign_dirs_flag_resumes_existing_runs(project):
    first = CampaignRunner()
    assert run_campaign(project, first, "--runs", "1", "--budget", "8") == 0
    (run_dir,) = run_dirs(project, 1)

    second = CampaignRunner()
    assert run_campaign(project, second, "--dirs", str(run_dir), "--budget", "8") == 0
    tags = {tag for tag, _, _, _ in second.events}
    assert "pairs" not in tags


def test_campaign_rejects_a_budget_below_one(project):
    with pytest.raises(SystemExit):
        run_campaign(project, CampaignRunner(), "--budget", "0")


def test_campaign_forwards_the_probe_repeats(project):
    runner = CampaignRunner()
    args = ("--runs", "1", "--budget", "8", "--probe-repeats", "2")
    assert run_campaign(project, runner, *args) == 0
    (run_dir,) = run_dirs(project, 1)
    probe = json.loads((run_dir / "cost-probe.json").read_text())
    assert probe["repeats"] == 2
    assert len(runner.spans("probe", None)) == 4  # 2 repeats x 2 arms


def test_campaign_probes_with_three_repeats_without_the_flag(project):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--runs", "1", "--budget", "8") == 0
    (run_dir,) = run_dirs(project, 1)
    probe = json.loads((run_dir / "cost-probe.json").read_text())
    assert probe["repeats"] == 3
    assert len(runner.spans("probe", None)) == 6  # 3 repeats x 2 arms


def test_campaign_rejects_probe_repeats_below_one(project):
    runner = CampaignRunner()
    with pytest.raises(SystemExit) as error:
        run_campaign(project, runner, "--probe-repeats", "0")
    assert error.value.code == 2
    assert runner.events == []


def test_campaign_screening_produces_one_reduced_run(project):
    runner = CampaignRunner()
    assert run_campaign(project, runner, "--screening", "--budget", "8") == 0
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    run_dir = project / "runs" / f"{date}-screening"
    for artifact in ARTIFACTS:
        assert (run_dir / artifact).exists(), f"{run_dir / artifact} is missing"
    provenance = json.loads((run_dir / "provenance.json").read_text())
    assert provenance["screening"] == {
        "prompts_per_type": 2,
        "seed": 0,
        "prompt_ids": ["debugging-01", "explanation-01"],
        "full_prompt_count": 2,
    }
    assert "**Screening run.**" in (run_dir / "rank.md").read_text()
    assert not (project / "runs" / date).exists()


def test_campaign_screening_rejects_an_explicit_runs_count(project):
    with pytest.raises(SystemExit) as error:
        run_campaign(project, CampaignRunner(), "--screening", "--runs", "2")
    assert error.value.code == 2


def test_campaign_dirs_flag_resumes_a_screening_run(project):
    first = CampaignRunner()
    assert run_campaign(project, first, "--screening", "--budget", "8") == 0
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    run_dir = project / "runs" / f"{date}-screening"

    second = CampaignRunner()
    args = ("--dirs", str(run_dir), "--screening", "--budget", "8")
    assert run_campaign(project, second, *args) == 0
    tags = {tag for tag, _, _, _ in second.events}
    assert "pairs" not in tags
    provenance = json.loads((run_dir / "provenance.json").read_text())
    assert "screening" in provenance


# --- Worker gate unit tests: fake runners behind wrapped leases. ---


def in_thread(target):
    thread = threading.Thread(target=target)
    thread.start()
    return thread


def wait_until(condition, timeout=10.0):
    deadline = time.monotonic() + timeout
    while not condition():
        assert time.monotonic() < deadline, "condition not met in time"
        time.sleep(0.001)


def test_gate_lets_a_lone_lease_use_the_whole_budget():
    gate = WorkerGate(4)
    lease = gate.lease("judge", priority=2)
    barrier = threading.Barrier(4, timeout=10)

    def call(argv, cwd):
        barrier.wait()
        return "ok"

    gated = lease.wrap(call)
    threads = [in_thread(lambda: gated([], None)) for _ in range(4)]
    for thread in threads:
        thread.join()
    assert lease.peak == 4
    assert gate.peak == 4
    assert gate.free == 4
    assert lease.live == 0


def test_gate_prefers_the_lower_priority_number():
    gate = WorkerGate(1)
    release = threading.Event()
    done = []

    def holder(argv, cwd):
        release.wait(timeout=10)
        return "ok"

    def call(name):
        def run(argv, cwd):
            done.append(name)
            return "ok"

        return run

    hold = in_thread(lambda: gate.lease("hold", 0).wrap(holder)([], None))
    wait_until(lambda: gate.free == 0)
    late = in_thread(lambda: gate.lease("late", 5).wrap(call("late"))([], None))
    wait_until(lambda: gate.waiting == 1)
    early = in_thread(lambda: gate.lease("early", 1).wrap(call("early"))([], None))
    wait_until(lambda: gate.waiting == 2)
    release.set()
    for thread in (hold, late, early):
        thread.join()
    assert done == ["early", "late"]


def test_gate_keeps_arrival_order_at_equal_priority():
    gate = WorkerGate(1)
    release = threading.Event()
    done = []

    def holder(argv, cwd):
        release.wait(timeout=10)
        return "ok"

    def call(name):
        def run(argv, cwd):
            done.append(name)
            return "ok"

        return run

    hold = in_thread(lambda: gate.lease("hold", 0).wrap(holder)([], None))
    wait_until(lambda: gate.free == 0)
    first = in_thread(lambda: gate.lease("first", 3).wrap(call("first"))([], None))
    wait_until(lambda: gate.waiting == 1)
    second = in_thread(lambda: gate.lease("second", 3).wrap(call("second"))([], None))
    wait_until(lambda: gate.waiting == 2)
    release.set()
    for thread in (hold, first, second):
        thread.join()
    assert done == ["first", "second"]


def test_gate_returns_the_permit_on_an_error():
    gate = WorkerGate(2)
    lease = gate.lease("judge", 1)

    def bad(argv, cwd):
        raise GenerationError("injected failure")

    with pytest.raises(GenerationError):
        lease.wrap(bad)([], None)
    assert gate.free == 2
    assert lease.live == 0


# --- Scheduler unit tests: stub actions, no fakes. ---


def spec(name, run_index=0, **kwargs):
    return StageSpec(key=(name, run_index), **kwargs)


class Recorder:
    def __init__(self):
        self.lock = threading.Lock()
        self.rows = []

    def action(self, name, exit_code=0, delay=0.01, raises=None):
        def act(workers):
            start = time.monotonic()
            time.sleep(delay)
            with self.lock:
                self.rows.append((name, workers, start, time.monotonic()))
            if raises is not None:
                raise raises
            return exit_code

        return act

    def span(self, name):
        rows = [row for row in self.rows if row[0] == name]
        assert rows, f"no recorded call for {name}"
        return rows[-1]


def test_scheduler_runs_dependencies_in_order():
    recorder = Recorder()
    results = Scheduler(
        [
            spec("a", action=recorder.action("a")),
            spec("b", action=recorder.action("b"), needs=(("a", 0),)),
        ],
    ).run()
    assert all(result.state == "done" for result in results.values())
    assert recorder.span("a")[3] <= recorder.span("b")[2]


def test_scheduler_passes_the_threads_value_to_the_action():
    recorder = Recorder()
    results = Scheduler([spec("a", action=recorder.action("a"), threads=5)]).run()
    assert results[("a", 0)].state == "done"
    assert recorder.span("a")[1] == 5


def test_scheduler_retries_a_failure_once_and_not_a_warning():
    attempts = {"failing": 0, "warning": 0}

    def failing(workers):
        attempts["failing"] += 1
        if attempts["failing"] == 1:
            raise SystemExit(2)
        return 0

    def warning(workers):
        attempts["warning"] += 1
        return 1

    results = Scheduler([spec("failing", action=failing), spec("warning", action=warning)]).run()
    assert results[("failing", 0)].state == "done"
    assert results[("failing", 0)].attempts == 2
    assert results[("warning", 0)].state == "done"
    assert results[("warning", 0)].attempts == 1
    assert results[("warning", 0)].exit_code == 1


def test_scheduler_normalizes_a_string_system_exit():
    def bad(workers):
        raise SystemExit("the picker refused")

    results = Scheduler([spec("bad", action=bad)]).run()
    result = results[("bad", 0)]
    assert result.state == "failed"
    assert result.attempts == 2
    assert result.exit_code is None
    assert "the picker refused" in result.detail


def test_scheduler_skips_needs_dependents_and_keeps_after_dependents():
    def fail(workers):
        raise SystemExit(2)

    recorder = Recorder()
    results = Scheduler(
        [
            spec("bad", action=fail),
            spec("dependent", action=recorder.action("dependent"), needs=(("bad", 0),)),
            spec("follower", action=recorder.action("follower"), after=(("bad", 0),)),
        ],
    ).run()
    assert results[("bad", 0)].state == "failed"
    assert results[("dependent", 0)].state == "skipped"
    assert results[("follower", 0)].state == "done"
    assert recorder.span("follower")
