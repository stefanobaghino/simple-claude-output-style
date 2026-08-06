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

Judge: opus. Judged on 2026-08-06T07:05:46+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 19 | 14 | 1 | 4 | 0 | 13 |
| plain-language | unstyled | 20 | 8 | 5 | 7 | 0 | 3 |
| technical-simplified | unstyled | 19 | 1 | 9 | 9 | 0 | -8 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 16.0 | 11.5 |
| technical-simplified | 3.0 | - | 5.5 |
| unstyled | 8.5 | 13.5 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 1.52 | [0.829, 2.763] |
| technical-simplified | 0.351 | [0.177, 0.584] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.379 over 116 usable picks.
Split rate: 0.345 over 58 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 0 | 1 | 0 | 4 |
| plain-language | unstyled | 5 | 3 | 0 | 2 | 0 | 3 |
| technical-simplified | unstyled | 5 | 0 | 2 | 3 | 0 | -2 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 0 | 2 | 0 | 3 |
| plain-language | unstyled | 5 | 3 | 2 | 0 | 0 | 1 |
| technical-simplified | unstyled | 5 | 1 | 3 | 1 | 0 | -2 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 4 | 0 | 0 | 0 | 4 |
| plain-language | unstyled | 5 | 2 | 2 | 1 | 0 | 0 |
| technical-simplified | unstyled | 4 | 0 | 3 | 1 | 0 | -3 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 1 | 1 | 0 | 2 |
| plain-language | unstyled | 5 | 0 | 1 | 4 | 0 | -1 |
| technical-simplified | unstyled | 5 | 0 | 1 | 4 | 0 | -1 |

## Length confound

Samples: 56 contests with unequal word counts.
Pearson: 0.311. Spearman: 0.304.
Longer-text win rate: 0.661.

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
