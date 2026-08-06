# Reader-value report

The checks compare the styled answer with the unstyled answer of
the same prompt, pair by pair, as win, loss, or tie. Only pairs
whose styled answer passes the fidelity gate enter the checks.
Each judge call sees one bare text: no style name, no arm label,
and never both answers. Thus a judge cannot know which answer is
styled. The judge models differ from the writer of the answers.

Judges: reader haiku, grader opus. Comprehension asks up to 6 questions per pair, worded by both answers in balance, with 3 reader replicates per answer, ambiguity uses 3 restatements per answer, and the round-trip goes through Italian. Judged on 2026-08-06T09:15:58+00:00.

## Comprehension (weak reader)

The questions come from the shared facts of the pair, mined in both directions: the facts of the unstyled answer that survive in the styled answer, and the facts of the styled answer that the unstyled answer also states. The quiz takes half of its questions from each wording, so neither answer sets the phrasing alone, and the Sources column counts the questions per wording (unstyled/styled). A grader call turns each fact into one question, and the fact is the reference answer. The weak reader answers the questions from one answer text, once per replicate, and the grader marks every reply. Each styled replicate meets each unstyled replicate as a win, a loss, or a tie, and the pair outcome is the strict plurality, else a tie. The agreement is the plurality share, and the buried-fact rate counts "NOT IN TEXT" replies to a shared fact, per arm. The check measures extraction over shared material. Absence belongs to the content-loss report. Higher is better.

| Style | Wins | Losses | Ties | Mean delta | Agreement | Buried (styled) | Buried (unstyled) |
|---|---|---|---|---|---|---|---|
| plain-language | 2 | 2 | 16 | -0.011 | 0.872 | 0.036 | 0.022 |
| technical-simplified | 2 | 6 | 11 | -0.053 | 0.895 | 0.056 | 0.015 |

The styled answer must not score worse than the unstyled answer.
- plain-language: the styled answer holds (2 wins, 2 losses, 16 ties).
- technical-simplified: the styled answer scores worse (2 wins, 6 losses, 11 ties).

### plain-language

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-04 | 6 | 3/3 | 0.889 | 0.778 | 0.556 | win |
| code-review-05 | 6 | 3/3 | 0.944 | 1.0 | 0.667 | tie |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| debugging-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-02 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| explanation-03 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-04 | 6 | 3/3 | 0.667 | 0.722 | 0.667 | tie |
| explanation-05 | 6 | 3/3 | 0.944 | 0.944 | 0.556 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-02 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

### technical-simplified

| Pair | Questions | Sources (u/s) | Styled | Unstyled | Agreement | Result |
|---|---|---|---|---|---|---|
| code-review-01 | 6 | 3/3 | 0.667 | 1.0 | 1.0 | loss |
| code-review-02 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-03 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| code-review-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| code-review-05 | 6 | 3/3 | 1.0 | 0.889 | 0.667 | win |
| debugging-01 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| debugging-02 | 6 | 3/3 | 0.833 | 0.944 | 0.667 | loss |
| debugging-04 | 6 | 3/3 | 0.5 | 0.833 | 1.0 | loss |
| debugging-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-01 | 6 | 3/3 | 0.889 | 1.0 | 0.667 | loss |
| explanation-02 | 6 | 3/3 | 0.833 | 1.0 | 1.0 | loss |
| explanation-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-04 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| explanation-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-01 | 6 | 3/3 | 1.0 | 0.944 | 0.667 | tie |
| summarization-02 | 6 | 3/3 | 0.667 | 0.833 | 1.0 | loss |
| summarization-03 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |
| summarization-04 | 6 | 3/3 | 0.833 | 0.889 | 0.667 | tie |
| summarization-05 | 6 | 3/3 | 1.0 | 1.0 | 1.0 | tie |

## Ambiguity (paraphrase agreement)

Independent reader calls restate one answer text in their own words. The score is the mean pairwise lexical similarity between the restatements: when the readers agree on what the text says, the text is less ambiguous. Higher is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 11 | 2 | 7 |
| technical-simplified | 9 | 6 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.022, Spearman -0.002, over 20 pairs.
- technical-simplified: Pearson -0.245, Spearman -0.258, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.661 | 0.64 | win |
| code-review-02 | 0.772 | 0.64 | win |
| code-review-03 | 0.733 | 0.744 | tie |
| code-review-04 | 0.739 | 0.664 | win |
| code-review-05 | 0.673 | 0.645 | win |
| debugging-01 | 0.801 | 0.734 | win |
| debugging-02 | 0.795 | 0.658 | win |
| debugging-03 | 0.848 | 0.8 | win |
| debugging-04 | 0.776 | 0.774 | tie |
| debugging-05 | 0.81 | 0.694 | win |
| explanation-01 | 0.669 | 0.67 | tie |
| explanation-02 | 0.728 | 0.7 | win |
| explanation-03 | 0.671 | 0.645 | win |
| explanation-04 | 0.659 | 0.664 | tie |
| explanation-05 | 0.744 | 0.618 | win |
| summarization-01 | 0.669 | 0.671 | tie |
| summarization-02 | 0.62 | 0.605 | tie |
| summarization-03 | 0.627 | 0.641 | tie |
| summarization-04 | 0.619 | 0.722 | loss |
| summarization-05 | 0.789 | 0.85 | loss |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.675 | 0.64 | win |
| code-review-02 | 0.643 | 0.64 | tie |
| code-review-03 | 0.695 | 0.744 | loss |
| code-review-04 | 0.586 | 0.664 | loss |
| code-review-05 | 0.686 | 0.645 | win |
| debugging-01 | 0.769 | 0.734 | win |
| debugging-02 | 0.798 | 0.658 | win |
| debugging-04 | 0.768 | 0.774 | tie |
| debugging-05 | 0.714 | 0.694 | win |
| explanation-01 | 0.643 | 0.67 | loss |
| explanation-02 | 0.709 | 0.7 | tie |
| explanation-03 | 0.67 | 0.645 | win |
| explanation-04 | 0.688 | 0.664 | win |
| explanation-05 | 0.749 | 0.618 | win |
| summarization-01 | 0.67 | 0.671 | tie |
| summarization-02 | 0.641 | 0.605 | win |
| summarization-03 | 0.595 | 0.641 | loss |
| summarization-04 | 0.617 | 0.722 | loss |
| summarization-05 | 0.748 | 0.85 | loss |

## Translation round-trip

One call translates the answer to another language, and a second call translates the result back to English. The score is the lexical loss between the original and the round-trip: simpler text survives the round-trip with less loss. Lower is better.

| Style | Wins | Losses | Ties |
|---|---|---|---|
| plain-language | 6 | 5 | 9 |
| technical-simplified | 9 | 6 | 4 |

The length confound is the correlation between the length ratio of a pair (styled words over unstyled words) and the styled advantage (the score gain of the styled arm). A negative value means that the shorter styled answers score better.
- plain-language: Pearson 0.598, Spearman 0.444, over 20 pairs.
- technical-simplified: Pearson 0.405, Spearman 0.463, over 19 pairs.

### plain-language

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.07 | 0.087 | tie |
| code-review-02 | 0.055 | 0.074 | tie |
| code-review-03 | 0.093 | 0.11 | tie |
| code-review-04 | 0.069 | 0.102 | win |
| code-review-05 | 0.077 | 0.103 | win |
| debugging-01 | 0.085 | 0.16 | win |
| debugging-02 | 0.068 | 0.101 | win |
| debugging-03 | 0.039 | 0.045 | tie |
| debugging-04 | 0.094 | 0.027 | loss |
| debugging-05 | 0.08 | 0.077 | tie |
| explanation-01 | 0.174 | 0.081 | loss |
| explanation-02 | 0.113 | 0.112 | tie |
| explanation-03 | 0.115 | 0.096 | tie |
| explanation-04 | 0.106 | 0.07 | loss |
| explanation-05 | 0.1 | 0.099 | tie |
| summarization-01 | 0.084 | 0.052 | loss |
| summarization-02 | 0.134 | 0.233 | win |
| summarization-03 | 0.126 | 0.144 | tie |
| summarization-04 | 0.137 | 0.085 | loss |
| summarization-05 | 0.055 | 0.143 | win |

### technical-simplified

| Pair | Styled | Unstyled | Result |
|---|---|---|---|
| code-review-01 | 0.059 | 0.087 | win |
| code-review-02 | 0.081 | 0.074 | tie |
| code-review-03 | 0.066 | 0.11 | win |
| code-review-04 | 0.11 | 0.102 | tie |
| code-review-05 | 0.139 | 0.103 | loss |
| debugging-01 | 0.065 | 0.16 | win |
| debugging-02 | 0.042 | 0.101 | win |
| debugging-04 | 0.067 | 0.027 | loss |
| debugging-05 | 0.093 | 0.077 | tie |
| explanation-01 | 0.117 | 0.081 | loss |
| explanation-02 | 0.067 | 0.112 | win |
| explanation-03 | 0.107 | 0.096 | tie |
| explanation-04 | 0.151 | 0.07 | loss |
| explanation-05 | 0.13 | 0.099 | loss |
| summarization-01 | 0.085 | 0.052 | loss |
| summarization-02 | 0.108 | 0.233 | win |
| summarization-03 | 0.088 | 0.144 | win |
| summarization-04 | 0.039 | 0.085 | win |
| summarization-05 | 0.053 | 0.143 | win |

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 802, measured: 802.
Mean duration: 10951 ms. Mean wall: 41603 ms. Mean startup: 30652 ms.

## Warnings

- technical-simplified/debugging-03: the pair failed the gate, excluded
- comprehension:v3:questions:technical-simplified:summarization-02: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-5qm1ot4u","session_id":"bd24b738-bb9b-4dc4-bf9a-c38c7ad06251","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- comprehension:v3:grades:plain-language:explanation-03:unstyled:1: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-5qm1ot4u","session_id":"68cc9737-de63-4d0c-8800-36ce15a74e2d","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- comprehension:v3:grades:plain-language:explanation-04:styled:2: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-5qm1ot4u","session_id":"f123dc1c-c5e1-474f-9ee3-ef4b9f8b003e","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- comprehension:v3:grades:plain-language:code-review-05:unstyled:2: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-value-5qm1ot4u","session_id":"e948bb03-0136-4969-860b-8a5ec8df49c4","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","cle
- technical-simplified: the styled answer scores worse than the unstyled answer on comprehension (2 wins, 6 losses)
