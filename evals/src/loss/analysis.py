"""Score the content-loss checks from the stored judge rows. Pure.

The scoring is a pure function of the answers, the gated pairs, and
the raw judge rows: no network, no clock beyond the caller. Per pair,
the completeness check yields the fraction of the facts that survive,
and the hedging check yields the fraction of the uncertain claims
that keep their uncertainty among the claims that survive at all.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median

from value.judges import parse_bools

from .judges import CHECKS, parse_string_list, parse_verdicts


@dataclass
class LossResult:
    checks: dict[str, dict]
    warnings: list[str]


def _median(values: list[float]) -> float | None:
    return round(median(values), 3) if values else None


def score_checks(
    *,
    pairs: dict[str, list[str]],
    answers: dict[tuple[str, str | None], dict],
    rows: dict[str, dict],
) -> LossResult:
    """Score both checks for every pair.

    The answers mapping goes from (prompt_id, style or None) to a dict
    with text and sha256. The rows mapping is the raw judge data keyed
    by call key.
    """
    warnings: list[str] = []
    checks_out: dict[str, dict] = {}

    lists_cache: dict[str, list[str] | None] = {}

    def list_for(check: str, role: str, sha: str) -> list[str] | None:
        key = f"{check}:{role}:{sha}"
        if key not in lists_cache:
            row = rows.get(key)
            lists_cache[key] = parse_string_list(row["output"]) if row else None
        return lists_cache[key]

    def completeness_pair(style: str, prompt_id: str) -> dict | None:
        facts = list_for("completeness", "facts", answers[(prompt_id, None)]["sha256"])
        if facts is None:
            warnings.append(
                f"{style}/{prompt_id}: the completeness check has no usable fact list, "
                "so the pair is unscored"
            )
            return None
        if not facts:
            return {"facts": 0, "survived": 0, "fraction": None, "lost": []}
        row = rows.get(f"completeness:check:{answers[(prompt_id, style)]['sha256']}")
        marks = parse_bools(row["output"], len(facts)) if row else None
        if marks is None:
            warnings.append(
                f"{style}/{prompt_id}: the completeness check has no usable survival marks, "
                "so the pair is unscored"
            )
            return None
        return {
            "facts": len(facts),
            "survived": sum(marks),
            "fraction": round(sum(marks) / len(facts), 3),
            "lost": [fact for fact, kept in zip(facts, marks, strict=True) if not kept],
        }

    def hedging_pair(style: str, prompt_id: str) -> dict | None:
        claims = list_for("hedging", "claims", answers[(prompt_id, None)]["sha256"])
        if claims is None:
            warnings.append(
                f"{style}/{prompt_id}: the hedging check has no usable claim list, "
                "so the pair is unscored"
            )
            return None
        if not claims:
            return {
                "claims": 0,
                "hedged": 0,
                "certain": 0,
                "absent": 0,
                "survival": None,
                "lost": [],
            }
        row = rows.get(f"hedging:check:{answers[(prompt_id, style)]['sha256']}")
        verdicts = parse_verdicts(row["output"], len(claims)) if row else None
        if verdicts is None:
            warnings.append(
                f"{style}/{prompt_id}: the hedging check has no usable verdicts, "
                "so the pair is unscored"
            )
            return None
        hedged = verdicts.count("hedged")
        certain = verdicts.count("certain")
        return {
            "claims": len(claims),
            "hedged": hedged,
            "certain": certain,
            "absent": verdicts.count("absent"),
            "survival": round(hedged / (hedged + certain), 3) if hedged + certain else None,
            "lost": [
                claim
                for claim, verdict in zip(claims, verdicts, strict=True)
                if verdict == "certain"
            ],
        }

    scorers = {
        "completeness": ("fraction", completeness_pair),
        "hedging": ("survival", hedging_pair),
    }

    for check in CHECKS:
        if not any(row.get("check") == check for row in rows.values()):
            checks_out[check] = {"judged": False, "per_style": None}
            warnings.append(f"the {check} check has no judge data: run style-loss with --judge")
            continue
        score_key, scorer = scorers[check]
        per_style: dict[str, dict] = {}
        for style in sorted(pairs):
            pair_scores: dict[str, dict] = {}
            for prompt_id in pairs[style]:
                scored = scorer(style, prompt_id)
                if scored is not None:
                    pair_scores[prompt_id] = scored
            scores = [
                entry[score_key] for entry in pair_scores.values() if entry[score_key] is not None
            ]
            per_style[style] = {"median": _median(scores), "pairs": pair_scores}
        checks_out[check] = {"judged": True, "per_style": per_style}

    return LossResult(checks=checks_out, warnings=warnings)
