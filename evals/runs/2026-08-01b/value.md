# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-01T20:09:19+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 5 | 6 | 9 | -0.003 | 0.856 | 0.042 | 0.047 |
| technical-simplified | 4 | 2 | 12 | 0.009 | 0.846 | 0.043 | 0.059 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer scores worse (5 wins, 6 losses, 9 ties).
- technical-simplified: the styled answer holds (4 wins, 2 losses, 12 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 1.0 | 0.667 | loss |
| code-review-02 | 6 | 3/3 | 0.944 | 0.833 | 0.667 | win |
| code-review-03 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| code-review-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.833 | 0.333 | tie |
| debugging-05 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 0.667 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| summarization-01 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-02 | 6 | 3/3 | 0.778 | 0.944 | 0.778 | loss |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 0.778 | 0.833 | 0.667 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.778 | 0.667 | 0.667 | win |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-03 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.611 | 0.778 | 0.778 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-04 | 6 | 3/3 | 0.833 | 0.833 | 0.333 | tie |
| explanation-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-01 | 6 | 3/3 | 0.944 | 0.889 | 0.444 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 13 | 2 | 5 |
| technical-simplified | 14 | 4 | 0 |

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.648 | 0.596 | win |
| code-review-02 | 0.682 | 0.619 | win |
| code-review-03 | 0.686 | 0.69 | tie |
| code-review-04 | 0.671 | 0.697 | loss |
| code-review-05 | 0.712 | 0.647 | win |
| debugging-01 | 0.69 | 0.68 | tie |
| debugging-02 | 0.751 | 0.736 | tie |
| debugging-03 | 0.777 | 0.665 | win |
| debugging-04 | 0.813 | 0.66 | win |
| debugging-05 | 0.69 | 0.685 | tie |
| explanation-01 | 0.629 | 0.709 | loss |
| explanation-02 | 0.692 | 0.667 | win |
| explanation-03 | 0.703 | 0.659 | win |
| explanation-04 | 0.66 | 0.613 | win |
| explanation-05 | 0.738 | 0.623 | win |
| summarization-01 | 0.669 | 0.667 | tie |
| summarization-02 | 0.653 | 0.588 | win |
| summarization-03 | 0.695 | 0.578 | win |
| summarization-04 | 0.651 | 0.584 | win |
| summarization-05 | 0.783 | 0.705 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.621 | 0.596 | win |
| code-review-02 | 0.75 | 0.619 | win |
| code-review-03 | 0.654 | 0.69 | loss |
| code-review-04 | 0.661 | 0.697 | loss |
| code-review-05 | 0.756 | 0.647 | win |
| debugging-01 | 0.786 | 0.68 | win |
| debugging-02 | 0.863 | 0.736 | win |
| debugging-03 | 0.814 | 0.665 | win |
| debugging-04 | 0.724 | 0.66 | win |
| debugging-05 | 0.769 | 0.685 | win |
| explanation-01 | 0.749 | 0.709 | win |
| explanation-02 | 0.725 | 0.667 | win |
| explanation-04 | 0.714 | 0.613 | win |
| explanation-05 | 0.667 | 0.623 | win |
| summarization-01 | 0.604 | 0.667 | loss |
| summarization-03 | 0.652 | 0.578 | win |
| summarization-04 | 0.551 | 0.584 | loss |
| summarization-05 | 0.754 | 0.705 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 7 | 2 | 11 |
| technical-simplified | 12 | 4 | 2 |

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.07 | 0.104 | win |
| code-review-02 | 0.088 | 0.058 | loss |
| code-review-03 | 0.099 | 0.061 | loss |
| code-review-04 | 0.099 | 0.096 | tie |
| code-review-05 | 0.115 | 0.115 | tie |
| debugging-01 | 0.102 | 0.133 | win |
| debugging-02 | 0.042 | 0.072 | win |
| debugging-03 | 0.082 | 0.074 | tie |
| debugging-04 | 0.116 | 0.128 | tie |
| debugging-05 | 0.072 | 0.088 | tie |
| explanation-01 | 0.138 | 0.124 | tie |
| explanation-02 | 0.082 | 0.141 | win |
| explanation-03 | 0.102 | 0.107 | tie |
| explanation-04 | 0.126 | 0.116 | tie |
| explanation-05 | 0.106 | 0.116 | tie |
| summarization-01 | 0.14 | 0.126 | tie |
| summarization-02 | 0.166 | 0.198 | win |
| summarization-03 | 0.121 | 0.153 | win |
| summarization-04 | 0.082 | 0.063 | tie |
| summarization-05 | 0.094 | 0.217 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.074 | 0.104 | win |
| code-review-02 | 0.06 | 0.058 | tie |
| code-review-03 | 0.114 | 0.061 | loss |
| code-review-04 | 0.062 | 0.096 | win |
| code-review-05 | 0.087 | 0.115 | win |
| debugging-01 | 0.0 | 0.133 | win |
| debugging-02 | 0.054 | 0.072 | tie |
| debugging-03 | 0.043 | 0.074 | win |
| debugging-04 | 0.054 | 0.128 | win |
| debugging-05 | 0.113 | 0.088 | loss |
| explanation-01 | 0.172 | 0.124 | loss |
| explanation-02 | 0.065 | 0.141 | win |
| explanation-04 | 0.088 | 0.116 | win |
| explanation-05 | 0.179 | 0.116 | loss |
| summarization-01 | 0.065 | 0.126 | win |
| summarization-03 | 0.083 | 0.153 | win |
| summarization-04 | 0.025 | 0.063 | win |
| summarization-05 | 0.068 | 0.217 | win |

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (5 wins, 6 losses)
