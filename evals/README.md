# Evaluation harness

This directory holds the evaluation harness for the output styles in
`plugin/output-styles/`. The harness stays outside `plugin/` on purpose:
the marketplace serves only the `plugin/` directory, so installers never
receive the harness.

The first component is a deterministic linter. It checks a Markdown text
against the writing rules of a style and reports each violation, plus a
rate per 100 sentences. See the tracking issue in this repository for the
other planned components.

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
```

The linter exits with code 1 when it finds a violation.

## Run data

Stored runs will live under `runs/`, one directory per run, named
`<date>-<style>`. Each run directory holds `provenance.json` (style name,
style version, model, date), `answers.jsonl`, and `report.md`. The data is
plain text in plain git: no LFS, and no single file above about 5 MB. Keep
raw transcripts out; store only what the reports consume.
