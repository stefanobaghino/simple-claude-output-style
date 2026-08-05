# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-05T05:59:26+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 5 | 2 | 13 | 0.022 | 0.883 | 0.028 | 0.056 |
| technical-simplified | 1 | 3 | 12 | -0.021 | 0.889 | 0.021 | 0.01 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (5 wins, 2 losses, 13 ties).
- technical-simplified: the styled answer scores worse (1 wins, 3 losses, 12 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 0.778 | 0.833 | 0.667 | tie |
| code-review-04 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| debugging-02 | 6 | 3/3 | 0.944 | 0.778 | 0.667 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 0.833 | 0.667 | 1.0 | win |
| summarization-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 0.778 | 0.778 | 0.556 | tie |
| code-review-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| code-review-05 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 5 | 8 | 7 |
| technical-simplified | 4 | 7 | 5 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.047, Spearman 0.012, over 20 pairs.
- technical-simplified: Pearson 0.161, Spearman 0.106, over 16 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.653 | 0.65 | tie |
| code-review-02 | 0.76 | 0.733 | win |
| code-review-03 | 0.682 | 0.677 | tie |
| code-review-04 | 0.693 | 0.666 | win |
| code-review-05 | 0.644 | 0.678 | loss |
| debugging-01 | 0.734 | 0.767 | loss |
| debugging-02 | 0.727 | 0.791 | loss |
| debugging-03 | 0.827 | 0.862 | loss |
| debugging-04 | 0.732 | 0.737 | tie |
| debugging-05 | 0.734 | 0.641 | win |
| explanation-01 | 0.655 | 0.679 | loss |
| explanation-02 | 0.59 | 0.643 | loss |
| explanation-03 | 0.68 | 0.684 | tie |
| explanation-04 | 0.644 | 0.63 | tie |
| explanation-05 | 0.674 | 0.677 | tie |
| summarization-01 | 0.658 | 0.737 | loss |
| summarization-02 | 0.624 | 0.604 | win |
| summarization-03 | 0.627 | 0.612 | tie |
| summarization-04 | 0.562 | 0.589 | loss |
| summarization-05 | 0.801 | 0.747 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.604 | 0.65 | loss |
| code-review-02 | 0.734 | 0.733 | tie |
| code-review-03 | 0.639 | 0.677 | loss |
| code-review-04 | 0.638 | 0.666 | loss |
| code-review-05 | 0.639 | 0.678 | loss |
| debugging-01 | 0.625 | 0.767 | loss |
| debugging-02 | 0.651 | 0.791 | loss |
| debugging-03 | 0.595 | 0.862 | loss |
| debugging-05 | 0.707 | 0.641 | win |
| explanation-02 | 0.691 | 0.643 | win |
| explanation-04 | 0.641 | 0.63 | tie |
| explanation-05 | 0.717 | 0.677 | win |
| summarization-01 | 0.734 | 0.737 | tie |
| summarization-03 | 0.742 | 0.612 | win |
| summarization-04 | 0.595 | 0.589 | tie |
| summarization-05 | 0.729 | 0.747 | tie |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 6 | 3 | 11 |
| technical-simplified | 8 | 2 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.018, Spearman 0.053, over 20 pairs.
- technical-simplified: Pearson 0.389, Spearman 0.371, over 16 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.066 | 0.076 | tie |
| code-review-02 | 0.066 | 0.046 | tie |
| code-review-03 | 0.1 | 0.121 | win |
| code-review-04 | 0.109 | 0.109 | tie |
| code-review-05 | 0.078 | 0.075 | tie |
| debugging-01 | 0.016 | 0.091 | win |
| debugging-02 | 0.112 | 0.07 | loss |
| debugging-03 | 0.026 | 0.019 | tie |
| debugging-04 | 0.038 | 0.041 | tie |
| debugging-05 | 0.097 | 0.092 | tie |
| explanation-01 | 0.083 | 0.102 | tie |
| explanation-02 | 0.114 | 0.141 | win |
| explanation-03 | 0.091 | 0.095 | tie |
| explanation-04 | 0.103 | 0.117 | tie |
| explanation-05 | 0.13 | 0.096 | loss |
| summarization-01 | 0.105 | 0.14 | win |
| summarization-02 | 0.145 | 0.186 | win |
| summarization-03 | 0.208 | 0.128 | loss |
| summarization-04 | 0.07 | 0.133 | win |
| summarization-05 | 0.135 | 0.115 | tie |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.045 | 0.076 | win |
| code-review-02 | 0.077 | 0.046 | loss |
| code-review-03 | 0.04 | 0.121 | win |
| code-review-04 | 0.052 | 0.109 | win |
| code-review-05 | 0.057 | 0.075 | tie |
| debugging-01 | 0.043 | 0.091 | win |
| debugging-02 | 0.052 | 0.07 | tie |
| debugging-03 | 0.011 | 0.019 | tie |
| debugging-05 | 0.101 | 0.092 | tie |
| explanation-02 | 0.114 | 0.141 | win |
| explanation-04 | 0.111 | 0.117 | tie |
| explanation-05 | 0.117 | 0.096 | loss |
| summarization-01 | 0.129 | 0.14 | tie |
| summarization-03 | 0.079 | 0.128 | win |
| summarization-04 | 0.082 | 0.133 | win |
| summarization-05 | 0.058 | 0.115 | win |

## Warnings

- technical-simplified/explanation-01: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (1 wins, 3 losses)
