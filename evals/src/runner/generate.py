"""Generate one answer through the Claude Code CLI, headless.

The invocation isolates the call as far as the CLI permits: no tools,
no MCP servers, no hooks, a single turn, no dynamic system-prompt
sections, and no session persistence. Plugins from the user
configuration still load; the caller records them in the provenance,
so a change in the environment stays visible across runs.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

Runner = Callable[[list[str], Path], str]
"""Runs a command in a working directory and returns its stdout."""

# The frozen flag set. The stream-json format carries the init event,
# which names the active output style, the resolved model, and the
# loaded plugins. --verbose is required for stream-json in print mode.
ISOLATION_FLAGS = (
    "--output-format",
    "stream-json",
    "--verbose",
    "--no-session-persistence",
    "--max-turns",
    "1",
    "--disallowedTools",
    "*",
    "--exclude-dynamic-system-prompt-sections",
    "--strict-mcp-config",
)

TIMEOUT_SECONDS = 600


class GenerationError(RuntimeError):
    """A single answer generation failed."""


@dataclass(frozen=True)
class Generation:
    """One generated answer plus the environment that produced it."""

    answer: str
    output_style: str
    resolved_model: str
    models_used: tuple[str, ...]
    plugins: tuple[str, ...]
    claude_code_version: str
    output_tokens: int
    duration_ms: int


def build_argv(prompt: str, model: str, style: str | None, plugin_dir: Path | None) -> list[str]:
    """Build the claude invocation for one answer.

    A styled answer activates the output style through --settings and
    loads the plugin through --plugin-dir. The unstyled answer forces
    the default style instead, because the user configuration can hold
    an active output style of its own. Everything else is identical.
    """
    settings: dict[str, object] = {"disableAllHooks": True, "outputStyle": "default"}
    argv = ["claude", "-p", prompt, "--model", model]
    if style is not None:
        if plugin_dir is None:
            raise ValueError("a styled answer needs the plugin directory")
        settings["outputStyle"] = style
        argv += ["--plugin-dir", str(plugin_dir)]
    argv += ["--settings", json.dumps(settings)]
    argv += list(ISOLATION_FLAGS)
    return argv


def subprocess_runner(argv: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        argv, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise GenerationError(f"claude exited with code {completed.returncode}: {detail[:500]}")
    return completed.stdout


def generate(
    prompt: str,
    model: str,
    style: str | None,
    plugin_dir: Path | None,
    workdir: Path,
    run: Runner = subprocess_runner,
) -> Generation:
    """Generate one answer and check that the intended style was active."""
    argv = build_argv(prompt, model, style, plugin_dir)
    stdout = run(argv, workdir)
    init, result = _parse_events(stdout)

    expected_style = style if style is not None else "default"
    active_style = init.get("output_style")
    if active_style != expected_style:
        raise GenerationError(
            f"expected output style {expected_style!r}, but {active_style!r} was active"
        )
    if result.get("is_error"):
        raise GenerationError(f"claude reported an error: {str(result.get('result', ''))[:500]}")

    usage = result.get("usage") or {}
    return Generation(
        answer=str(result.get("result", "")),
        output_style=active_style,
        resolved_model=str(init.get("model", "")),
        models_used=tuple(sorted((result.get("modelUsage") or {}).keys())),
        plugins=tuple(sorted(p["name"] for p in init.get("plugins", []))),
        claude_code_version=str(init.get("claude_code_version", "")),
        output_tokens=int(usage.get("output_tokens", 0)),
        duration_ms=int(result.get("duration_ms", 0)),
    )


def _parse_events(stdout: str) -> tuple[dict, dict]:
    """Extract the init event and the result event from stream-json output."""
    init: dict | None = None
    result: dict | None = None
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            init = event
        elif event.get("type") == "result":
            result = event
    if init is None or result is None:
        raise GenerationError("the claude output holds no init event or no result event")
    return init, result
