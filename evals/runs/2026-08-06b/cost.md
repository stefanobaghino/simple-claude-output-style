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

Probe: 2026-08-06T06:55:09+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 9369, unstyled 11041, ratio of totals 0.85

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.54 | 0.78 | 0.97 | 1.21 | 1.81 | 1.03 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.54 | 0.87 | 0.94 | 1.81 |
| debugging | 5 | 0.81 | 1.29 | 1.28 | 1.73 |
| explanation | 5 | 0.59 | 0.66 | 0.78 | 1.08 |
| summarization | 5 | 0.82 | 1.05 | 1.13 | 1.6 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 9715, unstyled 11041, ratio of totals 0.88

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.5 | 0.68 | 0.77 | 1.07 | 1.91 | 0.9 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.61 | 0.79 | 0.92 | 1.29 |
| debugging | 5 | 0.66 | 0.75 | 0.81 | 1.18 |
| explanation | 5 | 0.5 | 0.68 | 0.91 | 1.91 |
| summarization | 5 | 0.67 | 1.01 | 0.97 | 1.2 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
