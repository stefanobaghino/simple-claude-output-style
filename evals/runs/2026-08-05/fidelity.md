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
- Baseline rate: 6.22 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 14 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 16/20
- Styled rate: 5.3 per 100 sentences
- Baseline rate: 62.67 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 1 | 11 |
| banned-word | 12 | 25 |
| contraction | 0 | 44 |
| latin-abbreviation | 0 | 14 |
| semicolon | 0 | 11 |
| sentence-length | 2 | 36 |

### Failing pairs

- explanation-01 (rate 23.53):
  - [sentence-length] 'To find a key, the map hashes the key, t': To find a key, the map hashes the key, then it checks slots in the same probe order until it finds the key or an empty slot.
  - [banned-word] 'As': As more entries fill the map, chaining slows down at a steady rate, because each list grows by a small amount.
  - [banned-word] 'amount': As more entries fill the map, chaining slows down at a steady rate, because each list grows by a small amount.
  - [banned-word] 'as': But open addressing degrades fast when the load factor gets high, because probes get longer as free slots become rare.
- explanation-03 (rate 18.18):
  - [banned-word] 'amount': The congestion window is the amount of unacknowledged data that the sender can have in flight.
  - [banned-word] 'follows': The sender then follows this process:
  - [banned-word] 'detects': The sender detects packet loss.
  - [banned-word] 'confirms': The mechanism trades a slow, cautious start for a fast ramp-up once the sender confirms that the network can handle more traffic.
- summarization-02 (rate 25.0):
  - [banned-word] 'main': Here are the three main takeaways:
  - [banned-word] 'detected': The team detected and fixed the issue fast: paged at 09:21, 27 minutes after the first errors, and the rollback finished at 09:48, 34 minutes after the page.
  - [sentence-length] 'The team detected and fixed the issue fa': The team detected and fixed the issue fast: paged at 09:21, 27 minutes after the first errors, and the rollback finished at 09:48, 34 minutes after the page.
- debugging-04 (rate 25.0):
  - [banned-word] 'detect': If you do not know the exact encoding of the file, use CODEREF or detect the encoding first with a library such as CODEREF.

## Warnings

- none
