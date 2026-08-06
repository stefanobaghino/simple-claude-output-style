# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-06T09:14:27+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 3 | 2 | 15 | 0.031 | 0.933 | 0.025 | 0.061 |
| technical-simplified | 3 | 2 | 13 | 0.003 | 0.864 | 0.037 | 0.031 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (3 wins, 2 losses, 15 ties).
- technical-simplified: the styled answer holds (3 wins, 2 losses, 13 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 0.5 | 1.0 | win |
| code-review-02 | 6 | 3/3 | 0.667 | 0.889 | 1.0 | loss |
| code-review-03 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| code-review-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 0.889 | 0.833 | 0.667 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 0.833 | 1.0 | win |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 0.778 | 1.0 | win |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-04 | 6 | 3/3 | 0.833 | 0.833 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-01 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.778 | 0.944 | 0.778 | loss |
| explanation-02 | 6 | 3/3 | 1.0 | 0.722 | 1.0 | win |
| explanation-03 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-02 | 6 | 3/3 | 0.722 | 0.778 | 0.444 | tie |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 13 | 3 | 4 |
| technical-simplified | 10 | 5 | 3 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson -0.064, Spearman 0.017, over 20 pairs.
- technical-simplified: Pearson -0.365, Spearman -0.265, over 18 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.745 | 0.639 | win |
| code-review-02 | 0.754 | 0.655 | win |
| code-review-03 | 0.721 | 0.642 | win |
| code-review-04 | 0.684 | 0.735 | loss |
| code-review-05 | 0.693 | 0.689 | tie |
| debugging-01 | 0.765 | 0.739 | win |
| debugging-02 | 0.835 | 0.748 | win |
| debugging-03 | 0.851 | 0.796 | win |
| debugging-04 | 0.772 | 0.776 | tie |
| debugging-05 | 0.74 | 0.608 | win |
| explanation-01 | 0.671 | 0.71 | loss |
| explanation-02 | 0.66 | 0.707 | loss |
| explanation-03 | 0.685 | 0.663 | win |
| explanation-04 | 0.666 | 0.681 | tie |
| explanation-05 | 0.711 | 0.659 | win |
| summarization-01 | 0.645 | 0.633 | tie |
| summarization-02 | 0.659 | 0.625 | win |
| summarization-03 | 0.663 | 0.624 | win |
| summarization-04 | 0.794 | 0.562 | win |
| summarization-05 | 0.702 | 0.67 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.644 | 0.639 | tie |
| code-review-02 | 0.736 | 0.655 | win |
| code-review-03 | 0.736 | 0.642 | win |
| code-review-04 | 0.758 | 0.735 | win |
| code-review-05 | 0.765 | 0.689 | win |
| debugging-01 | 0.652 | 0.739 | loss |
| debugging-02 | 0.802 | 0.748 | win |
| debugging-03 | 0.747 | 0.796 | loss |
| debugging-05 | 0.716 | 0.608 | win |
| explanation-01 | 0.656 | 0.71 | loss |
| explanation-02 | 0.679 | 0.707 | loss |
| explanation-03 | 0.744 | 0.663 | win |
| explanation-05 | 0.661 | 0.659 | tie |
| summarization-01 | 0.611 | 0.633 | loss |
| summarization-02 | 0.692 | 0.625 | win |
| summarization-03 | 0.607 | 0.624 | tie |
| summarization-04 | 0.643 | 0.562 | win |
| summarization-05 | 0.778 | 0.67 | win |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 5 | 6 | 9 |
| technical-simplified | 6 | 3 | 9 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.197, Spearman 0.183, over 20 pairs.
- technical-simplified: Pearson 0.433, Spearman 0.243, over 18 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.033 | 0.093 | win |
| code-review-02 | 0.077 | 0.049 | loss |
| code-review-03 | 0.055 | 0.078 | win |
| code-review-04 | 0.059 | 0.085 | win |
| code-review-05 | 0.074 | 0.079 | tie |
| debugging-01 | 0.069 | 0.136 | win |
| debugging-02 | 0.073 | 0.073 | tie |
| debugging-03 | 0.058 | 0.012 | loss |
| debugging-04 | 0.102 | 0.112 | tie |
| debugging-05 | 0.062 | 0.056 | tie |
| explanation-01 | 0.1 | 0.111 | tie |
| explanation-02 | 0.117 | 0.122 | tie |
| explanation-03 | 0.146 | 0.118 | loss |
| explanation-04 | 0.084 | 0.085 | tie |
| explanation-05 | 0.132 | 0.088 | loss |
| summarization-01 | 0.109 | 0.053 | loss |
| summarization-02 | 0.119 | 0.191 | win |
| summarization-03 | 0.126 | 0.134 | tie |
| summarization-04 | 0.098 | 0.075 | loss |
| summarization-05 | 0.105 | 0.122 | tie |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.065 | 0.093 | win |
| code-review-02 | 0.162 | 0.049 | loss |
| code-review-03 | 0.081 | 0.078 | tie |
| code-review-04 | 0.096 | 0.085 | tie |
| code-review-05 | 0.103 | 0.079 | loss |
| debugging-01 | 0.05 | 0.136 | win |
| debugging-02 | 0.057 | 0.073 | tie |
| debugging-03 | 0.055 | 0.012 | loss |
| debugging-05 | 0.054 | 0.056 | tie |
| explanation-01 | 0.068 | 0.111 | win |
| explanation-02 | 0.086 | 0.122 | win |
| explanation-03 | 0.093 | 0.118 | win |
| explanation-05 | 0.075 | 0.088 | tie |
| summarization-01 | 0.069 | 0.053 | tie |
| summarization-02 | 0.184 | 0.191 | tie |
| summarization-03 | 0.114 | 0.134 | tie |
| summarization-04 | 0.067 | 0.075 | tie |
| summarization-05 | 0.065 | 0.122 | win |

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 784, measured: 784.
Mean duration: 10341 ms. Mean wall: 45940 ms. Mean startup: 35600 ms.

## Warnings

- technical-simplified/explanation-04: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- comprehension:v3:questions:technical-simplified:code-review-04: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-edtz9j60","session_id":"dc1bda79-7ca0-49de-9bba-3ed0a6ec248e","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- comprehension:v3:grades:plain-language:summarization-01:styled:1: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-edtz9j60","session_id":"7e0b4dd2-7a9d-4ebe-8ec5-aef2180bfc48","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
