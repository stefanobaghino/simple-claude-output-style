"""The screening mode: one reduced run for a candidate style.

The style-design loop screens many candidate styles cheaply, and only
the best candidate gets a full campaign. A screening run covers a
fixed prompt subset, all measurement axes, and one run instead of
three. The subset rule below is a condition of a screening run: a
change of the rule, the count, or the seed makes old screening runs
incomparable with new ones, like a comparability-era change does for
full runs.
"""

from __future__ import annotations

import random

PROMPTS_PER_TYPE = 2
"""The prompts that the subset draws per task type."""

SEED = 0
"""The fixed seed of the subset draw, so the subset is deterministic."""

FULL_CAMPAIGN_RUNS = 3
"""The run count of a full campaign, the base of the cost fraction."""


def select_screening_prompts(prompts: list[dict]) -> list[dict]:
    """The deterministic prompt subset of a screening run.

    The draw groups the prompt ids per type, sorts the ids, and
    samples PROMPTS_PER_TYPE ids per type with the fixed seed, so
    every screening run over one prompt set uses the same balanced
    subset. A type with fewer prompts contributes all of its prompts.
    The result keeps the file order of the prompt set.
    """
    ids_by_type: dict[str, list[str]] = {}
    for prompt in prompts:
        ids_by_type.setdefault(prompt["type"], []).append(prompt["id"])
    chosen: set[str] = set()
    for ids in ids_by_type.values():
        ordered = sorted(ids)
        chosen.update(random.Random(SEED).sample(ordered, min(PROMPTS_PER_TYPE, len(ordered))))
    return [prompt for prompt in prompts if prompt["id"] in chosen]


def screening_provenance(subset: list[dict], full_count: int) -> dict:
    """The screening block of provenance.json."""
    return {
        "prompts_per_type": PROMPTS_PER_TYPE,
        "seed": SEED,
        "prompt_ids": sorted(prompt["id"] for prompt in subset),
        "full_prompt_count": full_count,
    }


def screening_section(provenance: dict | None) -> list[str]:
    """The screening note of a report, or an empty list.

    The note tells the reader what a screening verdict is worth. The
    stated fractions are design numbers, not measurements: piece 2 of
    the screening ticket replaces them with a measurement against the
    baseline campaign.
    """
    block = (provenance or {}).get("screening")
    if not block:
        return []
    count = len(block["prompt_ids"])
    total = block["full_prompt_count"]
    generation = round(100 * count / (total * FULL_CAMPAIGN_RUNS))
    judged = round(100 * count / total)
    return [
        f"**Screening run.** This run covers {count} of {total} prompts, as one",
        f"run instead of {FULL_CAMPAIGN_RUNS}. By design, the generation calls are about",
        f"{generation}% of a full campaign, and the judge calls are about {judged}%",
        "of one full run. The fractions are design numbers, not",
        "measurements. The error bars are wider than in a full run,",
        "because fewer contests feed the bootstrap intervals.",
        "`style-compare` rejects a comparison of this run with a full run.",
        "",
    ]
