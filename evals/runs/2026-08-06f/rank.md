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

Judge: opus. Judged on 2026-08-06T09:15:58+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 19 | 10 | 4 | 5 | 0 | 6 |
| plain-language | unstyled | 20 | 9 | 5 | 6 | 0 | 4 |
| technical-simplified | unstyled | 19 | 7 | 8 | 4 | 0 | -1 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 12.5 | 12.0 |
| technical-simplified | 6.5 | - | 9.0 |
| unstyled | 8.0 | 10.0 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 1.57 | [0.813, 3.096] |
| technical-simplified | 0.859 | [0.433, 1.631] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.457 over 116 usable picks.
Split rate: 0.259 over 58 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 2 | 2 | 1 | 0 | 0 |
| plain-language | unstyled | 5 | 2 | 1 | 2 | 0 | 1 |
| technical-simplified | unstyled | 5 | 4 | 0 | 1 | 0 | 4 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 3 | 0 | 1 | 0 | 3 |
| plain-language | unstyled | 5 | 2 | 1 | 2 | 0 | 1 |
| technical-simplified | unstyled | 4 | 1 | 3 | 0 | 0 | -2 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 5 | 0 | 0 | 0 | 5 |
| plain-language | unstyled | 5 | 4 | 1 | 0 | 0 | 3 |
| technical-simplified | unstyled | 5 | 1 | 4 | 0 | 0 | -3 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 0 | 2 | 3 | 0 | -2 |
| plain-language | unstyled | 5 | 1 | 2 | 2 | 0 | -1 |
| technical-simplified | unstyled | 5 | 1 | 1 | 3 | 0 | 0 |

## Length confound

Samples: 57 contests with unequal word counts.
Pearson: 0.198. Spearman: 0.181.
Longer-text win rate: 0.553.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 116, measured: 116.
Mean duration: 5334 ms. Mean wall: 341754 ms. Mean startup: 336420 ms.

## Warnings

- technical-simplified/debugging-03: the pair failed the gate, excluded
