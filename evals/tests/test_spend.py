"""Tests for the shared token-spend summarizer."""

from runner.spend import spend_section, spend_summary

ROW = {
    "input_tokens": 3,
    "cache_creation_input_tokens": 2,
    "cache_read_input_tokens": 1,
    "output_tokens": 7,
}


def test_summary_totals_over_the_measured_rows():
    rows = [dict(ROW), dict(ROW, cache_read_input_tokens=13, output_tokens=11)]
    assert spend_summary(rows) == {
        "calls": 2,
        "measured": 2,
        "input_tokens": 6,
        "cache_creation_input_tokens": 4,
        "cache_read_input_tokens": 14,
        "output_tokens": 18,
        "cache_read_share": 0.583,
    }


def test_summary_counts_every_call_but_measures_only_the_token_rows():
    rows = [dict(ROW), {"output_tokens": 999}]
    spend = spend_summary(rows)
    assert spend["calls"] == 2
    assert spend["measured"] == 1
    assert spend["input_tokens"] == 3
    assert spend["output_tokens"] == 7
    assert spend["cache_read_share"] == 0.167


def test_summary_without_a_measured_row_has_no_totals():
    assert spend_summary([{"output_tokens": 5}]) == {
        "calls": 1,
        "measured": 0,
        "input_tokens": None,
        "cache_creation_input_tokens": None,
        "cache_read_input_tokens": None,
        "output_tokens": None,
        "cache_read_share": None,
    }


def test_summary_of_zero_rows_is_none():
    assert spend_summary([]) is None


def test_a_zero_input_total_has_no_share():
    zero = dict.fromkeys(ROW, 0)
    assert spend_summary([zero])["cache_read_share"] is None


def test_section_states_the_totals():
    text = "\n".join(spend_section(spend_summary([dict(ROW)])))
    assert "## Harness spend" in text
    assert "Calls: 1, measured: 1." in text
    assert "Input tokens: 3 uncached, 2 cache write, 1 cache read. Output tokens: 7." in text
    assert "Cache-read share: 0.167." in text


def test_section_states_not_measured_without_a_token_row():
    for spend in (None, spend_summary([{"output_tokens": 5}])):
        text = "\n".join(spend_section(spend))
        assert "## Harness spend" in text
        assert "The spend is not measured" in text
