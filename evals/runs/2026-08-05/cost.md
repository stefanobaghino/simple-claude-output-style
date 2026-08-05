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

Probe: 2026-08-05T06:03:57+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 8876, unstyled 10107, ratio of totals 0.88

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.47 | 0.71 | 0.87 | 1.24 | 1.96 | 0.98 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.47 | 0.77 | 0.83 | 1.4 |
| debugging | 5 | 0.58 | 1.31 | 1.19 | 1.96 |
| explanation | 5 | 0.69 | 0.8 | 0.83 | 1.11 |
| summarization | 5 | 0.83 | 0.95 | 1.08 | 1.5 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8128, unstyled 10107, ratio of totals 0.8

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.36 | 0.64 | 0.82 | 1.07 | 1.83 | 0.88 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.36 | 0.7 | 0.77 | 1.42 |
| debugging | 5 | 0.53 | 1.06 | 1.06 | 1.83 |
| explanation | 5 | 0.46 | 0.65 | 0.67 | 0.84 |
| summarization | 5 | 0.84 | 0.99 | 1.04 | 1.24 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
