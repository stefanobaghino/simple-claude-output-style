"""Acceptance tests for the linter engine.

The ticket sets the bar per style: the check finds all violations in the
known-dirty sample, and the check reports zero violations on the known-clean
sample and on the traps sample. The clean sample of each style is dirty
under the rules of one designed conflict style, because clean under one
rule set is not automatically dirty under every other; the CONFLICTS map
names the designed pair per style.
"""

from pathlib import Path

import pytest

from linter import Linter, load_rules

HERE = Path(__file__).parent
RULES_DIR = HERE.parent / "rules"
SAMPLES = HERE / "samples"

EXPECTED_DIRTY = {
    "technical-simplified": [
        ("banned-word", "begin"),
        ("banned-word", "utilize"),
        ("banned-word", "ensure"),
        ("banned-modal", "should"),
        ("banned-modal", "could"),
        ("semicolon", ";"),
        ("contraction", "n't"),
        ("latin-abbreviation", "e.g."),
        ("banned-word", "carry out"),
        ("banned-word", "however"),
        ("banned-word", "since"),
    ],
    "plain-language": [
        ("banned-modal", "shall"),
        ("latin-abbreviation", "e.g."),
        ("latin-abbreviation", "i.e."),
        ("and-or", "and/or"),
        ("double-negative", "no fewer than"),
    ],
    "classic-concise": [
        ("needless-phrase", "the fact that"),
        ("banned-word", "very"),
        ("needless-phrase", "the question as to whether"),
        ("banned-word", "certainly"),
        ("needless-phrase", "there is no doubt but that"),
        ("needless-phrase", "in a hasty manner"),
        ("needless-phrase", "one of the most"),
        ("banned-word", "kind of"),
        ("banned-word", "sort of"),
    ],
    "clarity-flow": [
        ("metadiscourse", "it should be noted that"),
        ("banned-word", "made a decision"),
        ("banned-word", "conducted an analysis"),
        ("banned-word", "reached a conclusion"),
        ("banned-word", "carried out an investigation"),
        ("banned-word", "made an assumption"),
        ("metadiscourse", "as previously mentioned"),
        ("banned-word", "give consideration to"),
        ("metadiscourse", "needless to say"),
        ("banned-word", "provide an explanation"),
        ("banned-word", "come to an agreement"),
    ],
    "developer-docs": [
        ("banned-word", "please"),
        ("minimizer", "simply"),
        ("banned-modal", "may"),
        ("banned-modal", "shall"),
        ("minimizer", "obviously"),
        ("latin-abbreviation", "e.g."),
        ("latin-abbreviation", "etc."),
        ("click-here", "click here"),
        ("and-or", "and/or"),
    ],
}

# Violations in the dirty samples beyond the pairs above: the dirty sample of
# technical-simplified holds one over-long sentence.
EXTRA_DIRTY = {
    "technical-simplified": 1,
    "plain-language": 0,
    "classic-concise": 0,
    "clarity-flow": 0,
    "developer-docs": 0,
}

STYLES = sorted(EXPECTED_DIRTY)

# The designed conflict pair per style: the clean sample of the key style is
# dirty under the rules of the value style. Every new clean sample carries a
# contraction (and some a semicolon), so technical-simplified rejects it.
CONFLICTS = {
    "classic-concise": "technical-simplified",
    "clarity-flow": "technical-simplified",
    "developer-docs": "technical-simplified",
    "plain-language": "technical-simplified",
    "technical-simplified": "plain-language",
}


@pytest.fixture(scope="session")
def linters() -> dict[str, Linter]:
    return {style: Linter(load_rules(RULES_DIR / f"{style}.rules.yaml")) for style in STYLES}


@pytest.mark.parametrize("style", STYLES)
def test_clean_sample_has_zero_violations(linters, style):
    report = linters[style].lint_file(SAMPLES / style / "clean.md")
    assert report.violations == []
    assert report.sentence_count > 0
    assert report.rate == 0.0
    assert report.style == style


@pytest.mark.parametrize("style", STYLES)
def test_traps_sample_has_zero_violations(linters, style):
    report = linters[style].lint_file(SAMPLES / style / "traps.md")
    assert report.violations == []


@pytest.mark.parametrize("style", STYLES)
def test_dirty_sample_reports_every_violation(linters, style):
    report = linters[style].lint_file(SAMPLES / style / "dirty.md")
    found = [(v.rule, v.match.lower()) for v in report.violations]
    for expected in EXPECTED_DIRTY[style]:
        assert expected in found, f"missing {expected}"
    assert len(report.violations) == len(EXPECTED_DIRTY[style]) + EXTRA_DIRTY[style]
    assert report.rate > 0


def test_dirty_sample_counts_one_long_sentence(linters):
    style = "technical-simplified"
    report = linters[style].lint_file(SAMPLES / style / "dirty.md")
    assert sum(1 for v in report.violations if v.rule == "sentence-length") == 1


@pytest.mark.parametrize("style", STYLES)
def test_clean_sample_is_dirty_for_the_conflict_style(linters, style):
    other = CONFLICTS[style]
    report = linters[other].lint_file(SAMPLES / style / "clean.md")
    assert report.violations != []


def test_word_exceptions_spare_the_phrase_but_not_the_word(linters):
    linter = linters["technical-simplified"]
    assert linter.lint_text("The sender then follows these steps:").violations == []
    assert linter.lint_text("The main risk is a delay.").violations == []
    flagged = linter.lint_text("Follow the security rules.").violations
    assert [v.match for v in flagged] == ["Follow"]
    flagged = linter.lint_text("The main goal is speed.").violations
    assert [v.match for v in flagged] == ["main"]


def test_rate_is_per_100_sentences(linters):
    report = linters["technical-simplified"].lint_text("You should retry. The test failed.")
    assert report.sentence_count == 2
    assert len(report.violations) == 1
    assert report.rate == 50.0
