# Evaluation harness

This directory holds the evaluation harness for the output styles in
`plugin/output-styles/`. The harness stays outside `plugin/` on purpose:
the marketplace serves only the `plugin/` directory, so installers never
receive the harness.

The harness has ten components. The first is a deterministic linter.
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
in the styled answer, the facts that only the styled answer states,
and each uncertain claim that lost its uncertainty. The seventh is a
drift report. It runs a scripted long session per style, several
times, lints every turn, and shows the violation rate over turn
positions with a verdict per style: flat or growing. The eighth is a cross-run
comparison. It reads several runs with identical conditions and
states, per style and axis, the spread across the runs: the error
bar of the harness. The ninth is a clarity ranking. It runs blind
head-to-head contests between the answers of a run, with the
unstyled answer as a competitor, and fits one Bradley-Terry
strength per competitor. The tenth is a campaign driver. It runs
several full runs under one schedule: the pair stages run one at a
time, the judge stages overlap, the value pass splits around the
loss pass, and one worker gate meters every CLI call against one
worker budget. The campaign driver also has a screening mode: one
reduced run over a fixed prompt subset, for a cheap first verdict
on a candidate style. See the tracking issue in this repository for
the other planned components.

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

## The style field

The measured styles form the field: the competitor set of every
campaign, and the reference frame for a candidate style. Each member
derives from one published writing guideline, picked for diversity of
philosophy, because the references carry human validation from outside
the harness. The members:

- **classic-concise** — The Elements of Style (Strunk, 1918): classic
  prescriptive concision, omit needless words.
- **clarity-flow** — Style: Toward Clarity and Grace (Williams):
  reader-centered clarity, actors as subjects, actions as verbs, old
  information before new.
- **developer-docs** — the Google developer documentation style guide:
  the modern industry documentation voice, for a global audience.
- **plain-language** — the Federal Plain Language Guidelines:
  government plain language, reader first.
- **technical-simplified** — ASD-STE100 Issue 9: controlled technical
  language with a restricted vocabulary and grammar.

The field is provisional until #79 p2 freezes it. Every member adds a
linear cost to every campaign, so an addition needs a reason that a
smaller field cannot serve.

## How to add a style

A style has two parts: the plugin serves the style text, and the
harness measures the style. Add both parts:

1. Add the style text as `plugin/output-styles/<style>.md`. The file
   name before `.md` is the style name.
2. Add the style to the table in the top-level `README.md`, with the
   original source and the needed disclaimers.
3. Add the rule file `rules/<style>.rules.yaml`. Every harness tool
   discovers the styles from the rule files, so a style without a rule
   file is invisible to the harness. Document the exclusions of the
   style in the header comment, as the section above describes.
4. Add a provisional threshold for the style in `rules/gate.yaml`. A
   new style has no measured rates, so calibrate the threshold against
   the first run, as the header comment of `rules/gate.yaml` describes.
   The calibration run carries a one-time asterisk, because the same
   data sets the threshold and takes the test.
5. Produce a new pair run with `uv run style-pairs`, then gate the run,
   then produce the reports. Do not extend an old run, because the
   provenance of a run records the styles of the run.
6. Run the drift sessions with `uv run style-drift --generate`.

The CLI tests need no change for a new style, because they use
synthetic rules. The linter acceptance tests are per style: a new
style adds the samples `tests/samples/<style>/{clean,dirty,traps}.md`,
its expected violations in `tests/test_lint.py`, and one designed
conflict pair in the conflict map of that file.

## How to run

The harness uses [uv](https://docs.astral.sh/uv/). From this directory:

```
uv run pytest
uv run style-lint FILE.md --rules rules/technical-simplified.rules.yaml
uv run style-pairs [--parallel N]
uv run style-gate runs/<date>
uv run style-cost runs/<date> [--probe] [--repeats N]
uv run style-value runs/<date> [--judge] [--parallel N]
uv run style-loss runs/<date> [--judge] [--parallel N]
uv run style-rank runs/<date> [--judge] [--parallel N]
uv run style-campaign [--runs N] [--budget W] [--probe-repeats N] [--screening]
uv run style-drift [--generate] [--out runs/<date>-drift]
uv run style-compare runs/<a> runs/<b> [...] [--out runs/<date>-compare]
```

The linter exits with code 1 when it finds a violation.

The pair runner reads the prompt set in `prompts/prompts.yaml` and calls
the `claude` CLI once per answer, on the account of the person who runs
it. The call is isolated as far as the CLI permits: no tools, no MCP
servers, no hooks, one turn, and no dynamic system-prompt sections.
Every call also runs in an empty temp directory outside the repository,
because the CLI loads instruction files, the memory index, and the git
state from the ancestor directories of its cwd. Thus no workspace
context enters a call, and the provenance records the workdir mode.
The probe calls, the judge calls, and the drift calls use the same
kind of directory.
The user configuration stays out of every call as well. Each tool
invocation builds one hermetic config directory, points the CLI at
that directory through `CLAUDE_CONFIG_DIR`, and passes a whitelisted
environment (`HOME`, `PATH`, `TERM`, `USER`, plus the config
variable) instead of the inherited one. Thus zero user plugins load,
and the runner asserts that every call reports exactly the declared
plugins: the harness plugin where the call passes `--plugin-dir`,
and none otherwise. A leak fails the call without a retry. The
credential has two routes: when `CLAUDE_CODE_OAUTH_TOKEN` is set
(see `claude setup-token`), the token passes through and nothing is
written; else an existing `~/.claude/.credentials.json` is copied
into the hermetic directory with mode 600 and removed with it. The
credential never lands in the run data. Without a credential, the
tool warns and proceeds, and the first live call fails with zero
tokens spent. The provenance records the config mode, the manifest
hash of the declared config inputs, the resolved absolute path of
the `claude` binary, and the names of the passed variables. The
config mode marks a comparability era: a run from before the
hermetic directory saw the user plugins, so old runs and new runs
warn in a comparison.
The generation calls run several at a time (8 by default), and
`--parallel` sets the count (1 runs one call at a time). The calls do
not interact, so the concurrency changes no condition of a run. The
answers land in completion order, and every reader of the answers
reads them by key, so the row order carries no meaning.
Every stored call row holds two times: `duration_ms` is the model
time that the CLI reports, and `wall_ms` is the wall clock of the
subprocess. The difference is the startup cost of one CLI call. The
generation rows, the probe arms, the judge rows, and the drift rows
all hold both times, and the run report, the reader-value report,
the content-loss report, and the clarity-ranking report state the
means in a call-timing section. A row from before the `wall_ms`
field reads as "not measured". The measurement changes no call
condition, so old runs stay comparable.
Every stored call row also holds four token counts: the uncached
input tokens, the cache-write input tokens, the cache-read input
tokens, and the output tokens. The counts show what the harness
itself spends, apart from what the styles cost. The run report,
the cost report, the reader-value report, the content-loss report,
the clarity-ranking report, and the drift report state the totals
of their own calls in a harness-spend section, with the cache-read
share of the input. A row from before the token fields reads as
"not measured" here as well, and this measurement also changes no
call condition, so old runs stay comparable.
The judge prompts stay as they are on purpose, after a measured
audit against issue #74: every template already puts its fixed
instructions first and the variable text last. The CLI exposes no
cache-control surface for a `-p` call, and every fixed block sits
far below the cacheable minimum of the judge models, so a
manufactured cacheable preamble would cost more than it saves. A
rubric trim would shave about 530 fixed tokens across all eleven
templates, against prompts that are more than 90 percent variable
text, so the saving is immaterial. The lenient JSON parser also
stays, because one salvaged parse saves one retry call.
An interrupted run resumes when the same invocation runs again. When
the default directory already holds a complete run, a repeat without
`--out` starts the next free letter suffix (`runs/<date>b`, then `c`,
and so on) and tells the choice, because a silent reuse of a complete
run produces no new sample. The
runner exits with code 1 when the pair set is incomplete.

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
one minimal call per arm and repeat, and takes the difference in input
context tokens between the styled call and the unstyled call of the
same repeat. Both probe arms load the plugin, so the difference
isolates the style block. `--repeats` sets the repeat count (3 by
default), and the report states the mean and the spread per style.
The report also states a weighted overhead per style: each token
count times its price ratio against one uncached input token (a
cache write costs 1.25, a cache read costs 0.1), so the unit is
uncached-token equivalents and the number holds under any absolute
price. The repeat count changes no call condition, so old runs stay
comparable, and a stored probe in the old single-call format reads
as one repeat. The probe data
lands in `cost-probe.json`, and a later `style-cost` call without
`--probe` reuses it. Exit codes: 0 when both numbers exist and no
warnings exist, 1 when warnings exist (for example, the overhead is not
measured), 2 when the run cannot be reported.

The reader-value report reads only the pairs whose styled answer
passes the gate, because rule obedience alone can produce compliant,
useless text, and this report measures whether a reader gains
anything. Three checks compare the two answers of a pair: weak-reader
comprehension (a weaker model answers quiz questions from one answer
text, and a grader marks every reply), ambiguity through paraphrase
(independent restatements of one answer text, scored by their mutual
agreement), and translation round-trip (one answer text goes to
another language and back, scored by the lexical loss). The
paraphrase check and the round-trip check build on lexical
similarity, so a shorter text can score better, because less text
exists to diverge on. The report thus states, per check and style,
the length confound: the correlation between the length ratio of a
pair (styled words over unstyled words) and the styled advantage
(the score gain of the styled arm). A negative value means that the
shorter styled answers score better. The
comprehension questions come from the shared facts of the pair. The
completeness check of the content-loss report mined these facts in
both directions, so a shared fact exists in two wordings, and the
quiz takes half of its questions from the facts of each answer. Thus
the questions probe only material that both answers contain, neither
answer sets the phrasing alone, and the score measures extraction,
not coverage. The check reads the facts from `loss-raw.jsonl`: run
`style-loss <run> --judge` before the first
`style-value <run> --judge`. Each judge tool works in its own
scratch directory, so the two tools can run at the same time on one
run. But the comprehension check reads `loss-raw.jsonl` once, at
the start, so make sure that the loss judge pass is complete first.
Each answer gets several reader
replicates. The pair outcome is the plurality over the replicate
outcomes, and the report states the replicate
agreement next to a buried-fact rate per arm (a "NOT IN TEXT" reply
to a shared fact). Every judge call sees one bare text without a
style name or an arm label, and the judge models must differ from
the writer model of the run. The harness pins each judge alias to
one exact model ID. A live judge call that resolves to a different
ID stops the pass, without a retry, because the mismatch is not
transient. `--judge` runs the live calls and
appends the raw outputs to `value-raw.jsonl`; an interrupted judge
run resumes when the same invocation runs again. The meta row of
the raw file stores one sha256 over the judge prompt templates of
the tool. A raw file from before the hash gets the hash backfilled
on the next `--judge`, because the prompts did not change across
that boundary. A stored hash that differs from the current
templates stops the resume with exit code 2, because a resumed
pass must not mix two prompt versions in one raw file. A judge call that
fails runs once more, and the retry becomes a warning, because one
transient failure must not abort a whole pass. A second failure
stops the pass. The judge calls
run several at a time (8 by default), and `--parallel` sets the
count (1 runs one call at a time). One pool spans the checks: a
call that consumes the output of an earlier call waits for that
call only, and every other call starts as soon as a worker is
free. Without `--judge`
the tool rescores the stored raw data offline. Exit codes: 0 when
the checks are scored and no warnings exist, 1 when warnings exist
(for example, a check without judge data), 2 when the run cannot be
scored.

The content-loss report also reads only the gated pairs. Two checks
measure what the rewrite loses: completeness (the judge lists the
facts of the unstyled answer, then checks each fact against the
styled answer) and hedging survival (the judge lists the uncertain
claims of the unstyled answer, then judges whether the styled answer
keeps, hardens, or drops each claim). A claim that hardens becomes a
false certainty, which is worse than a lost fact. The completeness
check also mines the reverse direction: the judge lists the facts of
the styled answer and checks each fact against the unstyled answer.
A styled fact that the unstyled answer does not state counts as an
addition, reported per pair, because material that only the rewrite
states is otherwise invisible. No judge call sees both answers of a
pair: the extracted items travel between the calls, never the source
text. The judge model must differ from the writer model of the
run, and the judge-model pin applies here as well. `--judge` runs
the live calls and appends the raw
outputs to `loss-raw.jsonl`; an interrupted judge run resumes when
the same invocation runs again, and the prompt-hash rule applies
here as well. A failed judge call retries once
here as well, with the same warning. The judge calls run several at a
time (8 by default), and `--parallel` sets the count (1 runs one
call at a time). One pool spans the checks here as well, and a
check call starts as soon as its own extraction is complete, with
no barrier between the checks. Without `--judge` the tool rescores
the stored raw data offline. The exit codes equal the exit codes of
`style-value`.

The clarity ranking also reads only the gated pairs, and the
unstyled answer joins as its own competitor under the reserved name
`unstyled`. Per prompt and per competitor pair, a blind judge sees
the two texts side by side and picks the clearer one, in both
orders, so a position preference cancels: the orders agree and the
contest is a decisive win for the picked competitor, or the orders
disagree and the contest is a split. A contest with an unusable
pick is unscored, because a single scored order would reintroduce
the position bias that the swap cancels. This tool relaxes one
harness invariant on purpose: a clarity contest is a choice, so a
judge call sees both answers of a prompt. Blindness holds through
the absence of labels: no prompt names a style or an arm, and the
position mapping lives only in the raw rows. The unstyled
competitor is ungated, but every styled competitor passed its
gate, and the report states the asymmetry. A Bradley-Terry fit
turns the contests into one strength per competitor, anchored on
the unstyled answer at 1.0, with a bootstrap interval per
strength. The fit stays dormant below 3 competitors, and a
competitor with zero wins or zero losses has no finite strength.
The report lists the strengths from the highest to the lowest, so
the order per style is explicit. The report also
states the position bias of the judge, the matchups per task type,
and the length confound: the correlation between the length ratio
of a contest and the points of the longer text. The judge model
must differ from the writer model of the run, and the judge-model
pin applies here as well. `--judge` runs the
live calls and appends the raw outputs to `rank-raw.jsonl`; an
interrupted judge run resumes when the same invocation runs again,
and the prompt-hash rule applies here as well.
A failed judge call retries once here as well, with the same
warning. The judge calls run several at a time (8 by default), and
`--parallel` sets the count (1 runs one call at a time). Without
`--judge` the tool rescores the stored raw data offline. The exit
codes equal the exit codes of `style-value`.

The drift report owns its own run directory, because it measures
sessions, not pairs. A session is 15 scripted turns in one Claude Code
session, with the style active: each turn resumes the session of the
previous turn, so the context grows. The turns reuse 15 of the 20 pair
prompts, and each repeat rotates the order, so a hard prompt does not
always sit at the same turn position. The linter checks every turn
with the rule set of the style. The rate of a turn position pools
the complete sessions: 100 times the violations at that position
over the sentences at that position. Thus a short answer weighs by
its sentence count and cannot dominate the series. The verdict per
style compares the slope of the pooled series against a per-style
threshold: "growing" when the slope is above the threshold, else
"flat". The threshold comes from a permutation null: the turn order
of each session shuffles 1000 times with a fixed seed, the pooled
slope refits per shuffle, and the threshold is the 0.95 nearest-rank
quantile of the shuffled slopes. A drift signal is thus a slope that
the shuffled data almost never produces. The report states the
quantile, the permutation count, and the seed per style.
`--slope-threshold` replaces the derived threshold with one fixed
value for every style, and the report then states both values. Few
short sessions give a coarse null, and the quantile can then equal
the largest possible slope, so the verdict needs enough complete
sessions to be sensitive. The scoring is offline, so a rescore of an
old run uses the derived threshold as well. `--generate` runs the
missing sessions; an interrupted run restarts an incomplete session
from turn 1. Session persistence stays on for these calls, because a
resumable session must persist. The session files land in the
hermetic config directory of the invocation and vanish with it; the
resume chain works because the directory lives for the whole
invocation. Without `--generate` the
tool rescores the stored session data offline. Exit codes: 0 when
every session is complete, every verdict is flat, and no warnings
exist, 1 when a session failed or a verdict is "growing" or warnings
exist, 2 when the run cannot run or cannot be scored.

The cross-run comparison reads the stored artifacts of two or more
runs and writes `compare.json` and `compare.md` into its own
directory, because the comparison belongs to no single run. Per
style and axis, the report states one value per run and the spread:
minimum, mean, maximum, and the sample standard deviation. The axes
are the headline scalars of the other reports: the styled violation
rate and the gated pairs passed, the output-token ratio, the net
wins (wins minus losses) per reader-value check, the fact and
hedge survival medians, the Bradley-Terry strength, and the net
wins against the unstyled competitor. The unstyled anchor gets no
section of its own, because its strength is 1.0 by construction. The comparison is offline and makes no
judge calls. The runs must share their conditions: the tool checks
the prompt-set hash, the style and rule hashes, the writer model,
the Claude CLI version, the workdir mode, the config mode and its
manifest hash, the judge parameters,
the resolved judge models, the judge-prompt hashes, and the
fact-mine design, and a mismatch
becomes a warning, because the reader must see how far apart the
conditions are. The binary path stays out of the check, because an
absolute path is machine-local; the CLI version is the
cross-machine invariant. A run from before the judge-prompt hash
states no hash, and that entry stays silent for it, because the
prompt text did not differ across that boundary. A missing artifact drops the axes of that artifact
for that run, and n states the run count per axis. Exit codes: 0
when no warnings exist, 1 when warnings exist, 2 when the
comparison cannot run.

### Human spot check

The judges are models, so the verdicts need a human anchor. Run
this protocol before you accept a candidate style, on the
confirmation run of that style:

1. Sort the contest keys of `rank-raw.jsonl` and draw 12 contests
   with seed 0 (for example, `random.Random(0).sample(keys, 12)`).
2. Read the two answers of each contest without the style names.
3. Record a winner or a tie per contest, before you look at the
   judge verdicts.
4. Compute the agreement rate: the contests where your record
   agrees with the judge outcome, divided by 12.
5. Write the picks and the agreement rate to `spot-check.md` in
   the run directory, and link that file in the acceptance PR.

When the agreement rate is below 0.7, do not accept the style, and
open an issue that lists the disagreements. The protocol is manual:
no tool draws the sample or computes the rate.

### Screening threshold

A screening run gives a cheap first verdict on a candidate style,
and this threshold states which verdict earns a full campaign. Read
the Bradley-Terry strengths in the `rank.md` of the screening run.
The candidate earns a full confirmation campaign when the candidate
ranks first among the styled competitors, or when its bootstrap
interval overlaps the interval of the first-ranked styled
competitor. Any other outcome rejects the candidate, without a full
campaign. A screening run accepts no style: acceptance needs the
full campaign, the cross-run comparison, and the human spot check.

### Campaign overlap

A campaign is several runs under identical conditions, produced for
the cross-run comparison. The campaign driver produces one with one
command: `style-campaign` runs N full runs (3 by default), and
`--budget` sets the total worker count across every stage (32 by
default). The cost stage probes with 3 repeats, and
`--probe-repeats` forwards a different count to `style-cost`. One
worker gate meters every CLI call of the campaign:
a call takes a permit before its subprocess starts and returns the
permit when the subprocess ends. Thus the live call total never
rises above the budget, and a stage that runs alone can use the
whole budget, because an idle permit is free for any live stage.
When calls compete, the permit goes to the stage that is earlier
in the schedule, so the critical path stays fast. The workers
column of the final table states the observed peak of live calls
per stage. The driver retries a stopped stage once, prints the wall
clock per stage at the end, and exits 0 only when every stage is
clean. An interrupted campaign resumes through `--dirs`, with the
run directories of the interrupted campaign. The first value
invocation of a run exits 1 by design, because its comprehension
check is not judged yet; the driver reports that exit code but does
not count it.

The schedule rests on four dependencies:

- The gate needs the complete pair set of its run.
- The cost report needs the complete pair set of its run.
- The judged reports need the gate marks of their run.
- Only the comprehension check of `style-value` needs the complete
  `loss-raw.jsonl` of its run. Thus the paraphrase check and the
  round-trip check run next to the loss pass, and only the
  comprehension pass follows the loss pass.

Everything else runs at the same time without conflict. Each tool
works in its own scratch directory, and each judge pass appends to
its own raw file, so the judge tools of one run can run together,
and the tools of two different runs can too. The two value
invocations of one run are the one exception: both append to
`value-raw.jsonl`, so the comprehension pass also waits for the
paraphrase and round-trip pass. The schedule of one run:

```
pairs ─→ gate ─→ loss ───────────────────→ value (comprehension)
              ├─→ value (paraphrase, round-trip) ─↗
              ├─→ rank
              └─→ cost
```

The next run starts its `pairs` stage when the previous `pairs`
stage is complete, the judge stages of the runs overlap without
constraint, and the comparison runs last, over the complete runs.

The driver enforces two limits by construction, and the limits stay
the rule for a manual run of the tools. First, do not run two
`style-pairs` invocations at the same time. Without `--out`, both
invocations pick the same run directory, because the picker takes
the first incomplete run, and the two processes then write
duplicate rows and spend duplicate calls. Second, the concurrent
CLI calls add up across the live tools: each tool holds 8 workers
by default, so three live tools produce 24 concurrent calls, and
workers above the account throughput add latency, not throughput.
When the account limit rejects calls, a judge call that fails twice
stops its pass, so lower the worker count. An interrupted pass
resumes, so a stop loses no data.

`style-campaign --screening` screens one candidate style: one run
instead of three, over a fixed prompt subset, with every stage of a
full run. The subset draws 2 prompts per task type from the full
prompt file, sorted and with seed 0, so every screening run uses
the same 8 of the 20 prompts. By design, the generation calls are
about 13% of a full campaign, and the judge calls are about 40% of
one full run. These fractions are design numbers until a
measurement against the baseline campaign replaces them. The run
lands under its own `-screening` directory family, the provenance
carries a screening block, and every report of the run starts with
a screening note, because the error bars of a screening run are
wider than the error bars of a full run. `style-compare` rejects a
comparison that mixes a screening run with a full run. A resume
through `--dirs` needs `--screening` again, and the pair runner
rejects a directory whose mode differs from the flag.

## Run data

Stored runs live under `runs/`, one directory per run, named `<date>`,
with a letter suffix when more than one run happens on one date. The
pair runner picks the suffix on a same-day repeat:

```
runs/<YYYY-MM-DD>/
  provenance.json   # prompt-set hash, conditions (workdir and config modes), style hashes, linter toolchain
  answers.jsonl     # one line per answer; style null marks the unstyled answer
  report.md         # completeness, volume, call timing, environment, warnings
  fidelity.jsonl    # one line per (answer, rule set), with the pass or fail mark
  fidelity.json     # gate provenance and the per-style summary
  fidelity.md       # thresholds, marks, per-rule table, baseline comparison
  cost-probe.json   # probe provenance and the measured input overhead per style
  cost.json         # answer-length ratios and input overhead, machine-readable
  cost.md           # the token-cost report for a human
  value-raw.jsonl   # judge provenance plus one line per raw judge call
  value.json        # win/loss/tie and length confound per check and style
  value.md          # the reader-value report for a human
  loss-raw.jsonl    # judge provenance plus one line per raw judge call
  loss.json         # fact and hedge survival per style, machine-readable
  loss.md           # the content-loss report for a human
  rank-raw.jsonl    # judge provenance plus one line per raw judge call
  rank.json         # matchups, win matrix, and strengths, machine-readable
  rank.md           # the clarity-ranking report for a human
  spot-check.md     # the human spot-check record and the agreement rate (manual)

runs/<YYYY-MM-DD>-screening/
  # the same files as a pair run, over the fixed prompt subset; the
  # provenance carries the screening block, and every report starts
  # with the screening note

runs/<YYYY-MM-DD>-drift/
  provenance.json   # like the pair runs, plus the session script per repeat
  sessions.jsonl    # one line per turn, with the session-id chain
  drift.json        # pooled rate series, slope, derived threshold, and verdict per style
  drift.md          # the drift report for a human

runs/<YYYY-MM-DD>-compare/
  compare.json      # the spread per style and axis across runs, machine-readable
  compare.md        # the cross-run comparison for a human
```

A pair is not stored twice: it is the line for `(prompt, style)` plus
the line for `(prompt, null)`. The data is plain text in plain git: no
LFS, and no single file above about 5 MB. Keep raw transcripts out;
store only what the reports consume.

## License

The Apache License 2.0 covers this directory. See [LICENSE](LICENSE). One
exception exists: the Zero-Clause BSD license of the repository root covers
the rule files in `rules/`, because a rule file pairs with a style text, and
a fork of a style needs the matched rule file. The License section of the
top-level `README.md` states the full split.

## Keep this document current

This document is the only description of the harness workflow. A change
to the harness must update this document in the same PR. The sections
that go stale are: the component list in the introduction, "How to add
a style", "How to run", and "Run data". No automated check makes sure that
the document matches the code, so the reviewer must check it.
