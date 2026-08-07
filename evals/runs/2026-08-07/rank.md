# Clarity-ranking report

Every contest shows a blind judge the two answers of one prompt,
in both orders, and the judge picks the clearer text. This tool
relaxes one harness invariant on purpose: a clarity contest is a
choice, so a judge call sees both answers of a prompt side by
side. Blindness holds through the absence of labels: no prompt
names a style or an arm, and the position mapping lives only in
the raw rows. The judge model differs from the writer of the
answers. The unstyled answer competes as its own arm and anchors
the strength scale.

Caveats:

- The judge is a proxy reader: the picks state a model preference for clarity, not a measured human outcome.
- The unstyled competitor is ungated: every styled competitor passed its rule gate, and the unstyled answer has no gate.
- A clarity pick can reward the shorter text. The length-confound section states the correlation.

Judge: opus. Judged on 2026-08-07T08:39:11+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| clarity-flow | classic-concise | 32 | 8 | 15 | 9 | 0 | -7 |
| clarity-flow | developer-docs | 32 | 6 | 14 | 12 | 0 | -8 |
| clarity-flow | plain-language | 32 | 7 | 18 | 7 | 0 | -11 |
| clarity-flow | technical-simplified | 26 | 12 | 4 | 10 | 0 | 8 |
| clarity-flow | unstyled | 32 | 9 | 10 | 13 | 0 | -1 |
| classic-concise | developer-docs | 32 | 7 | 14 | 11 | 0 | -7 |
| classic-concise | plain-language | 32 | 8 | 16 | 8 | 0 | -8 |
| classic-concise | technical-simplified | 26 | 13 | 3 | 10 | 0 | 10 |
| classic-concise | unstyled | 32 | 9 | 9 | 14 | 0 | 0 |
| developer-docs | plain-language | 32 | 7 | 12 | 13 | 0 | -5 |
| developer-docs | technical-simplified | 26 | 18 | 4 | 4 | 0 | 14 |
| developer-docs | unstyled | 32 | 16 | 6 | 10 | 0 | 10 |
| plain-language | technical-simplified | 26 | 13 | 6 | 7 | 0 | 7 |
| plain-language | unstyled | 32 | 17 | 9 | 6 | 0 | 8 |
| technical-simplified | unstyled | 26 | 3 | 12 | 11 | 0 | -9 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | clarity-flow | classic-concise | developer-docs | plain-language | technical-simplified | unstyled |
|---|---|---|---|---|---|---|
| clarity-flow | - | 12.5 | 12.0 | 10.5 | 17.0 | 15.5 |
| classic-concise | 19.5 | - | 12.5 | 12.0 | 18.0 | 16.0 |
| developer-docs | 20.0 | 19.5 | - | 13.5 | 20.0 | 21.0 |
| plain-language | 21.5 | 20.0 | 18.5 | - | 16.5 | 20.0 |
| technical-simplified | 9.0 | 8.0 | 6.0 | 9.5 | - | 8.5 |
| unstyled | 16.5 | 16.0 | 11.0 | 12.0 | 17.5 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

The table lists the competitors from the highest strength to the
lowest. A competitor without a finite strength comes last.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 1.695 | [1.222, 2.458] |
| developer-docs | 1.6 | [1.164, 2.303] |
| classic-concise | 1.117 | [0.827, 1.595] |
| unstyled | 1.0 | n/a |
| clarity-flow | 0.884 | [0.646, 1.225] |
| technical-simplified | 0.554 | [0.377, 0.775] |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.386 over 900 usable picks.
Split rate: 0.322 over 450 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| clarity-flow | classic-concise | 8 | 3 | 4 | 1 | 0 | -1 |
| clarity-flow | developer-docs | 8 | 2 | 4 | 2 | 0 | -2 |
| clarity-flow | plain-language | 8 | 2 | 4 | 2 | 0 | -2 |
| clarity-flow | technical-simplified | 6 | 3 | 2 | 1 | 0 | 1 |
| clarity-flow | unstyled | 8 | 3 | 1 | 4 | 0 | 2 |
| classic-concise | developer-docs | 8 | 3 | 2 | 3 | 0 | 1 |
| classic-concise | plain-language | 8 | 2 | 5 | 1 | 0 | -3 |
| classic-concise | technical-simplified | 6 | 2 | 1 | 3 | 0 | 1 |
| classic-concise | unstyled | 8 | 3 | 2 | 3 | 0 | 1 |
| developer-docs | plain-language | 8 | 0 | 5 | 3 | 0 | -5 |
| developer-docs | technical-simplified | 6 | 4 | 2 | 0 | 0 | 2 |
| developer-docs | unstyled | 8 | 3 | 2 | 3 | 0 | 1 |
| plain-language | technical-simplified | 6 | 3 | 1 | 2 | 0 | 2 |
| plain-language | unstyled | 8 | 4 | 2 | 2 | 0 | 2 |
| technical-simplified | unstyled | 6 | 3 | 2 | 1 | 0 | 1 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| clarity-flow | classic-concise | 8 | 2 | 3 | 3 | 0 | -1 |
| clarity-flow | developer-docs | 8 | 1 | 3 | 4 | 0 | -2 |
| clarity-flow | plain-language | 8 | 2 | 4 | 2 | 0 | -2 |
| clarity-flow | technical-simplified | 7 | 2 | 1 | 4 | 0 | 1 |
| clarity-flow | unstyled | 8 | 2 | 4 | 2 | 0 | -2 |
| classic-concise | developer-docs | 8 | 3 | 4 | 1 | 0 | -1 |
| classic-concise | plain-language | 8 | 3 | 4 | 1 | 0 | -1 |
| classic-concise | technical-simplified | 7 | 3 | 1 | 3 | 0 | 2 |
| classic-concise | unstyled | 8 | 1 | 3 | 4 | 0 | -2 |
| developer-docs | plain-language | 8 | 1 | 4 | 3 | 0 | -3 |
| developer-docs | technical-simplified | 7 | 5 | 2 | 0 | 0 | 3 |
| developer-docs | unstyled | 8 | 6 | 0 | 2 | 0 | 6 |
| plain-language | technical-simplified | 7 | 3 | 3 | 1 | 0 | 0 |
| plain-language | unstyled | 8 | 4 | 3 | 1 | 0 | 1 |
| technical-simplified | unstyled | 7 | 0 | 3 | 4 | 0 | -3 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| clarity-flow | classic-concise | 8 | 2 | 4 | 2 | 0 | -2 |
| clarity-flow | developer-docs | 8 | 2 | 4 | 2 | 0 | -2 |
| clarity-flow | plain-language | 8 | 0 | 7 | 1 | 0 | -7 |
| clarity-flow | technical-simplified | 7 | 5 | 1 | 1 | 0 | 4 |
| clarity-flow | unstyled | 8 | 1 | 4 | 3 | 0 | -3 |
| classic-concise | developer-docs | 8 | 0 | 4 | 4 | 0 | -4 |
| classic-concise | plain-language | 8 | 1 | 4 | 3 | 0 | -3 |
| classic-concise | technical-simplified | 7 | 6 | 0 | 1 | 0 | 6 |
| classic-concise | unstyled | 8 | 2 | 3 | 3 | 0 | -1 |
| developer-docs | plain-language | 8 | 1 | 2 | 5 | 0 | -1 |
| developer-docs | technical-simplified | 7 | 7 | 0 | 0 | 0 | 7 |
| developer-docs | unstyled | 8 | 2 | 3 | 3 | 0 | -1 |
| plain-language | technical-simplified | 7 | 6 | 1 | 0 | 0 | 5 |
| plain-language | unstyled | 8 | 5 | 2 | 1 | 0 | 3 |
| technical-simplified | unstyled | 7 | 0 | 6 | 1 | 0 | -6 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| clarity-flow | classic-concise | 8 | 1 | 4 | 3 | 0 | -3 |
| clarity-flow | developer-docs | 8 | 1 | 3 | 4 | 0 | -2 |
| clarity-flow | plain-language | 8 | 3 | 3 | 2 | 0 | 0 |
| clarity-flow | technical-simplified | 6 | 2 | 0 | 4 | 0 | 2 |
| clarity-flow | unstyled | 8 | 3 | 1 | 4 | 0 | 2 |
| classic-concise | developer-docs | 8 | 1 | 4 | 3 | 0 | -3 |
| classic-concise | plain-language | 8 | 2 | 3 | 3 | 0 | -1 |
| classic-concise | technical-simplified | 6 | 2 | 1 | 3 | 0 | 1 |
| classic-concise | unstyled | 8 | 3 | 1 | 4 | 0 | 2 |
| developer-docs | plain-language | 8 | 5 | 1 | 2 | 0 | 4 |
| developer-docs | technical-simplified | 6 | 2 | 0 | 4 | 0 | 2 |
| developer-docs | unstyled | 8 | 5 | 1 | 2 | 0 | 4 |
| plain-language | technical-simplified | 6 | 1 | 1 | 4 | 0 | 0 |
| plain-language | unstyled | 8 | 4 | 2 | 2 | 0 | 2 |
| technical-simplified | unstyled | 6 | 0 | 1 | 5 | 0 | -1 |

## Length confound

Samples: 444 contests with unequal word counts.
Pearson: 0.189. Spearman: 0.22.
Longer-text win rate: 0.64.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 900, measured: 900.
Mean duration: 4075 ms. Mean wall: 66738 ms. Mean startup: 62663 ms.

## Harness spend

A stored call row holds the token counts of its call: the
uncached input, cache-write input, cache-read input, and
output tokens. The cache-read share is the cache-read total
over the whole input total.

Calls: 900, measured: 900.
Input tokens: 1800 uncached, 1825880 cache write, 1849500 cache read. Output tokens: 44737.
Cache-read share: 0.503.

## Warnings

- technical-simplified/explanation-08: the pair failed the gate, excluded
- technical-simplified/code-review-07: the pair failed the gate, excluded
- technical-simplified/summarization-06: the pair failed the gate, excluded
- technical-simplified/summarization-07: the pair failed the gate, excluded
- technical-simplified/debugging-07: the pair failed the gate, excluded
- technical-simplified/code-review-08: the pair failed the gate, excluded
