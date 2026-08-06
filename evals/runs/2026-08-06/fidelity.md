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
- Baseline rate: 8.14 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 21 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 19/20
- Styled rate: 5.0 per 100 sentences
- Baseline rate: 73.64 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 1 | 19 |
| banned-word | 8 | 36 |
| contraction | 0 | 51 |
| latin-abbreviation | 0 | 21 |
| semicolon | 0 | 12 |
| sentence-length | 6 | 51 |

### Failing pairs

- explanation-03 (rate 22.73):
  - [banned-word] 'begins': Slow start begins with a small window, often equal to a few packets.
  - [banned-word] 'detects': The sender detects packet loss.
  - [banned-word] 'reduces': When this happens, the sender reduces the window and starts a new growth phase.
  - [banned-word] 'avoids': It avoids an unsafe burst of traffic at the start of a connection, but it still reaches full speed within a small number of round trips.
  - [sentence-length] 'It avoids an unsafe burst of traffic at ': It avoids an unsafe burst of traffic at the start of a connection, but it still reaches full speed within a small number of round trips.

## Warnings

- none
