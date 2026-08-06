"""Run one scripted session through the Claude Code CLI.

A session chains single-shot claude -p calls through --resume: the
first turn starts a fresh session, and every later turn resumes from
the session id that the previous turn reported, because a resumed
call can report a fresh id. The calls keep the isolation flags of the
pair runner, except --no-session-persistence, because a resumable
session must persist. Thus session files stay under ~/.claude after a
run. The code never deletes that user state.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from runner.generate import (
    ISOLATION_FLAGS,
    GenerationError,
    Runner,
    parse_events,
    style_reference,
    subprocess_runner,
)

SESSION_FLAGS = tuple(flag for flag in ISOLATION_FLAGS if flag != "--no-session-persistence")


@dataclass(frozen=True)
class SessionTurn:
    """One generated turn plus the session chain that produced it."""

    answer: str
    session_id: str
    resume_from: str | None
    output_style: str
    resolved_model: str
    claude_code_version: str
    output_tokens: int
    input_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    duration_ms: int
    wall_ms: int


Record = Callable[[int, dict, SessionTurn], None]
"""Receives the turn number, the prompt, and the generated turn."""


def build_session_argv(
    prompt: str, model: str, style: str, plugin_dir: Path, resume_id: str | None
) -> list[str]:
    """Build the claude invocation for one session turn.

    Every turn is styled; the drift measurement has no unstyled arm.
    The first turn of a session passes no --resume flag.
    """
    settings = {"disableAllHooks": True, "outputStyle": style_reference(plugin_dir, style)}
    argv = ["claude", "-p", prompt, "--model", model, "--plugin-dir", str(plugin_dir)]
    argv += ["--settings", json.dumps(settings)]
    argv += list(SESSION_FLAGS)
    if resume_id is not None:
        argv += ["--resume", resume_id]
    return argv


def generate_turn(
    prompt: str,
    model: str,
    style: str,
    plugin_dir: Path,
    workdir: Path,
    resume_id: str | None,
    run: Runner = subprocess_runner,
) -> SessionTurn:
    """Generate one turn and check that the intended style was active."""
    argv = build_session_argv(prompt, model, style, plugin_dir, resume_id)
    start = time.monotonic()
    stdout = run(argv, workdir)
    wall_ms = round((time.monotonic() - start) * 1000)
    init, result = parse_events(stdout)

    expected_style = style_reference(plugin_dir, style)
    active_style = init.get("output_style")
    if active_style != expected_style:
        raise GenerationError(
            f"expected output style {expected_style!r}, but {active_style!r} was active"
        )
    if result.get("is_error"):
        raise GenerationError(f"claude reported an error: {str(result.get('result', ''))[:500]}")
    session_id = result.get("session_id") or init.get("session_id")
    if not session_id:
        raise GenerationError(
            "the claude output holds no session id, so the next turn cannot resume"
        )

    usage = result.get("usage") or {}
    return SessionTurn(
        answer=str(result.get("result", "")),
        session_id=str(session_id),
        resume_from=resume_id,
        output_style=active_style,
        resolved_model=str(init.get("model", "")),
        claude_code_version=str(init.get("claude_code_version", "")),
        output_tokens=int(usage.get("output_tokens", 0)),
        input_tokens=int(usage.get("input_tokens", 0)),
        cache_creation_input_tokens=int(usage.get("cache_creation_input_tokens", 0)),
        cache_read_input_tokens=int(usage.get("cache_read_input_tokens", 0)),
        duration_ms=int(result.get("duration_ms", 0)),
        wall_ms=wall_ms,
    )


def session_script(prompts: list[dict], turns: int, repeat: int, repeats: int) -> list[dict]:
    """The prompt order of one repeat.

    The base order round-robins across the task types in file order,
    so one task type does not cluster at one end of the session. Each
    repeat rotates the base order, so a prompt sits at a different
    turn position per repeat, and prompt difficulty does not
    masquerade as drift.
    """
    if turns > len(prompts):
        raise ValueError(f"the script needs {turns} prompts, but the set holds {len(prompts)}")
    by_type: dict[str, list[dict]] = {}
    for prompt in prompts:
        by_type.setdefault(prompt["type"], []).append(prompt)
    queues = list(by_type.values())
    base = [
        queue[index]
        for index in range(max(len(queue) for queue in queues))
        for queue in queues
        if index < len(queue)
    ]
    order = base[:turns]
    offset = ((repeat - 1) * turns) // repeats % turns
    return order[offset:] + order[:offset]


def run_session(
    script: list[dict],
    model: str,
    style: str,
    plugin_dir: Path,
    workdir: Path,
    run: Runner,
    record: Record,
) -> None:
    """Run one scripted session and record every turn.

    The record callback runs after each turn, so an interrupted
    session keeps the turns that completed. A failed turn raises
    GenerationError and aborts the session.
    """
    resume_id: str | None = None
    for turn_number, prompt in enumerate(script, start=1):
        turn = generate_turn(prompt["text"], model, style, plugin_dir, workdir, resume_id, run=run)
        record(turn_number, prompt, turn)
        resume_id = turn.session_id
