# Run report

- Date: 2026-08-06T09:14:23+00:00
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
| unstyled | 11703 | 218 |
| plain-language | 8952 | 209 |
| technical-simplified | 8682 | 159 |

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 60, measured: 60.
Mean duration: 7208 ms. Mean wall: 9060 ms. Mean startup: 1852 ms.

## Environment

- Claude Code versions observed: 2.1.223
- Models observed: claude-haiku-4-5-20251001, claude-sonnet-5
- Plugin sets observed:
  - playwright, pyright-lsp, rust-analyzer-lsp, simple-output-styles, typescript-lsp

## Warnings

- none
