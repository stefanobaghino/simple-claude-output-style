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

Judge: opus. Judged on 2026-08-05T21:12:18+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 20 | 16 | 3 | 1 | 0 | 13 |
| plain-language | unstyled | 20 | 10 | 4 | 6 | 0 | 6 |
| technical-simplified | unstyled | 20 | 4 | 13 | 3 | 0 | -9 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 16.5 | 13.0 |
| technical-simplified | 3.5 | - | 5.5 |
| unstyled | 7.0 | 14.5 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 1.838 | [0.995, 3.876] |
| technical-simplified | 0.384 | [0.158, 0.769] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.433 over 120 usable picks.
Split rate: 0.167 over 60 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 1 | 0 | 0 | 3 |
| plain-language | unstyled | 5 | 4 | 0 | 1 | 0 | 4 |
| technical-simplified | unstyled | 5 | 0 | 4 | 1 | 0 | -4 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 0 | 1 | 0 | 4 |
| plain-language | unstyled | 5 | 4 | 0 | 1 | 0 | 4 |
| technical-simplified | unstyled | 5 | 1 | 3 | 1 | 0 | -2 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 5 | 0 | 0 | 0 | 5 |
| plain-language | unstyled | 5 | 1 | 2 | 2 | 0 | -1 |
| technical-simplified | unstyled | 5 | 0 | 5 | 0 | 0 | -5 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 2 | 0 | 0 | 1 |
| plain-language | unstyled | 5 | 1 | 2 | 2 | 0 | -1 |
| technical-simplified | unstyled | 5 | 3 | 1 | 1 | 0 | 2 |

## Length confound

Samples: 59 contests with unequal word counts.
Pearson: 0.275. Spearman: 0.306.
Longer-text win rate: 0.695.

## Warnings

- none
