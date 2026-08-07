# Fidelity report

A pair passes the gate when its styled answer has at least one
sentence and a violation rate at or below the threshold of its
style. The baseline columns check the unstyled answers with the
same rules; the baseline carries no mark, because the unstyled
answers are not supposed to obey a style. The judged measurements
read only the passing pairs.

## clarity-flow

- Threshold: 10.0 violations per 100 sentences
- Passing pairs: 32/32
- Styled rate: 0.0 per 100 sentences
- Baseline rate: 0.0 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| none | 0 | 0 |

## classic-concise

- Threshold: 10.0 violations per 100 sentences
- Passing pairs: 32/32
- Styled rate: 0.47 per 100 sentences
- Baseline rate: 1.96 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-word | 1 | 9 |
| needless-phrase | 1 | 1 |

## developer-docs

- Threshold: 10.0 violations per 100 sentences
- Passing pairs: 32/32
- Styled rate: 0.18 per 100 sentences
- Baseline rate: 8.61 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 0 | 6 |
| latin-abbreviation | 0 | 37 |
| minimizer | 1 | 1 |

## plain-language

- Threshold: 5.0 violations per 100 sentences
- Passing pairs: 32/32
- Styled rate: 0.0 per 100 sentences
- Baseline rate: 7.24 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| latin-abbreviation | 0 | 37 |

## technical-simplified

- Threshold: 15.0 violations per 100 sentences
- Passing pairs: 26/32
- Styled rate: 7.71 per 100 sentences
- Baseline rate: 79.06 per 100 sentences

| Rule | Styled | Baseline |
|---|---|---|
| banned-modal | 6 | 46 |
| banned-word | 22 | 74 |
| contraction | 0 | 129 |
| latin-abbreviation | 0 | 37 |
| semicolon | 0 | 10 |
| sentence-length | 15 | 108 |

### Failing pairs

- explanation-08 (rate 25.0):
  - [sentence-length] 'The serialization step is often a small ': The serialization step is often a small part of the total request time, so a faster format can still give a small end-to-end gain.
- code-review-07 (rate 0.0):
- summarization-06 (rate 20.0):
  - [banned-modal] 'might': A deploy 20 minutes before the incident changed retry settings and might have contributed, but rollback alone did not restore service.
- summarization-07 (rate 16.67):
  - [sentence-length] 'Second, we do not know the cause of the ': Second, we do not know the cause of the memory growth or the crash: we suspect a larger buffer pool for the memory growth, but we have not profiled it, and we suspect the newer staging kernel for the crash, but we cannot rule out a batcher bug yet.
- debugging-07 (rate 17.95):
  - [sentence-length] 'If two events get the exact same timesta': If two events get the exact same timestamp, and the digest logic uses timestamp as part of a dedup key, one event can overwrite the other.
  - [banned-word] 'amount': If the test waits a fixed amount of time after seeding events, that wait can be enough on an idle developer machine but not enough under CODEREF load.
  - [sentence-length] 'If the test waits a fixed amount of time': If the test waits a fixed amount of time after seeding events, that wait can be enough on an idle developer machine but not enough under CODEREF load.
  - [banned-word] 'Confirm': Confirm that each worker gets an isolated database or schema.
  - [banned-word] 'since': Configure the CODEREF runner to capture logs and the actual digest content on failure, since the runner keeps no artifacts today.
  - [sentence-length] 'Configure the CODEREF runner to capture ': Configure the CODEREF runner to capture logs and the actual digest content on failure, since the runner keeps no artifacts today.
  - [banned-word] 'confirms': If the failure rate increases, this confirms a race and points to the write path as the cause.
- code-review-08 (rate 20.0):
  - [sentence-length] 'If the process that imports this module ': If the process that imports this module stays alive and calls CODEREF many times (a long-running scheduler, not a fresh process per run), the cutoff never moves forward.
  - [banned-word] 'Confirm': Confirm how the schedule actually invokes this function.
  - [banned-modal] 'might': Which of these might be deliberate
  - [banned-modal] 'would': The 500-item cap reads like a deliberate guardrail: a limit on blast radius per run, in case a clock problem or a wrong CODEREF value would otherwise trigger a mass deletion.
  - [sentence-length] 'The 500-item cap reads like a deliberate': The 500-item cap reads like a deliberate guardrail: a limit on blast radius per run, in case a clock problem or a wrong CODEREF value would otherwise trigger a mass deletion.
  - [sentence-length] 'The 45-day cutoff looks like an intended': The 45-day cutoff looks like an intended retention window, not an accident, but it needs a written source (a compliance rule, a storage-cost decision, and so on) so a future reader does not have to guess.
  - [sentence-length] 'My recommendation: before this runs agai': My recommendation: before this runs again, add a minimum age check for CODEREF/CODEREF files, wrap CODEREF in a CODEREF that logs and continues, and apply the 500 cap to all deletions, not just the age-based branch.

## Warnings

- technical-simplified/code-review-07: the answer has no sentences and fails the gate
