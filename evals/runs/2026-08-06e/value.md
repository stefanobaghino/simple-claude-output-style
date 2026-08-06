# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-06T09:15:15+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 4 | 1 | 15 | 0.025 | 0.922 | 0.033 | 0.047 |
| technical-simplified | 2 | 6 | 9 | -0.046 | 0.797 | 0.036 | 0.016 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (4 wins, 1 losses, 15 ties).
- technical-simplified: the styled answer scores worse (2 wins, 6 losses, 9 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| code-review-05 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| explanation-04 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 0.833 | 0.611 | 1.0 | win |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.889 | 0.944 | 0.444 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| code-review-02 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-04 | 6 | 3/3 | 0.778 | 0.944 | 0.778 | loss |
| code-review-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-01 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| explanation-04 | 6 | 3/3 | 0.778 | 1.0 | 1.0 | loss |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| summarization-03 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.889 | 0.444 | loss |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 12 | 2 | 6 |
| technical-simplified | 10 | 7 | 0 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.115, Spearman -0.012, over 20 pairs.
- technical-simplified: Pearson -0.062, Spearman 0.0, over 17 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.685 | 0.604 | win |
| code-review-02 | 0.74 | 0.651 | win |
| code-review-03 | 0.69 | 0.682 | tie |
| code-review-04 | 0.708 | 0.708 | tie |
| code-review-05 | 0.67 | 0.698 | loss |
| debugging-01 | 0.717 | 0.698 | tie |
| debugging-02 | 0.824 | 0.656 | win |
| debugging-03 | 0.843 | 0.768 | win |
| debugging-04 | 0.743 | 0.658 | win |
| debugging-05 | 0.743 | 0.691 | win |
| explanation-01 | 0.701 | 0.704 | tie |
| explanation-02 | 0.726 | 0.728 | tie |
| explanation-03 | 0.688 | 0.747 | loss |
| explanation-04 | 0.689 | 0.701 | tie |
| explanation-05 | 0.726 | 0.655 | win |
| summarization-01 | 0.721 | 0.647 | win |
| summarization-02 | 0.634 | 0.601 | win |
| summarization-03 | 0.646 | 0.578 | win |
| summarization-04 | 0.813 | 0.79 | win |
| summarization-05 | 0.806 | 0.723 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.63 | 0.604 | win |
| code-review-02 | 0.686 | 0.651 | win |
| code-review-03 | 0.736 | 0.682 | win |
| code-review-04 | 0.78 | 0.708 | win |
| code-review-05 | 0.675 | 0.698 | loss |
| debugging-01 | 0.606 | 0.698 | loss |
| debugging-02 | 0.812 | 0.656 | win |
| debugging-03 | 0.663 | 0.768 | loss |
| debugging-05 | 0.746 | 0.691 | win |
| explanation-01 | 0.679 | 0.704 | loss |
| explanation-02 | 0.676 | 0.728 | loss |
| explanation-04 | 0.671 | 0.701 | loss |
| summarization-01 | 0.751 | 0.647 | win |
| summarization-02 | 0.662 | 0.601 | win |
| summarization-03 | 0.668 | 0.578 | win |
| summarization-04 | 0.765 | 0.79 | loss |
| summarization-05 | 0.801 | 0.723 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 6 | 3 | 11 |
| technical-simplified | 7 | 4 | 6 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.419, Spearman 0.496, over 20 pairs.
- technical-simplified: Pearson 0.42, Spearman 0.363, over 17 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.052 | 0.103 | win |
| code-review-02 | 0.066 | 0.068 | tie |
| code-review-03 | 0.1 | 0.105 | tie |
| code-review-04 | 0.076 | 0.083 | tie |
| code-review-05 | 0.103 | 0.05 | loss |
| debugging-01 | 0.036 | 0.132 | win |
| debugging-02 | 0.025 | 0.03 | tie |
| debugging-03 | 0.075 | 0.038 | loss |
| debugging-04 | 0.089 | 0.104 | tie |
| debugging-05 | 0.094 | 0.092 | tie |
| explanation-01 | 0.101 | 0.107 | tie |
| explanation-02 | 0.08 | 0.109 | win |
| explanation-03 | 0.103 | 0.104 | tie |
| explanation-04 | 0.118 | 0.092 | loss |
| explanation-05 | 0.127 | 0.118 | tie |
| summarization-01 | 0.102 | 0.143 | win |
| summarization-02 | 0.129 | 0.15 | win |
| summarization-03 | 0.106 | 0.123 | tie |
| summarization-04 | 0.06 | 0.063 | tie |
| summarization-05 | 0.046 | 0.183 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.095 | 0.103 | tie |
| code-review-02 | 0.105 | 0.068 | loss |
| code-review-03 | 0.032 | 0.105 | win |
| code-review-04 | 0.059 | 0.083 | win |
| code-review-05 | 0.085 | 0.05 | loss |
| debugging-01 | 0.04 | 0.132 | win |
| debugging-02 | 0.042 | 0.03 | tie |
| debugging-03 | 0.071 | 0.038 | loss |
| debugging-05 | 0.085 | 0.092 | tie |
| explanation-01 | 0.07 | 0.107 | win |
| explanation-02 | 0.102 | 0.109 | tie |
| explanation-04 | 0.139 | 0.092 | loss |
| summarization-01 | 0.135 | 0.143 | tie |
| summarization-02 | 0.111 | 0.15 | win |
| summarization-03 | 0.1 | 0.123 | win |
| summarization-04 | 0.083 | 0.063 | tie |
| summarization-05 | 0.042 | 0.183 | win |

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 766, measured: 766.
Mean duration: 12217 ms. Mean wall: 46578 ms. Mean startup: 34361 ms.

## Warnings

- technical-simplified/explanation-05: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- comprehension:v3:questions:technical-simplified:summarization-05: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-9vfkfgp9","session_id":"cb5f52a4-6c28-4914-8170-f0f556279cb9","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- code-review-01: the grader returned no usable grades for the text 5ee3ea3053e7, so comprehension skips the replicate
- comprehension:v3:grades:plain-language:explanation-03:styled:1: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-9vfkfgp9","session_id":"fa50ab72-9d88-4b2d-844c-eb32bc062e63","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (2 wins, 6 losses)
