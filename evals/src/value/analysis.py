"""Score the reader-value checks from the stored judge rows. Pure.

The scoring is a pure function of the answers, the gated pairs, and
the raw judge rows: no network, no clock beyond the caller. Per check
and per pair, the styled score and the unstyled score become a win, a
loss, or a tie for the styled answer.
"""

from __future__ import annotations

from dataclasses import dataclass

from .judges import CHECKS, parse_bools, parse_questions
from .similarity import mean_pairwise_f1, unigram_f1

TIE_EPSILON = 0.02
"""Two similarity scores closer than this count as a tie."""

# Per check: does a higher score win, and how close is a tie? The
# comprehension score is a fraction of a small question count, so only
# an exact match counts as a tie.
CHECK_RULES = {
    "comprehension": {"higher_wins": True, "tie_epsilon": 0.0},
    "paraphrase": {"higher_wins": True, "tie_epsilon": TIE_EPSILON},
    "roundtrip": {"higher_wins": False, "tie_epsilon": TIE_EPSILON},
}


@dataclass
class ValueResult:
    checks: dict[str, dict]
    warnings: list[str]


def select_pairs(
    fidelity_rows: list[dict], answer_shas: dict[tuple[str, str | None], str]
) -> tuple[dict[str, list[str]], list[str]]:
    """The pairs that enter the checks: styled rows that pass the gate.

    A pair drops out with a warning when the styled answer failed the
    gate, when the unstyled counterpart is missing, or when the answer
    text changed after the gate ran.
    """
    pairs: dict[str, list[str]] = {}
    warnings: list[str] = []
    for row in fidelity_rows:
        if row.get("pass") is None:
            continue
        style, prompt_id = row["style"], row["prompt_id"]
        pairs.setdefault(style, [])
        if not row["pass"]:
            warnings.append(f"{style}/{prompt_id}: the pair failed the gate, excluded")
            continue
        if (prompt_id, None) not in answer_shas:
            warnings.append(f"{style}/{prompt_id}: no unstyled counterpart, excluded")
            continue
        if answer_shas.get((prompt_id, style)) != row.get("answer_sha256"):
            warnings.append(
                f"{style}/{prompt_id}: the answer changed after the gate ran, excluded; "
                "run style-gate again"
            )
            continue
        pairs[style].append(prompt_id)
    return {style: sorted(ids) for style, ids in pairs.items()}, warnings


def _outcome(styled: float, unstyled: float, higher_wins: bool, tie_epsilon: float) -> str:
    delta = styled - unstyled
    if abs(delta) <= tie_epsilon:
        return "tie"
    return "win" if (delta > 0) == higher_wins else "loss"


def score_checks(
    *,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    rows: dict[str, dict],
    paraphrases_k: int,
) -> ValueResult:
    """Score every check for every pair.

    The answers mapping goes from (prompt_id, style or None) to a dict
    with text and sha256. The rows mapping is the raw judge data keyed
    by call key.
    """
    warnings: list[str] = []
    checks_out: dict[str, dict] = {}

    questions_cache: dict[str, list[dict] | None] = {}

    def questions_for(prompt_id: str) -> list[dict] | None:
        if prompt_id not in questions_cache:
            row = rows.get(f"comprehension:questions:{prompt_id}")
            questions_cache[prompt_id] = parse_questions(row["output"]) if row else None
        return questions_cache[prompt_id]

    def comprehension_score(prompt_id: str, arm: dict) -> float | None:
        questions = questions_for(prompt_id)
        row = rows.get(f"comprehension:grades:{arm['sha256']}")
        if questions is None or row is None:
            return None
        grades = parse_bools(row["output"], len(questions))
        if grades is None:
            return None
        return sum(grades) / len(grades)

    def paraphrase_score(prompt_id: str, arm: dict) -> float | None:
        restatements = [
            rows[key]["output"]
            for index in range(paraphrases_k)
            if (key := f"paraphrase:reader:{arm['sha256']}:{index}") in rows
        ]
        if len(restatements) < 2:
            return None
        return mean_pairwise_f1(restatements)

    def roundtrip_score(prompt_id: str, arm: dict) -> float | None:
        row = rows.get(f"roundtrip:back:{arm['sha256']}")
        if row is None:
            return None
        return 1 - unigram_f1(arm["text"], row["output"])

    scorers = {
        "comprehension": comprehension_score,
        "paraphrase": paraphrase_score,
        "roundtrip": roundtrip_score,
    }

    for check in CHECKS:
        if not any(row.get("check") == check for row in rows.values()):
            checks_out[check] = {"judged": False, "per_style": None}
            warnings.append(f"the {check} check has no judge data: run style-value with --judge")
            continue
        rules = CHECK_RULES[check]
        per_style: dict[str, dict] = {}
        for style in sorted(pairs):
            tally = {"win": 0, "loss": 0, "tie": 0}
            pair_scores: dict[str, dict] = {}
            for prompt_id in pairs[style]:
                styled = scorers[check](prompt_id, answers[(prompt_id, style)])
                unstyled = scorers[check](prompt_id, answers[(prompt_id, None)])
                missing = [
                    side
                    for side, score in (("styled", styled), ("unstyled", unstyled))
                    if score is None
                ]
                if missing:
                    warnings.append(
                        f"{style}/{prompt_id}: the {check} check has no usable score for "
                        f"the {' and the '.join(missing)} answer, so the pair is unscored"
                    )
                    continue
                outcome = _outcome(styled, unstyled, rules["higher_wins"], rules["tie_epsilon"])
                tally[outcome] += 1
                pair_scores[prompt_id] = {
                    "styled": round(styled, 3),
                    "unstyled": round(unstyled, 3),
                    "result": outcome,
                }
            per_style[style] = {
                "wins": tally["win"],
                "losses": tally["loss"],
                "ties": tally["tie"],
                "pairs": pair_scores,
            }
        checks_out[check] = {"judged": True, "per_style": per_style}

    comprehension = checks_out["comprehension"]
    if comprehension["judged"]:
        for style, stats in comprehension["per_style"].items():
            if stats["losses"] > stats["wins"]:
                warnings.append(
                    f"{style}: the styled answer scores worse than the unstyled answer on "
                    f"comprehension ({stats['wins']} wins, {stats['losses']} losses)"
                )

    return ValueResult(checks=checks_out, warnings=warnings)
