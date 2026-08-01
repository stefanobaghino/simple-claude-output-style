"""Load rule data for a style.

The engine is style-agnostic. All rule content comes from a YAML rule file.
Each style has one rule file in the rules directory, and the header comment
of the rule file documents the exclusions of the style: the rules that need
judgment and thus stay outside the mechanical checks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_UNIVERSAL_POS = {
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SYM",
    "VERB",
    "X",
}


@dataclass(frozen=True)
class WordRule:
    """One entry of the canonical word table."""

    avoid: tuple[str, ...]
    write: str
    pos: frozenset[str] | None = None
    dep: frozenset[str] | None = None
    except_phrases: tuple[str, ...] = ()
    only_before_pos: frozenset[str] | None = None


@dataclass(frozen=True)
class LatinRule:
    avoid: str
    write: str


@dataclass(frozen=True)
class PatternRule:
    """One regex check. The id of the entry becomes the rule name in the report."""

    id: str
    regex: str
    message: str


@dataclass(frozen=True)
class RuleSet:
    style: str
    instruction_limit: int | None
    description_limit: int | None
    banned_modals: frozenset[str]
    permitted_modals: tuple[str, ...]
    check_contractions: bool
    check_semicolons: bool
    latin_abbreviations: tuple[LatinRule, ...]
    patterns: tuple[PatternRule, ...] = field(default=())
    word_rules: tuple[WordRule, ...] = field(default=())


def _parse_word_rule(raw: dict) -> WordRule:
    avoid = raw["avoid"]
    if isinstance(avoid, str):
        avoid = [avoid]
    pos = raw.get("pos")
    if pos is not None:
        unknown = set(pos) - _UNIVERSAL_POS
        if unknown:
            raise ValueError(f"unknown part-of-speech tags {sorted(unknown)} in rule {raw!r}")
    only_before = raw.get("only_before_pos")
    dep = raw.get("dep")
    return WordRule(
        avoid=tuple(str(w).lower() for w in avoid),
        write=str(raw["write"]),
        pos=frozenset(pos) if pos else None,
        dep=frozenset(dep) if dep else None,
        except_phrases=tuple(str(p).lower() for p in raw.get("except_phrases", [])),
        only_before_pos=frozenset(only_before) if only_before else None,
    )


def _parse_pattern_rule(raw: dict) -> PatternRule:
    regex = str(raw["regex"])
    re.compile(regex)  # fail at load time on a bad pattern
    return PatternRule(id=str(raw["id"]), regex=regex, message=str(raw["message"]))


def load_rules(path: str | Path) -> RuleSet:
    """Read a rule file and return the rule set that the engine consumes."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    lengths = raw.get("sentence_length")
    modals = raw.get("modals", {})
    return RuleSet(
        style=str(raw.get("style", "unknown")),
        instruction_limit=int(lengths.get("instruction", 20)) if lengths is not None else None,
        description_limit=int(lengths.get("description", 25)) if lengths is not None else None,
        banned_modals=frozenset(str(m).lower() for m in modals.get("banned", [])),
        permitted_modals=tuple(str(m).lower() for m in modals.get("permitted", [])),
        check_contractions=bool(raw.get("contractions", {}).get("banned", False)),
        check_semicolons=bool(raw.get("semicolons", {}).get("banned", False)),
        latin_abbreviations=tuple(
            LatinRule(avoid=str(e["avoid"]), write=str(e["write"]))
            for e in raw.get("latin_abbreviations", [])
        ),
        patterns=tuple(_parse_pattern_rule(e) for e in raw.get("patterns", [])),
        word_rules=tuple(_parse_word_rule(e) for e in raw.get("words", [])),
    )
