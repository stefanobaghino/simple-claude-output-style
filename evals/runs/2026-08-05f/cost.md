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

Probe: 2026-08-05T21:13:04+00:00, model sonnet.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### plain-language

- Pairs: 20
- Output tokens: styled 9138, unstyled 10173, ratio of totals 0.9

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.6 | 0.77 | 0.93 | 1.1 | 1.65 | 0.97 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.6 | 0.96 | 0.95 | 1.42 |
| debugging | 5 | 0.78 | 1.06 | 1.12 | 1.65 |
| explanation | 5 | 0.61 | 0.73 | 0.81 | 1.09 |
| summarization | 5 | 0.83 | 1.07 | 1.0 | 1.13 |

### technical-simplified

- Pairs: 20
- Output tokens: styled 9247, unstyled 10173, ratio of totals 0.91

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 20 | 0.49 | 0.77 | 0.96 | 1.1 | 1.69 | 0.99 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 5 | 0.76 | 0.8 | 0.93 | 1.25 |
| debugging | 5 | 0.76 | 1.12 | 1.23 | 1.69 |
| explanation | 5 | 0.49 | 0.84 | 0.81 | 1.09 |
| summarization | 5 | 0.61 | 0.95 | 1.01 | 1.55 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
