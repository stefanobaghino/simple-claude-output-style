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
- Baseline rate: 7.56 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 18 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 17/20
- Styled rate: 4.63 per 100 sentences
- Baseline rate: 61.76 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 1 | 11 |
| banned-word | 11 | 24 |
| contraction | 1 | 35 |
| latin-abbreviation | 0 | 18 |
| semicolon | 0 | 11 |
| sentence-length | 2 | 48 |

### Failing pairs

- summarization-01 (rate 16.67):
  - [contraction] "'s": What's new
- summarization-02 (rate 30.0):
  - [banned-word] 'main': Here are the three main takeaways:
  - [banned-word] 'began': The team found the problem only after checkout errors began.
  - [banned-modal] 'could': An alert on high pool use could have caught the issue before it caused errors.
- explanation-01 (rate 18.75):
  - [banned-word] 'follows': To find a key, the map follows the same probe order and checks each slot.
  - [sentence-length] 'Chaining is simple and tolerates a high ': Chaining is simple and tolerates a high load factor, but each lookup can need an extra list traversal, and each slot needs extra memory for the list structure.
  - [banned-word] 'as': But performance drops fast as the array fills up, so the map must resize sooner.

## Warnings

- none
