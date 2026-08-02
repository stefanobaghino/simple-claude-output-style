# Evaluation harness

This directory holds the evaluation harness for the output styles in
`plugin/output-styles/`. The harness stays outside `plugin/` on purpose:
the marketplace serves only the `plugin/` directory, so installers never
receive the harness.

The harness has seven components. The first is a deterministic linter.
It checks a Markdown text against the writing rules of a style and
reports each violation, plus a rate per 100 sentences. The second is a
pair runner. It produces, per prompt, one answer per style and one
shared unstyled answer, through the Claude Code CLI, and stores the
answers with their provenance. The third is a fidelity gate. It checks
each styled answer of a run with the rules of its style and marks each
pair as pass or fail, because a non-compliant answer does not represent
its style. The judged measurements read only the pairs with a true
`pass` mark; the token-cost measurement reads all pairs. The fourth is
a token-cost report. It states two numbers per style: the fixed input
overhead of the style block per request, and the distribution of the
ratio of styled answer length to unstyled answer length. The fifth is
a reader-value report. It compares, per gated pair, the styled answer
with the unstyled answer on three reader-facing checks, as win, loss,
or tie. The sixth is a content-loss report. It measures, per gated
pair, the fraction of the facts of the unstyled answer that survive
in the styled answer, and each uncertain claim that lost its
uncertainty. The seventh is a drift report. It runs a scripted long
session per style, several times, lints every turn, and shows the
violation rate over turn positions with a verdict per style: flat or
growing. See the tracking issue in this repository for the other
planned components.

## Rule files

The engine is shared, and the rules are data. Each style has one rule file
in `rules/`, named `<style>.rules.yaml`. The header comment of each rule
file documents the exclusions of the style: the rules that need judgment
and thus stay outside the mechanical checks.

The gate policy lives apart, in `rules/gate.yaml`: the pass threshold
per style, as the highest violation rate per 100 sentences that passes.
A threshold edit changes only the pass mark, never the measured rate,
so the policy must not change the rule-file hashes in the provenance.
The thresholds differ per style, because the rule counts differ and
thus the rates are not comparable across styles.

## How to run

The harness uses [uv](https://docs.astral.sh/uv/). From this directory:

```
uv run pytest
uv run style-lint FILE.md --rules rules/technical-simplified.rules.yaml
uv run style-pairs
uv run style-gate runs/<date>
uv run style-cost runs/<date> [--probe]
uv run style-value runs/<date> [--judge]
uv run style-loss runs/<date> [--judge]
uv run style-drift [--generate] [--out runs/<date>-drift]
```

The linter exits with code 1 when it finds a violation.

The pair runner reads the prompt set in `prompts/prompts.yaml` and calls
the `claude` CLI once per answer, on the account of the person who runs
it. The call is isolated as far as the CLI permits: no tools, no MCP
servers, no hooks, one turn, and no dynamic system-prompt sections.
Plugins from the user configuration still load; the run data records
them, so a change in the environment stays visible. An interrupted run
resumes when the same invocation runs again. The runner exits with code
1 when the pair set is incomplete.

The gate reads the answers of a run and writes the fidelity files into
the run directory. It checks every styled answer with the rules of its
style, and it checks every unstyled answer with every rule set of the
run, as a baseline: the baseline shows how much rule obedience exists
without a style. Re-gating overwrites the fidelity files, because the
gate is a pure function of the answers, the rules, and the policy. Exit
codes: 0 when every pair passes and no warnings exist, 1 when pairs
fail or warnings exist, 2 when the run cannot be gated.

The cost report reads all pairs of a run and writes the cost files into
the run directory. The answer-length part is offline: the ratio of a
pair is the output-token count of the styled answer divided by the
output-token count of the unstyled answer, reported as a distribution
and per task type. The input-overhead part needs a live measurement,
because a stored run holds no input-token data for it: `--probe` runs
one minimal call per arm and takes the difference in input context
tokens between a styled call and an unstyled call. Both probe arms load
the plugin, so the difference isolates the style block; the probe data
lands in `cost-probe.json`, and a later `style-cost` call without
`--probe` reuses it. Exit codes: 0 when both numbers exist and no
warnings exist, 1 when warnings exist (for example, the overhead is not
measured), 2 when the run cannot be reported.

The reader-value report reads only the pairs whose styled answer
passes the gate, because rule obedience alone can produce compliant,
useless text, and this report measures whether a reader gains
anything. Three checks compare the two answers of a pair: weak-reader
comprehension (a weaker model answers questions about one answer text,
and a grader marks the answers), ambiguity through paraphrase
(independent restatements of one answer text, scored by their mutual
agreement), and translation round-trip (one answer text goes to
another language and back, scored by the lexical loss). Every judge
call sees one bare text without a style name or an arm label, and the
judge models must differ from the writer model of the run. `--judge`
runs the live calls and appends the raw outputs to `value-raw.jsonl`;
an interrupted judge run resumes when the same invocation runs again.
Without `--judge` the tool rescores the stored raw data offline. Exit
codes: 0 when the checks are scored and no warnings exist, 1 when
warnings exist (for example, a check without judge data), 2 when the
run cannot be scored.

The content-loss report also reads only the gated pairs. Two checks
measure what the rewrite loses: completeness (the judge lists the
facts of the unstyled answer, then checks each fact against the
styled answer) and hedging survival (the judge lists the uncertain
claims of the unstyled answer, then judges whether the styled answer
keeps, hardens, or drops each claim). A claim that hardens becomes a
false certainty, which is worse than a lost fact. No judge call sees
both answers of a pair: the extracted items travel between the calls,
never the source text. The judge model must differ from the writer
model of the run. `--judge` runs the live calls and appends the raw
outputs to `loss-raw.jsonl`; an interrupted judge run resumes when
the same invocation runs again. Without `--judge` the tool rescores
the stored raw data offline. The exit codes equal the exit codes of
`style-value`.

The drift report owns its own run directory, because it measures
sessions, not pairs. A session is 15 scripted turns in one Claude Code
session, with the style active: each turn resumes the session of the
previous turn, so the context grows. The turns reuse 15 of the 20 pair
prompts, and each repeat rotates the order, so a hard prompt does not
always sit at the same turn position. The linter checks every turn
with the rule set of the style. The verdict per style compares the
slope of the mean rate series against a threshold: "growing" when the
slope is above the threshold, else "flat". `--generate` runs the
missing sessions; an interrupted run restarts an incomplete session
from turn 1. Session persistence stays on for these calls, so session
files remain under `~/.claude` after a run. Without `--generate` the
tool rescores the stored session data offline. Exit codes: 0 when
every session is complete, every verdict is flat, and no warnings
exist, 1 when a session failed or a verdict is "growing" or warnings
exist, 2 when the run cannot run or cannot be scored.

## Run data

Stored runs live under `runs/`, one directory per run, named `<date>`,
with a letter suffix when more than one run happens on one date:

```
runs/<YYYY-MM-DD>/
  provenance.json   # prompt-set hash, conditions, style hashes, linter toolchain
  answers.jsonl     # one line per answer; style null marks the unstyled answer
  report.md         # completeness, volume, environment, warnings
  fidelity.jsonl    # one line per (answer, rule set), with the pass or fail mark
  fidelity.json     # gate provenance and the per-style summary
  fidelity.md       # thresholds, marks, per-rule table, baseline comparison
  cost-probe.json   # probe provenance and the measured input overhead per style
  cost.json         # answer-length ratios and input overhead, machine-readable
  cost.md           # the token-cost report for a human
  value-raw.jsonl   # judge provenance plus one line per raw judge call
  value.json        # win/loss/tie per check and per style, machine-readable
  value.md          # the reader-value report for a human
  loss-raw.jsonl    # judge provenance plus one line per raw judge call
  loss.json         # fact and hedge survival per style, machine-readable
  loss.md           # the content-loss report for a human

runs/<YYYY-MM-DD>-drift/
  provenance.json   # like the pair runs, plus the session script per repeat
  sessions.jsonl    # one line per turn, with the session-id chain
  drift.json        # rate series, slope, and verdict per style, machine-readable
  drift.md          # the drift report for a human
```

A pair is not stored twice: it is the line for `(prompt, style)` plus
the line for `(prompt, null)`. The data is plain text in plain git: no
LFS, and no single file above about 5 MB. Keep raw transcripts out;
store only what the reports consume.
