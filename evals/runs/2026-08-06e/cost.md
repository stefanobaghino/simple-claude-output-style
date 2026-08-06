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

Probe: 2026-08-06T09:36:45+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 9320, unstyled 10610, ratio of totals 0.88

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.55 | 0.72 | 1.01 | 1.13 | 1.38 | 0.96 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.64 | 1.07 | 1.01 | 1.29 |
| debugging | 5 | 0.55 | 0.81 | 0.86 | 1.38 |
| explanation | 5 | 0.66 | 0.73 | 0.81 | 1.12 |
| summarization | 5 | 1.07 | 1.16 | 1.18 | 1.35 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8328, unstyled 10610, ratio of totals 0.78

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.37 | 0.7 | 0.83 | 0.99 | 2.22 | 0.91 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.53 | 0.84 | 0.91 | 1.59 |
| debugging | 5 | 0.49 | 0.83 | 0.91 | 1.24 |
| explanation | 5 | 0.37 | 0.57 | 0.61 | 0.83 |
| summarization | 5 | 0.89 | 0.98 | 1.21 | 2.22 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
