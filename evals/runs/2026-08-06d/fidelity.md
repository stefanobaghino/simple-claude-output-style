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
- Baseline rate: 6.37 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 16 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 18/20
- Styled rate: 4.53 per 100 sentences
- Baseline rate: 74.1 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 1 | 19 |
| banned-word | 11 | 36 |
| contraction | 0 | 50 |
| latin-abbreviation | 0 | 16 |
| semicolon | 0 | 14 |
| sentence-length | 1 | 51 |

### Failing pairs

- explanation-04 (rate 15.38):
  - [sentence-length] 'A program benefits from more processes w': A program benefits from more processes when it needs strong isolation or when it must use more than one CODEREF core, but the work does not need to share much memory.
  - [banned-word] 'main': Here are the main reasons:
  - [banned-word] 'amounts': Threads work better when tasks share large amounts of data and you want to avoid the cost of process isolation.
  - [banned-word] 'avoid': Threads work better when tasks share large amounts of data and you want to avoid the cost of process isolation.
- debugging-04 (rate 28.57):
  - [banned-word] 'since': Use CODEREF-8 encoding, since it is the most common encoding for text files:
  - [banned-word] 'detect': If you do not know the encoding of the input files, add CODEREF or detect the encoding first with a library such as CODEREF.

## Warnings

- none
