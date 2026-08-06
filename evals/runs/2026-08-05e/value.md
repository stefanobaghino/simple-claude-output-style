# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-05T21:14:52+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 8 | 1 | 11 | 0.056 | 0.883 | 0.014 | 0.056 |
| technical-simplified | 3 | 6 | 9 | -0.028 | 0.852 | 0.056 | 0.04 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (8 wins, 1 losses, 11 ties).
- technical-simplified: the styled answer scores worse (3 wins, 6 losses, 9 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-03 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| code-review-04 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-05 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.944 | 0.889 | 0.444 | tie |
| explanation-02 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| explanation-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 0.833 | 0.667 | win |
| summarization-01 | 6 | 3/3 | 0.889 | 0.722 | 0.778 | win |
| summarization-02 | 6 | 3/3 | 0.889 | 0.889 | 0.556 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.889 | 0.778 | 0.556 | win |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| code-review-02 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-04 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.833 | 0.722 | 0.667 | win |
| debugging-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| explanation-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| explanation-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 12 | 4 | 4 |
| technical-simplified | 12 | 2 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.106, Spearman -0.14, over 20 pairs.
- technical-simplified: Pearson 0.272, Spearman 0.168, over 18 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.69 | 0.58 | win |
| code-review-02 | 0.62 | 0.669 | loss |
| code-review-03 | 0.668 | 0.719 | loss |
| code-review-04 | 0.767 | 0.684 | win |
| code-review-05 | 0.758 | 0.698 | win |
| debugging-01 | 0.709 | 0.631 | win |
| debugging-02 | 0.783 | 0.734 | win |
| debugging-03 | 0.792 | 0.812 | loss |
| debugging-04 | 0.751 | 0.736 | tie |
| debugging-05 | 0.765 | 0.722 | win |
| explanation-01 | 0.706 | 0.662 | win |
| explanation-02 | 0.735 | 0.744 | tie |
| explanation-03 | 0.671 | 0.725 | loss |
| explanation-04 | 0.688 | 0.695 | tie |
| explanation-05 | 0.726 | 0.651 | win |
| summarization-01 | 0.744 | 0.692 | win |
| summarization-02 | 0.582 | 0.579 | tie |
| summarization-03 | 0.681 | 0.643 | win |
| summarization-04 | 0.7 | 0.581 | win |
| summarization-05 | 0.762 | 0.74 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.602 | 0.58 | win |
| code-review-02 | 0.719 | 0.669 | win |
| code-review-03 | 0.639 | 0.719 | loss |
| code-review-04 | 0.709 | 0.684 | win |
| code-review-05 | 0.717 | 0.698 | tie |
| debugging-01 | 0.663 | 0.631 | win |
| debugging-02 | 0.756 | 0.734 | win |
| debugging-03 | 0.801 | 0.812 | tie |
| debugging-05 | 0.785 | 0.722 | win |
| explanation-01 | 0.726 | 0.662 | win |
| explanation-03 | 0.688 | 0.725 | loss |
| explanation-04 | 0.696 | 0.695 | tie |
| explanation-05 | 0.756 | 0.651 | win |
| summarization-01 | 0.758 | 0.692 | win |
| summarization-02 | 0.665 | 0.579 | win |
| summarization-03 | 0.693 | 0.643 | win |
| summarization-04 | 0.754 | 0.581 | win |
| summarization-05 | 0.756 | 0.74 | tie |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 7 | 7 | 6 |
| technical-simplified | 10 | 3 | 5 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.18, Spearman 0.114, over 20 pairs.
- technical-simplified: Pearson 0.371, Spearman 0.3, over 18 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.074 | 0.06 | tie |
| code-review-02 | 0.074 | 0.052 | loss |
| code-review-03 | 0.081 | 0.103 | win |
| code-review-04 | 0.074 | 0.106 | win |
| code-review-05 | 0.102 | 0.061 | loss |
| debugging-01 | 0.022 | 0.217 | win |
| debugging-02 | 0.071 | 0.028 | loss |
| debugging-03 | 0.059 | 0.054 | tie |
| debugging-04 | 0.109 | 0.067 | loss |
| debugging-05 | 0.112 | 0.096 | tie |
| explanation-01 | 0.106 | 0.122 | tie |
| explanation-02 | 0.118 | 0.088 | loss |
| explanation-03 | 0.116 | 0.127 | tie |
| explanation-04 | 0.106 | 0.104 | tie |
| explanation-05 | 0.056 | 0.125 | win |
| summarization-01 | 0.115 | 0.087 | loss |
| summarization-02 | 0.097 | 0.194 | win |
| summarization-03 | 0.104 | 0.158 | win |
| summarization-04 | 0.213 | 0.12 | loss |
| summarization-05 | 0.109 | 0.17 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.073 | 0.06 | tie |
| code-review-02 | 0.062 | 0.052 | tie |
| code-review-03 | 0.13 | 0.103 | loss |
| code-review-04 | 0.073 | 0.106 | win |
| code-review-05 | 0.107 | 0.061 | loss |
| debugging-01 | 0.0 | 0.217 | win |
| debugging-02 | 0.055 | 0.028 | loss |
| debugging-03 | 0.024 | 0.054 | win |
| debugging-05 | 0.109 | 0.096 | tie |
| explanation-01 | 0.118 | 0.122 | tie |
| explanation-03 | 0.079 | 0.127 | win |
| explanation-04 | 0.068 | 0.104 | win |
| explanation-05 | 0.084 | 0.125 | win |
| summarization-01 | 0.103 | 0.087 | tie |
| summarization-02 | 0.124 | 0.194 | win |
| summarization-03 | 0.096 | 0.158 | win |
| summarization-04 | 0.074 | 0.12 | win |
| summarization-05 | 0.063 | 0.17 | win |

## Warnings

- technical-simplified/explanation-02: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (3 wins, 6 losses)
