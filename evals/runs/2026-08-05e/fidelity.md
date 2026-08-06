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
- Baseline rate: 7.39 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 19 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 18/20
- Styled rate: 4.78 per 100 sentences
- Baseline rate: 70.04 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 0 | 18 |
| banned-word | 9 | 22 |
| contraction | 0 | 59 |
| latin-abbreviation | 0 | 19 |
| semicolon | 0 | 13 |
| sentence-length | 4 | 49 |

### Failing pairs

- explanation-02 (rate 19.05):
  - [banned-word] 'detects': The update affects zero rows, and your code detects the conflict.
  - [sentence-length] 'When it fits: Use optimistic locking whe': When it fits: Use optimistic locking when conflicts are rare and reads are frequent, such as in web applications with many users who view data but few who edit the same row at the same time.
  - [sentence-length] 'When it fits: Use pessimistic locking wh': When it fits: Use pessimistic locking when conflicts are frequent and a failed update is expensive, such as in banking systems that update the same account balance many times per second.
  - [banned-word] 'reduce': Pessimistic locking prevents conflicts but can reduce throughput because processes wait for locks.
- debugging-04 (rate 16.67):
  - [banned-word] 'substitutes': Use CODEREF only if you do not need exact text content, because it substitutes invalid bytes with a placeholder character.

## Warnings

- none
