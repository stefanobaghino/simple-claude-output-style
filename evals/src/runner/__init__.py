"""Answer-pair generation through the Claude Code CLI.

The runner produces, per prompt, one answer per style and one shared
unstyled answer, under identical conditions, and stores the answers
with their provenance.
"""

from .generate import Generation, GenerationError, build_argv, generate

__all__ = ["Generation", "GenerationError", "build_argv", "generate"]
