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
- Baseline rate: 8.98 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 22 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 17/20
- Styled rate: 6.01 per 100 sentences
- Baseline rate: 65.71 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 1 | 13 |
| banned-word | 13 | 31 |
| contraction | 0 | 43 |
| latin-abbreviation | 0 | 22 |
| semicolon | 0 | 7 |
| sentence-length | 3 | 45 |

### Failing pairs

- explanation-05 (rate 16.67):
  - [banned-word] 'as': The garbage collector cannot free an object as long as a reference to that object exists.
  - [sentence-length] 'If an object registers a listener on a l': If an object registers a listener on a long-lived object, such as an event emitter, and the program never removes that listener, the long-lived object keeps a reference to the listener.
- explanation-03 (rate 20.0):
  - [banned-word] 'amount': Thus it sends a small amount of data first, then increases the send rate step by step.
  - [banned-word] 'amount': If a sender pushes a large amount of data at once, routers along the path can fill their buffers and drop packets.
  - [banned-modal] 'could': Without slow start, a new connection could send data at full speed from the first packet.
  - [banned-word] 'detects': The sender learns the available capacity through gradual increases, and it backs off when it detects loss.
- debugging-04 (rate 25.0):
  - [banned-word] 'detect': If you do not know the exact encoding of the file, add CODEREF or use a library like CODEREF to detect it first.

## Warnings

- none
