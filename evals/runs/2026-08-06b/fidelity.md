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
- Baseline rate: 6.35 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 16 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 18/20
- Styled rate: 4.74 per 100 sentences
- Baseline rate: 61.11 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 1 | 10 |
| banned-word | 9 | 35 |
| contraction | 0 | 48 |
| latin-abbreviation | 0 | 16 |
| semicolon | 0 | 7 |
| sentence-length | 3 | 38 |

### Failing pairs

- explanation-03 (rate 29.17):
  - [banned-word] 'amount': This window sets the amount of data the sender can send before it must wait for an acknowledgment.
  - [banned-word] 'detects': This doubling continues until the sender detects a loss, or until the window reaches a threshold called ssthresh (slow start threshold).
  - [banned-word] 'begins': The word CODEREF refers only to the start: the first window is small, so the sender begins cautiously instead of sending a large burst of data immediately.
  - [sentence-length] 'The word CODEREF refers only to the star': The word CODEREF refers only to the start: the first window is small, so the sender begins cautiously instead of sending a large burst of data immediately.
  - [banned-modal] 'would': Slow start lets a connection find a safe sending rate quickly, without a fixed rate that would waste capacity on fast networks or overwhelm slow ones.
  - [sentence-length] 'Slow start lets a connection find a safe': Slow start lets a connection find a safe sending rate quickly, without a fixed rate that would waste capacity on fast networks or overwhelm slow ones.
  - [banned-word] 'reduces': When a loss occurs, CODEREF treats this loss as a sign of congestion, and it reduces the window.
- summarization-02 (rate 30.0):
  - [banned-word] 'main': Here are the three main takeaways:
  - [banned-word] 'reduce': A faster alert can reduce the time to detect similar issues in the future.
  - [banned-word] 'detect': A faster alert can reduce the time to detect similar issues in the future.

## Warnings

- none
