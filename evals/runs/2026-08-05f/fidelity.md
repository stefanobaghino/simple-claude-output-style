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
- Styled rate: 0.33 per 100 sentences
- Baseline rate: 8.02 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 1 | 19 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 20/20
- Styled rate: 3.06 per 100 sentences
- Baseline rate: 63.29 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 0 | 10 |
| banned-word | 5 | 26 |
| contraction | 0 | 43 |
| latin-abbreviation | 0 | 19 |
| semicolon | 0 | 13 |
| sentence-length | 4 | 39 |

## Warnings

- none
