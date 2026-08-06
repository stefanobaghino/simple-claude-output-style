"""Schedule and score the blind clarity contests. Pure.

The schedule pairs every competitor with every other competitor, one
contest per prompt that both sides answer. A competitor is a style
with at least one gated pair, plus the unstyled answer under the
reserved name "unstyled". The unstyled competitor is ungated by
design, so the report states the asymmetry.

The scoring is a pure function of the schedule and the raw judge
rows. A contest is decisive when both orders pick the same
competitor, a split when the orders disagree, and unscored when an
order has no usable pick, because a single scored order would
reintroduce the position bias that the swap cancels. A contest with
two identical texts is a split without a judge call.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import combinations
from math import prod
from statistics import StatisticsError, correlation

from cost.analysis import task_type
from runner.stats import nearest_rank
from value.similarity import tokens

from .judges import contest_key, parse_pick

UNSTYLED = "unstyled"
"""The reserved competitor name of the unstyled answer."""


@dataclass
class RankResult:
    competitors: list[str]
    matchups: list[dict]
    win_matrix: dict[str, dict[str, float]]
    position_bias: dict
    bradley_terry: dict
    by_task_type: dict[str, list[dict]]
    length_confound: dict
    warnings: list[str]


def build_schedule(
    pairs: dict[str, list[str]], index: dict[tuple[str, str | None], dict]
) -> tuple[list[str], list[dict]]:
    """The competitors and the contests of a run, in a fixed order.

    A style competes on its gated prompts. The unstyled answer
    competes on every prompt that it answers. A matchup holds one
    contest per prompt that both sides answer, and a contest with two
    byte-identical texts carries the identical mark, so the judge
    step can skip it.
    """
    eligible: dict[str, dict[str, dict]] = {UNSTYLED: {}}
    for (prompt_id, style), arm in index.items():
        if style is None:
            eligible[UNSTYLED][prompt_id] = arm
    for style, prompt_ids in pairs.items():
        for prompt_id in prompt_ids:
            eligible.setdefault(style, {})[prompt_id] = index[(prompt_id, style)]
    competitors = sorted(name for name, prompts in eligible.items() if prompts)
    contests = []
    for a, b in combinations(competitors, 2):
        for prompt_id in sorted(set(eligible[a]) & set(eligible[b])):
            arm_a, arm_b = eligible[a][prompt_id], eligible[b][prompt_id]
            contests.append(
                {
                    "a": a,
                    "b": b,
                    "prompt_id": prompt_id,
                    "a_sha": arm_a["sha256"],
                    "b_sha": arm_b["sha256"],
                    "a_text": arm_a["text"],
                    "b_text": arm_b["text"],
                    "identical": arm_a["sha256"] == arm_b["sha256"],
                }
            )
    return competitors, contests


def _totals(outcomes: list[tuple[str, str, float]]) -> tuple[dict[str, float], dict[str, int]]:
    """The win points and the contest count per competitor."""
    wins: dict[str, float] = {}
    counts: dict[str, int] = {}
    for a, b, points_a in outcomes:
        wins[a] = wins.get(a, 0.0) + points_a
        wins[b] = wins.get(b, 0.0) + (1 - points_a)
        counts[a] = counts.get(a, 0) + 1
        counts[b] = counts.get(b, 0) + 1
    return wins, counts


def _fit_once(
    outcomes: list[tuple[str, str, float]], anchor: str, *, tol: float, max_iter: int
) -> tuple[dict[str, float | None], bool, list[str]]:
    """One Bradley-Terry fit: the degeneracy drop, then the MM iteration.

    Returns a strength per competitor of the outcomes, whether the
    anchor kept a finite strength, and the notes. A competitor with
    zero wins or zero losses has no finite maximum-likelihood
    strength, so its strength is None, its contests leave the fit,
    and the check repeats until no competitor is degenerate. The MM
    (Zermelo) iteration runs on the survivors, with the anchor
    rescaled to 1.0 each step; without the anchor the geometric mean
    holds the scale instead. Non-convergence leaves every survivor
    at None.
    """
    notes: list[str] = []
    strengths: dict[str, float | None] = {name: None for a, b, _ in outcomes for name in (a, b)}
    live = list(outcomes)
    while live:
        wins, counts = _totals(live)
        degenerate = sorted(name for name in wins if wins[name] in (0, counts[name]))
        if not degenerate:
            break
        notes += [
            f"{name}: zero wins or zero losses over the scored contests, so the "
            "strength has no finite value and its contests leave the fit"
            for name in degenerate
        ]
        live = [
            outcome
            for outcome in live
            if outcome[0] not in degenerate and outcome[1] not in degenerate
        ]
    wins, _ = _totals(live)
    survivors = sorted(wins)
    if len(survivors) < 2:
        if survivors:
            notes.append(
                "fewer than 2 competitors remain after the degeneracy drop, "
                "so no strength is fitted"
            )
        return strengths, False, notes
    pair_counts: dict[tuple[str, str], int] = {}
    for a, b, _ in live:
        pair = (a, b) if a < b else (b, a)
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    anchored = anchor in wins
    current = dict.fromkeys(survivors, 1.0)
    for _ in range(max_iter):
        new = {}
        for name in survivors:
            denominator = 0.0
            for (a, b), count in pair_counts.items():
                if name == a:
                    denominator += count / (current[name] + current[b])
                elif name == b:
                    denominator += count / (current[name] + current[a])
            new[name] = wins[name] / denominator
        scale = new[anchor] if anchored else prod(new.values()) ** (1 / len(new))
        new = {name: value / scale for name, value in new.items()}
        delta = max(abs(new[name] - current[name]) for name in survivors)
        current = new
        if delta < tol:
            for name in survivors:
                strengths[name] = current[name]
            return strengths, anchored, notes
    notes.append("the Bradley-Terry iteration did not converge, so the strengths are None")
    return strengths, False, notes


def _round3(value: float | None) -> float | None:
    return None if value is None else round(value, 3)


def fit_bradley_terry(
    outcomes: list[tuple[str, str, float]],
    anchor: str = UNSTYLED,
    *,
    tol: float = 1e-9,
    max_iter: int = 1000,
    resamples: int = 1000,
    seed: int = 0,
) -> tuple[dict, list[str]]:
    """The Bradley-Terry block of the scored contests, plus the warnings.

    An outcome is (a, b, points_a) with the points of a in the
    contest: 1 for a decisive win, 0.5 for a split, 0 for a loss.
    The fit needs at least 3 competitors, else the layer stays
    dormant. The uncertainty comes from a seeded bootstrap over the
    outcomes: each resample refits, and the interval takes the
    nearest-rank 2.5 and 97.5 percentiles of the finite anchored
    refits. The anchor holds the scale at 1.0, so its interval is
    None by construction.
    """
    warnings: list[str] = []
    competitors = sorted({name for a, b, _ in outcomes for name in (a, b)})
    if len(competitors) < 3:
        return {
            "fitted": False,
            "note": "the fit needs at least 3 competitors with a scored contest",
        }, warnings

    strengths, anchored, notes = _fit_once(outcomes, anchor, tol=tol, max_iter=max_iter)
    warnings += notes
    fitted_any = any(value is not None for value in strengths.values())
    intervals: dict[str, tuple[float | None, float | None]] = dict.fromkeys(
        competitors, (None, None)
    )
    if anchored and fitted_any and resamples > 0:
        rng = random.Random(seed)
        collected: dict[str, list[float]] = {name: [] for name in competitors}
        for _ in range(resamples):
            sample = [outcomes[rng.randrange(len(outcomes))] for _ in range(len(outcomes))]
            refit, refit_anchored, _ = _fit_once(sample, anchor, tol=tol, max_iter=max_iter)
            if not refit_anchored:
                continue
            for name, value in refit.items():
                if value is not None:
                    collected[name].append(value)
        for name in competitors:
            values = sorted(collected[name])
            if name != anchor and values:
                intervals[name] = (nearest_rank(values, 2.5), nearest_rank(values, 97.5))
    elif fitted_any and not anchored:
        warnings.append(
            f"the anchor {anchor!r} has no finite strength, so the strengths are "
            "scaled by their geometric mean and the bootstrap is skipped"
        )
    return {
        "fitted": True,
        "anchored_on": anchor if anchored else None,
        "strengths": {
            name: {
                "strength": _round3(strengths[name]),
                "ci_low": _round3(intervals[name][0]),
                "ci_high": _round3(intervals[name][1]),
            }
            for name in competitors
        },
        "bootstrap": {"resamples": resamples, "seed": seed},
    }, warnings


def _length_confound(samples: list[tuple[float, float]]) -> dict:
    """Correlation between the length ratio and the points of the longer text.

    Each scored contest with unequal word counts contributes one
    sample: the word count of the longer text over the word count of
    the shorter text, paired with the points of the longer text. A
    contest with equal word counts carries no length signal, so the
    contest contributes no sample. A statistic becomes None when it
    is not computable: no sample, fewer than two samples, or a
    constant input.
    """
    result: dict = {"n": len(samples)}
    ratios = [ratio for ratio, _ in samples]
    points = [point for _, point in samples]
    for name, method in (("pearson", "linear"), ("spearman", "ranked")):
        try:
            result[name] = round(correlation(ratios, points, method=method), 3)
        except StatisticsError:
            result[name] = None
    result["longer_win_rate"] = round(sum(points) / len(points), 3) if points else None
    return result


def _matchup(store: dict[tuple[str, str], dict], a: str, b: str) -> dict:
    return store.setdefault(
        (a, b),
        {"a": a, "b": b, "contests": 0, "wins_a": 0, "wins_b": 0, "splits": 0, "unscored": 0},
    )


def score_contests(
    competitors: list[str], contests: list[dict], rows: dict[str, dict]
) -> RankResult:
    """Score every contest of the schedule from the stored judge rows."""
    warnings: list[str] = []
    matchup_stats: dict[tuple[str, str], dict] = {}
    type_stats: dict[str, dict[tuple[str, str], dict]] = {}
    win_matrix = {
        name: {other: 0.0 for other in competitors if other != name} for name in competitors
    }
    first_picks = usable_picks = 0
    judged_splits = judged_scored = 0
    outcomes: list[tuple[str, str, float]] = []
    samples: list[tuple[float, float]] = []

    for contest in contests:
        a, b, prompt_id = contest["a"], contest["b"], contest["prompt_id"]
        entries = [
            _matchup(matchup_stats, a, b),
            _matchup(type_stats.setdefault(task_type(prompt_id), {}), a, b),
        ]
        for entry in entries:
            entry["contests"] += 1

        if contest["identical"]:
            warnings.append(
                f"{a} vs {b} on {prompt_id}: the two texts are identical, "
                "so the contest is a split without a judge call"
            )
            points_a = 0.5
        else:
            picks = []
            for first, first_sha, second_sha in (
                (a, contest["a_sha"], contest["b_sha"]),
                (b, contest["b_sha"], contest["a_sha"]),
            ):
                row = rows.get(contest_key(prompt_id, first_sha, second_sha))
                pick = parse_pick(row["output"]) if row else None
                if pick is not None:
                    usable_picks += 1
                    if pick == 1:
                        first_picks += 1
                picks.append((first, pick))
            if any(pick is None for _, pick in picks):
                for entry in entries:
                    entry["unscored"] += 1
                warnings.append(
                    f"{a} vs {b} on {prompt_id}: an order has no usable pick, "
                    "so the contest is unscored"
                )
                continue
            winners = [first if pick == 1 else (b if first == a else a) for first, pick in picks]
            judged_scored += 1
            if winners[0] == winners[1]:
                points_a = 1.0 if winners[0] == a else 0.0
            else:
                points_a = 0.5
                judged_splits += 1

        if points_a == 0.5:
            for entry in entries:
                entry["splits"] += 1
            win_matrix[a][b] += 0.5
            win_matrix[b][a] += 0.5
        else:
            winner, loser = (a, b) if points_a == 1.0 else (b, a)
            side = "wins_a" if winner == a else "wins_b"
            for entry in entries:
                entry[side] += 1
            win_matrix[winner][loser] += 1.0
        outcomes.append((a, b, points_a))

        words_a, words_b = len(tokens(contest["a_text"])), len(tokens(contest["b_text"]))
        if words_a != words_b and min(words_a, words_b) > 0:
            points_long = points_a if words_a > words_b else 1 - points_a
            samples.append((max(words_a, words_b) / min(words_a, words_b), points_long))

    for store in (matchup_stats, *type_stats.values()):
        for entry in store.values():
            entry["net"] = entry["wins_a"] - entry["wins_b"]

    bradley_terry, fit_warnings = fit_bradley_terry(outcomes)
    return RankResult(
        competitors=competitors,
        matchups=[matchup_stats[key] for key in sorted(matchup_stats)],
        win_matrix=win_matrix,
        position_bias={
            "first_pick_rate": round(first_picks / usable_picks, 3) if usable_picks else None,
            "picks": usable_picks,
            "split_rate": round(judged_splits / judged_scored, 3) if judged_scored else None,
            "contests": judged_scored,
        },
        bradley_terry=bradley_terry,
        by_task_type={
            name: [store[key] for key in sorted(store)]
            for name, store in sorted(type_stats.items())
        },
        length_confound=_length_confound(samples),
        warnings=warnings + fit_warnings,
    )
