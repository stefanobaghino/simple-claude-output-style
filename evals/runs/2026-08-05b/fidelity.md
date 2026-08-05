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
- Baseline rate: 6.05 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 13 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 16/20
- Styled rate: 6.34 per 100 sentences
- Baseline rate: 80.93 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 2 | 17 |
| banned-word | 10 | 29 |
| contraction | 0 | 47 |
| latin-abbreviation | 0 | 13 |
| semicolon | 0 | 15 |
| sentence-length | 6 | 53 |

### Failing pairs

- explanation-01 (rate 17.65):
  - [banned-word] 'follow': But each list node needs extra memory, and the map must follow a pointer for each step.
  - [banned-word] 'avoids': Open addressing avoids the pointer cost, because entries sit inside one array.
  - [banned-modal] 'would': Also, a deletion needs a special marker, because a plain empty slot would break the probe sequence for other keys.
- explanation-03 (rate 16.0):
  - [banned-word] 'amount': If the sender sends a large amount of data at once, the sender can fill up router buffers along the path.
  - [banned-word] 'amount': This value sets the amount of data that the sender can send before the sender must wait for an acknowledgment.
  - [banned-word] 'detects': The sender detects packet loss.
  - [sentence-length] 'The doubling pattern of slow start finds': The doubling pattern of slow start finds a workable rate within a few round-trips, and the loss response keeps the rate from a growing without bound.
- explanation-05 (rate 15.38):
  - [banned-word] 'since': This is why a leak can happen: the leak is not a failure of the collector, but a mistake in the code, since the code keeps a reference alive past its correct lifetime.
  - [sentence-length] 'This is why a leak can happen: the leak ': This is why a leak can happen: the leak is not a failure of the collector, but a mistake in the code, since the code keeps a reference alive past its correct lifetime.
- debugging-04 (rate 33.33):
  - [banned-word] 'detect': If you do not know the encoding of the input files in advance, add CODEREF or detect the encoding first with a library such as CODEREF.
  - [sentence-length] 'If you do not know the encoding of the i': If you do not know the encoding of the input files in advance, add CODEREF or detect the encoding first with a library such as CODEREF.

## Warnings

- none
