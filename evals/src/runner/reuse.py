"""Import stored answers from another run.

The answers layer of the explicit reuse: with --reuse-from, the pair
runner imports the answer rows of a source run for the arms whose
conditions match, and generates only the rest. The judge layers chain
off this one, because a fresh generation of the same style and prompt
yields a different text, and a stored judge row speaks about the
stored answer. The import key is the issue #76 key: the style text
hash, the prompt id (under one prompt-set hash), and the model. An
imported row is the source row plus the reused_from marker. Reuse
opens no era: a reused row and a live row are the same row.

Every failure here raises a bare SystemExit with a message, the exit
style of the pair runner.
"""

from __future__ import annotations

import json
from pathlib import Path

from .provenance import sha256_of
from .report import arm_name


def load_source_provenance(source_dir: Path) -> dict:
    path = source_dir / "provenance.json"
    if not path.exists():
        raise SystemExit(f"{source_dir}: no provenance.json, so the directory is not a run")
    return json.loads(path.read_text(encoding="utf-8"))


def check_answer_conditions(
    source_dir: Path,
    provenance: dict,
    *,
    out: Path,
    prompts_path: Path,
    model: str,
    screening: bool,
) -> None:
    """Stop when the source run cannot feed this invocation.

    The prompt-set hash makes the prompt ids of the two runs mean the
    same texts, the model match keeps the writer condition, and the
    screening-mode match keeps the mode families apart, like the
    resume guards of the run directory.
    """
    if source_dir.resolve() == out.resolve():
        raise SystemExit(f"{source_dir}: the reuse source is the run itself; pass another run")
    stored_hash = (provenance.get("prompt_set") or {}).get("sha256")
    if stored_hash != sha256_of(prompts_path):
        raise SystemExit(f"{source_dir}: the source run covers another prompt set")
    source_model = provenance.get("conditions", {}).get("model_requested")
    if source_model != model:
        raise SystemExit(
            f"{source_dir}: the source run used the model {source_model!r}, not {model!r}"
        )
    if ("screening" in provenance) != screening:
        source_mode = "a screening run" if "screening" in provenance else "a full run"
        this_mode = "a screening run" if screening else "a full run"
        raise SystemExit(f"{source_dir}: the source holds {source_mode}, but this is {this_mode}")


def importable_arms(
    provenance: dict, styles: list[str], style_shas: dict[str, str]
) -> tuple[list[str | None], list[str]]:
    """The arms whose source answers can import, and one note per skip.

    The unstyled arm rests on the run-level conditions alone. A styled
    arm needs the same style text: the sha in the source provenance
    must equal the sha of the current style file.
    """
    arms: list[str | None] = [None]
    notes: list[str] = []
    source_styles = provenance.get("styles") or {}
    for style in styles:
        entry = source_styles.get(style)
        if entry is None:
            notes.append(
                f"reuse: {style}: the source run does not hold this style; generating live"
            )
        elif entry.get("sha256") != style_shas[style]:
            notes.append(f"reuse: {style}: the style text differs from the source; generating live")
        else:
            arms.append(style)
    return arms, notes


def import_answers(
    *,
    source_dir: Path,
    answers_path: Path,
    existing: dict[tuple[str, str], dict],
    arms: list[str | None],
    prompt_ids: list[str],
    source_name: str,
) -> int:
    """Append the missing source answers, marked; returns the count.

    Only a key that the current run does not hold imports, so a
    resumed reuse invocation appends nothing. A source without a row
    for a key leaves that key to the live generation. A chained
    marker is overwritten with the direct source.
    """
    source_path = source_dir / "answers.jsonl"
    if not source_path.exists():
        raise SystemExit(f"{source_dir}: the source run holds no answers")
    source: dict[tuple[str, str], dict] = {}
    for line in source_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        answer = json.loads(line)
        source[(answer["prompt_id"], arm_name(answer.get("style")))] = answer
    imported = 0
    with answers_path.open("a", encoding="utf-8") as answers_file:
        for style in arms:
            for prompt_id in prompt_ids:
                key = (prompt_id, arm_name(style))
                row = source.get(key)
                if key in existing or row is None:
                    continue
                marked = {**row, "reused_from": source_name}
                answers_file.write(json.dumps(marked, ensure_ascii=False) + "\n")
                existing[key] = marked
                imported += 1
    return imported
