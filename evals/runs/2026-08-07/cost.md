# Token cost report

A style costs tokens in two ways: the style block adds a fixed
quantity of input tokens to every request, and the style changes
the answer length. The report states both numbers per style. The
report reads all pairs of the run, gated or not.

## Input overhead per request

The overhead is the difference in input context tokens between
a styled probe call and an unstyled probe call of the same
repeat. Both probe arms load the plugin, so the difference
isolates the style block. The weighted overhead multiplies each
token count by its price ratio against one uncached input token
(uncached 1.0, cache write 1.25, cache read 0.1), so the unit is
uncached-token equivalents.

| Style | Overhead tokens (mean ± stdev) | Weighted overhead (mean ± stdev) |
|---|---|---|
| clarity-flow | 1238.0 ± 0.0 | 123.8 ± 0.0 |
| classic-concise | 1302.0 ± 0.0 | 130.2 ± 0.0 |
| developer-docs | 1241.0 ± 0.0 | 124.1 ± 0.0 |
| plain-language | 1460.0 ± 0.0 | 146.0 ± 0.0 |
| technical-simplified | 1988.0 ± 0.0 | 198.8 ± 0.0 |

Probe: 2026-08-07T09:00:46+00:00, model sonnet, repeats 3.

## Harness spend

A stored call row holds the token counts of its call: the
uncached input, cache-write input, cache-read input, and
output tokens. The cache-read share is the cache-read total
over the whole input total.

Calls: 18, measured: 18.
Input tokens: 36 uncached, 2226 cache write, 171597 cache read. Output tokens: 72.
Cache-read share: 0.987.

## Answer-length ratio

The ratio of a pair is the output-token count of the styled
answer divided by the output-token count of the unstyled answer
of the same prompt. A ratio below 1 means a shorter styled
answer.

### clarity-flow

- Pairs: 32
- Output tokens: styled 28483, unstyled 27423, ratio of totals 1.04

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 32 | 0.36 | 0.68 | 0.86 | 1.04 | 13.07 | 1.36 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 8 | 0.6 | 0.8 | 0.97 | 2.12 |
| debugging | 8 | 0.36 | 0.94 | 2.44 | 13.07 |
| explanation | 8 | 0.41 | 0.63 | 1.02 | 3.6 |
| summarization | 8 | 0.68 | 0.95 | 1.01 | 1.86 |

### classic-concise

- Pairs: 32
- Output tokens: styled 24000, unstyled 27423, ratio of totals 0.88

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 32 | 0.36 | 0.55 | 0.73 | 0.93 | 14.21 | 1.17 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 8 | 0.36 | 0.67 | 0.67 | 1.17 |
| debugging | 8 | 0.41 | 0.85 | 2.52 | 14.21 |
| explanation | 8 | 0.48 | 0.67 | 0.7 | 1.0 |
| summarization | 8 | 0.37 | 0.84 | 0.79 | 1.08 |

### developer-docs

- Pairs: 32
- Output tokens: styled 27959, unstyled 27423, ratio of totals 1.02

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 32 | 0.09 | 0.75 | 0.99 | 1.34 | 16.01 | 1.48 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 8 | 0.09 | 1.15 | 1.01 | 1.61 |
| debugging | 8 | 0.59 | 1.16 | 2.97 | 16.01 |
| explanation | 8 | 0.67 | 0.8 | 0.91 | 1.39 |
| summarization | 8 | 0.73 | 0.98 | 1.04 | 1.7 |

### plain-language

- Pairs: 32
- Output tokens: styled 25389, unstyled 27423, ratio of totals 0.93

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 32 | 0.24 | 0.8 | 0.91 | 1.38 | 4.25 | 1.14 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 8 | 0.35 | 0.96 | 1.0 | 1.95 |
| debugging | 8 | 0.24 | 0.86 | 1.42 | 4.25 |
| explanation | 8 | 0.5 | 0.86 | 0.99 | 1.8 |
| summarization | 8 | 0.8 | 0.97 | 1.16 | 1.9 |

### technical-simplified

- Pairs: 32
- Output tokens: styled 27391, unstyled 27423, ratio of totals 1.0

| n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|
| 32 | 0.08 | 0.69 | 1.03 | 1.24 | 22.83 | 1.67 |

| Task type | n | min | median | mean | max |
|---|---|---|---|---|---|
| code-review | 8 | 0.08 | 0.87 | 0.82 | 1.62 |
| debugging | 8 | 0.78 | 1.22 | 3.88 | 22.83 |
| explanation | 8 | 0.53 | 0.69 | 0.87 | 2.02 |
| summarization | 8 | 0.22 | 1.05 | 1.11 | 2.38 |

## Reading the ratio

A lower ratio is not by itself a win: fewer tokens with less content is a loss. Issue #7 measures whether the content survives.

## Warnings

- none
