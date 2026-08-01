# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension uses 5 questions per prompt, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-01T20:09:19+00:00.

## Comprehension (weak reader)

The grader model writes questions with reference answers from the task prompt alone, so the questions cannot favor an arm. The weak reader answers the questions from one answer text only, and the grader marks each reader answer against the reference. The score is the fraction of questions correct: an answer that drops content loses questions, so a short answer wins only when the content survives. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 2 | 6 | 12 |
| technical-simplified | 1 | 6 | 11 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer scores worse (2 wins, 6 losses, 12 ties).
- technical-simplified: the styled answer scores worse (1 wins, 6 losses, 11 ties).

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.8 | 1.0 | loss |
| code-review-02 | 0.6 | 0.8 | loss |
| code-review-03 | 0.6 | 0.8 | loss |
| code-review-04 | 0.4 | 0.6 | loss |
| code-review-05 | 0.8 | 0.8 | tie |
| debugging-01 | 0.4 | 0.6 | loss |
| debugging-02 | 0.6 | 0.6 | tie |
| debugging-03 | 0.6 | 0.6 | tie |
| debugging-04 | 0.8 | 0.8 | tie |
| debugging-05 | 0.6 | 0.6 | tie |
| explanation-01 | 0.8 | 0.8 | tie |
| explanation-02 | 1.0 | 1.0 | tie |
| explanation-03 | 0.6 | 0.8 | loss |
| explanation-04 | 1.0 | 0.8 | win |
| explanation-05 | 0.8 | 0.8 | tie |
| summarization-01 | 0.8 | 0.8 | tie |
| summarization-02 | 0.8 | 0.6 | win |
| summarization-03 | 1.0 | 1.0 | tie |
| summarization-04 | 0.8 | 0.8 | tie |
| summarization-05 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 1.0 | 1.0 | tie |
| code-review-02 | 0.6 | 0.8 | loss |
| code-review-03 | 0.6 | 0.8 | loss |
| code-review-04 | 0.6 | 0.6 | tie |
| code-review-05 | 0.8 | 0.8 | tie |
| debugging-01 | 0.4 | 0.6 | loss |
| debugging-02 | 0.6 | 0.6 | tie |
| debugging-03 | 0.8 | 0.6 | win |
| debugging-04 | 0.8 | 0.8 | tie |
| debugging-05 | 0.6 | 0.6 | tie |
| explanation-01 | 0.6 | 0.8 | loss |
| explanation-02 | 1.0 | 1.0 | tie |
| explanation-04 | 0.6 | 0.8 | loss |
| explanation-05 | 0.8 | 0.8 | tie |
| summarization-01 | 0.8 | 0.8 | tie |
| summarization-03 | 1.0 | 1.0 | tie |
| summarization-04 | 0.6 | 0.8 | loss |
| summarization-05 | 1.0 | 1.0 | tie |

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
- plain-language: the styled answer scores worse than the unstyled answer on comprehension (2 wins, 6 losses)
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (1 wins, 6 losses)
