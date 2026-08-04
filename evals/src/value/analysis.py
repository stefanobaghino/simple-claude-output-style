"""Score the reader-value checks from the stored judge rows. Pure.

The scoring is a pure function of the answers, the gated pairs, and
the raw judge rows: no network, no clock beyond the caller. Per check
and per pair, the styled score and the unstyled score become a win, a
loss, or a tie for the styled answer.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from statistics import StatisticsError, correlation

from loss.judges import parse_string_list

from .judges import CHECKS, parse_bools, parse_questions, parse_strings
from .similarity import mean_pairwise_f1, tokens, unigram_f1

TIE_EPSILON = 0.02
"""Two similarity scores closer than this count as a tie."""

# The scoring spec per stored shared-facts design. The design tag of
# a run selects the spec, so every stored run stays rescoreable.
SHARED_DESIGNS = {
    "shared-facts-v2": {"prefix": "comprehension:v2:", "burial_arms": ("styled",)},
    "balanced-facts-v3": {"prefix": "comprehension:v3:", "burial_arms": ("styled", "unstyled")},
}

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


def _length_correlation(samples: list[tuple[float, float]]) -> dict:
    """Pearson and Spearman between the length ratio and the advantage.

    A lexical check can reward the shorter text, because less text
    exists to diverge on. Each sample pairs the length ratio of a pair
    (styled words over unstyled words) with the styled advantage (the
    unrounded score gain of the styled arm). A negative correlation
    means that the shorter styled answers score better. A statistic
    becomes None when it is not computable: fewer than two samples, or
    a constant input.
    """
    result: dict = {"n": len(samples)}
    ratios = [ratio for ratio, _ in samples]
    advantages = [advantage for _, advantage in samples]
    for name, method in (("pearson", "linear"), ("spearman", "ranked")):
        try:
            result[name] = round(correlation(ratios, advantages, method=method), 3)
        except StatisticsError:
            result[name] = None
    return result


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


def shared_facts(
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    loss_rows: dict[str, dict],
) -> tuple[dict[tuple[str, str], dict[str, list[str]]], list[str]]:
    """The facts of each pair that both answers hold, in both wordings.

    The completeness check of the content-loss report mined both
    directions: the facts of the unstyled answer judged against the
    styled answer, and the facts of the styled answer judged against
    the unstyled answer. A survivor of either direction is a shared
    fact, worded by its source answer. An empty fact list has no
    check row and yields an empty survivor list. The row keys carry
    the answer hashes, so a stale row never matches a current pair.
    """
    facts_by_pair: dict[tuple[str, str], dict[str, list[str]]] = {}
    warnings: list[str] = []
    for style in sorted(pairs):
        for prompt_id in pairs[style]:
            unstyled_sha = answers[(prompt_id, None)]["sha256"]
            styled_sha = answers[(prompt_id, style)]["sha256"]
            directions = {
                "unstyled": (
                    f"completeness:facts:{unstyled_sha}",
                    f"completeness:check:{styled_sha}",
                ),
                "styled": (
                    f"completeness:facts:{styled_sha}",
                    f"completeness:reverse:{styled_sha}",
                ),
            }
            survivors: dict[str, list[str]] = {}
            for source, (facts_key, marks_key) in directions.items():
                facts_row = loss_rows.get(facts_key)
                facts = parse_string_list(facts_row["output"]) if facts_row else None
                if facts == []:
                    survivors[source] = []
                    continue
                marks_row = loss_rows.get(marks_key)
                if facts_row is None or marks_row is None:
                    warnings.append(
                        f"{style}/{prompt_id}: loss-raw.jsonl holds no completeness rows "
                        f"for the {source} facts, so comprehension skips the pair; run "
                        "style-loss --judge first"
                    )
                    break
                marks = None if facts is None else parse_bools(marks_row["output"], len(facts))
                if facts is None or marks is None:
                    warnings.append(
                        f"{style}/{prompt_id}: the completeness rows for the {source} "
                        "facts do not parse, so comprehension skips the pair"
                    )
                    break
                survivors[source] = [fact for fact, mark in zip(facts, marks, strict=True) if mark]
            else:
                facts_by_pair[(style, prompt_id)] = survivors
    return facts_by_pair, warnings


def _outcome(styled: float, unstyled: float, higher_wins: bool, tie_epsilon: float) -> str:
    delta = styled - unstyled
    if abs(delta) <= tie_epsilon:
        return "tie"
    return "win" if (delta > 0) == higher_wins else "loss"


def _score_comprehension_shared(
    *,
    pairs: dict[str, list[str]],
    rows: dict[str, dict],
    replicates: int,
    warnings: list[str],
    prefix: str,
    design: str,
    burial_arms: tuple[str, ...],
) -> dict:
    """Score the shared-facts comprehension rows, pair by pair.

    Per pair, every styled replicate meets every unstyled replicate,
    and each meeting is a win, a loss, or a tie under the exact-tie
    rule. The pair outcome is the strict plurality of the meetings,
    else a tie. The agreement of a pair is the plurality share. The
    buried-fact rate counts "NOT IN TEXT" replies per burial arm: the
    reader missed a fact that the loss judge found present. The
    balanced design adds the unstyled burial rate and the question
    sources of each pair.
    """
    if not any(key.startswith(prefix) for key in rows):
        warnings.append("the comprehension check has no judge data: run style-value with --judge")
        return {"judged": False, "design": design, "per_style": None}
    per_style: dict[str, dict] = {}
    for style in sorted(pairs):
        tally = {"win": 0, "loss": 0, "tie": 0}
        pair_scores: dict[str, dict] = {}
        deltas: list[float] = []
        agreements: list[float] = []
        buried = dict.fromkeys(burial_arms, 0)
        replies_seen = dict.fromkeys(burial_arms, 0)
        for prompt_id in pairs[style]:
            questions_row = rows.get(f"{prefix}questions:{style}:{prompt_id}")
            questions = parse_string_list(questions_row["output"]) if questions_row else None
            if not questions:
                warnings.append(
                    f"{style}/{prompt_id}: the comprehension check has no usable "
                    "questions for the pair, so the pair is unscored"
                )
                continue
            n = len(questions)
            scores: dict[str, list[float]] = {"styled": [], "unstyled": []}
            for arm, values in scores.items():
                for replicate in range(replicates):
                    key = f"{prefix}grades:{style}:{prompt_id}:{arm}:{replicate}"
                    row = rows.get(key)
                    grades = parse_bools(row["output"], n) if row else None
                    if grades is not None:
                        values.append(sum(grades) / n)
            for arm in burial_arms:
                for replicate in range(replicates):
                    key = f"{prefix}reader:{style}:{prompt_id}:{arm}:{replicate}"
                    row = rows.get(key)
                    replies = parse_strings(row["output"], n) if row else None
                    if replies is not None:
                        replies_seen[arm] += n
                        buried[arm] += sum(1 for reply in replies if reply == "NOT IN TEXT")
            missing = [arm for arm, values in scores.items() if not values]
            if missing:
                warnings.append(
                    f"{style}/{prompt_id}: the comprehension check has no usable score "
                    f"for the {' and the '.join(missing)} answer, so the pair is unscored"
                )
                continue
            outcomes = Counter(
                _outcome(styled, unstyled, True, 0.0)
                for styled in scores["styled"]
                for unstyled in scores["unstyled"]
            )
            ranked = outcomes.most_common()
            result = ranked[0][0]
            if len(ranked) > 1 and ranked[1][1] == ranked[0][1]:
                result = "tie"
            agreement = ranked[0][1] / sum(outcomes.values())
            styled_mean = sum(scores["styled"]) / len(scores["styled"])
            unstyled_mean = sum(scores["unstyled"]) / len(scores["unstyled"])
            tally[result] += 1
            deltas.append(styled_mean - unstyled_mean)
            agreements.append(agreement)
            entry = {
                "styled": round(styled_mean, 3),
                "unstyled": round(unstyled_mean, 3),
                "questions": n,
                "agreement": round(agreement, 3),
                "result": result,
            }
            if design == "balanced-facts-v3":
                entry["sources"] = questions_row.get("sources")
            pair_scores[prompt_id] = entry

        rates = {
            arm: round(buried[arm] / replies_seen[arm], 3) if replies_seen[arm] else None
            for arm in burial_arms
        }
        stats = {
            "wins": tally["win"],
            "losses": tally["loss"],
            "ties": tally["tie"],
            "mean_delta": round(sum(deltas) / len(deltas), 3) if deltas else None,
            "mean_agreement": round(sum(agreements) / len(agreements), 3) if agreements else None,
            "buried_fact_rate": rates["styled"],
        }
        if "unstyled" in burial_arms:
            stats["buried_fact_rate_unstyled"] = rates["unstyled"]
        stats["pairs"] = pair_scores
        per_style[style] = stats
    return {"judged": True, "design": design, "per_style": per_style}


def score_checks(
    *,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    rows: dict[str, dict],
    paraphrases_k: int,
    comprehension_design: str | None = None,
    replicates: int = 1,
) -> ValueResult:
    """Score every check for every pair.

    The answers mapping goes from (prompt_id, style or None) to a dict
    with text and sha256. The rows mapping is the raw judge data keyed
    by call key. The comprehension_design value comes from the meta
    row and selects the matched scorer: None selects the first-design
    scorer, so every stored run stays rescoreable.
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
        if check == "comprehension" and comprehension_design in SHARED_DESIGNS:
            checks_out[check] = _score_comprehension_shared(
                pairs=pairs,
                rows=rows,
                replicates=replicates,
                warnings=warnings,
                design=comprehension_design,
                **SHARED_DESIGNS[comprehension_design],
            )
            continue
        if not any(row.get("check") == check for row in rows.values()):
            checks_out[check] = {"judged": False, "per_style": None}
            warnings.append(f"the {check} check has no judge data: run style-value with --judge")
            continue
        rules = CHECK_RULES[check]
        per_style: dict[str, dict] = {}
        for style in sorted(pairs):
            tally = {"win": 0, "loss": 0, "tie": 0}
            pair_scores: dict[str, dict] = {}
            length_samples: list[tuple[float, float]] = []
            for prompt_id in pairs[style]:
                styled_arm = answers[(prompt_id, style)]
                unstyled_arm = answers[(prompt_id, None)]
                styled = scorers[check](prompt_id, styled_arm)
                unstyled = scorers[check](prompt_id, unstyled_arm)
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
                unstyled_words = len(tokens(unstyled_arm["text"]))
                if unstyled_words > 0:
                    ratio = len(tokens(styled_arm["text"])) / unstyled_words
                    advantage = styled - unstyled if rules["higher_wins"] else unstyled - styled
                    length_samples.append((ratio, advantage))
                pair_scores[prompt_id] = {
                    "styled": round(styled, 3),
                    "unstyled": round(unstyled, 3),
                    "result": outcome,
                }
            per_style[style] = {
                "wins": tally["win"],
                "losses": tally["loss"],
                "ties": tally["tie"],
                "length_correlation": _length_correlation(length_samples),
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
