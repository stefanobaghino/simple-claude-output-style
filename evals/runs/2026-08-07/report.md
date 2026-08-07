# Run report

- Date: 2026-08-07T08:39:00+00:00
- Model requested: sonnet
- Prompts: 32
- Styles: clarity-flow, classic-concise, developer-docs, plain-language, technical-simplified

## Completeness

| Arm | Answers | Missing |
|---|---|---|
| unstyled | 32/32 | none |
| clarity-flow | 32/32 | none |
| classic-concise | 32/32 | none |
| developer-docs | 32/32 | none |
| plain-language | 32/32 | none |
| technical-simplified | 32/32 | none |

## Volume

| Arm | Output tokens | Mean words per answer |
|---|---|---|
| unstyled | 27423 | 271 |
| clarity-flow | 28483 | 182 |
| classic-concise | 24000 | 201 |
| developer-docs | 27959 | 234 |
| plain-language | 25389 | 256 |
| technical-simplified | 27391 | 194 |

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 192, measured: 192.
Mean duration: 11608 ms. Mean wall: 13112 ms. Mean startup: 1504 ms.

## Harness spend

A stored call row holds the token counts of its call: the
uncached input, cache-write input, cache-read input, and
output tokens. The cache-read share is the cache-read total
over the whole input total.

Calls: 192, measured: 192.
Input tokens: 192 uncached, 133426 cache write, 1747410 cache read. Output tokens: 160645.
Cache-read share: 0.929.

## Environment

- Claude Code versions observed: 2.1.224
- Models observed: claude-haiku-4-5-20251001, claude-sonnet-5
- Plugin sets observed:
  - none
  - simple-output-styles

## Warnings

- The answers come from more than one plugin environment.
