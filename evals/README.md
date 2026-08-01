# Evaluation harness

This directory holds the evaluation harness for the output styles in
`plugin/output-styles/`. The harness stays outside `plugin/` on purpose:
the marketplace serves only the `plugin/` directory, so installers never
receive the harness.

The harness has two components. The first is a deterministic linter. It
checks a Markdown text against the writing rules of a style and reports
each violation, plus a rate per 100 sentences. The second is a pair
runner. It produces, per prompt, one answer per style and one shared
unstyled answer, through the Claude Code CLI, and stores the answers
with their provenance. See the tracking issue in this repository for
the other planned components.

## Rule files

The engine is shared, and the rules are data. Each style has one rule file
in `rules/`, named `<style>.rules.yaml`. The header comment of each rule
file documents the exclusions of the style: the rules that need judgment
and thus stay outside the mechanical checks.

## How to run

The harness uses [uv](https://docs.astral.sh/uv/). From this directory:

```
uv run pytest
uv run style-lint FILE.md --rules rules/technical-simplified.rules.yaml
uv run style-pairs
```

The linter exits with code 1 when it finds a violation.

The pair runner reads the prompt set in `prompts/prompts.yaml` and calls
the `claude` CLI once per answer, on the account of the person who runs
it. The call is isolated as far as the CLI permits: no tools, no MCP
servers, no hooks, one turn, and no dynamic system-prompt sections.
Plugins from the user configuration still load; the run data records
them, so a change in the environment stays visible. An interrupted run
resumes when the same invocation runs again. The runner exits with code
1 when the pair set is incomplete.

## Run data

Stored runs live under `runs/`, one directory per run, named `<date>`:

```
runs/<YYYY-MM-DD>/
  provenance.json   # prompt-set hash, conditions, style hashes, linter toolchain
  answers.jsonl     # one line per answer; style null marks the unstyled answer
  report.md         # completeness, volume, environment, warnings
```

A pair is not stored twice: it is the line for `(prompt, style)` plus
the line for `(prompt, null)`. The data is plain text in plain git: no
LFS, and no single file above about 5 MB. Keep raw transcripts out;
store only what the reports consume.
