"""Lexical similarity between texts.

The reader-value checks compare texts that different judge calls
produce. The metric is the unigram F1 over lowercased alphanumeric
tokens, counted as a multiset: deterministic, symmetric, and free of
extra dependencies. The metric measures surface overlap, not meaning.
The checks only compare scores between the two arms of a pair, so a
bias that both arms share cancels out.
"""

from __future__ import annotations

import re
from collections import Counter
from itertools import combinations

_TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def unigram_f1(a: str, b: str) -> float:
    """The harmonic mean of token precision and token recall."""
    counts_a, counts_b = Counter(tokens(a)), Counter(tokens(b))
    total = sum(counts_a.values()) + sum(counts_b.values())
    if total == 0:
        return 1.0
    overlap = sum((counts_a & counts_b).values())
    return 2 * overlap / total


def mean_pairwise_f1(texts: list[str]) -> float:
    """The mean unigram F1 over every pair of texts. Needs two texts or more."""
    pairs = list(combinations(texts, 2))
    if not pairs:
        raise ValueError("mean_pairwise_f1 needs at least two texts")
    return sum(unigram_f1(a, b) for a, b in pairs) / len(pairs)
