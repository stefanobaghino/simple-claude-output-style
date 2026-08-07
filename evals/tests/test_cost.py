"""Tests for the token-cost report. No test touches the network: the
claude subprocess is replaced with fake runners that return canned
stream-json output."""

import json

import pytest

from cost import analyze_ratios, cli, probe_argv, probe_overhead
from cost.analysis import distribution
from cost.report import SHORTNESS_WARNING
from runner import GenerationError, PluginLeakError
from runner.provenance import sha256_of


def answer(prompt_id, style, output_tokens):
    return {
        "prompt_id": prompt_id,
        "style": style,
        "answer": "x",
        "output_tokens": output_tokens,
    }


def test_pair_ratio_math_is_exact():
    result = analyze_ratios(
        [
            answer("explanation-01", None, 100),
            answer("debugging-01", None, 100),
            answer("explanation-01", "alpha", 50),
            answer("debugging-01", "alpha", 200),
        ]
    )
    stats = result.per_style["alpha"]
    assert stats["pairs"] == 2
    assert stats["styled_output_tokens_total"] == 250
    assert stats["unstyled_output_tokens_total"] == 200
    assert stats["ratio_of_totals"] == 1.25
    assert stats["distribution"]["min"] == 0.5
    assert stats["distribution"]["max"] == 2.0
    assert stats["distribution"]["mean"] == 1.25
    assert result.warnings == []


def test_distribution_stats_on_a_known_list():
    stats = distribution([1.0, 2.0, 3.0, 4.0])
    assert stats == {
        "n": 4,
        "min": 1.0,
        "p25": 1.75,
        "median": 2.5,
        "p75": 3.25,
        "max": 4.0,
        "mean": 2.5,
    }


def test_distribution_collapses_for_a_single_value():
    stats = distribution([1.5])
    assert stats["n"] == 1
    assert stats["min"] == stats["p25"] == stats["median"] == stats["p75"] == stats["max"] == 1.5


def test_task_types_group_by_the_id_prefix():
    result = analyze_ratios(
        [
            answer("explanation-01", None, 100),
            answer("explanation-02", None, 100),
            answer("debugging-01", None, 100),
            answer("explanation-01", "alpha", 50),
            answer("explanation-02", "alpha", 150),
            answer("debugging-01", "alpha", 100),
        ]
    )
    by_type = result.per_style["alpha"]["by_task_type"]
    assert set(by_type) == {"explanation", "debugging"}
    assert by_type["explanation"] == {"n": 2, "min": 0.5, "median": 1.0, "mean": 1.0, "max": 1.5}
    assert by_type["debugging"]["n"] == 1


def test_a_missing_counterpart_warns_and_excludes_the_pair():
    result = analyze_ratios(
        [
            answer("explanation-01", None, 100),
            answer("explanation-01", "alpha", 50),
            answer("debugging-01", "alpha", 80),
            answer("summarization-01", None, 100),
        ]
    )
    stats = result.per_style["alpha"]
    assert stats["pairs"] == 1
    assert any("debugging-01: no unstyled counterpart" in w for w in result.warnings)
    assert any("summarization-01: no styled answer" in w for w in result.warnings)


def test_a_zero_unstyled_count_warns_and_excludes_the_pair():
    result = analyze_ratios(
        [
            answer("explanation-01", None, 0),
            answer("explanation-01", "alpha", 50),
        ]
    )
    assert result.per_style["alpha"]["pairs"] == 0
    assert result.per_style["alpha"]["distribution"] is None
    assert result.per_style["alpha"]["ratio_of_totals"] is None
    assert any("zero output tokens" in w for w in result.warnings)


def make_plugin(root, name="test-plugin", styles=("alpha",)):
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": name}))
    style_dir = root / "output-styles"
    style_dir.mkdir()
    for style in styles:
        (style_dir / f"{style}.md").write_text(f"# {style}\n")
    return root


def style_of(argv):
    settings = json.loads(argv[argv.index("--settings") + 1])
    return settings.get("outputStyle")


def probe_stream(output_style, usage, plugins=("test-plugin",)):
    init = {
        "type": "system",
        "subtype": "init",
        "output_style": output_style,
        "model": "claude-sonnet-5",
        "plugins": [{"name": name} for name in plugins],
    }
    result = {"type": "result", "is_error": False, "result": "OK", "usage": usage}
    return "\n".join(json.dumps(event) for event in (init, result))


UNSTYLED_USAGE = {
    "input_tokens": 10,
    "cache_creation_input_tokens": 100,
    "cache_read_input_tokens": 1000,
    "output_tokens": 1,
}
STYLED_USAGE = {
    "input_tokens": 10,
    "cache_creation_input_tokens": 400,
    "cache_read_input_tokens": 1000,
    "output_tokens": 1,
}


class FakeProbeRunner:
    """Answers each arm with canned usage, keyed off the settings style.

    styled_usages, when set, serves one usage per styled call in order,
    and the last entry repeats, so a test can give the repeats a spread.
    second_unstyled_usage, when set, serves every unstyled call after
    the first.
    """

    def __init__(self, styled_usage=STYLED_USAGE, second_unstyled_usage=None, styled_usages=None):
        self.styled_usage = styled_usage
        self.second_unstyled_usage = second_unstyled_usage
        self.styled_usages = styled_usages
        self.unstyled_calls = 0
        self.styled_calls = 0
        self.calls = []

    def __call__(self, argv, cwd, env=None):
        self.calls.append(argv)
        style = style_of(argv)
        if style == "default":
            self.unstyled_calls += 1
            if self.unstyled_calls > 1 and self.second_unstyled_usage:
                return probe_stream("default", self.second_unstyled_usage)
            return probe_stream("default", UNSTYLED_USAGE)
        self.styled_calls += 1
        if self.styled_usages:
            index = min(self.styled_calls - 1, len(self.styled_usages) - 1)
            return probe_stream(style, self.styled_usages[index])
        return probe_stream(style, self.styled_usage)


def test_probe_rejects_an_undeclared_plugin(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        usage = UNSTYLED_USAGE if style_of(argv) == "default" else STYLED_USAGE
        return probe_stream(style_of(argv), usage, plugins=("test-plugin", "user-plugin"))

    with pytest.raises(PluginLeakError, match="user-plugin"):
        probe_overhead(
            styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=run
        )


def test_probe_argv_loads_the_plugin_on_both_arms(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    unstyled = probe_argv("prompt", "sonnet", None, plugin)
    assert unstyled[unstyled.index("--plugin-dir") + 1] == str(plugin)
    assert style_of(unstyled) == "default"
    styled = probe_argv("prompt", "sonnet", "alpha", plugin)
    assert styled[styled.index("--plugin-dir") + 1] == str(plugin)
    assert style_of(styled) == "test-plugin:alpha"
    assert "--disallowedTools" in styled
    assert "--exclude-dynamic-system-prompt-sections" in styled


def test_probe_measures_the_overhead(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    runner = FakeProbeRunner()
    probe = probe_overhead(
        styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=runner
    )
    assert [arm["arm"] for arm in probe["arms"]] == ["unstyled", "alpha"] * 3
    assert [arm["repeat"] for arm in probe["arms"]] == [0, 0, 1, 1, 2, 2]
    assert probe["repeats"] == 3
    assert probe["unstyled_totals"] == [1110, 1110, 1110]
    tokens = probe["overhead"]["alpha"]["tokens"]
    assert tokens == {
        "n": 3,
        "per_repeat": [300, 300, 300],
        "min": 300,
        "mean": 300,
        "max": 300,
        "stdev": 0.0,
    }
    weighted = probe["overhead"]["alpha"]["weighted"]
    assert weighted["per_repeat"] == [375.0, 375.0, 375.0]
    assert weighted["mean"] == 375.0
    assert probe["price_weights"]["cache_read_input_tokens"] == 0.1
    assert probe["styles"]["alpha"]["sha256"] == sha256_of(plugin / "output-styles" / "alpha.md")
    assert probe["plugin"]["name"] == "test-plugin"
    assert probe["warnings"] == []
    for arm in probe["arms"]:
        assert isinstance(arm["duration_ms"], int)
        assert isinstance(arm["wall_ms"], int)


def test_probe_repeats_give_the_overhead_a_spread(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    creations = (400, 500, 450)
    runner = FakeProbeRunner(
        styled_usages=[dict(STYLED_USAGE, cache_creation_input_tokens=c) for c in creations]
    )
    probe = probe_overhead(
        styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=runner
    )
    tokens = probe["overhead"]["alpha"]["tokens"]
    assert tokens["per_repeat"] == [300, 400, 350]
    assert tokens["mean"] == 350.0
    assert tokens["stdev"] == 50.0
    weighted = probe["overhead"]["alpha"]["weighted"]
    assert weighted["per_repeat"] == [375.0, 500.0, 437.5]
    assert weighted["mean"] == 437.5
    assert weighted["stdev"] == 62.5
    assert probe["warnings"] == []


def test_probe_rejects_a_wrong_active_style(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        return probe_stream("default", UNSTYLED_USAGE)  # the style never activates

    with pytest.raises(GenerationError, match="output style"):
        probe_overhead(
            styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=run
        )


def test_probe_rejects_absent_usage_fields(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")

    def run(argv, cwd, env=None):
        return probe_stream(style_of(argv), {"output_tokens": 1})

    with pytest.raises(GenerationError, match="usage carries no"):
        probe_overhead(
            styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=run
        )


def test_probe_rejects_a_zero_reading(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    zero = {
        "input_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "output_tokens": 1,
    }
    first = iter([zero])

    def run(argv, cwd, env=None):
        default = UNSTYLED_USAGE if style_of(argv) == "default" else STYLED_USAGE
        return probe_stream(style_of(argv), next(first, default))

    with pytest.raises(GenerationError, match="zero input tokens"):
        probe_overhead(
            styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=run
        )


def test_an_unstable_unstyled_total_warns_but_reports(tmp_path):
    plugin = make_plugin(tmp_path / "plugin")
    moved = dict(UNSTYLED_USAGE, cache_creation_input_tokens=150)
    runner = FakeProbeRunner(second_unstyled_usage=moved)
    probe = probe_overhead(
        styles=["alpha"], model="sonnet", plugin_dir=plugin, workdir=tmp_path, run=runner
    )
    assert probe["unstyled_totals"] == [1110, 1160, 1160]
    # Each overhead subtracts the unstyled arm of its own repeat.
    assert probe["overhead"]["alpha"]["tokens"]["per_repeat"] == [300, 250, 250]
    assert any("moved between the probe repeats" in w for w in probe["warnings"])


@pytest.fixture
def project(tmp_path):
    """A run directory with 2 complete pairs, plus the plugin."""
    plugin = make_plugin(tmp_path / "plugin")
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    answers = [
        answer("explanation-01", None, 100),
        answer("debugging-01", None, 100),
        answer("explanation-01", "alpha", 80),
        answer("debugging-01", "alpha", 120),
    ]
    with (run_dir / "answers.jsonl").open("w") as answers_file:
        for line in answers:
            answers_file.write(json.dumps(line) + "\n")
    provenance = {
        "conditions": {"model_requested": "sonnet"},
        "styles": {"alpha": {"sha256": sha256_of(plugin / "output-styles" / "alpha.md")}},
    }
    (run_dir / "provenance.json").write_text(json.dumps(provenance))
    return tmp_path


def run_cli(project, *extra, run=None):
    argv = [str(project / "run"), "--plugin-dir", str(project / "plugin"), *extra]
    return cli.main(argv, run=run or FakeProbeRunner())


def test_cli_without_probe_data_reports_the_ratios_only(project, capsys):
    assert run_cli(project) == 1
    report = (project / "run" / "cost.md").read_text()
    assert "The overhead is not measured" in report
    assert "## Harness spend" not in report
    assert SHORTNESS_WARNING in report
    assert "| explanation | 1 |" in report
    summary = json.loads((project / "run" / "cost.json").read_text())
    assert summary["input_overhead"]["measured"] is False
    assert summary["answer_ratio"]["per_style"]["alpha"]["ratio_of_totals"] == 1.0
    assert any("not measured" in w for w in summary["warnings"])
    assert "alpha: ratio of totals 1.0, overhead not measured" in capsys.readouterr().out


def test_cli_with_probe_writes_both_numbers(project, capsys):
    assert run_cli(project, "--probe") == 0
    probe = json.loads((project / "run" / "cost-probe.json").read_text())
    assert probe["overhead"]["alpha"]["tokens"]["mean"] == 300
    summary = json.loads((project / "run" / "cost.json").read_text())
    overhead = summary["input_overhead"]
    assert overhead["measured"] is True
    assert overhead["repeats"] == 3
    assert overhead["price_weights"]["cache_creation_input_tokens"] == 1.25
    assert overhead["per_style"]["alpha"]["tokens"]["n"] == 3
    assert overhead["per_style"]["alpha"]["tokens"]["mean"] == 300
    assert overhead["per_style"]["alpha"]["weighted"]["mean"] == 375.0
    assert overhead["per_style"]["alpha"]["styled_input_total_mean"] == 1410
    assert overhead["per_style"]["alpha"]["unstyled_input_total_mean"] == 1110
    assert summary["warnings"] == []
    report = (project / "run" / "cost.md").read_text()
    assert "| alpha | 300.0 ± 0.0 | 375.0 ± 0.0 |" in report
    assert "repeats 3." in report
    assert "## Harness spend" in report
    assert (
        "Input tokens: 60 uncached, 1500 cache write, 6000 cache read. Output tokens: 6." in report
    )
    assert SHORTNESS_WARNING in report
    out = capsys.readouterr().out
    assert (
        "alpha: ratio of totals 1.0, overhead mean 300.0 input tokens, weighted mean 375.0" in out
    )


def test_cli_with_one_repeat_reports_no_spread(project):
    assert run_cli(project, "--probe", "--repeats", "1") == 0
    summary = json.loads((project / "run" / "cost.json").read_text())
    tokens = summary["input_overhead"]["per_style"]["alpha"]["tokens"]
    assert tokens["n"] == 1
    assert tokens["stdev"] is None
    report = (project / "run" / "cost.md").read_text()
    assert "| alpha | 300.0 (n = 1) | 375.0 (n = 1) |" in report


def test_cli_rejects_repeats_below_one(project):
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--probe", "--repeats", "0")
    assert error.value.code == 2


def test_cli_reads_a_stored_probe_in_the_old_format(project, capsys):
    old_probe = {
        "date": "2026-08-01T00:00:00+00:00",
        "model_requested": "sonnet",
        "arms": [
            dict(UNSTYLED_USAGE, arm="unstyled", total_input_tokens=1110),
            dict(STYLED_USAGE, arm="alpha", total_input_tokens=1410),
            dict(UNSTYLED_USAGE, arm="unstyled-check", total_input_tokens=1110),
        ],
        "unstyled_totals": [1110, 1110],
        "overhead": {"alpha": 300},
        "styles": {},
        "warnings": [],
    }
    (project / "run" / "cost-probe.json").write_text(json.dumps(old_probe))

    assert run_cli(project) == 0
    summary = json.loads((project / "run" / "cost.json").read_text())
    overhead = summary["input_overhead"]
    assert overhead["repeats"] == 1
    tokens = overhead["per_style"]["alpha"]["tokens"]
    assert tokens == {
        "n": 1,
        "per_repeat": [300],
        "min": 300,
        "mean": 300,
        "max": 300,
        "stdev": None,
    }
    assert overhead["per_style"]["alpha"]["weighted"]["per_repeat"] == [375.0]
    assert "weighted mean 375.0" in capsys.readouterr().out


def test_cli_reuses_the_stored_probe_and_stays_idempotent(project):
    run_cli(project, "--probe")
    first_summary = json.loads((project / "run" / "cost.json").read_text())
    first_report = (project / "run" / "cost.md").read_text()

    assert run_cli(project) == 0  # no --probe: the stored probe data is reused
    second_summary = json.loads((project / "run" / "cost.json").read_text())
    second_report = (project / "run" / "cost.md").read_text()

    first_summary.pop("date")
    second_summary.pop("date")
    assert first_summary == second_summary
    assert first_report == second_report


def test_cli_warns_when_the_probe_and_the_run_differ(project):
    run_cli(project, "--probe")
    style_file = project / "plugin" / "output-styles" / "alpha.md"
    style_file.write_text("# alpha, edited\n")
    provenance = json.loads((project / "run" / "provenance.json").read_text())
    provenance["styles"]["alpha"]["sha256"] = sha256_of(style_file)
    (project / "run" / "provenance.json").write_text(json.dumps(provenance))

    assert run_cli(project) == 1
    summary = json.loads((project / "run" / "cost.json").read_text())
    assert any("differs from the style file of the run" in w for w in summary["warnings"])


def test_cli_cannot_report_without_answers(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_dir)])
    assert error.value.code == 2

    (run_dir / "answers.jsonl").write_text("")
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_dir)])
    assert error.value.code == 2

    (run_dir / "answers.jsonl").write_text(json.dumps(answer("explanation-01", None, 100)) + "\n")
    with pytest.raises(SystemExit) as error:
        cli.main([str(run_dir)])
    assert error.value.code == 2


def test_cli_fails_when_the_probe_fails(project):
    def run(argv, cwd, env=None):
        return probe_stream("default", {"output_tokens": 1})  # no input-token fields

    with pytest.raises(SystemExit) as error:
        run_cli(project, "--probe", run=run)
    assert error.value.code == 2
    assert not (project / "run" / "cost-probe.json").exists()


def test_cli_needs_a_model_for_the_probe(project):
    (project / "run" / "provenance.json").unlink()
    with pytest.raises(SystemExit) as error:
        run_cli(project, "--probe")
    assert error.value.code == 2
