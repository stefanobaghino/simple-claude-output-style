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

Probe: 2026-08-06T06:55:54+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 10019, unstyled 11498, ratio of totals 0.87

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.59 | 0.81 | 0.9 | 1.12 | 1.32 | 0.94 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.59 | 0.88 | 0.87 | 1.03 |
| debugging | 5 | 0.73 | 0.91 | 0.93 | 1.32 |
| explanation | 5 | 0.7 | 0.84 | 0.88 | 1.22 |
| summarization | 5 | 0.88 | 1.12 | 1.1 | 1.19 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8783, unstyled 11498, ratio of totals 0.76

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.5 | 0.62 | 0.86 | 1.0 | 1.49 | 0.83 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.5 | 0.84 | 0.9 | 1.49 |
| debugging | 5 | 0.55 | 0.77 | 0.84 | 1.16 |
| explanation | 5 | 0.5 | 0.62 | 0.63 | 0.87 |
| summarization | 5 | 0.89 | 0.99 | 0.97 | 1.02 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
