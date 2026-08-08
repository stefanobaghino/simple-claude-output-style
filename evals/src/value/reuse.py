"""Import stored judge rows from another run, with a freshness sample.

Reuse is explicit, never the default: the multi-run repetition of a
campaign measures variance, and a silent cache hit turns a repetition
into a copy. With the flag on, a tool imports a stored row when the
row speaks about the answers of the current run, and calls only on a
miss. The judge keys already carry the answer hashes, so a key names
its content; the comprehension keys carry the style and the prompt id
instead, so their import checks the answer hashes of the pair. The
source conditions must match the invocation on the META match keys of
the resume path, minus the whole-file answers hash that the per-row
checks replace. Reuse opens no era: a reused row and a live row are
the same row, plus one provenance field.

The judge can shift between the store date of a row and the reuse
date, in ways that the key does not see. Thus each reuse pass re-runs
a small fixed sample of the imported verdict rows live and stores the
comparison in the report. A disagreement is a warning. The per-axis
noise floor of issue #29 does not exist yet; once it does, it replaces
the equality rule and invalidates the reuse for an axis past the
floor. The probe arms of the cost tool carry no freshness sample,
because they are token measurements, not judge scores.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path

from .judges import JUDGE_MODEL_PINS

RowSink = Callable[[dict], None]

SAMPLE_PREFIXES = {
    "loss": {"completeness:check:": 2, "completeness:reverse:": 2, "hedging:check:": 2},
    "value": {"comprehension:v3:grades:": 6},
    "rank": {"clarity:": 6},
}
"""The freshness sample per tool: imported keys per prefix, sorted order.

Only verdict rows are sampled. The extraction rows (facts, claims,
questions, readers, paraphrases, translations) feed the scorers as
inputs, so an equality comparison of their free text means nothing.
"""


def _fail(message: str) -> SystemExit:
    print(message, file=sys.stderr)
    return SystemExit(2)


def check_source_meta(
    source_meta: dict | None,
    meta: dict,
    *,
    match_keys: tuple[str, ...],
    upgrade_keys: tuple[str, ...],
    source_raw: Path,
) -> dict:
    """The source meta row, after the condition check of the reuse.

    The match keys mirror the META match of the resume path, without
    the whole-file answers hash: the per-row checks replace it. An
    upgrade key absent in the source is tolerated, like the resume
    backfill; a present value that differs is a hard mismatch.
    """
    if source_meta is None:
        raise _fail(f"{source_raw}: the source run holds no judge data; judge the source first")
    mismatched = [key for key in match_keys if source_meta.get(key) != meta[key]]
    mismatched += [
        key for key in upgrade_keys if key in source_meta and source_meta[key] != meta[key]
    ]
    if mismatched:
        raise _fail(
            f"{source_raw} does not match this invocation on {', '.join(mismatched)}; "
            "reuse needs a source with the same judge conditions"
        )
    return source_meta


def check_source_pins(source_rows: dict[str, dict], source_raw: Path) -> None:
    """Stop when a source row resolves an alias against the pin table.

    A live call checks its resolved model against the pin per call.
    An imported row skips that check, so the whole source must pass
    it up front: every requested alias must resolve to one ID, and
    that ID must equal the pin of the alias.
    """
    by_request: dict[str, set[str]] = {}
    for row in source_rows.values():
        requested = row.get("model_requested")
        resolved = row.get("model_resolved")
        if requested and resolved:
            by_request.setdefault(requested, set()).add(resolved)
    for requested, values in sorted(by_request.items()):
        expected = JUDGE_MODEL_PINS.get(requested, requested)
        if values != {expected}:
            raise _fail(
                f"{source_raw}: the judge model {requested!r} must resolve to {expected!r}, "
                f"but the source rows hold {', '.join(sorted(values))}; "
                "the source comes from another judge era"
            )


def import_judge_rows(
    *,
    source_rows: dict[str, dict],
    source_name: str,
    rows: dict[str, dict],
    sink: RowSink,
    valid: Callable[[dict], bool],
) -> list[str]:
    """Import the valid source rows that this run does not hold yet.

    An imported row is the source row plus the reused_from marker; a
    chained marker is overwritten with the direct source. A key that
    the current raw file already holds never imports, so a resumed
    reuse pass appends nothing. Returns the imported keys.
    """
    imported: list[str] = []
    for key in sorted(source_rows):
        if key in rows:
            continue
        row = source_rows[key]
        if not valid(row):
            continue
        marked = {**row, "reused_from": source_name}
        rows[key] = marked
        sink(marked)
        imported.append(key)
    return imported


def sample_forced_keys(imported: list[str], tool: str) -> set[str]:
    """The fixed freshness sample: the first sorted keys per prefix."""
    forced: set[str] = set()
    for prefix, count in SAMPLE_PREFIXES[tool].items():
        matching = sorted(key for key in imported if key.startswith(prefix))
        forced.update(matching[:count])
    return forced


def read_raw_calls(path: Path) -> list[dict]:
    """Every call row of a raw file, in file order."""
    calls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("type") == "call":
            calls.append(row)
    return calls


def freshness_block(
    raw_calls: list[dict], parse: Callable[[dict], object]
) -> tuple[dict | None, list[str]]:
    """The freshness comparisons of a raw file, and their warnings.

    A comparison is a key whose line sequence holds a reused row with
    a later live row: the forced sample, and any validation retry of
    an imported row. The last reused row compares against the last
    live row after it, parsed with the scorer of the tool. Unusable
    output on either side leaves agree null. The block is a pure
    function of the raw file, so an offline rescore reproduces it.
    """
    last_reused: dict[str, int] = {}
    fresh_of: dict[str, tuple[dict, dict]] = {}
    for position, row in enumerate(raw_calls):
        key = row["key"]
        if "reused_from" in row:
            last_reused[key] = position
            fresh_of.pop(key, None)
        elif key in last_reused:
            fresh_of[key] = (raw_calls[last_reused[key]], row)
    if not fresh_of:
        return None, []
    comparisons = []
    warnings = []
    for key in sorted(fresh_of):
        reused_row, live_row = fresh_of[key]
        reused_value = parse(reused_row)
        live_value = parse(live_row)
        agree = None if reused_value is None or live_value is None else reused_value == live_value
        comparisons.append(
            {
                "key": key,
                "check": reused_row.get("check"),
                "role": reused_row.get("role"),
                "reused": reused_value,
                "live": live_value,
                "agree": agree,
            }
        )
        if agree is False:
            warnings.append(f"reuse freshness: {key}: the live verdict differs from the reused one")
        elif agree is None:
            warnings.append(f"reuse freshness: {key}: a side gave no usable verdict")
    block = {
        "sampled": len(comparisons),
        "agreements": sum(1 for entry in comparisons if entry["agree"] is True),
        "comparisons": comparisons,
    }
    return block, warnings


def reuse_section(reuse: dict | None) -> list[str]:
    """The md lines of the reuse section of a report."""
    if reuse is None:
        return []
    source = reuse["source"]
    source_text = source if isinstance(source, str) else ", ".join(source)
    lines = [
        "## Reuse",
        "",
        f"Reused rows: {reuse['reused_rows']}, imported from {source_text}.",
        f"Live calls of this run: {reuse['live_calls']}.",
        "",
    ]
    freshness = reuse.get("freshness")
    if freshness is None:
        lines += ["No freshness comparison exists in the raw file.", ""]
        return lines
    lines += [
        (
            f"The freshness sample re-ran {freshness['sampled']} imported "
            f"verdicts live; {freshness['agreements']} agree."
        ),
    ]
    for entry in freshness["comparisons"]:
        if entry["agree"] is True:
            continue
        state = "no usable verdict on a side" if entry["agree"] is None else "the verdicts differ"
        lines.append(f"- {entry['key']}: {state}.")
    lines += [
        "",
        "The comparison uses exact verdict equality. The per-axis noise",
        "floor of issue #29 does not exist yet; once it does, it replaces",
        "the equality rule and invalidates the reuse for an axis past the",
        "floor.",
        "",
    ]
    return lines


def reuse_summary(
    rows: dict[str, dict], raw_calls: list[dict], freshness: dict | None
) -> dict | None:
    """The reuse block of a report, or None without reused rows.

    The sources come from the raw file, so the block survives even
    when the freshness sample replaced every imported row. The counts
    come from the final last-wins row map: a reused row that a live
    row replaced counts as live, because the live measurement wins
    at load.
    """
    sources = sorted({row["reused_from"] for row in raw_calls if "reused_from" in row})
    if not sources:
        return None
    reused = sum(1 for row in rows.values() if "reused_from" in row)
    return {
        "source": sources[0] if len(sources) == 1 else sources,
        "reused_rows": reused,
        "live_calls": len(rows) - reused,
        "freshness": freshness,
    }
