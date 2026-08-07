"""Shared test isolation.

Every test runs with a scratch HOME and without the config and token
variables, so no test reads the real user configuration or the real
credentials of the developer machine.
"""

import pytest


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path_factory, monkeypatch):
    home = tmp_path_factory.mktemp("home")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
    return home
