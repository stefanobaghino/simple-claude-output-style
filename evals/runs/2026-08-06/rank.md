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

Judge: opus. Judged on 2026-08-06T07:03:15+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 19 | 13 | 3 | 3 | 0 | 10 |
| plain-language | unstyled | 20 | 12 | 5 | 3 | 0 | 7 |
| technical-simplified | unstyled | 19 | 5 | 10 | 4 | 0 | -5 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 14.5 | 13.5 |
| technical-simplified | 4.5 | - | 7.0 |
| unstyled | 6.5 | 12.0 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 2.015 | [0.984, 4.654] |
| technical-simplified | 0.601 | [0.28, 1.237] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.483 over 116 usable picks.
Split rate: 0.172 over 58 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 1 | 0 | 0 | 3 |
| plain-language | unstyled | 5 | 2 | 3 | 0 | 0 | -1 |
| technical-simplified | unstyled | 5 | 2 | 2 | 1 | 0 | 0 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 0 | 1 | 0 | 4 |
| plain-language | unstyled | 5 | 3 | 0 | 2 | 0 | 3 |
| technical-simplified | unstyled | 5 | 1 | 3 | 1 | 0 | -2 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 4 | 0 | 0 | 0 | 4 |
| plain-language | unstyled | 5 | 3 | 1 | 1 | 0 | 2 |
| technical-simplified | unstyled | 4 | 0 | 4 | 0 | 0 | -4 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 1 | 2 | 2 | 0 | -1 |
| plain-language | unstyled | 5 | 4 | 1 | 0 | 0 | 3 |
| technical-simplified | unstyled | 5 | 2 | 1 | 2 | 0 | 1 |

## Length confound

Samples: 58 contests with unequal word counts.
Pearson: 0.194. Spearman: 0.306.
Longer-text win rate: 0.621.

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
