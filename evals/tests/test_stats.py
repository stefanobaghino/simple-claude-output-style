"""Tests for the shared order statistics."""

from runner.stats import nearest_rank


def test_nearest_rank_picks_the_ceiling_rank():
    values = [1.0, 2.0, 3.0, 4.0]
    assert nearest_rank(values, 25) == 1.0
    assert nearest_rank(values, 50) == 2.0
    assert nearest_rank(values, 95) == 4.0
    assert nearest_rank(values, 100) == 4.0


def test_nearest_rank_never_goes_below_the_first_value():
    assert nearest_rank([7.0, 9.0], 0) == 7.0
    assert nearest_rank([7.0], 2.5) == 7.0
