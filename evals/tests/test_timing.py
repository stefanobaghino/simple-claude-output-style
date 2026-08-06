"""Tests for the shared call-timing summarizer."""

from runner.timing import timing_section, timing_summary


def test_summary_means_over_the_measured_rows():
    rows = [
        {"duration_ms": 100, "wall_ms": 350},
        {"duration_ms": 200, "wall_ms": 450},
    ]
    assert timing_summary(rows) == {
        "calls": 2,
        "measured": 2,
        "mean_duration_ms": 150,
        "mean_wall_ms": 400,
        "mean_startup_ms": 250,
    }


def test_summary_counts_every_call_but_measures_only_the_wall_rows():
    rows = [
        {"duration_ms": 100, "wall_ms": 350},
        {"duration_ms": 999},
    ]
    timing = timing_summary(rows)
    assert timing["calls"] == 2
    assert timing["measured"] == 1
    assert timing["mean_duration_ms"] == 100
    assert timing["mean_wall_ms"] == 350
    assert timing["mean_startup_ms"] == 250


def test_summary_without_a_measured_row_has_no_means():
    assert timing_summary([{"duration_ms": 100}]) == {
        "calls": 1,
        "measured": 0,
        "mean_duration_ms": None,
        "mean_wall_ms": None,
        "mean_startup_ms": None,
    }


def test_summary_of_zero_rows_is_none():
    assert timing_summary([]) is None


def test_section_states_the_means():
    text = "\n".join(timing_section(timing_summary([{"duration_ms": 100, "wall_ms": 350}])))
    assert "## Call timing" in text
    assert "Calls: 1, measured: 1." in text
    assert "Mean duration: 100 ms." in text
    assert "Mean wall: 350 ms." in text
    assert "Mean startup: 250 ms." in text


def test_section_states_not_measured_without_a_wall_row():
    for timing in (None, timing_summary([{"duration_ms": 100}])):
        text = "\n".join(timing_section(timing))
        assert "## Call timing" in text
        assert "The wall is not measured" in text
