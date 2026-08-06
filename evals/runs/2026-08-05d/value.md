# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-05T21:13:05+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 4 | 5 | 11 | -0.022 | 0.828 | 0.033 | 0.039 |
| technical-simplified | 2 | 2 | 13 | -0.003 | 0.961 | 0.016 | 0.01 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer scores worse (4 wins, 5 losses, 11 ties).
- technical-simplified: the styled answer holds (2 wins, 2 losses, 13 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| code-review-02 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| code-review-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 0.889 | 0.889 | 0.556 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 0.611 | 1.0 | 1.0 | loss |
| summarization-01 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| summarization-02 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| summarization-03 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-04 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| summarization-05 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.667 | 0.667 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 10 | 6 | 4 |
| technical-simplified | 9 | 5 | 3 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.312, Spearman -0.38, over 20 pairs.
- technical-simplified: Pearson -0.276, Spearman -0.289, over 17 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.633 | 0.648 | tie |
| code-review-02 | 0.759 | 0.71 | win |
| code-review-03 | 0.696 | 0.654 | win |
| code-review-04 | 0.661 | 0.633 | win |
| code-review-05 | 0.669 | 0.669 | tie |
| debugging-01 | 0.791 | 0.654 | win |
| debugging-02 | 0.784 | 0.807 | loss |
| debugging-03 | 0.83 | 0.713 | win |
| debugging-04 | 0.761 | 0.74 | win |
| debugging-05 | 0.69 | 0.793 | loss |
| explanation-01 | 0.665 | 0.725 | loss |
| explanation-02 | 0.628 | 0.657 | loss |
| explanation-03 | 0.717 | 0.659 | win |
| explanation-04 | 0.689 | 0.596 | win |
| explanation-05 | 0.721 | 0.672 | win |
| summarization-01 | 0.618 | 0.717 | loss |
| summarization-02 | 0.564 | 0.558 | tie |
| summarization-03 | 0.663 | 0.648 | tie |
| summarization-04 | 0.61 | 0.672 | loss |
| summarization-05 | 0.801 | 0.712 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.595 | 0.648 | loss |
| code-review-02 | 0.711 | 0.71 | tie |
| code-review-03 | 0.663 | 0.654 | tie |
| code-review-04 | 0.679 | 0.633 | win |
| code-review-05 | 0.741 | 0.669 | win |
| debugging-01 | 0.544 | 0.654 | loss |
| debugging-02 | 0.714 | 0.807 | loss |
| debugging-03 | 0.767 | 0.713 | win |
| debugging-04 | 0.832 | 0.74 | win |
| debugging-05 | 0.729 | 0.793 | loss |
| explanation-02 | 0.718 | 0.657 | win |
| explanation-03 | 0.734 | 0.659 | win |
| explanation-04 | 0.701 | 0.596 | win |
| explanation-05 | 0.65 | 0.672 | loss |
| summarization-03 | 0.667 | 0.648 | tie |
| summarization-04 | 0.698 | 0.672 | win |
| summarization-05 | 0.753 | 0.712 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 10 | 3 | 7 |
| technical-simplified | 8 | 5 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.275, Spearman 0.344, over 20 pairs.
- technical-simplified: Pearson 0.563, Spearman 0.407, over 17 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.053 | 0.043 | tie |
| code-review-02 | 0.096 | 0.085 | tie |
| code-review-03 | 0.14 | 0.109 | loss |
| code-review-04 | 0.067 | 0.06 | tie |
| code-review-05 | 0.089 | 0.081 | tie |
| debugging-01 | 0.0 | 0.146 | win |
| debugging-02 | 0.051 | 0.098 | win |
| debugging-03 | 0.032 | 0.021 | tie |
| debugging-04 | 0.088 | 0.123 | win |
| debugging-05 | 0.073 | 0.073 | tie |
| explanation-01 | 0.11 | 0.135 | win |
| explanation-02 | 0.089 | 0.117 | win |
| explanation-03 | 0.134 | 0.061 | loss |
| explanation-04 | 0.077 | 0.106 | win |
| explanation-05 | 0.081 | 0.149 | win |
| summarization-01 | 0.095 | 0.122 | win |
| summarization-02 | 0.118 | 0.152 | win |
| summarization-03 | 0.134 | 0.1 | loss |
| summarization-04 | 0.093 | 0.076 | tie |
| summarization-05 | 0.038 | 0.217 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.068 | 0.043 | loss |
| code-review-02 | 0.078 | 0.085 | tie |
| code-review-03 | 0.082 | 0.109 | win |
| code-review-04 | 0.09 | 0.06 | loss |
| code-review-05 | 0.068 | 0.081 | tie |
| debugging-01 | 0.0 | 0.146 | win |
| debugging-02 | 0.068 | 0.098 | win |
| debugging-03 | 0.019 | 0.021 | tie |
| debugging-04 | 0.07 | 0.123 | win |
| debugging-05 | 0.105 | 0.073 | loss |
| explanation-02 | 0.068 | 0.117 | win |
| explanation-03 | 0.091 | 0.061 | loss |
| explanation-04 | 0.088 | 0.106 | tie |
| explanation-05 | 0.097 | 0.149 | win |
| summarization-03 | 0.05 | 0.1 | win |
| summarization-04 | 0.122 | 0.076 | loss |
| summarization-05 | 0.053 | 0.217 | win |

## Warnings

- technical-simplified/summarization-01: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
- technical-simplified/explanation-01: the pair failed the gate, excluded
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (4 wins, 5 losses)
