"""Tests for the hermetic config directory and the whitelisted
environment. The canary test runs the real subprocess_runner against a
stub claude script, so the boundary is measured, not assumed."""

import json
import sys
from pathlib import Path

import pytest

from runner import hermetic
from runner.generate import GenerationError, subprocess_runner
from runner.hermetic import (
    CONFIG_DIR_VAR,
    CREDENTIALS_FILE,
    ENV_WHITELIST,
    TOKEN_VAR,
    hermetic_call,
    manifest_sha256,
)

STUB_BODY = """
import json, os
init = {
    "type": "system",
    "subtype": "init",
    "output_style": "default",
    "model": "claude-sonnet-5",
    "claude_code_version": "0.0.0",
    "plugins": [],
    "environ": dict(os.environ),
}
result = {
    "type": "result",
    "is_error": False,
    "result": "OK",
    "usage": {
        "output_tokens": 1,
        "input_tokens": 1,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    },
    "modelUsage": {},
    "duration_ms": 1,
}
print(json.dumps(init))
print(json.dumps(result))
"""


def make_stub(tmp_path):
    """A fake claude binary that echoes its environment in the init event."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stub = bin_dir / "claude"
    stub.write_text(f"#!{sys.executable}\n{STUB_BODY}")
    stub.chmod(0o755)
    return bin_dir


def base_environ(tmp_path, **extra):
    home = tmp_path / "parent-home"
    home.mkdir(exist_ok=True)
    environ = {"HOME": str(home), "PATH": "/usr/bin:/bin", "TERM": "dumb", "USER": "tester"}
    environ.update(extra)
    return environ


def test_hermetic_call_hides_the_user_config(tmp_path):
    bin_dir = make_stub(tmp_path)
    user_config = tmp_path / "user-config"
    user_config.mkdir()
    (user_config / "marker.json").write_text("{}")
    environ = base_environ(
        tmp_path,
        PATH=f"{bin_dir}:/usr/bin:/bin",
        CANARY="leak",
        **{CONFIG_DIR_VAR: str(user_config)},
    )

    with hermetic_call("test", environ=environ) as h:
        stdout = subprocess_runner(["claude", "-p", "x"], h.workdir, h.env)
        init = json.loads(stdout.splitlines()[0])
        seen = init["environ"]
        assert seen[CONFIG_DIR_VAR] == str(h.config_dir)
        assert seen[CONFIG_DIR_VAR] != str(user_config)
        assert "CANARY" not in seen
        assert set(h.env) <= set(seen)
        # The platform injects a few variables of its own, but no
        # parent variable outside the whitelist reaches the call.
        assert not (set(environ) - set(h.env)) & set(seen)
        assert h.binary == str(bin_dir / "claude")


def test_hermetic_env_holds_only_the_whitelist(tmp_path):
    environ = base_environ(tmp_path, CANARY="leak", SHELL="/bin/zsh")
    with hermetic_call("test", environ=environ) as h:
        assert set(h.env) == {*ENV_WHITELIST, CONFIG_DIR_VAR}
        for name in ENV_WHITELIST:
            assert h.env[name] == environ[name]


def test_hermetic_env_passes_the_oauth_token_through(tmp_path):
    environ = base_environ(tmp_path, **{TOKEN_VAR: "the-token"})
    with hermetic_call("test", environ=environ) as h:
        assert h.env[TOKEN_VAR] == "the-token"
        assert h.credential_source == "token"
        assert not (h.config_dir / CREDENTIALS_FILE).exists()


def test_hermetic_call_copies_the_credential_with_mode_600(tmp_path):
    environ = base_environ(tmp_path)
    source = Path(environ["HOME"]) / ".claude"
    source.mkdir()
    (source / CREDENTIALS_FILE).write_text('{"token": "secret"}')

    with hermetic_call("test", environ=environ) as h:
        copy = h.config_dir / CREDENTIALS_FILE
        assert copy.read_text() == '{"token": "secret"}'
        assert copy.stat().st_mode & 0o777 == 0o600
        assert h.credential_source == "file"


def test_hermetic_call_removes_the_config_dir(tmp_path):
    environ = base_environ(tmp_path)
    source = Path(environ["HOME"]) / ".claude"
    source.mkdir()
    (source / CREDENTIALS_FILE).write_text('{"token": "secret"}')

    with hermetic_call("test", environ=environ) as h:
        config_dir = h.config_dir
        assert config_dir.is_dir()
    assert not config_dir.exists()


def test_hermetic_call_without_a_credential_warns_and_proceeds(tmp_path, capsys):
    with hermetic_call("test", environ=base_environ(tmp_path)) as h:
        assert h.credential_source == "none"
    assert "no credential found" in capsys.readouterr().err


def test_manifest_sha256_is_stable(monkeypatch):
    first = manifest_sha256()
    assert manifest_sha256() == first
    monkeypatch.setattr(hermetic, "DECLARED_FILES", {"settings.json": "a" * 8})
    assert manifest_sha256() != first


def test_hermetic_call_resolves_the_binary_on_the_whitelisted_path(tmp_path):
    bin_dir = make_stub(tmp_path)
    with_stub = base_environ(tmp_path, PATH=str(bin_dir))
    with hermetic_call("test", environ=with_stub) as h:
        assert h.binary == str(bin_dir / "claude")

    empty = tmp_path / "empty"
    empty.mkdir()
    without = base_environ(tmp_path, PATH=str(empty))
    with hermetic_call("test", environ=without) as h:
        assert h.binary is None


def test_subprocess_runner_rejects_a_missing_env(tmp_path):
    with pytest.raises(GenerationError, match="hermetic environment"):
        subprocess_runner(["claude", "-p", "x"], tmp_path, None)
