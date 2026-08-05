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

Probe: 2026-08-05T06:28:25+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 8353, unstyled 10430, ratio of totals 0.8

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.44 | 0.73 | 0.93 | 1.08 | 1.3 | 0.9 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.44 | 0.9 | 0.87 | 1.16 |
| debugging | 5 | 0.5 | 0.96 | 0.95 | 1.3 |
| explanation | 5 | 0.54 | 0.72 | 0.8 | 1.05 |
| summarization | 5 | 0.86 | 1.0 | 0.99 | 1.16 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 8717, unstyled 10430, ratio of totals 0.84

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.38 | 0.66 | 0.8 | 0.98 | 2.32 | 0.9 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.66 | 0.93 | 1.15 | 2.32 |
| debugging | 5 | 0.45 | 0.73 | 0.93 | 1.83 |
| explanation | 5 | 0.38 | 0.65 | 0.63 | 0.82 |
| summarization | 5 | 0.68 | 0.88 | 0.9 | 1.17 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
