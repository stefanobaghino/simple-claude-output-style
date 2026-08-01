"""Turn Markdown into lintable text segments.

The style exempts code, identifiers, file paths, error messages, and quoted
text. Each exempt span becomes one placeholder token, because the style counts
each technical noun as one word.

Exempt spans:
- Fenced code blocks and indented code blocks: dropped.
- Inline code: one placeholder token.
- Block quotes: dropped, because a block quote reproduces text of another
  author.
- Double-quoted spans: one placeholder token.
- URLs, file paths, dotted names, snake_case, camelCase, and uppercase
  acronyms: one placeholder token each.
- Link targets and images: dropped. Link text stays.

The HTML comments <!-- style-lint off --> and <!-- style-lint on --> switch
the linter off and on between blocks. A style file quotes banned words as
content, and that content must not count as violations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from markdown_it import MarkdownIt
from markdown_it.token import Token

PLACEHOLDER = "CODEREF"

_QUOTED = re.compile(r'"[^"\n]*"')
_URL = re.compile(r"https?://\S+")
_IDENTIFIER = re.compile(
    r"""
      (?<![\w.])(?:~?/|\.{1,2}/)[\w./-]+   # unix path
    | \b\w{2,}(?:\.\w{2,})+\b              # dotted name, file name
    | \b\w+_[\w.]+\b                       # snake_case
    | \b[a-z]+[A-Z]\w*\b                   # camelCase
    | \b[A-Z]{2,}[A-Z0-9]*\b               # uppercase acronym
    | (?<![\w.])\.\w{2,}\b                 # dotfile, such as .venv
    """,
    re.VERBOSE,
)
_DIRECTIVE = re.compile(r"<!--\s*style-lint\s+(off|on)\s*-->")
_CURLY = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})


@dataclass(frozen=True)
class Segment:
    """One lintable run of text, with its 1-based source line."""

    text: str
    line: int


def _assemble(children: list[Token] | None) -> str:
    parts: list[str] = []
    for child in children or []:
        if child.type == "text":
            parts.append(child.content)
        elif child.type == "code_inline":
            parts.append(PLACEHOLDER)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
        # link_open, link_close, image, html_inline: dropped
    return "".join(parts)


def extract_segments(markdown: str) -> list[Segment]:
    """Parse Markdown and return the segments that the linter must check."""
    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(markdown)
    segments: list[Segment] = []
    quote_depth = 0
    lint_on = True
    line = 1
    for token in tokens:
        if token.type == "blockquote_open":
            quote_depth += 1
        elif token.type == "blockquote_close":
            quote_depth -= 1
        elif token.type == "html_block":
            for match in _DIRECTIVE.finditer(token.content):
                lint_on = match.group(1) == "on"
        elif token.type == "inline":
            if quote_depth > 0 or not lint_on:
                continue
            if token.map:
                line = token.map[0] + 1
            text = _assemble(token.children).translate(_CURLY)
            text = _QUOTED.sub(PLACEHOLDER, text)
            text = _URL.sub(PLACEHOLDER, text)
            text = _IDENTIFIER.sub(PLACEHOLDER, text)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                segments.append(Segment(text=text, line=line))
    return segments
