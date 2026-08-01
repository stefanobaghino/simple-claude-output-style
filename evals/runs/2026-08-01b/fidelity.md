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
- Baseline rate: 7.46 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 15 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 18/20
- Styled rate: 4.56 per 100 sentences
- Baseline rate: 80.1 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 2 | 18 |
| banned-word | 9 | 25 |
| contraction | 0 | 39 |
| latin-abbreviation | 0 | 15 |
| semicolon | 0 | 16 |
| sentence-length | 1 | 48 |

### Failing pairs

- explanation-03 (rate 16.67):
  - [banned-word] 'amount': The congestion window is the amount of data that the sender can send before it must wait for an acknowledgment.
  - [banned-word] 'avoids': Thus the sender avoids a burst of traffic that could overwhelm the network.
  - [banned-modal] 'could': Thus the sender avoids a burst of traffic that could overwhelm the network.
- summarization-02 (rate 30.0):
  - [banned-word] 'Reduce': Reduce the time between error start and page.
  - [banned-word] 'began': The checkout service began to fail at 09:14 CODEREF, but the page did not go out until 09:21 CODEREF.
  - [banned-modal] 'should': The team should check why the alert took 7 minutes to fire.

## Warnings

- none
