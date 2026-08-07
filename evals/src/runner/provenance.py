"""Assemble the provenance of a run.

The provenance makes a run attributable: a later rate change must
trace back to a style edit, a prompt edit, a model change, or a
toolchain change, and never to a silent difference.
"""

from __future__ import annotations

import hashlib
import subprocess
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path

from .generate import ISOLATION_FLAGS, WORKDIR_MODE
from .hermetic import CONFIG_DIR_VAR, CONFIG_MODE, ENV_WHITELIST, TOKEN_VAR

LINTER_PACKAGES = ("spacy", "en-core-web-sm")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_state(repo_dir: Path) -> dict:
    """The commit and the dirty flag of the repository that holds the styles."""

    def git(*args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(repo_dir), *args], capture_output=True, text=True, check=True
        )
        return completed.stdout.strip()

    try:
        # Untracked files stay out of the dirty check: the run writes its
        # own output into the repository, and untracked files cannot alter
        # the tracked style files.
        return {
            "commit": git("rev-parse", "HEAD"),
            "dirty": bool(git("status", "--porcelain", "-uno")),
        }
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": None}


def linter_toolchain() -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for package in LINTER_PACKAGES:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    return versions


def claude_version(binary: str | None = "claude", env: dict[str, str] | None = None) -> str | None:
    """The version of the CLI, under the environment of the run.

    The callers pass the resolved binary and the hermetic environment,
    so this call sees the same CLI as the measured calls.
    """
    if binary is None:
        return None
    try:
        completed = subprocess.run(
            [binary, "--version"], env=env, capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


def build_provenance(
    *,
    model: str,
    prompts_path: Path | None,
    styles: list[str],
    plugin_dir: Path,
    cli_version: str | None,
    claude_binary: str | None = None,
    config_manifest_sha256: str | None = None,
) -> dict:
    style_files = {style: plugin_dir / "output-styles" / f"{style}.md" for style in sorted(styles)}
    # A deep drift run reads no prompt file: its inputs are the session
    # scripts, hashed in the drift block of the provenance.
    prompt_set = (
        {"path": None, "sha256": None}
        if prompts_path is None
        else {"path": str(prompts_path), "sha256": sha256_of(prompts_path)}
    )
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "prompt_set": prompt_set,
        "conditions": {
            "model_requested": model,
            "claude_version": cli_version,
            "workdir": WORKDIR_MODE,
            "config": CONFIG_MODE,
            "config_manifest_sha256": config_manifest_sha256,
            "claude_binary": claude_binary,
            # The variable names of the whitelisted environment. The
            # values never land here.
            "env_passed": [*ENV_WHITELIST, CONFIG_DIR_VAR, TOKEN_VAR],
            "flags": list(ISOLATION_FLAGS),
            "settings": {
                "base": {"disableAllHooks": True},
                "unstyled_arm": {"outputStyle": "default"},
                "styled_arm": {"outputStyle": "<style>", "extra_flag": "--plugin-dir"},
            },
        },
        "repo": repo_state(plugin_dir),
        "styles": {
            style: {"file": str(path), "sha256": sha256_of(path)}
            for style, path in style_files.items()
        },
        "linter_toolchain": linter_toolchain(),
    }
