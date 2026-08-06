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

Probe: 2026-08-06T09:36:43+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 8952, unstyled 11703, ratio of totals 0.76

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.45 | 0.76 | 0.89 | 1.07 | 1.51 | 0.92 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.45 | 0.7 | 0.8 | 1.27 |
| debugging | 5 | 0.66 | 0.98 | 1.02 | 1.51 |
| explanation | 5 | 0.52 | 0.86 | 0.82 | 1.02 |
| summarization | 5 | 0.82 | 1.09 | 1.06 | 1.37 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8682, unstyled 11703, ratio of totals 0.74

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.45 | 0.65 | 0.81 | 1.06 | 2.82 | 0.94 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.46 | 0.75 | 0.88 | 1.51 |
| debugging | 5 | 0.58 | 0.86 | 0.9 | 1.48 |
| explanation | 5 | 0.45 | 0.63 | 0.62 | 0.88 |
| summarization | 5 | 0.65 | 1.11 | 1.35 | 2.82 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
