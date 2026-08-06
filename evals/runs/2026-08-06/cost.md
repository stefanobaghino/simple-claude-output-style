# Token cost report

A style costs tokens in two ways: the style block adds a fixed
quantity of input tokens to every request, and the style changes
the answer length. The report states both numbers per style. The
report reads all pairs of the run, gated or not.

## Input overhead per request

The overhead is the difference in input context tokens between
a styled probe call and an unstyled probe call. Both probe arms
load the plugin, so the difference isolates the style block.
The count weighs cached and uncached input tokens equally; the
dollar cost of a cached token differs.

| Style | Overhead (input context tokens) |
|---|---|
| plain-language | 1460 |
| technical-simplified | 1988 |

Probe: 2026-08-06T06:54:52+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 9329, unstyled 11992, ratio of totals 0.78

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.35 | 0.72 | 0.95 | 1.02 | 1.87 | 0.94 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.35 | 0.64 | 0.83 | 1.54 |
| debugging | 5 | 0.86 | 1.03 | 1.19 | 1.87 |
| explanation | 5 | 0.39 | 0.74 | 0.67 | 0.86 |
| summarization | 5 | 0.95 | 1.0 | 1.07 | 1.38 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8696, unstyled 11992, ratio of totals 0.73

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.37 | 0.59 | 0.83 | 0.95 | 1.96 | 0.88 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.47 | 0.67 | 0.84 | 1.53 |
| debugging | 5 | 0.61 | 0.9 | 1.05 | 1.96 |
| explanation | 5 | 0.37 | 0.53 | 0.55 | 0.85 |
| summarization | 5 | 0.74 | 0.95 | 1.06 | 1.73 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
