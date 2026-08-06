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

Probe: 2026-08-05T21:11:50+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 9053, unstyled 11556, ratio of totals 0.78

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.35 | 0.76 | 0.87 | 1.12 | 1.36 | 0.89 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.35 | 0.62 | 0.74 | 1.36 |
| debugging | 5 | 0.63 | 0.87 | 0.92 | 1.13 |
| explanation | 5 | 0.67 | 0.79 | 0.79 | 0.86 |
| summarization | 5 | 0.87 | 1.12 | 1.09 | 1.23 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8472, unstyled 11556, ratio of totals 0.73

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.33 | 0.65 | 0.78 | 1.05 | 1.95 | 0.84 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.33 | 0.66 | 0.67 | 1.09 |
| debugging | 5 | 0.64 | 1.07 | 1.1 | 1.95 |
| explanation | 5 | 0.47 | 0.66 | 0.64 | 0.78 |
| summarization | 5 | 0.78 | 0.98 | 0.95 | 1.17 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
