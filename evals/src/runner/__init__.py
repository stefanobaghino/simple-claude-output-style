"""Answer-pair generation through the Claude Code CLI.

The runner produces, per prompt, one answer per style and one shared
unstyled answer, under identical conditions, and stores the answers
with their provenance.
"""

from .generate import (
    Generation,
    GenerationError,
    PluginLeakError,
    build_argv,
    generate,
    parse_events,
    plugin_name,
    style_reference,
)
from .hermetic import CONFIG_MODE, Hermetic, hermetic_call, manifest_sha256

__all__ = [
    "CONFIG_MODE",
    "Generation",
    "GenerationError",
    "Hermetic",
    "PluginLeakError",
    "build_argv",
    "generate",
    "hermetic_call",
    "manifest_sha256",
    "parse_events",
    "plugin_name",
    "style_reference",
]
