# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-05T17:29:47+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 6 | 6 | 8 | -0.0 | 0.856 | 0.056 | 0.031 |
| technical-simplified | 7 | 3 | 9 | 0.009 | 0.789 | 0.058 | 0.053 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (6 wins, 6 losses, 8 ties).
- technical-simplified: the styled answer holds (7 wins, 3 losses, 9 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.944 | 0.889 | 0.444 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-05 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-01 | 6 | 3/3 | 0.667 | 1.0 | 1.0 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| explanation-05 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| summarization-01 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| summarization-02 | 6 | 3/3 | 1.0 | 0.667 | 1.0 | win |
| summarization-03 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| code-review-02 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| code-review-03 | 6 | 3/3 | 1.0 | 0.667 | 1.0 | win |
| code-review-04 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-05 | 6 | 3/3 | 0.889 | 0.722 | 0.778 | win |
| debugging-01 | 6 | 3/3 | 0.833 | 1.0 | 0.667 | tie |
| debugging-02 | 6 | 3/3 | 0.778 | 1.0 | 0.667 | loss |
| debugging-04 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.889 | 0.889 | 0.556 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| explanation-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 10 | 4 | 6 |
| technical-simplified | 13 | 2 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.053, Spearman -0.092, over 20 pairs.
- technical-simplified: Pearson 0.068, Spearman 0.116, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.693 | 0.673 | tie |
| code-review-02 | 0.726 | 0.613 | win |
| code-review-03 | 0.643 | 0.625 | tie |
| code-review-04 | 0.698 | 0.669 | win |
| code-review-05 | 0.668 | 0.615 | win |
| debugging-01 | 0.786 | 0.624 | win |
| debugging-02 | 0.854 | 0.737 | win |
| debugging-03 | 0.834 | 0.842 | tie |
| debugging-04 | 0.85 | 0.623 | win |
| debugging-05 | 0.733 | 0.64 | win |
| explanation-01 | 0.641 | 0.692 | loss |
| explanation-02 | 0.68 | 0.715 | loss |
| explanation-03 | 0.698 | 0.701 | tie |
| explanation-04 | 0.632 | 0.675 | loss |
| explanation-05 | 0.715 | 0.607 | win |
| summarization-01 | 0.641 | 0.624 | tie |
| summarization-02 | 0.628 | 0.638 | tie |
| summarization-03 | 0.678 | 0.601 | win |
| summarization-04 | 0.673 | 0.528 | win |
| summarization-05 | 0.664 | 0.717 | loss |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.703 | 0.673 | win |
| code-review-02 | 0.695 | 0.613 | win |
| code-review-03 | 0.64 | 0.625 | tie |
| code-review-04 | 0.778 | 0.669 | win |
| code-review-05 | 0.689 | 0.615 | win |
| debugging-01 | 0.644 | 0.624 | tie |
| debugging-02 | 0.808 | 0.737 | win |
| debugging-04 | 0.817 | 0.623 | win |
| debugging-05 | 0.72 | 0.64 | win |
| explanation-01 | 0.696 | 0.692 | tie |
| explanation-02 | 0.683 | 0.715 | loss |
| explanation-03 | 0.653 | 0.701 | loss |
| explanation-04 | 0.658 | 0.675 | tie |
| explanation-05 | 0.731 | 0.607 | win |
| summarization-01 | 0.648 | 0.624 | win |
| summarization-02 | 0.71 | 0.638 | win |
| summarization-03 | 0.643 | 0.601 | win |
| summarization-04 | 0.802 | 0.528 | win |
| summarization-05 | 0.841 | 0.717 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 11 | 5 | 4 |
| technical-simplified | 10 | 5 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.196, Spearman 0.212, over 20 pairs.
- technical-simplified: Pearson 0.248, Spearman 0.175, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.057 | 0.086 | win |
| code-review-02 | 0.065 | 0.094 | win |
| code-review-03 | 0.056 | 0.051 | tie |
| code-review-04 | 0.061 | 0.092 | win |
| code-review-05 | 0.11 | 0.11 | tie |
| debugging-01 | 0.098 | 0.127 | win |
| debugging-02 | 0.093 | 0.041 | loss |
| debugging-03 | 0.02 | 0.061 | win |
| debugging-04 | 0.076 | 0.077 | tie |
| debugging-05 | 0.052 | 0.112 | win |
| explanation-01 | 0.119 | 0.098 | loss |
| explanation-02 | 0.097 | 0.12 | win |
| explanation-03 | 0.138 | 0.114 | loss |
| explanation-04 | 0.088 | 0.1 | tie |
| explanation-05 | 0.122 | 0.149 | win |
| summarization-01 | 0.061 | 0.162 | win |
| summarization-02 | 0.154 | 0.23 | win |
| summarization-03 | 0.167 | 0.099 | loss |
| summarization-04 | 0.092 | 0.06 | loss |
| summarization-05 | 0.116 | 0.152 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.098 | 0.086 | tie |
| code-review-02 | 0.061 | 0.094 | win |
| code-review-03 | 0.083 | 0.051 | loss |
| code-review-04 | 0.043 | 0.092 | win |
| code-review-05 | 0.09 | 0.11 | win |
| debugging-01 | 0.0 | 0.127 | win |
| debugging-02 | 0.089 | 0.041 | loss |
| debugging-04 | 0.08 | 0.077 | tie |
| debugging-05 | 0.127 | 0.112 | tie |
| explanation-01 | 0.087 | 0.098 | tie |
| explanation-02 | 0.064 | 0.12 | win |
| explanation-03 | 0.07 | 0.114 | win |
| explanation-04 | 0.149 | 0.1 | loss |
| explanation-05 | 0.098 | 0.149 | win |
| summarization-01 | 0.119 | 0.162 | win |
| summarization-02 | 0.116 | 0.23 | win |
| summarization-03 | 0.135 | 0.099 | loss |
| summarization-04 | 0.089 | 0.06 | loss |
| summarization-05 | 0.054 | 0.152 | win |

## Warnings

- technical-simplified/debugging-03: the pair failed the gate, excluded
