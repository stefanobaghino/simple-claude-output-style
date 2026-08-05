# Cross-run comparison

The comparison reads the stored artifacts of several runs with identical conditions. Per style and axis, the table states one value per run and the spread: minimum, mean, maximum, and the sample standard deviation. The spread is the error bar of the harness: it shows how much a verdict moves on a resample. Net wins is wins minus losses, and n counts the runs that hold a value for the axis.

Runs: 2026-08-01b, 2026-08-05, 2026-08-05b.

## plain-language

| Axis | 2026-08-01b | 2026-08-05 | 2026-08-05b | n | Min | Mean | Max | Stdev |
|---|---|---|---|---|---|---|---|---|
| fidelity: styled violation rate | 0.0 | 0.0 | 0.0 | 3 | 0.0 | 0.0 | 0.0 | 0.0 |
| fidelity: gated pairs passed | 20 | 20 | 20 | 3 | 20 | 20.0 | 20 | 0.0 |
| cost: output-token ratio | 0.87 | 0.88 | 0.8 | 3 | 0.8 | 0.85 | 0.88 | 0.044 |
| value: net wins (comprehension) | -1 | 3 | -2 | 3 | -2 | 0.0 | 3 | 2.646 |
| value: net wins (paraphrase) | 11 | -3 | 2 | 3 | -3 | 3.333 | 11 | 7.095 |
| value: net wins (roundtrip) | 5 | 3 | 1 | 3 | 1 | 3.0 | 5 | 2.0 |
| loss: fact survival median | 0.786 | 0.806 | 0.769 | 3 | 0.769 | 0.787 | 0.806 | 0.019 |
| loss: hedge survival median | 0.333 | 0.5 | 0.75 | 3 | 0.333 | 0.528 | 0.75 | 0.21 |

## technical-simplified

| Axis | 2026-08-01b | 2026-08-05 | 2026-08-05b | n | Min | Mean | Max | Stdev |
|---|---|---|---|---|---|---|---|---|
| fidelity: styled violation rate | 4.56 | 5.3 | 6.34 | 3 | 4.56 | 5.4 | 6.34 | 0.894 |
| fidelity: gated pairs passed | 18 | 16 | 16 | 3 | 16 | 16.667 | 18 | 1.155 |
| cost: output-token ratio | 0.88 | 0.8 | 0.84 | 3 | 0.8 | 0.84 | 0.88 | 0.04 |
| value: net wins (comprehension) | 2 | -2 | 0 | 3 | -2 | 0.0 | 2 | 2.0 |
| value: net wins (paraphrase) | 10 | -3 | 6 | 3 | -3 | 4.333 | 10 | 6.658 |
| value: net wins (roundtrip) | 8 | 6 | 8 | 3 | 6 | 7.333 | 8 | 1.155 |
| loss: fact survival median | 0.859 | 0.806 | 0.862 | 3 | 0.806 | 0.842 | 0.862 | 0.032 |
| loss: hedge survival median | 0.0 | 0.0 | 0.834 | 3 | 0.0 | 0.278 | 0.834 | 0.482 |

## Warnings

- condition mismatch on claude version: 2026-08-01b 2.1.220 (Claude Code), 2026-08-05 2.1.222 (Claude Code), 2026-08-05b 2.1.222 (Claude Code)
