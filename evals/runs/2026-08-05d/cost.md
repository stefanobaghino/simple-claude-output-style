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

Probe: 2026-08-05T21:08:54+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 9786, unstyled 11830, ratio of totals 0.83

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.45 | 0.72 | 0.9 | 1.02 | 1.43 | 0.89 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.45 | 0.76 | 0.78 | 1.17 |
| debugging | 5 | 0.65 | 0.99 | 0.98 | 1.32 |
| explanation | 5 | 0.64 | 0.72 | 0.78 | 1.05 |
| summarization | 5 | 0.69 | 1.0 | 1.03 | 1.43 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8806, unstyled 11830, ratio of totals 0.74

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.41 | 0.68 | 0.82 | 1.05 | 1.3 | 0.85 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.52 | 0.7 | 0.77 | 1.3 |
| debugging | 5 | 0.86 | 0.92 | 1.0 | 1.18 |
| explanation | 5 | 0.41 | 0.7 | 0.69 | 1.0 |
| summarization | 5 | 0.58 | 1.04 | 0.92 | 1.13 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
