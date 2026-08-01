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

Probe: 2026-08-01T19:32:43+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 7935, unstyled 9156, ratio of totals 0.87

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.51 | 0.79 | 0.99 | 1.09 | 1.33 | 0.94 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.51 | 0.94 | 0.93 | 1.29 |
| debugging | 5 | 0.57 | 0.84 | 0.9 | 1.33 |
| explanation | 5 | 0.6 | 0.85 | 0.83 | 1.19 |
| summarization | 5 | 1.03 | 1.05 | 1.1 | 1.32 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8083, unstyled 9156, ratio of totals 0.88

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.43 | 0.71 | 0.93 | 1.11 | 1.63 | 0.93 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.61 | 0.76 | 0.91 | 1.49 |
| debugging | 5 | 0.76 | 1.14 | 1.15 | 1.63 |
| explanation | 5 | 0.43 | 0.61 | 0.69 | 0.98 |
| summarization | 5 | 0.73 | 0.99 | 0.97 | 1.15 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
