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

Probe: 2026-08-06T09:36:48+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 10590, unstyled 11480, ratio of totals 0.92

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.23 | 0.84 | 0.97 | 1.15 | 2.11 | 1.01 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.85 | 0.98 | 1.3 | 2.11 |
| debugging | 5 | 0.23 | 0.89 | 0.86 | 1.45 |
| explanation | 5 | 0.59 | 0.87 | 0.84 | 1.1 |
| summarization | 5 | 0.7 | 1.15 | 1.05 | 1.26 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 9045, unstyled 11480, ratio of totals 0.79

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.17 | 0.7 | 0.86 | 1.15 | 1.68 | 0.92 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.86 | 1.14 | 1.12 | 1.27 |
| debugging | 5 | 0.17 | 0.76 | 0.88 | 1.68 |
| explanation | 5 | 0.49 | 0.7 | 0.69 | 0.86 |
| summarization | 5 | 0.72 | 1.04 | 0.97 | 1.2 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
