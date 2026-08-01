# Run report

- Date: 2026-08-01T19:08:04+00:00
- Model requested: sonnet
- Prompts: 20
- Styles: plain-language, technical-simplified

## Completeness

| Arm | Answers | Missing |
|---|---|---|
| unstyled | 20/20 | none |
| plain-language | 20/20 | none |
| technical-simplified | 20/20 | none |

## Volume

| Arm | Output tokens | Mean words per answer |
|---|---|---|
| unstyled | 9156 | 188 |
| plain-language | 7935 | 184 |
| technical-simplified | 8083 | 154 |

## Environment

- Claude Code versions observed: 2.1.220
- Models observed: claude-haiku-4-5-20251001, claude-sonnet-5
- Plugin sets observed:
  - allium, playwright, rust-analyzer-lsp, simple-output-styles, typescript-lsp
  - playwright, rust-analyzer-lsp, simple-output-styles, typescript-lsp

## Warnings

- The repository was dirty during the run. The style hashes in the provenance are authoritative, the commit is not.
- The answers come from more than one plugin environment.
