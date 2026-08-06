# Fidelity report

A pair passes the gate when its styled answer has at least one
sentence and a violation rate at or below the threshold of its
style. The baseline columns check the unstyled answers with the
same rules; the baseline carries no mark, because the unstyled
answers are not supposed to obey a style. The judged measurements
read only the passing pairs.

## plain-language

- Threshold: 5.0 violations per 100 sentences
- Passing pairs: 20/20
- Styled rate: 0.0 per 100 sentences
- Baseline rate: 5.6 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 13 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 19/20
- Styled rate: 4.48 per 100 sentences
- Baseline rate: 69.83 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 2 | 20 |
| banned-word | 7 | 27 |
| contraction | 0 | 42 |
| latin-abbreviation | 0 | 13 |
| semicolon | 0 | 11 |
| sentence-length | 4 | 49 |

### Failing pairs

- explanation-03 (rate 16.67):
  - [banned-word] 'detects': The sender detects packet loss.
  - [banned-word] 'reduces': CODEREF then reduces the congestion window and adjusts the threshold.
  - [banned-modal] 'would': A fixed, large window from the start would risk immediate congestion.
  - [banned-modal] 'would': A slow, linear ramp-up would waste bandwidth during the early part of the connection.

## Warnings

- none
