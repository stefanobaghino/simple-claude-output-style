# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-05T06:33:24+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 1 | 3 | 16 | -0.003 | 0.872 | 0.039 | 0.036 |
| technical-simplified | 4 | 4 | 8 | 0.021 | 0.938 | 0.024 | 0.052 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer scores worse (1 wins, 3 losses, 16 ties).
- technical-simplified: the styled answer holds (4 wins, 4 losses, 8 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-02 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| code-review-03 | 6 | 3/3 | 0.944 | 0.611 | 0.889 | win |
| code-review-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |
| explanation-02 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-04 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 0.833 | 0.778 | 0.667 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.722 | 1.0 | win |
| code-review-02 | 6 | 3/3 | 0.722 | 0.833 | 0.667 | loss |
| code-review-03 | 6 | 3/3 | 1.0 | 0.667 | 1.0 | win |
| code-review-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 10 | 8 | 2 |
| technical-simplified | 9 | 3 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.215, Spearman -0.23, over 20 pairs.
- technical-simplified: Pearson -0.212, Spearman -0.318, over 16 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.63 | 0.608 | win |
| code-review-02 | 0.782 | 0.626 | win |
| code-review-03 | 0.694 | 0.618 | win |
| code-review-04 | 0.642 | 0.672 | loss |
| code-review-05 | 0.633 | 0.672 | loss |
| debugging-01 | 0.684 | 0.698 | tie |
| debugging-02 | 0.681 | 0.672 | tie |
| debugging-03 | 0.694 | 0.767 | loss |
| debugging-04 | 0.629 | 0.663 | loss |
| debugging-05 | 0.755 | 0.735 | win |
| explanation-01 | 0.693 | 0.6 | win |
| explanation-02 | 0.704 | 0.646 | win |
| explanation-03 | 0.736 | 0.669 | win |
| explanation-04 | 0.591 | 0.626 | loss |
| explanation-05 | 0.672 | 0.602 | win |
| summarization-01 | 0.683 | 0.585 | win |
| summarization-02 | 0.573 | 0.63 | loss |
| summarization-03 | 0.679 | 0.626 | win |
| summarization-04 | 0.547 | 0.599 | loss |
| summarization-05 | 0.7 | 0.766 | loss |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.614 | 0.608 | tie |
| code-review-02 | 0.673 | 0.626 | win |
| code-review-03 | 0.634 | 0.618 | tie |
| code-review-04 | 0.712 | 0.672 | win |
| code-review-05 | 0.698 | 0.672 | win |
| debugging-01 | 0.667 | 0.698 | loss |
| debugging-02 | 0.703 | 0.672 | win |
| debugging-03 | 0.79 | 0.767 | win |
| debugging-05 | 0.782 | 0.735 | win |
| explanation-02 | 0.636 | 0.646 | tie |
| explanation-04 | 0.678 | 0.626 | win |
| summarization-01 | 0.587 | 0.585 | tie |
| summarization-02 | 0.557 | 0.63 | loss |
| summarization-03 | 0.67 | 0.626 | win |
| summarization-04 | 0.633 | 0.599 | win |
| summarization-05 | 0.724 | 0.766 | loss |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 7 | 6 | 7 |
| technical-simplified | 9 | 1 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.024, Spearman 0.084, over 20 pairs.
- technical-simplified: Pearson 0.078, Spearman -0.003, over 16 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.07 | 0.092 | win |
| code-review-02 | 0.088 | 0.095 | tie |
| code-review-03 | 0.124 | 0.082 | loss |
| code-review-04 | 0.162 | 0.122 | loss |
| code-review-05 | 0.123 | 0.094 | loss |
| debugging-01 | 0.081 | 0.103 | win |
| debugging-02 | 0.028 | 0.136 | win |
| debugging-03 | 0.035 | 0.066 | win |
| debugging-04 | 0.083 | 0.04 | loss |
| debugging-05 | 0.067 | 0.146 | win |
| explanation-01 | 0.094 | 0.118 | win |
| explanation-02 | 0.107 | 0.112 | tie |
| explanation-03 | 0.103 | 0.11 | tie |
| explanation-04 | 0.06 | 0.07 | tie |
| explanation-05 | 0.138 | 0.125 | tie |
| summarization-01 | 0.241 | 0.068 | loss |
| summarization-02 | 0.157 | 0.137 | loss |
| summarization-03 | 0.105 | 0.16 | win |
| summarization-04 | 0.111 | 0.093 | tie |
| summarization-05 | 0.115 | 0.134 | tie |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.077 | 0.092 | tie |
| code-review-02 | 0.062 | 0.095 | win |
| code-review-03 | 0.106 | 0.082 | loss |
| code-review-04 | 0.06 | 0.122 | win |
| code-review-05 | 0.057 | 0.094 | win |
| debugging-01 | 0.019 | 0.103 | win |
| debugging-02 | 0.059 | 0.136 | win |
| debugging-03 | 0.052 | 0.066 | tie |
| debugging-05 | 0.111 | 0.146 | win |
| explanation-02 | 0.084 | 0.112 | win |
| explanation-04 | 0.086 | 0.07 | tie |
| summarization-01 | 0.042 | 0.068 | win |
| summarization-02 | 0.123 | 0.137 | tie |
| summarization-03 | 0.15 | 0.16 | tie |
| summarization-04 | 0.103 | 0.093 | tie |
| summarization-05 | 0.039 | 0.134 | win |

## Warnings

- technical-simplified/explanation-01: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/explanation-05: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (1 wins, 3 losses)
