# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-06T06:53:46+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 7 | 2 | 11 | 0.028 | 0.911 | 0.042 | 0.044 |
| technical-simplified | 4 | 3 | 12 | 0.006 | 0.848 | 0.041 | 0.026 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (7 wins, 2 losses, 11 ties).
- technical-simplified: the styled answer holds (4 wins, 3 losses, 12 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-03 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| code-review-04 | 6 | 3/3 | 0.778 | 0.944 | 0.667 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-05 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 0.611 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 0.944 | 0.722 | 0.889 | win |
| summarization-01 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | win |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.722 | 0.889 | 0.667 | loss |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-04 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-01 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| explanation-02 | 6 | 3/3 | 0.778 | 0.833 | 0.667 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 0.722 | 1.0 | win |
| explanation-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| summarization-05 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 10 | 6 | 4 |
| technical-simplified | 11 | 2 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.364, Spearman 0.287, over 20 pairs.
- technical-simplified: Pearson 0.473, Spearman 0.339, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.652 | 0.731 | loss |
| code-review-02 | 0.731 | 0.655 | win |
| code-review-03 | 0.668 | 0.603 | win |
| code-review-04 | 0.658 | 0.688 | loss |
| code-review-05 | 0.626 | 0.678 | loss |
| debugging-01 | 0.714 | 0.549 | win |
| debugging-02 | 0.766 | 0.75 | tie |
| debugging-03 | 0.838 | 0.843 | tie |
| debugging-04 | 0.746 | 0.653 | win |
| debugging-05 | 0.732 | 0.708 | win |
| explanation-01 | 0.754 | 0.727 | win |
| explanation-02 | 0.76 | 0.597 | win |
| explanation-03 | 0.705 | 0.675 | win |
| explanation-04 | 0.66 | 0.681 | loss |
| explanation-05 | 0.654 | 0.662 | tie |
| summarization-01 | 0.72 | 0.687 | win |
| summarization-02 | 0.643 | 0.627 | tie |
| summarization-03 | 0.644 | 0.666 | loss |
| summarization-04 | 0.584 | 0.75 | loss |
| summarization-05 | 0.672 | 0.638 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.719 | 0.731 | tie |
| code-review-02 | 0.755 | 0.655 | win |
| code-review-03 | 0.658 | 0.603 | win |
| code-review-04 | 0.707 | 0.688 | tie |
| code-review-05 | 0.79 | 0.678 | win |
| debugging-01 | 0.743 | 0.549 | win |
| debugging-02 | 0.753 | 0.75 | tie |
| debugging-03 | 0.839 | 0.843 | tie |
| debugging-04 | 0.801 | 0.653 | win |
| debugging-05 | 0.729 | 0.708 | win |
| explanation-01 | 0.665 | 0.727 | loss |
| explanation-02 | 0.736 | 0.597 | win |
| explanation-04 | 0.726 | 0.681 | win |
| explanation-05 | 0.739 | 0.662 | win |
| summarization-01 | 0.605 | 0.687 | loss |
| summarization-02 | 0.673 | 0.627 | win |
| summarization-03 | 0.669 | 0.666 | tie |
| summarization-04 | 0.755 | 0.75 | tie |
| summarization-05 | 0.793 | 0.638 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 3 | 9 | 8 |
| technical-simplified | 4 | 3 | 12 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.594, Spearman 0.513, over 20 pairs.
- technical-simplified: Pearson 0.144, Spearman 0.242, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.083 | 0.081 | tie |
| code-review-02 | 0.103 | 0.057 | loss |
| code-review-03 | 0.083 | 0.069 | tie |
| code-review-04 | 0.097 | 0.075 | loss |
| code-review-05 | 0.099 | 0.057 | loss |
| debugging-01 | 0.0 | 0.111 | win |
| debugging-02 | 0.079 | 0.088 | tie |
| debugging-03 | 0.038 | 0.017 | loss |
| debugging-04 | 0.061 | 0.051 | tie |
| debugging-05 | 0.106 | 0.099 | tie |
| explanation-01 | 0.139 | 0.08 | loss |
| explanation-02 | 0.114 | 0.062 | loss |
| explanation-03 | 0.11 | 0.081 | loss |
| explanation-04 | 0.11 | 0.108 | tie |
| explanation-05 | 0.099 | 0.066 | loss |
| summarization-01 | 0.072 | 0.107 | win |
| summarization-02 | 0.145 | 0.162 | tie |
| summarization-03 | 0.134 | 0.126 | tie |
| summarization-04 | 0.137 | 0.05 | loss |
| summarization-05 | 0.026 | 0.162 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.071 | 0.081 | tie |
| code-review-02 | 0.091 | 0.057 | loss |
| code-review-03 | 0.083 | 0.069 | tie |
| code-review-04 | 0.055 | 0.075 | tie |
| code-review-05 | 0.068 | 0.057 | tie |
| debugging-01 | 0.062 | 0.111 | win |
| debugging-02 | 0.067 | 0.088 | win |
| debugging-03 | 0.074 | 0.017 | loss |
| debugging-04 | 0.062 | 0.051 | tie |
| debugging-05 | 0.1 | 0.099 | tie |
| explanation-01 | 0.092 | 0.08 | tie |
| explanation-02 | 0.074 | 0.062 | tie |
| explanation-04 | 0.094 | 0.108 | tie |
| explanation-05 | 0.065 | 0.066 | tie |
| summarization-01 | 0.091 | 0.107 | tie |
| summarization-02 | 0.114 | 0.162 | win |
| summarization-03 | 0.124 | 0.126 | tie |
| summarization-04 | 0.209 | 0.05 | loss |
| summarization-05 | 0.071 | 0.162 | win |

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
