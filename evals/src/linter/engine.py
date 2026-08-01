"""The linter engine.

The engine is deterministic: same text, same rule file, same model version,
same report. All rule content comes from the rule file. The engine only knows
the check types:

- banned-word: the canonical word table
- banned-modal: modal verbs, matched on the modal tag only
- contraction: clitics such as "n't" and "'re" (the possessive 's stays legal)
- semicolon: semicolons outside code
- latin-abbreviation: abbreviations such as "e.g."
- sentence-length: word limits, 1 placeholder counts as 1 word
- patterns: regex checks from the rule file, with the entry id as rule name

A rule set enables a subset of the checks. Rules that need judgment are out
of scope for every style; each rule file documents the exclusions of its
style. The fidelity score covers only the enabled checks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import spacy
from spacy.tokens import Span, Token

from .extract import PLACEHOLDER, extract_segments
from .rules import RuleSet, WordRule

SPACY_MODEL = "en_core_web_sm"

# Clitics that spaCy splits off a contraction. "'ll" and "'d" stand for the
# modals "will" and "would", but the contraction check flags them first.
_CONTRACTION_PARTS = {"n't", "'re", "'ve", "'ll", "'d", "'m"}


@dataclass(frozen=True)
class Violation:
    rule: str
    match: str
    message: str
    file: str
    line: int
    sentence: str

    def as_dict(self) -> dict:
        return {
            "rule": self.rule,
            "match": self.match,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "sentence": self.sentence,
        }


@dataclass
class Report:
    file: str
    style: str
    violations: list[Violation]
    sentence_count: int

    @property
    def rate(self) -> float:
        """Violations per 100 sentences."""
        if self.sentence_count == 0:
            return 0.0
        return 100.0 * len(self.violations) / self.sentence_count

    def as_dict(self) -> dict:
        return {
            "file": self.file,
            "style": self.style,
            "sentences": self.sentence_count,
            "violations": [v.as_dict() for v in self.violations],
            "rate": round(self.rate, 2),
        }


def _latin_pattern(avoid: str) -> re.Pattern:
    core = re.escape(avoid.rstrip("."))
    return re.compile(rf"(?<![\w.]){core}(?:\.|\b)", re.IGNORECASE)


class Linter:
    def __init__(self, rules: RuleSet):
        self.rules = rules
        self.nlp = spacy.load(SPACY_MODEL, exclude=["ner"])
        self._latin = [(rule, _latin_pattern(rule.avoid)) for rule in rules.latin_abbreviations]
        self._patterns = [(rule, re.compile(rule.regex, re.IGNORECASE)) for rule in rules.patterns]
        if rules.permitted_modals:
            permitted = ", ".join(rules.permitted_modals)
            self._modal_message = 'Do not use the modal verb "{word}". Use only: ' + permitted + "."
        else:
            self._modal_message = 'Do not use the modal verb "{word}".'
        self._single: dict[str, list[WordRule]] = {}
        self._multi: dict[str, list[WordRule]] = {}
        for rule in rules.word_rules:
            table = self._single if len(rule.avoid) == 1 else self._multi
            table.setdefault(rule.avoid[0], []).append(rule)

    def lint_file(self, path: str | Path) -> Report:
        text = Path(path).read_text(encoding="utf-8")
        return self.lint_text(text, file=str(path))

    def lint_text(self, text: str, file: str = "<text>") -> Report:
        violations: list[Violation] = []
        sentence_count = 0
        for segment in extract_segments(text):
            for rule, pattern in self._latin:
                for match in pattern.finditer(segment.text):
                    violations.append(
                        Violation(
                            rule="latin-abbreviation",
                            match=match.group(0),
                            message=f'Do not write "{rule.avoid}". Write "{rule.write}".',
                            file=file,
                            line=segment.line,
                            sentence=segment.text,
                        )
                    )
            for rule, pattern in self._patterns:
                for match in pattern.finditer(segment.text):
                    violations.append(
                        Violation(
                            rule=rule.id,
                            match=match.group(0),
                            message=rule.message,
                            file=file,
                            line=segment.line,
                            sentence=segment.text,
                        )
                    )
            doc = self.nlp(segment.text)
            for sentence in doc.sents:
                sentence_count += 1
                violations.extend(self._check_sentence(sentence, file, segment.line))
        return Report(
            file=file,
            style=self.rules.style,
            violations=violations,
            sentence_count=sentence_count,
        )

    def _check_sentence(self, sentence: Span, file: str, line: int) -> list[Violation]:
        found: list[Violation] = []

        def add(rule: str, match: str, message: str) -> None:
            found.append(
                Violation(
                    rule=rule,
                    match=match,
                    message=message,
                    file=file,
                    line=line,
                    sentence=sentence.text,
                )
            )

        tokens = list(sentence)
        for i, token in enumerate(tokens):
            if token.text == PLACEHOLDER:
                continue
            if self.rules.check_semicolons and token.text == ";":
                add("semicolon", ";", "Never use a semicolon. Write two sentences.")
            if self.rules.check_contractions and self._is_contraction(token):
                add(
                    "contraction",
                    token.text,
                    f'Do not use the contraction "{token.text}". Write the words in full.',
                )
            if token.tag_ == "MD" and token.lower_ in self.rules.banned_modals:
                add(
                    "banned-modal",
                    token.text,
                    self._modal_message.format(word=token.lower_),
                )
            found.extend(
                Violation(
                    rule="banned-word",
                    match=match,
                    message=f'Write "{rule.write}", not "{match}".',
                    file=file,
                    line=line,
                    sentence=sentence.text,
                )
                for rule, match in self._word_matches(tokens, i, sentence)
            )

        if self.rules.instruction_limit is not None and self.rules.description_limit is not None:
            words = [t for t in tokens if not (t.is_punct or t.is_space)]
            imperative = bool(words) and words[0].tag_ == "VB"
            limit = self.rules.instruction_limit if imperative else self.rules.description_limit
            kind = "instruction" if imperative else "description"
            if len(words) > limit:
                add(
                    "sentence-length",
                    sentence.text[:40],
                    f"The sentence has {len(words)} words. The limit for the {kind} is {limit} words.",
                )
        return found

    @staticmethod
    def _is_contraction(token: Token) -> bool:
        if token.lower_ in _CONTRACTION_PARTS:
            return True
        # The possessive 's carries the POS tag and stays legal.
        return token.lower_ == "'s" and token.tag_ != "POS"

    def _word_matches(
        self, tokens: list[Token], i: int, sentence: Span
    ) -> list[tuple[WordRule, str]]:
        token = tokens[i]
        lemma = token.lemma_.lower()
        matches: list[tuple[WordRule, str]] = []
        for rule in self._single.get(lemma, []):
            if self._applies(rule, token, tokens, i, sentence):
                matches.append((rule, token.text))
        for rule in self._multi.get(lemma, []):
            span = tokens[i : i + len(rule.avoid)]
            if len(span) < len(rule.avoid):
                continue
            if all(t.lemma_.lower() == part for t, part in zip(span, rule.avoid)) and self._applies(
                rule, token, tokens, i, sentence
            ):
                matches.append((rule, " ".join(t.text for t in span)))
        return matches

    def _applies(
        self, rule: WordRule, token: Token, tokens: list[Token], i: int, sentence: Span
    ) -> bool:
        if rule.pos is not None and token.pos_ not in rule.pos:
            return False
        if rule.dep is not None and token.dep_ not in rule.dep:
            return False
        if rule.only_before_pos is not None:
            following = next((t for t in tokens[i + 1 :] if not (t.is_punct or t.is_space)), None)
            if following is None or following.pos_ not in rule.only_before_pos:
                return False
        if rule.except_phrases:
            text = sentence.text.lower()
            offset = token.idx - sentence.start_char
            for phrase in rule.except_phrases:
                for match in re.finditer(re.escape(phrase), text):
                    if match.start() <= offset < match.end():
                        return False
        return True
