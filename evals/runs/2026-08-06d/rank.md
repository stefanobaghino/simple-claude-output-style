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

Judge: opus. Judged on 2026-08-06T09:14:27+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 18 | 12 | 1 | 5 | 0 | 11 |
| plain-language | unstyled | 20 | 12 | 4 | 4 | 0 | 8 |
| technical-simplified | unstyled | 18 | 3 | 11 | 4 | 0 | -8 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 14.5 | 14.0 |
| technical-simplified | 3.5 | - | 5.0 |
| unstyled | 6.0 | 13.0 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 2.108 | [1.12, 4.776] |
| technical-simplified | 0.433 | [0.208, 0.86] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.473 over 112 usable picks.
Split rate: 0.232 over 56 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 1 | 1 | 0 | 2 |
| plain-language | unstyled | 5 | 5 | 0 | 0 | 0 | 5 |
| technical-simplified | unstyled | 5 | 1 | 2 | 2 | 0 | -1 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 3 | 0 | 1 | 0 | 3 |
| plain-language | unstyled | 5 | 2 | 1 | 2 | 0 | 1 |
| technical-simplified | unstyled | 4 | 0 | 3 | 1 | 0 | -3 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 3 | 0 | 1 | 0 | 3 |
| plain-language | unstyled | 5 | 3 | 2 | 0 | 0 | 1 |
| technical-simplified | unstyled | 4 | 1 | 3 | 0 | 0 | -2 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 0 | 2 | 0 | 3 |
| plain-language | unstyled | 5 | 2 | 1 | 2 | 0 | 1 |
| technical-simplified | unstyled | 5 | 1 | 3 | 1 | 0 | -2 |

## Length confound

Samples: 53 contests with unequal word counts.
Pearson: 0.138. Spearman: 0.15.
Longer-text win rate: 0.66.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 112, measured: 112.
Mean duration: 3721 ms. Mean wall: 374646 ms. Mean startup: 370925 ms.

## Warnings

- technical-simplified/explanation-04: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
