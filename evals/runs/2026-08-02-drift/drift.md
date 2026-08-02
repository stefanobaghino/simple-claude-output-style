# Drift report

Run: 2026-08-02-drift

The report measures rule obedience across long sessions. A session is
15 scripted turns in one Claude Code session, with the style
active. Each turn resumes the session of the previous turn, so the
context grows. Each session runs 3 time(s), and each repeat
rotates the prompt order, so a hard prompt does not always sit at the
same turn position. The linter checks each answer with the rule set
of the style. The verdict compares the slope of the mean rate series
against the threshold: "growing" when the slope is more than
0.25 violations per 100 sentences per turn, else "flat".

## plain-language

- Sessions: 3/3 complete
- Slope of the mean series: 0.0 violations per 100 sentences per turn
- Slope threshold: 0.25
- Verdict: flat

| Turn | Mean rate | Repeat 1 | Repeat 2 | Repeat 3 |
|---|---|---|---|---|
| 1 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 |
| 3 | 0.00 | 0.00 | 0.00 | 0.00 |
| 4 | 0.00 | 0.00 | 0.00 | 0.00 |
| 5 | 0.00 | 0.00 | 0.00 | 0.00 |
| 6 | 0.00 | 0.00 | 0.00 | 0.00 |
| 7 | 0.00 | 0.00 | 0.00 | 0.00 |
| 8 | 0.00 | 0.00 | 0.00 | 0.00 |
| 9 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10 | 0.00 | 0.00 | 0.00 | 0.00 |
| 11 | 0.00 | 0.00 | 0.00 | 0.00 |
| 12 | 0.00 | 0.00 | 0.00 | 0.00 |
| 13 | 0.00 | 0.00 | 0.00 | 0.00 |
| 14 | 0.00 | 0.00 | 0.00 | 0.00 |
| 15 | 0.00 | 0.00 | 0.00 | 0.00 |

## technical-simplified

- Sessions: 3/3 complete
- Slope of the mean series: 0.455 violations per 100 sentences per turn
- Slope threshold: 0.25
- Verdict: growing

| Turn | Mean rate | Repeat 1 | Repeat 2 | Repeat 3 |
|---|---|---|---|---|
| 1 | 7.25 | 5.88 | 4.76 | 11.11 |
| 2 | 4.76 | 14.29 | 0.00 | 0.00 |
| 3 | 8.61 | 0.00 | 13.33 | 12.50 |
| 4 | 4.98 | 0.00 | 8.70 | 6.25 |
| 5 | 4.00 | 12.00 | 0.00 | 0.00 |
| 6 | 10.65 | 0.00 | 14.29 | 17.65 |
| 7 | 0.00 | 0.00 | 0.00 | 0.00 |
| 8 | 4.44 | 0.00 | 13.33 | 0.00 |
| 9 | 10.00 | 20.00 | 10.00 | 0.00 |
| 10 | 11.69 | 17.65 | 8.33 | 9.09 |
| 11 | 34.05 | 75.00 | 20.00 | 7.14 |
| 12 | 4.55 | 0.00 | 13.64 | 0.00 |
| 13 | 7.58 | 22.73 | 0.00 | 0.00 |
| 14 | 7.94 | 0.00 | 0.00 | 23.81 |
| 15 | 9.12 | 0.00 | 20.69 | 6.67 |

## Warnings

- none
