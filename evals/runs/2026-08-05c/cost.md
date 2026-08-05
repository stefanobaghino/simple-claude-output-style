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

Probe: 2026-08-05T17:25:06+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 8541, unstyled 11176, ratio of totals 0.76

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.22 | 0.69 | 0.77 | 1.37 | 1.58 | 0.95 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.56 | 0.76 | 0.96 | 1.45 |
| debugging | 5 | 0.22 | 0.71 | 0.95 | 1.58 |
| explanation | 5 | 0.66 | 0.75 | 0.79 | 0.96 |
| summarization | 5 | 0.67 | 1.19 | 1.1 | 1.47 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8703, unstyled 11176, ratio of totals 0.78

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.2 | 0.66 | 0.81 | 1.09 | 1.73 | 0.89 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.68 | 0.98 | 1.08 | 1.73 |
| debugging | 5 | 0.2 | 0.73 | 0.77 | 1.2 |
| explanation | 5 | 0.34 | 0.6 | 0.62 | 0.88 |
| summarization | 5 | 0.59 | 1.08 | 1.08 | 1.66 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
