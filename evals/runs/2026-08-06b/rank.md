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

Judge: opus. Judged on 2026-08-06T07:04:33+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 18 | 14 | 1 | 3 | 0 | 13 |
| plain-language | unstyled | 20 | 9 | 3 | 8 | 0 | 6 |
| technical-simplified | unstyled | 18 | 4 | 11 | 3 | 0 | -7 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 15.5 | 13.0 |
| technical-simplified | 2.5 | - | 5.5 |
| unstyled | 7.0 | 12.5 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 2.037 | [1.125, 4.253] |
| technical-simplified | 0.394 | [0.157, 0.781] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.482 over 112 usable picks.
Split rate: 0.25 over 56 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 5 | 0 | 0 | 0 | 5 |
| plain-language | unstyled | 5 | 3 | 0 | 2 | 0 | 3 |
| technical-simplified | unstyled | 5 | 2 | 3 | 0 | 0 | -1 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 0 | 1 | 0 | 4 |
| plain-language | unstyled | 5 | 1 | 1 | 3 | 0 | 0 |
| technical-simplified | unstyled | 5 | 1 | 4 | 0 | 0 | -3 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 4 | 0 | 0 | 0 | 4 |
| plain-language | unstyled | 5 | 3 | 2 | 0 | 0 | 1 |
| technical-simplified | unstyled | 4 | 0 | 4 | 0 | 0 | -4 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 1 | 1 | 2 | 0 | 0 |
| plain-language | unstyled | 5 | 2 | 0 | 3 | 0 | 2 |
| technical-simplified | unstyled | 4 | 1 | 0 | 3 | 0 | 1 |

## Length confound

Samples: 54 contests with unequal word counts.
Pearson: 0.294. Spearman: 0.303.
Longer-text win rate: 0.63.

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
