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
- Baseline rate: 6.5 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 16 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 19/20
- Styled rate: 4.65 per 100 sentences
- Baseline rate: 69.92 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 2 | 12 |
| banned-word | 10 | 29 |
| contraction | 0 | 56 |
| latin-abbreviation | 0 | 16 |
| semicolon | 0 | 11 |
| sentence-length | 2 | 48 |

### Failing pairs

- debugging-03 (rate 16.67):
  - [banned-word] 'as': This gives CODEREF as expected.

## Warnings

- none
