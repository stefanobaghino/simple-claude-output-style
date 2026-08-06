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

Judge: opus. Judged on 2026-08-06T09:15:15+00:00.

## Matchups

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 17 | 12 | 2 | 3 | 0 | 10 |
| plain-language | unstyled | 20 | 8 | 6 | 6 | 0 | 2 |
| technical-simplified | unstyled | 17 | 4 | 10 | 3 | 0 | -6 |

## Win matrix

A cell holds the points of the row competitor against the column
competitor: 1 per decisive win plus 0.5 per split.

| | plain-language | technical-simplified | unstyled |
|---|---|---|---|
| plain-language | - | 13.5 | 11.0 |
| technical-simplified | 3.5 | - | 5.5 |
| unstyled | 9.0 | 11.5 | - |

## Bradley-Terry strengths

The scale is anchored on unstyled at strength 1.0.

| Competitor | Strength | 95% CI |
|---|---|---|
| plain-language | 1.353 | [0.704, 2.802] |
| technical-simplified | 0.417 | [0.183, 0.849] |
| unstyled | 1.0 | n/a |

The interval comes from 1000 bootstrap resamples of the scored contests (seed 0).

## Position bias

First-pick rate: 0.444 over 108 usable picks.
Split rate: 0.222 over 54 judged contests.

## Per task type

### code-review

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 4 | 0 | 1 | 0 | 4 |
| plain-language | unstyled | 5 | 3 | 1 | 1 | 0 | 2 |
| technical-simplified | unstyled | 5 | 1 | 3 | 1 | 0 | -2 |

### debugging

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 4 | 2 | 0 | 2 | 0 | 2 |
| plain-language | unstyled | 5 | 2 | 3 | 0 | 0 | -1 |
| technical-simplified | unstyled | 4 | 0 | 3 | 1 | 0 | -3 |

### explanation

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 3 | 3 | 0 | 0 | 0 | 3 |
| plain-language | unstyled | 5 | 1 | 2 | 2 | 0 | -1 |
| technical-simplified | unstyled | 3 | 0 | 3 | 0 | 0 | -3 |

### summarization

| A | B | Contests | A wins | B wins | Splits | Unscored | Net (A) |
|---|---|---|---|---|---|---|---|
| plain-language | technical-simplified | 5 | 3 | 2 | 0 | 0 | 1 |
| plain-language | unstyled | 5 | 2 | 0 | 3 | 0 | 2 |
| technical-simplified | unstyled | 5 | 3 | 1 | 1 | 0 | 2 |

## Length confound

Samples: 54 contests with unequal word counts.
Pearson: 0.34. Spearman: 0.334.
Longer-text win rate: 0.648.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 108, measured: 108.
Mean duration: 3380 ms. Mean wall: 364425 ms. Mean startup: 361045 ms.

## Warnings

- technical-simplified/explanation-05: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- clarity:explanation-01:738cfdf4e9ac844f57547a9e5a8d7554752747e20ec8d015ba0e1e771c138d9a:c606f73750cbeb62884291e6a0312293e2aacfd9beff5cc616460319c5956fb7: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-rank-dkcunvg8","session_id":"23837033-f039-4915-b9ab-ed2b44910b77","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","clea
