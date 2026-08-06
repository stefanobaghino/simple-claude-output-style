# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-05T21:16:35+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 5 | 4 | 11 | 0.011 | 0.811 | 0.014 | 0.042 |
| technical-simplified | 3 | 5 | 12 | -0.006 | 0.878 | 0.061 | 0.042 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (5 wins, 4 losses, 11 ties).
- technical-simplified: the styled answer scores worse (3 wins, 5 losses, 12 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-04 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-05 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.778 | 0.889 | 0.556 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| explanation-02 | 6 | 3/3 | 0.944 | 0.667 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 0.722 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.778 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| code-review-02 | 6 | 3/3 | 0.611 | 0.889 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 0.944 | 0.611 | 0.889 | win |
| code-review-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.889 | 0.778 | 0.556 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| debugging-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-01 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 0.722 | 0.889 | 0.778 | loss |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.556 | 0.5 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 13 | 4 | 3 |
| technical-simplified | 6 | 8 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.157, Spearman 0.209, over 20 pairs.
- technical-simplified: Pearson -0.067, Spearman -0.06, over 20 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.688 | 0.683 | tie |
| code-review-02 | 0.73 | 0.696 | win |
| code-review-03 | 0.622 | 0.665 | loss |
| code-review-04 | 0.686 | 0.617 | win |
| code-review-05 | 0.738 | 0.679 | win |
| debugging-01 | 0.81 | 0.677 | win |
| debugging-02 | 0.846 | 0.697 | win |
| debugging-03 | 0.761 | 0.776 | tie |
| debugging-04 | 0.843 | 0.571 | win |
| debugging-05 | 0.74 | 0.698 | win |
| explanation-01 | 0.702 | 0.653 | win |
| explanation-02 | 0.705 | 0.748 | loss |
| explanation-03 | 0.677 | 0.679 | tie |
| explanation-04 | 0.714 | 0.674 | win |
| explanation-05 | 0.723 | 0.695 | win |
| summarization-01 | 0.827 | 0.759 | win |
| summarization-02 | 0.662 | 0.55 | win |
| summarization-03 | 0.637 | 0.575 | win |
| summarization-04 | 0.562 | 0.676 | loss |
| summarization-05 | 0.705 | 0.789 | loss |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.625 | 0.683 | loss |
| code-review-02 | 0.7 | 0.696 | tie |
| code-review-03 | 0.674 | 0.665 | tie |
| code-review-04 | 0.621 | 0.617 | tie |
| code-review-05 | 0.718 | 0.679 | win |
| debugging-01 | 0.703 | 0.677 | win |
| debugging-02 | 0.8 | 0.697 | win |
| debugging-03 | 0.736 | 0.776 | loss |
| debugging-04 | 0.779 | 0.571 | win |
| debugging-05 | 0.652 | 0.698 | loss |
| explanation-01 | 0.637 | 0.653 | tie |
| explanation-02 | 0.721 | 0.748 | loss |
| explanation-03 | 0.662 | 0.679 | tie |
| explanation-04 | 0.638 | 0.674 | loss |
| explanation-05 | 0.67 | 0.695 | loss |
| summarization-01 | 0.655 | 0.759 | loss |
| summarization-02 | 0.77 | 0.55 | win |
| summarization-03 | 0.607 | 0.575 | win |
| summarization-04 | 0.683 | 0.676 | tie |
| summarization-05 | 0.681 | 0.789 | loss |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 9 | 6 | 5 |
| technical-simplified | 7 | 6 | 7 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.567, Spearman 0.604, over 20 pairs.
- technical-simplified: Pearson 0.154, Spearman 0.116, over 20 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.047 | 0.056 | tie |
| code-review-02 | 0.084 | 0.044 | loss |
| code-review-03 | 0.083 | 0.121 | win |
| code-review-04 | 0.063 | 0.105 | win |
| code-review-05 | 0.085 | 0.064 | loss |
| debugging-01 | 0.041 | 0.111 | win |
| debugging-02 | 0.043 | 0.1 | win |
| debugging-03 | 0.012 | 0.018 | tie |
| debugging-04 | 0.054 | 0.075 | win |
| debugging-05 | 0.087 | 0.103 | tie |
| explanation-01 | 0.125 | 0.103 | loss |
| explanation-02 | 0.128 | 0.066 | loss |
| explanation-03 | 0.104 | 0.121 | tie |
| explanation-04 | 0.086 | 0.051 | loss |
| explanation-05 | 0.084 | 0.17 | win |
| summarization-01 | 0.091 | 0.069 | loss |
| summarization-02 | 0.126 | 0.174 | win |
| summarization-03 | 0.139 | 0.194 | win |
| summarization-04 | 0.049 | 0.054 | tie |
| summarization-05 | 0.089 | 0.181 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.091 | 0.056 | loss |
| code-review-02 | 0.067 | 0.044 | loss |
| code-review-03 | 0.072 | 0.121 | win |
| code-review-04 | 0.111 | 0.105 | tie |
| code-review-05 | 0.061 | 0.064 | tie |
| debugging-01 | 0.0 | 0.111 | win |
| debugging-02 | 0.093 | 0.1 | tie |
| debugging-03 | 0.046 | 0.018 | loss |
| debugging-04 | 0.082 | 0.075 | tie |
| debugging-05 | 0.14 | 0.103 | loss |
| explanation-01 | 0.119 | 0.103 | tie |
| explanation-02 | 0.052 | 0.066 | tie |
| explanation-03 | 0.092 | 0.121 | win |
| explanation-04 | 0.097 | 0.051 | loss |
| explanation-05 | 0.107 | 0.17 | win |
| summarization-01 | 0.043 | 0.069 | win |
| summarization-02 | 0.161 | 0.174 | tie |
| summarization-03 | 0.105 | 0.194 | win |
| summarization-04 | 0.148 | 0.054 | loss |
| summarization-05 | 0.148 | 0.181 | win |

## Warnings

- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (3 wins, 5 losses)
