# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-06T06:55:20+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 2 | 8 | 10 | -0.031 | 0.844 | 0.042 | 0.031 |
| technical-simplified | 1 | 3 | 14 | -0.022 | 0.877 | 0.028 | 0.009 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer scores worse (2 wins, 8 losses, 10 ties).
- technical-simplified: the styled answer scores worse (1 wins, 3 losses, 14 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 1.0 | 0.667 | loss |
| code-review-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-02 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-02 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| summarization-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| summarization-04 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| summarization-05 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-02 | 6 | 3/3 | 0.889 | 0.889 | 0.556 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.722 | 0.667 | win |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 11 | 4 | 5 |
| technical-simplified | 6 | 2 | 10 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.062, Spearman -0.138, over 20 pairs.
- technical-simplified: Pearson -0.091, Spearman -0.218, over 18 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.681 | 0.615 | win |
| code-review-02 | 0.688 | 0.651 | win |
| code-review-03 | 0.597 | 0.661 | loss |
| code-review-04 | 0.737 | 0.694 | win |
| code-review-05 | 0.603 | 0.749 | loss |
| debugging-01 | 0.807 | 0.598 | win |
| debugging-02 | 0.738 | 0.704 | win |
| debugging-03 | 0.856 | 0.763 | win |
| debugging-04 | 0.745 | 0.691 | win |
| debugging-05 | 0.775 | 0.669 | win |
| explanation-01 | 0.623 | 0.69 | loss |
| explanation-02 | 0.697 | 0.752 | loss |
| explanation-03 | 0.672 | 0.668 | tie |
| explanation-04 | 0.7 | 0.591 | win |
| explanation-05 | 0.702 | 0.718 | tie |
| summarization-01 | 0.725 | 0.716 | tie |
| summarization-02 | 0.638 | 0.56 | win |
| summarization-03 | 0.674 | 0.661 | tie |
| summarization-04 | 0.672 | 0.673 | tie |
| summarization-05 | 0.772 | 0.724 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.641 | 0.615 | win |
| code-review-02 | 0.662 | 0.651 | tie |
| code-review-03 | 0.671 | 0.661 | tie |
| code-review-04 | 0.728 | 0.694 | win |
| code-review-05 | 0.778 | 0.749 | win |
| debugging-01 | 0.77 | 0.598 | win |
| debugging-02 | 0.822 | 0.704 | win |
| debugging-03 | 0.668 | 0.763 | loss |
| debugging-04 | 0.677 | 0.691 | tie |
| debugging-05 | 0.689 | 0.669 | tie |
| explanation-01 | 0.696 | 0.69 | tie |
| explanation-02 | 0.712 | 0.752 | loss |
| explanation-04 | 0.645 | 0.591 | win |
| explanation-05 | 0.724 | 0.718 | tie |
| summarization-01 | 0.722 | 0.716 | tie |
| summarization-03 | 0.657 | 0.661 | tie |
| summarization-04 | 0.672 | 0.673 | tie |
| summarization-05 | 0.728 | 0.724 | tie |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 7 | 2 | 11 |
| technical-simplified | 8 | 4 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.167, Spearman 0.14, over 20 pairs.
- technical-simplified: Pearson 0.242, Spearman 0.075, over 18 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.066 | 0.085 | tie |
| code-review-02 | 0.058 | 0.065 | tie |
| code-review-03 | 0.069 | 0.143 | win |
| code-review-04 | 0.087 | 0.1 | tie |
| code-review-05 | 0.092 | 0.102 | tie |
| debugging-01 | 0.057 | 0.117 | win |
| debugging-02 | 0.056 | 0.04 | tie |
| debugging-03 | 0.029 | 0.015 | tie |
| debugging-04 | 0.093 | 0.099 | tie |
| debugging-05 | 0.106 | 0.063 | loss |
| explanation-01 | 0.14 | 0.098 | loss |
| explanation-02 | 0.095 | 0.082 | tie |
| explanation-03 | 0.085 | 0.116 | win |
| explanation-04 | 0.07 | 0.086 | tie |
| explanation-05 | 0.096 | 0.145 | win |
| summarization-01 | 0.061 | 0.082 | win |
| summarization-02 | 0.149 | 0.147 | tie |
| summarization-03 | 0.114 | 0.164 | win |
| summarization-04 | 0.068 | 0.084 | tie |
| summarization-05 | 0.044 | 0.173 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.038 | 0.085 | win |
| code-review-02 | 0.109 | 0.065 | loss |
| code-review-03 | 0.086 | 0.143 | win |
| code-review-04 | 0.08 | 0.1 | tie |
| code-review-05 | 0.137 | 0.102 | loss |
| debugging-01 | 0.0 | 0.117 | win |
| debugging-02 | 0.078 | 0.04 | loss |
| debugging-03 | 0.037 | 0.015 | loss |
| debugging-04 | 0.041 | 0.099 | win |
| debugging-05 | 0.08 | 0.063 | tie |
| explanation-01 | 0.084 | 0.098 | tie |
| explanation-02 | 0.093 | 0.082 | tie |
| explanation-04 | 0.09 | 0.086 | tie |
| explanation-05 | 0.118 | 0.145 | win |
| summarization-01 | 0.086 | 0.082 | tie |
| summarization-03 | 0.132 | 0.164 | win |
| summarization-04 | 0.042 | 0.084 | win |
| summarization-05 | 0.055 | 0.173 | win |

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (2 wins, 8 losses)
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (1 wins, 3 losses)
