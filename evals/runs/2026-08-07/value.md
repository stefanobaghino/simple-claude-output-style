# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-07T08:39:11+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| clarity-flow | 5 | 5 | 20 | -0.013 | 0.881 | 0.041 | 0.035 |
| classic-concise | 4 | 7 | 20 | -0.018 | 0.828 | 0.034 | 0.023 |
| developer-docs | 6 | 7 | 16 | -0.01 | 0.889 | 0.056 | 0.029 |
| plain-language | 2 | 7 | 20 | -0.036 | 0.874 | 0.059 | 0.038 |
| technical-simplified | 2 | 5 | 16 | -0.012 | 0.884 | 0.031 | 0.034 |

The styled answer must not score worse than the unstyled answer.
- clarity-flow: the styled answer holds (5 wins, 5 losses, 20 ties).
- classic-concise: the styled answer scores worse (4 wins, 7 losses, 20 ties).
- developer-docs: the styled answer scores worse (6 wins, 7 losses, 16 ties).
- plain-language: the styled answer scores worse (2 wins, 7 losses, 20 ties).
- technical-simplified: the styled answer scores worse (2 wins, 5 losses, 16 ties).

### clarity-flow

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-04 | 6 | 3/3 | 0.556 | 0.833 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-06 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| code-review-07 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-08 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.778 | 0.667 | tie |
| debugging-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-06 | 6 | 3/3 | 0.833 | 0.722 | 0.667 | win |
| debugging-07 | 6 | 3/3 | 1.0 | 0.722 | 1.0 | win |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-06 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| explanation-07 | 6 | 3/3 | 0.722 | 1.0 | 1.0 | loss |
| explanation-08 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 0.778 | 0.778 | 0.556 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-06 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-07 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| summarization-08 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### classic-concise

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-02 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| code-review-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-06 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-07 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-08 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-06 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| debugging-07 | 6 | 3/3 | 0.778 | 0.667 | 0.667 | win |
| explanation-01 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| explanation-04 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| explanation-05 | 6 | 3/3 | 0.667 | 0.889 | 1.0 | loss |
| explanation-06 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-07 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| explanation-08 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| summarization-01 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 0.889 | 0.889 | 0.556 | tie |
| summarization-06 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| summarization-07 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| summarization-08 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### developer-docs

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 0.778 | 0.944 | 0.778 | loss |
| code-review-04 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-06 | 6 | 3/3 | 0.667 | 1.0 | 1.0 | loss |
| code-review-08 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 0.722 | 1.0 | win |
| debugging-02 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.722 | 1.0 | 1.0 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-06 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| debugging-07 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-06 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| explanation-07 | 6 | 3/3 | 0.667 | 0.722 | 0.667 | tie |
| explanation-08 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| summarization-01 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-06 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| summarization-07 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| summarization-08 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-02 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-06 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-07 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-08 | 6 | 3/3 | 0.778 | 0.833 | 0.667 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-07 | 6 | 3/3 | 0.778 | 0.722 | 0.444 | loss |
| explanation-01 | 6 | 3/3 | 0.667 | 0.889 | 0.778 | loss |
| explanation-02 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-04 | 6 | 3/3 | 0.722 | 1.0 | 1.0 | loss |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-06 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-07 | 6 | 3/3 | 0.944 | 0.778 | 0.778 | win |
| explanation-08 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |
| summarization-06 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-07 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| summarization-08 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-04 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| code-review-05 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-06 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 0.722 | 1.0 | win |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-06 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| explanation-07 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.778 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| clarity-flow | 9 | 9 | 14 |
| classic-concise | 12 | 10 | 10 |
| developer-docs | 16 | 7 | 9 |
| plain-language | 20 | 6 | 6 |
| technical-simplified | 14 | 10 | 2 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- clarity-flow: Pearson 0.503, Spearman 0.187, over 32 pairs.
- classic-concise: Pearson 0.489, Spearman 0.078, over 32 pairs.
- developer-docs: Pearson 0.534, Spearman 0.655, over 32 pairs.
- plain-language: Pearson 0.293, Spearman 0.413, over 32 pairs.
- technical-simplified: Pearson 0.418, Spearman 0.36, over 26 pairs.

### clarity-flow

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.584 | 0.637 | loss |
| code-review-02 | 0.711 | 0.718 | tie |
| code-review-03 | 0.713 | 0.67 | win |
| code-review-04 | 0.586 | 0.67 | loss |
| code-review-05 | 0.701 | 0.697 | tie |
| code-review-06 | 0.657 | 0.672 | tie |
| code-review-07 | 0.675 | 0.627 | win |
| code-review-08 | 0.686 | 0.598 | win |
| debugging-01 | 0.625 | 0.738 | loss |
| debugging-02 | 0.685 | 0.696 | tie |
| debugging-03 | 0.673 | 0.704 | loss |
| debugging-04 | 0.66 | 0.761 | loss |
| debugging-05 | 0.714 | 0.718 | tie |
| debugging-06 | 0.63 | 0.637 | tie |
| debugging-07 | 0.644 | 0.651 | tie |
| debugging-08 | 0.669 | 0.489 | win |
| explanation-01 | 0.595 | 0.72 | loss |
| explanation-02 | 0.655 | 0.663 | tie |
| explanation-03 | 0.682 | 0.688 | tie |
| explanation-04 | 0.72 | 0.635 | win |
| explanation-05 | 0.611 | 0.676 | loss |
| explanation-06 | 0.586 | 0.596 | tie |
| explanation-07 | 0.575 | 0.625 | loss |
| explanation-08 | 0.651 | 0.589 | win |
| summarization-01 | 0.667 | 0.548 | win |
| summarization-02 | 0.647 | 0.732 | loss |
| summarization-03 | 0.674 | 0.598 | win |
| summarization-04 | 0.672 | 0.668 | tie |
| summarization-05 | 0.769 | 0.7 | win |
| summarization-06 | 0.656 | 0.668 | tie |
| summarization-07 | 0.662 | 0.655 | tie |
| summarization-08 | 0.596 | 0.605 | tie |

### classic-concise

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.703 | 0.637 | win |
| code-review-02 | 0.679 | 0.718 | loss |
| code-review-03 | 0.641 | 0.67 | loss |
| code-review-04 | 0.72 | 0.67 | win |
| code-review-05 | 0.632 | 0.697 | loss |
| code-review-06 | 0.62 | 0.672 | loss |
| code-review-07 | 0.693 | 0.627 | win |
| code-review-08 | 0.682 | 0.598 | win |
| debugging-01 | 0.618 | 0.738 | loss |
| debugging-02 | 0.704 | 0.696 | tie |
| debugging-03 | 0.595 | 0.704 | loss |
| debugging-04 | 0.803 | 0.761 | win |
| debugging-05 | 0.518 | 0.718 | loss |
| debugging-06 | 0.627 | 0.637 | tie |
| debugging-07 | 0.667 | 0.651 | tie |
| debugging-08 | 0.68 | 0.489 | win |
| explanation-01 | 0.674 | 0.72 | loss |
| explanation-02 | 0.644 | 0.663 | tie |
| explanation-03 | 0.668 | 0.688 | tie |
| explanation-04 | 0.631 | 0.635 | tie |
| explanation-05 | 0.686 | 0.676 | tie |
| explanation-06 | 0.622 | 0.596 | win |
| explanation-07 | 0.584 | 0.625 | loss |
| explanation-08 | 0.618 | 0.589 | win |
| summarization-01 | 0.657 | 0.548 | win |
| summarization-02 | 0.695 | 0.732 | loss |
| summarization-03 | 0.642 | 0.598 | win |
| summarization-04 | 0.664 | 0.668 | tie |
| summarization-05 | 0.681 | 0.7 | tie |
| summarization-06 | 0.679 | 0.668 | tie |
| summarization-07 | 0.677 | 0.655 | win |
| summarization-08 | 0.66 | 0.605 | win |

### developer-docs

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.628 | 0.637 | tie |
| code-review-02 | 0.74 | 0.718 | win |
| code-review-03 | 0.458 | 0.67 | loss |
| code-review-04 | 0.716 | 0.67 | win |
| code-review-05 | 0.685 | 0.697 | tie |
| code-review-06 | 0.649 | 0.672 | loss |
| code-review-07 | 0.544 | 0.627 | loss |
| code-review-08 | 0.655 | 0.598 | win |
| debugging-01 | 0.74 | 0.738 | tie |
| debugging-02 | 0.73 | 0.696 | win |
| debugging-03 | 0.797 | 0.704 | win |
| debugging-04 | 0.698 | 0.761 | loss |
| debugging-05 | 0.7 | 0.718 | tie |
| debugging-06 | 0.644 | 0.637 | tie |
| debugging-07 | 0.65 | 0.651 | tie |
| debugging-08 | 0.68 | 0.489 | win |
| explanation-01 | 0.733 | 0.72 | tie |
| explanation-02 | 0.778 | 0.663 | win |
| explanation-03 | 0.68 | 0.688 | tie |
| explanation-04 | 0.672 | 0.635 | win |
| explanation-05 | 0.638 | 0.676 | loss |
| explanation-06 | 0.618 | 0.596 | win |
| explanation-07 | 0.539 | 0.625 | loss |
| explanation-08 | 0.65 | 0.589 | win |
| summarization-01 | 0.637 | 0.548 | win |
| summarization-02 | 0.662 | 0.732 | loss |
| summarization-03 | 0.666 | 0.598 | win |
| summarization-04 | 0.789 | 0.668 | win |
| summarization-05 | 0.742 | 0.7 | win |
| summarization-06 | 0.714 | 0.668 | win |
| summarization-07 | 0.675 | 0.655 | tie |
| summarization-08 | 0.639 | 0.605 | win |

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.7 | 0.637 | win |
| code-review-02 | 0.752 | 0.718 | win |
| code-review-03 | 0.589 | 0.67 | loss |
| code-review-04 | 0.307 | 0.67 | loss |
| code-review-05 | 0.723 | 0.697 | win |
| code-review-06 | 0.672 | 0.672 | tie |
| code-review-07 | 0.649 | 0.627 | win |
| code-review-08 | 0.654 | 0.598 | win |
| debugging-01 | 0.767 | 0.738 | win |
| debugging-02 | 0.707 | 0.696 | tie |
| debugging-03 | 0.808 | 0.704 | win |
| debugging-04 | 0.786 | 0.761 | win |
| debugging-05 | 0.763 | 0.718 | win |
| debugging-06 | 0.56 | 0.637 | loss |
| debugging-07 | 0.687 | 0.651 | win |
| debugging-08 | 0.598 | 0.489 | win |
| explanation-01 | 0.74 | 0.72 | tie |
| explanation-02 | 0.687 | 0.663 | win |
| explanation-03 | 0.669 | 0.688 | tie |
| explanation-04 | 0.674 | 0.635 | win |
| explanation-05 | 0.64 | 0.676 | loss |
| explanation-06 | 0.634 | 0.596 | win |
| explanation-07 | 0.636 | 0.625 | tie |
| explanation-08 | 0.668 | 0.589 | win |
| summarization-01 | 0.682 | 0.548 | win |
| summarization-02 | 0.659 | 0.732 | loss |
| summarization-03 | 0.661 | 0.598 | win |
| summarization-04 | 0.742 | 0.668 | win |
| summarization-05 | 0.647 | 0.7 | loss |
| summarization-06 | 0.704 | 0.668 | win |
| summarization-07 | 0.687 | 0.655 | win |
| summarization-08 | 0.621 | 0.605 | tie |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.702 | 0.637 | win |
| code-review-02 | 0.655 | 0.718 | loss |
| code-review-03 | 0.62 | 0.67 | loss |
| code-review-04 | 0.738 | 0.67 | win |
| code-review-05 | 0.806 | 0.697 | win |
| code-review-06 | 0.52 | 0.672 | loss |
| debugging-01 | 0.71 | 0.738 | loss |
| debugging-02 | 0.784 | 0.696 | win |
| debugging-03 | 0.86 | 0.704 | win |
| debugging-04 | 0.711 | 0.761 | loss |
| debugging-05 | 0.833 | 0.718 | win |
| debugging-06 | 0.633 | 0.637 | tie |
| debugging-08 | 0.704 | 0.489 | win |
| explanation-01 | 0.616 | 0.72 | loss |
| explanation-02 | 0.724 | 0.663 | win |
| explanation-03 | 0.719 | 0.688 | win |
| explanation-04 | 0.662 | 0.635 | win |
| explanation-05 | 0.691 | 0.676 | tie |
| explanation-06 | 0.663 | 0.596 | win |
| explanation-07 | 0.555 | 0.625 | loss |
| summarization-01 | 0.668 | 0.548 | win |
| summarization-02 | 0.657 | 0.732 | loss |
| summarization-03 | 0.658 | 0.598 | win |
| summarization-04 | 0.593 | 0.668 | loss |
| summarization-05 | 0.796 | 0.7 | win |
| summarization-08 | 0.246 | 0.605 | loss |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| clarity-flow | 11 | 13 | 8 |
| classic-concise | 9 | 12 | 11 |
| developer-docs | 13 | 6 | 13 |
| plain-language | 12 | 5 | 15 |
| technical-simplified | 10 | 8 | 8 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- clarity-flow: Pearson 0.359, Spearman 0.568, over 32 pairs.
- classic-concise: Pearson 0.459, Spearman 0.408, over 32 pairs.
- developer-docs: Pearson 0.292, Spearman -0.011, over 32 pairs.
- plain-language: Pearson 0.44, Spearman 0.295, over 32 pairs.
- technical-simplified: Pearson 0.506, Spearman 0.339, over 26 pairs.

### clarity-flow

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.959 | 0.079 | loss |
| code-review-02 | 0.057 | 0.092 | win |
| code-review-03 | 0.111 | 0.088 | loss |
| code-review-04 | 0.113 | 0.107 | tie |
| code-review-05 | 0.094 | 0.065 | loss |
| code-review-06 | 0.11 | 0.974 | win |
| code-review-07 | 0.115 | 0.118 | tie |
| code-review-08 | 0.142 | 0.124 | tie |
| debugging-01 | 0.098 | 0.165 | win |
| debugging-02 | 0.0 | 0.075 | win |
| debugging-03 | 0.049 | 0.009 | loss |
| debugging-04 | 0.057 | 0.085 | win |
| debugging-05 | 0.091 | 0.067 | loss |
| debugging-06 | 0.135 | 0.104 | loss |
| debugging-07 | 0.081 | 0.101 | win |
| debugging-08 | 0.137 | 0.56 | win |
| explanation-01 | 0.156 | 0.081 | loss |
| explanation-02 | 0.096 | 0.122 | win |
| explanation-03 | 0.177 | 0.139 | loss |
| explanation-04 | 0.124 | 0.071 | loss |
| explanation-05 | 0.185 | 0.105 | loss |
| explanation-06 | 0.115 | 0.094 | loss |
| explanation-07 | 0.131 | 0.084 | loss |
| explanation-08 | 0.112 | 0.151 | win |
| summarization-01 | 0.029 | 0.105 | win |
| summarization-02 | 0.163 | 0.151 | tie |
| summarization-03 | 0.14 | 0.148 | tie |
| summarization-04 | 0.078 | 0.088 | tie |
| summarization-05 | 0.143 | 0.128 | tie |
| summarization-06 | 0.212 | 0.206 | tie |
| summarization-07 | 0.152 | 0.207 | win |
| summarization-08 | 0.234 | 0.194 | loss |

### classic-concise

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.057 | 0.079 | win |
| code-review-02 | 0.035 | 0.092 | win |
| code-review-03 | 0.094 | 0.088 | tie |
| code-review-04 | 0.141 | 0.107 | loss |
| code-review-05 | 0.136 | 0.065 | loss |
| code-review-06 | 0.085 | 0.974 | win |
| code-review-07 | 0.106 | 0.118 | tie |
| code-review-08 | 0.081 | 0.124 | win |
| debugging-01 | 0.151 | 0.165 | tie |
| debugging-02 | 0.054 | 0.075 | win |
| debugging-03 | 0.043 | 0.009 | loss |
| debugging-04 | 0.07 | 0.085 | tie |
| debugging-05 | 0.117 | 0.067 | loss |
| debugging-06 | 0.124 | 0.104 | tie |
| debugging-07 | 0.085 | 0.101 | tie |
| debugging-08 | 0.086 | 0.56 | win |
| explanation-01 | 0.108 | 0.081 | loss |
| explanation-02 | 0.163 | 0.122 | loss |
| explanation-03 | 0.106 | 0.139 | win |
| explanation-04 | 0.123 | 0.071 | loss |
| explanation-05 | 0.123 | 0.105 | tie |
| explanation-06 | 0.097 | 0.094 | tie |
| explanation-07 | 0.13 | 0.084 | loss |
| explanation-08 | 0.116 | 0.151 | win |
| summarization-01 | 0.159 | 0.105 | loss |
| summarization-02 | 0.236 | 0.151 | loss |
| summarization-03 | 0.105 | 0.148 | win |
| summarization-04 | 0.071 | 0.088 | tie |
| summarization-05 | 0.158 | 0.128 | loss |
| summarization-06 | 0.216 | 0.206 | tie |
| summarization-07 | 0.194 | 0.207 | tie |
| summarization-08 | 0.296 | 0.194 | loss |

### developer-docs

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.949 | 0.079 | loss |
| code-review-02 | 0.083 | 0.092 | tie |
| code-review-03 | 0.462 | 0.088 | loss |
| code-review-04 | 0.057 | 0.107 | win |
| code-review-05 | 0.105 | 0.065 | loss |
| code-review-06 | 0.094 | 0.974 | win |
| code-review-07 | 0.265 | 0.118 | loss |
| code-review-08 | 0.114 | 0.124 | tie |
| debugging-01 | 0.025 | 0.165 | win |
| debugging-02 | 0.082 | 0.075 | tie |
| debugging-03 | 0.04 | 0.009 | loss |
| debugging-04 | 0.086 | 0.085 | tie |
| debugging-05 | 0.067 | 0.067 | tie |
| debugging-06 | 0.113 | 0.104 | tie |
| debugging-07 | 0.105 | 0.101 | tie |
| debugging-08 | 0.102 | 0.56 | win |
| explanation-01 | 0.082 | 0.081 | tie |
| explanation-02 | 0.087 | 0.122 | win |
| explanation-03 | 0.076 | 0.139 | win |
| explanation-04 | 0.082 | 0.071 | tie |
| explanation-05 | 0.083 | 0.105 | win |
| explanation-06 | 0.052 | 0.094 | win |
| explanation-07 | 0.065 | 0.084 | tie |
| explanation-08 | 0.1 | 0.151 | win |
| summarization-01 | 0.357 | 0.105 | loss |
| summarization-02 | 0.155 | 0.151 | tie |
| summarization-03 | 0.151 | 0.148 | tie |
| summarization-04 | 0.098 | 0.088 | tie |
| summarization-05 | 0.103 | 0.128 | win |
| summarization-06 | 0.166 | 0.206 | win |
| summarization-07 | 0.117 | 0.207 | win |
| summarization-08 | 0.164 | 0.194 | win |

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.088 | 0.079 | tie |
| code-review-02 | 0.043 | 0.092 | win |
| code-review-03 | 0.099 | 0.088 | tie |
| code-review-04 | 0.633 | 0.107 | loss |
| code-review-05 | 0.061 | 0.065 | tie |
| code-review-06 | 0.114 | 0.974 | win |
| code-review-07 | 0.091 | 0.118 | win |
| code-review-08 | 0.141 | 0.124 | tie |
| debugging-01 | 0.094 | 0.165 | win |
| debugging-02 | 0.05 | 0.075 | win |
| debugging-03 | 0.055 | 0.009 | loss |
| debugging-04 | 0.054 | 0.085 | win |
| debugging-05 | 0.07 | 0.067 | tie |
| debugging-06 | 0.12 | 0.104 | tie |
| debugging-07 | 0.088 | 0.101 | tie |
| debugging-08 | 0.061 | 0.56 | win |
| explanation-01 | 0.095 | 0.081 | tie |
| explanation-02 | 0.118 | 0.122 | tie |
| explanation-03 | 0.143 | 0.139 | tie |
| explanation-04 | 0.107 | 0.071 | loss |
| explanation-05 | 0.113 | 0.105 | tie |
| explanation-06 | 0.12 | 0.094 | loss |
| explanation-07 | 0.073 | 0.084 | tie |
| explanation-08 | 0.09 | 0.151 | win |
| summarization-01 | 0.089 | 0.105 | tie |
| summarization-02 | 0.156 | 0.151 | tie |
| summarization-03 | 0.109 | 0.148 | win |
| summarization-04 | 0.09 | 0.088 | tie |
| summarization-05 | 0.224 | 0.128 | loss |
| summarization-06 | 0.177 | 0.206 | win |
| summarization-07 | 0.126 | 0.207 | win |
| summarization-08 | 0.164 | 0.194 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.098 | 0.079 | tie |
| code-review-02 | 0.096 | 0.092 | tie |
| code-review-03 | 0.097 | 0.088 | tie |
| code-review-04 | 0.039 | 0.107 | win |
| code-review-05 | 0.09 | 0.065 | loss |
| code-review-06 | 0.474 | 0.974 | win |
| debugging-01 | 0.021 | 0.165 | win |
| debugging-02 | 0.085 | 0.075 | tie |
| debugging-03 | 0.035 | 0.009 | loss |
| debugging-04 | 0.071 | 0.085 | tie |
| debugging-05 | 0.13 | 0.067 | loss |
| debugging-06 | 0.092 | 0.104 | tie |
| debugging-08 | 0.178 | 0.56 | win |
| explanation-01 | 0.114 | 0.081 | loss |
| explanation-02 | 0.134 | 0.122 | tie |
| explanation-03 | 0.116 | 0.139 | win |
| explanation-04 | 0.161 | 0.071 | loss |
| explanation-05 | 0.103 | 0.105 | tie |
| explanation-06 | 0.127 | 0.094 | loss |
| explanation-07 | 0.111 | 0.084 | loss |
| summarization-01 | 0.061 | 0.105 | win |
| summarization-02 | 0.078 | 0.151 | win |
| summarization-03 | 0.096 | 0.148 | win |
| summarization-04 | 0.035 | 0.088 | win |
| summarization-05 | 0.018 | 0.128 | win |
| summarization-08 | 0.263 | 0.194 | loss |

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 2776, measured: 2776.
Mean duration: 12314 ms. Mean wall: 19383 ms. Mean startup: 7069 ms.

## Harness spend

A stored call row holds the token counts of its call: the
uncached input, cache-write input, cache-read input, and
output tokens. The cache-read share is the cache-read total
over the whole input total.

Calls: 2776, measured: 2776.
Input tokens: 19808 uncached, 2400230 cache write, 13045657 cache read. Output tokens: 2950919.
Cache-read share: 0.844.

## Warnings

- technical-simplified/explanation-08: the pair failed the gate, excluded
- technical-simplified/code-review-07: the pair failed the gate, excluded
- technical-simplified/summarization-06: the pair failed the gate, excluded
- technical-simplified/summarization-07: the pair failed the gate, excluded
- technical-simplified/debugging-07: the pair failed the gate, excluded
- technical-simplified/code-review-08: the pair failed the gate, excluded
- clarity-flow/code-review-01: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- clarity-flow/debugging-08: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- classic-concise/debugging-08: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- developer-docs/code-review-03: the pair has 1 shared facts, fewer than the floor of 3, so comprehension skips the pair
- developer-docs/code-review-07: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- developer-docs/debugging-08: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- plain-language/code-review-04: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- plain-language/debugging-06: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- plain-language/debugging-08: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- technical-simplified/code-review-06: the pair has 2 shared facts, fewer than the floor of 3, so comprehension skips the pair
- technical-simplified/debugging-08: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- technical-simplified/summarization-08: the pair has 0 shared facts, fewer than the floor of 3, so comprehension skips the pair
- clarity-flow/code-review-01: the comprehension check has no usable questions for the pair, so the pair is unscored
- clarity-flow/debugging-08: the comprehension check has no usable questions for the pair, so the pair is unscored
- classic-concise/debugging-08: the comprehension check has no usable questions for the pair, so the pair is unscored
- developer-docs/code-review-03: the comprehension check has no usable questions for the pair, so the pair is unscored
- developer-docs/code-review-07: the comprehension check has no usable questions for the pair, so the pair is unscored
- developer-docs/debugging-08: the comprehension check has no usable questions for the pair, so the pair is unscored
- plain-language/code-review-04: the comprehension check has no usable questions for the pair, so the pair is unscored
- plain-language/debugging-06: the comprehension check has no usable questions for the pair, so the pair is unscored
- plain-language/debugging-08: the comprehension check has no usable questions for the pair, so the pair is unscored
- technical-simplified/code-review-06: the comprehension check has no usable questions for the pair, so the pair is unscored
- technical-simplified/debugging-08: the comprehension check has no usable questions for the pair, so the pair is unscored
- technical-simplified/summarization-08: the comprehension check has no usable questions for the pair, so the pair is unscored
- classic-concise: the styled answer scores worse than the unstyled answer on comprehension (4 wins, 7 losses)
- developer-docs: the styled answer scores worse than the unstyled answer on comprehension (6 wins, 7 losses)
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (2 wins, 7 losses)
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (2 wins, 5 losses)
