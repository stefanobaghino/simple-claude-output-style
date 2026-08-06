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

Judge: opus. Judged on 2026-08-05T21:09:21+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 18 | 14 | 2 | 2 | 0 | 12 |
| plain-language | unstyled | 20 | 8 | 5 | 7 | 0 | 3 |
| technical-simplified | unstyled | 18 | 3 | 10 | 5 | 0 | -7 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 15.0 | 11.5 |
| technical-simplified | 3.0 | - | 5.5 |
| unstyled | 8.5 | 12.5 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 1.523 | [0.811, 3.227] |
| technical-simplified | 0.377 | [0.155, 0.726] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.411 over 112 usable picks.
Split rate: 0.25 over 56 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 1 | 0 | 0 | 3 |
| plain-language | unstyled | 5 | 2 | 2 | 1 | 0 | 0 |
| technical-simplified | unstyled | 5 | 0 | 4 | 1 | 0 | -4 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 3 | 1 | 0 | 0 | 2 |
| plain-language | unstyled | 5 | 2 | 1 | 2 | 0 | 1 |
| technical-simplified | unstyled | 4 | 2 | 2 | 0 | 0 | 0 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 4 | 0 | 0 | 0 | 4 |
| plain-language | unstyled | 5 | 2 | 2 | 1 | 0 | 0 |
| technical-simplified | unstyled | 4 | 0 | 3 | 1 | 0 | -3 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 0 | 2 | 0 | 3 |
| plain-language | unstyled | 5 | 2 | 0 | 3 | 0 | 2 |
| technical-simplified | unstyled | 5 | 1 | 1 | 3 | 0 | 0 |

## Length confound

Samples: 56 contests with unequal word counts.
Pearson: 0.304. Spearman: 0.259.
Longer-text win rate: 0.75.

## Warnings

- technical-simplified/explanation-02: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
