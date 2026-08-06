# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-06T06:59:39+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 1 | 3 | 16 | -0.011 | 0.883 | 0.022 | 0.025 |
| technical-simplified | 4 | 5 | 10 | -0.012 | 0.807 | 0.041 | 0.018 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer scores worse (1 wins, 3 losses, 16 ties).
- technical-simplified: the styled answer scores worse (4 wins, 5 losses, 10 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-02 | 6 | 3/3 | 1.0 | 0.833 | 0.667 | win |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | loss |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 0.778 | 0.778 | 0.556 | tie |
| explanation-03 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-04 | 6 | 3/3 | 0.944 | 0.889 | 0.444 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| code-review-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | tie |
| code-review-04 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| debugging-01 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |
| debugging-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-01 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| explanation-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.611 | 0.611 | 0.444 | win |
| summarization-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 14 | 2 | 4 |
| technical-simplified | 12 | 4 | 3 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.418, Spearman 0.325, over 20 pairs.
- technical-simplified: Pearson -0.111, Spearman -0.093, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.735 | 0.601 | win |
| code-review-02 | 0.67 | 0.652 | tie |
| code-review-03 | 0.631 | 0.66 | loss |
| code-review-04 | 0.703 | 0.647 | win |
| code-review-05 | 0.784 | 0.696 | win |
| debugging-01 | 0.861 | 0.621 | win |
| debugging-02 | 0.838 | 0.666 | win |
| debugging-03 | 0.807 | 0.772 | win |
| debugging-04 | 0.81 | 0.717 | win |
| debugging-05 | 0.741 | 0.692 | win |
| explanation-01 | 0.74 | 0.676 | win |
| explanation-02 | 0.729 | 0.61 | win |
| explanation-03 | 0.733 | 0.733 | tie |
| explanation-04 | 0.678 | 0.654 | win |
| explanation-05 | 0.616 | 0.699 | loss |
| summarization-01 | 0.75 | 0.611 | win |
| summarization-02 | 0.666 | 0.571 | win |
| summarization-03 | 0.653 | 0.66 | tie |
| summarization-04 | 0.639 | 0.629 | tie |
| summarization-05 | 0.747 | 0.72 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.765 | 0.601 | win |
| code-review-02 | 0.616 | 0.652 | loss |
| code-review-03 | 0.706 | 0.66 | win |
| code-review-04 | 0.678 | 0.647 | win |
| code-review-05 | 0.664 | 0.696 | loss |
| debugging-01 | 0.574 | 0.621 | loss |
| debugging-02 | 0.828 | 0.666 | win |
| debugging-03 | 0.818 | 0.772 | win |
| debugging-04 | 0.8 | 0.717 | win |
| debugging-05 | 0.767 | 0.692 | win |
| explanation-01 | 0.68 | 0.676 | tie |
| explanation-02 | 0.766 | 0.61 | win |
| explanation-04 | 0.691 | 0.654 | win |
| explanation-05 | 0.686 | 0.699 | tie |
| summarization-01 | 0.689 | 0.611 | win |
| summarization-02 | 0.634 | 0.571 | win |
| summarization-03 | 0.628 | 0.66 | loss |
| summarization-04 | 0.649 | 0.629 | tie |
| summarization-05 | 0.747 | 0.72 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 9 | 8 | 3 |
| technical-simplified | 9 | 4 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.322, Spearman 0.298, over 20 pairs.
- technical-simplified: Pearson 0.017, Spearman -0.109, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.071 | 0.11 | win |
| code-review-02 | 0.081 | 0.048 | loss |
| code-review-03 | 0.107 | 0.117 | tie |
| code-review-04 | 0.056 | 0.101 | win |
| code-review-05 | 0.072 | 0.088 | tie |
| debugging-01 | 0.016 | 0.129 | win |
| debugging-02 | 0.04 | 0.061 | win |
| debugging-03 | 0.082 | 0.036 | loss |
| debugging-04 | 0.062 | 0.038 | loss |
| debugging-05 | 0.094 | 0.074 | tie |
| explanation-01 | 0.149 | 0.11 | loss |
| explanation-02 | 0.104 | 0.076 | loss |
| explanation-03 | 0.143 | 0.103 | loss |
| explanation-04 | 0.131 | 0.078 | loss |
| explanation-05 | 0.095 | 0.16 | win |
| summarization-01 | 0.153 | 0.174 | win |
| summarization-02 | 0.11 | 0.174 | win |
| summarization-03 | 0.097 | 0.123 | win |
| summarization-04 | 0.118 | 0.058 | loss |
| summarization-05 | 0.023 | 0.089 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.064 | 0.11 | win |
| code-review-02 | 0.051 | 0.048 | tie |
| code-review-03 | 0.074 | 0.117 | win |
| code-review-04 | 0.071 | 0.101 | win |
| code-review-05 | 0.116 | 0.088 | loss |
| debugging-01 | 0.089 | 0.129 | win |
| debugging-02 | 0.077 | 0.061 | tie |
| debugging-03 | 0.067 | 0.036 | loss |
| debugging-04 | 0.122 | 0.038 | loss |
| debugging-05 | 0.08 | 0.074 | tie |
| explanation-01 | 0.07 | 0.11 | win |
| explanation-02 | 0.087 | 0.076 | tie |
| explanation-04 | 0.13 | 0.078 | loss |
| explanation-05 | 0.118 | 0.16 | win |
| summarization-01 | 0.151 | 0.174 | win |
| summarization-02 | 0.078 | 0.174 | win |
| summarization-03 | 0.091 | 0.123 | win |
| summarization-04 | 0.064 | 0.058 | tie |
| summarization-05 | 0.078 | 0.089 | tie |

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (1 wins, 3 losses)
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (4 wins, 5 losses)
