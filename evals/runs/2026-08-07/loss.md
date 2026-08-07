# Content-loss report

The checks measure what a rewrite loses relative to the unstyled
answer of the same prompt, per gated pair. The judge extracts the
facts and the uncertain claims from the unstyled answer, then
checks each item against the styled answer. No judge call sees
both answers of a pair: the extracted items travel between the
calls, never the source text. No prompt names a style or an arm,
and the judge model differs from the writer of the answers.

The unstyled answer is the reference, not a gold standard. A fact
that the unstyled answer omits is invisible to these checks, and
survival measures loss against that baseline, not correctness.

Judge: opus. Judged on 2026-08-07T08:39:11+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### clarity-flow

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 21 | 0 | 0.0 | 9 | 9 |
| code-review-02 | 23 | 17 | 0.739 | 24 | 4 |
| code-review-03 | 21 | 10 | 0.476 | 17 | 5 |
| code-review-04 | 22 | 17 | 0.773 | 16 | 1 |
| code-review-05 | 31 | 22 | 0.71 | 30 | 3 |
| code-review-06 | 38 | 23 | 0.605 | 26 | 8 |
| code-review-07 | 37 | 21 | 0.568 | 38 | 9 |
| code-review-08 | 36 | 30 | 0.833 | 39 | 10 |
| debugging-01 | 7 | 7 | 1.0 | 8 | 0 |
| debugging-02 | 9 | 8 | 0.889 | 9 | 2 |
| debugging-03 | 9 | 9 | 1.0 | 15 | 0 |
| debugging-04 | 14 | 11 | 0.786 | 12 | 1 |
| debugging-05 | 16 | 14 | 0.875 | 14 | 1 |
| debugging-06 | 40 | 7 | 0.175 | 6 | 1 |
| debugging-07 | 29 | 19 | 0.655 | 30 | 7 |
| debugging-08 | 5 | 0 | 0.0 | 33 | 33 |
| explanation-01 | 32 | 21 | 0.656 | 22 | 2 |
| explanation-02 | 27 | 24 | 0.889 | 25 | 5 |
| explanation-03 | 32 | 18 | 0.562 | 19 | 3 |
| explanation-04 | 39 | 26 | 0.667 | 21 | 1 |
| explanation-05 | 23 | 17 | 0.739 | 13 | 1 |
| explanation-06 | 25 | 22 | 0.88 | 23 | 4 |
| explanation-07 | 27 | 20 | 0.741 | 31 | 9 |
| explanation-08 | 13 | 10 | 0.769 | 21 | 10 |
| summarization-01 | 5 | 3 | 0.6 | 5 | 1 |
| summarization-02 | 15 | 12 | 0.8 | 17 | 3 |
| summarization-03 | 14 | 14 | 1.0 | 13 | 0 |
| summarization-04 | 13 | 13 | 1.0 | 14 | 3 |
| summarization-05 | 11 | 9 | 0.818 | 9 | 0 |
| summarization-06 | 14 | 14 | 1.0 | 14 | 0 |
| summarization-07 | 18 | 14 | 0.778 | 16 | 0 |
| summarization-08 | 19 | 19 | 1.0 | 19 | 1 |

Median fraction: 0.771 over 32 scored pairs.

Median additions: 2.5 over 32 scored pairs.

Lost facts:

- code-review-01: A mutable default argument like `roles=[]` creates a single list object that persists across calls.
- code-review-01: Each call to `add_user` without an explicit `roles` argument appends "member" to the same shared list.
- code-review-01: The mutable default argument causes state to leak between calls.
- code-review-01: A bare `except:` catches everything, including `KeyboardInterrupt` and `SystemExit`.
- code-review-01: A bare `except:` silently swallows real bugs, such as `db` being `None`, a malformed `name`, or a network error.
- code-review-01: With the bare except, the function returns `False` with no information about what went wrong.
- code-review-01: The `db` parameter defaults to `None` with no guard against it.
- code-review-01: If `db` isn't passed, `db.insert(...)` raises `AttributeError`.
- code-review-01: That `AttributeError` is silently swallowed by the bare except and returns `False` as if it were a normal failure.
- code-review-01: `roles.append("member")` mutates the list the caller passed in.
- code-review-01: Mutating the caller's list is a surprising side effect if the caller reuses that list elsewhere.
- code-review-01: The function performs no validation of `name`.
- code-review-01: An empty string, `None`, or a wrong type for `name` all pass through unchecked.
- code-review-01: If `roles` already contains "member", it gets added again because there is no deduplication.
- code-review-01: The `True`/`False` return value does not distinguish between "insert failed," "db not configured," and "bad input."
- code-review-01: Conflating failure modes in the return value makes the function hard to use and debug.
- code-review-01: The suggested fix raises `ValueError("db is required")` when `db` is `None`.
- code-review-01: The suggested fix uses `roles=None` as the default and assigns an empty list inside the function.
- code-review-01: The suggested fix builds a new list with `roles + ["member"]` instead of mutating the caller's list.
- code-review-01: The suggested fix only adds "member" when it is not already in `roles`.
- code-review-01: Exceptions should be allowed to propagate, or specific exception types should be caught, rather than using a bare `except`.
- code-review-02: Mixing `async`/`await` with `.then()` inconsistently defeats the purpose of the promise chain.
- code-review-02: The inconsistent mixing of `async` and `.then()` makes the race condition bug easy to miss.
- code-review-02: Network failures or non-JSON responses will produce an unhandled promise rejection.
- code-review-02: The code has no null or shape validation on the fetched data.
- code-review-02: There is no check that `data` has a `name` property.
- code-review-02: The fixed version throws an `Error` with the message `Failed to load user ${userId}: ${res.status}` when `res.ok` is false.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: A customer name containing a single quote, such as `O'Brien`, breaks the query syntactically.
- code-review-03: The single-quote bug causes errors even without malicious intent.
- code-review-03: If columns are added or reordered, callers relying on positional access to `fetchall()` results will silently break.
- code-review-03: The code does not validate that `status` is one of the expected enum values such as `'pending'` or `'shipped'`.
- code-review-03: The query has no LIMIT clause.
- code-review-03: Without a LIMIT, the query could return unbounded rows for a common customer name.
- code-review-03: Returning unbounded rows can cause memory and performance issues.
- code-review-03: psycopg2 and MySQLdb use `%s` as the placeholder.
- code-review-03: With parameterized queries, the driver handles escaping.
- code-review-03: Using parameterized queries fixes both the injection risk and the quote-breaking bug in one change.
- code-review-04: The `reset` method is not atomic, though to a lesser extent than `increment`.
- code-review-04: Dropping an increment this way is called a lost update.
- code-review-04: `+=` on an `int` is still a read-modify-write operation at the bytecode level.
- code-review-04: In CPython, `+=` narrows the race window but does not eliminate it.
- code-review-04: An increment can be lost immediately after a reset.
- code-review-05: If the script is called with no argument, $1 is empty and BACKUP_DIR is empty.
- code-review-05: With an empty BACKUP_DIR, `cd $BACKUP_DIR` becomes a plain `cd`, which changes to $HOME.
- code-review-05: After cd'ing to $HOME, the script would run `rm -rf *.tmp` in the user's home directory.
- code-review-05: Because globbing is not disabled, if no .tmp files exist the literal string `*.tmp` is passed to `rm -rf`.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` causes a harmless 'no such file' error.
- code-review-05: Running gzip on a file that already has a .gz counterpart prompts for overwrite confirmation.
- code-review-05: In a non-interactive or cron context, the gzip overwrite prompt can hang or silently fail depending on gzip's behavior.
- code-review-05: `gzip -f` should be used explicitly to avoid the overwrite prompt.
- code-review-05: In the suggested fix, `[ -e "$f" ] || continue` handles the case where the glob matches nothing.
- code-review-06: There are no relevant saved memory entries or preferences for this task.
- code-review-06: The None-as-delete behavior is an undocumented API decision.
- code-review-06: Overwriting when only the override value is a dict is arguably correct behavior.
- code-review-06: The code has no cycle protection.
- code-review-06: Circular references in `base` or `override` cause infinite recursion.
- code-review-06: The lack of cycle protection is low priority and almost certainly not deliberate.
- code-review-06: Some merge utilities do merge lists rather than replacing them.
- code-review-06: Merging conventions for settings vary widely between codebases.
- code-review-06: An empty dict in `override`, such as `{"key": {}}`, results in `merge_settings(merged[key], {})` returning `merged[key]` unchanged.
- code-review-06: An empty dict override is a no-op rather than a 'clear this sub-dict' operation.
- code-review-06: The function lacks a name/docstring stating its 'settings' semantics.
- code-review-06: Nothing in the code states whether it implements JSON-Merge-Patch-like semantics or bespoke semantics.
- code-review-06: The author probably consciously implemented the RFC 7396 pattern but did not document or fully finish it.
- code-review-06: The type-check bug (#3) is the most urgent fix because it can crash in production.
- code-review-06: The shallow-copy aliasing bug (#1) is the most dangerous latent bug because it can silently corrupt `base`.
- code-review-07: The silent-null behavior could be an intentional 'fail soft' convention inherited from the original library.
- code-review-07: An undocumented fail-soft convention is dangerous.
- code-review-07: Immediately retrying a struggling server on 5xx is the worse case to leave without backoff.
- code-review-07: The differing backoff treatment could be deliberate, treating 5xx as probably transient and 429 as requiring a cooldown.
- code-review-07: The delay computed on the last loop iteration is wasted because the loop exits immediately afterward with no further attempt.
- code-review-07: The backoff is linear rather than exponential, despite appearing intended to ramp up.
- code-review-07: The backoff is unbounded.
- code-review-07: The semantics of the `attempts` parameter are ambiguous.
- code-review-07: `attempts = 3` means 3 total calls, not 3 retries following an initial attempt.
- code-review-07: Some callers may assume `attempts` means retries-after-failure and therefore receive one fewer call than expected.
- code-review-07: Nobody knows the history of this code.
- code-review-07: If `attempts` is less than or equal to 0, the loop body never runs and `fn` is never called.
- code-review-07: If `attempts` is less than or equal to 0, the wrapped function silently returns undefined.
- code-review-07: The `attempts <= 0` case is probably not exercised by real callers but is a landmine if someone passes a dynamic value.
- code-review-07: 5xx retrying without backoff and `attempts` meaning total calls are ambiguous as to whether they were deliberate.
- code-review-07: The null/undefined inconsistency, the wasted last-iteration delay, and non-HTTP errors being treated like a legitimate empty result are almost certainly accidental.
- code-review-08: Unconditional deletion of in-progress `.part`/`tmp-` files is the most dangerous issue because it causes data loss rather than mere cleanup.
- code-review-08: The 500-item cap and the `removed` counter conflate two unrelated deletion policies.
- code-review-08: The `removed` counter is incremented by both deletion branches.
- code-review-08: If enough tmp/part files are deleted early in the loop, the cap blocks legitimate old-file cleanup for the rest of the run.
- code-review-08: Misconfigured `ROOT` or clock skew could make every file look old.
- code-review-08: The unconditional `.part`/`tmp-` deletion and the unhandled directory crash are the two issues most likely to cause real incidents.
- debugging-02: Because `setInterval` calls the callback as a plain function, `this` inside a regular function callback is the global object (`window`/`globalThis`), not the `Timer` instance.
- debugging-04: The byte 0xc3 likely begins an accented character such as é, à, or ü.
- debugging-04: Any byte greater than or equal to 0x80 raises `UnicodeDecodeError` under the `ascii` codec.
- debugging-04: If the user controls the input format, changing the hardcoded `"ascii"` to `"utf-8"` is almost certainly the real fix.
- debugging-05: A prior call can come from another test, from setup code, or from the same test running more than once via a fixture.
- debugging-05: In the fixed code, `make_post` has signature `make_post(title, tags=None)` and sets `tags = list(DEFAULT_TAGS)` when `tags is None`.
- debugging-06: The failing batch number varies between occurrences.
- debugging-06: Scheduled analytics queries such as hourly or nightly rollups can spike concurrent connection usage.
- debugging-06: The varying batch number is consistent with a cause that depends on wall-clock timing rather than job progress.
- debugging-06: Export, analytics, and other consumers may exceed pool_size plus max_overflow only under specific conditions.
- debugging-06: A slow analytics query holding a connection longer than usual is one such condition.
- debugging-06: A connection leak in one of the services could be the cause.
- debugging-06: A code path that acquires a connection but fails to release it on error causes leaks.
- debugging-06: Unreleased connections on error are common with unhandled exceptions in analytics jobs.
- debugging-06: A connection leak slowly shrinks the effective pool until it is exhausted.
- debugging-06: A leak tied to a rare analytics query or edge-case dataset fits a once-a-week failure cadence.
- debugging-06: A long-running or blocking query holding connections could be the cause.
- debugging-06: A lock wait or large analytics query holding a transaction open causes other connections to queue behind it.
- debugging-06: The database's own max_connections limit may be the actual bottleneck rather than the application pool.
- debugging-06: If the database connection limit is the bottleneck, both services' pools could report healthy while failing to obtain a physical connection.
- debugging-06: Correlating failure timestamps with the analytics job schedule and logs can narrow down the cause.
- debugging-06: Failures clustering around analytics batch windows or its cron schedule would be a strong signal.
- debugging-06: One failure occurred at 02:14:07 on 2026-07-29.
- debugging-06: Cross-referencing analytics logs at 02:14:07 on 2026-07-29 would confirm or rule out the analytics-overlap hypothesis.
- debugging-06: Pool metrics to export include checked-out count, wait queue length, and max pool size.
- debugging-06: Pool metrics should be sampled every few seconds and sent to monitoring.
- debugging-06: With pool metrics in place, the next failure would reveal exactly what was holding connections.
- debugging-06: Logging connection checkout and checkin with a query tag or caller identity reveals who owned the pool at exhaustion time.
- debugging-06: Caller-identity logging for connections is cheap to add and highly diagnostic.
- debugging-06: Checking DB-side pg_stat_activity history or logging can distinguish a real database connection limit from an app-level pool limit.
- debugging-06: Pool usage trending upward over days indicates a leak.
- debugging-06: A sudden spike in pool usage indicates contention.
- debugging-06: Increasing pool size or adding wait-timeout backoff with jitter is a mitigation, not a root-cause fix.
- debugging-06: Such mitigation reduces failure frequency and buys time to instrument.
- debugging-06: Isolating the export job to its own pool or connection budget is possible if the database can support it.
- debugging-06: Separate connection pools per service is often the long-term fix for two services sharing one pool.
- debugging-06: The failure is currently unreproducible.
- debugging-06: Instrumentation with pool metrics and caller tagging is the fastest path to an answer.
- debugging-06: The log lines surrounding the failure are missing, so further log analysis is unlikely to reveal what else was happening.
- debugging-07: No relevant memory was found for this project or codebase.
- debugging-07: The working directory is fresh with no prior context on this codebase.
- debugging-07: A digest query filtering broadly rather than by a seeded-test-owned ID can pick up rows belonging to another test.
- debugging-07: If the seed and the digest read use different DB connections or transactions and the isolation level is not read-committed, the read can observe only 2 of the 3 committed rows.
- debugging-07: If failures stop at single-worker execution, that confirms the issue is parallel-worker-related shared state rather than a pure timing bug in the code under test.
- debugging-07: A single test database shared across workers is the prime suspect for the flake.
- debugging-07: A consistently missing last-inserted event points to a race, while a randomly missing event points to cross-test contamination.
- debugging-07: Inspecting the digest query for LIMIT, missing ORDER BY, or time-window/status filters is a five-minute code read.
- debugging-07: Inspecting the digest query can immediately confirm or eliminate the ordering/LIMIT and time-window hypotheses.
- debugging-07: Checking DB fixture isolation and the digest query's filtering logic are both quick to inspect and would explain the intermittent under-count without reproducing the failure.
- debugging-08: The speaker intends to check whether actual code exists to ground the discussion in.
- debugging-08: The Bash tool is invoked.
- debugging-08: The command executed is `ls -la /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac`.
- debugging-08: The path /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac is the target of the listing command.
- debugging-08: The stated description of the command is that it lists working directory contents.
- explanation-01: A hash map uses a hash function to turn a key into an array index called a bucket.
- explanation-01: There are far more possible keys than buckets in a hash map.
- explanation-01: A hash map that does not handle collisions will overwrite or lose data.
- explanation-01: The collection in a separate chaining bucket is usually a linked list, and sometimes a tree.
- explanation-01: Insert in separate chaining hashes the key and appends to the bucket's list, first checking if the key already exists in order to update rather than duplicate.
- explanation-01: Quadratic probing tries index + 1², index + 2², index + 3², and so on.
- explanation-01: Double hashing uses a second hash function to decide the step size.
- explanation-01: Deletion in chaining is simple because the entry is just removed from the list.
- explanation-01: Chaining's worst case is O(n) per bucket if the hash function is bad.
- explanation-01: Clustering in open addressing can cause long probe sequences.
- explanation-01: Open addressing tends to win on raw performance for small, primitive keys such as integers and short strings.
- explanation-02: A document editor with occasional concurrent edits is an example workload suited to optimistic locking.
- explanation-02: Optimistic locking avoids holding locks during slow operations such as user think-time between read and write.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-03: A network path might be a fast local link or a congested trans-continental route through routers with limited buffer space.
- explanation-03: This phenomenon is called congestion collapse.
- explanation-03: Congestion collapse was a real problem on the early internet in the late 1980s.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The initial cwnd was historically 1 segment.
- explanation-03: The initial cwnd is now typically 10 segments per RFC 6928.
- explanation-03: Every time the sender receives an ACK confirming data was delivered, it increases cwnd.
- explanation-03: cwnd increases roughly by one segment per ACK during slow start.
- explanation-03: Congestion avoidance growth is typically additive, at +1 segment per RTT.
- explanation-03: Exponential growth is efficient because linear growth from a small starting point could take a very long time to ramp up to the available bandwidth on a fast link.
- explanation-03: Linear growth from a small starting point would waste capacity on a fast link.
- explanation-03: Exponential growth means slow start will overshoot and cause a loss event fairly soon after starting.
- explanation-03: Overshooting and causing a loss event during slow start is expected and intentional.
- explanation-03: Moving to congestion avoidance prevents TCP from repeatedly hitting the capacity ceiling at full speed.
- explanation-04: A process has its own memory address space, file descriptors, and OS resources.
- explanation-04: All threads in a process share the same memory address space, heap, and file descriptors.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Only one thread holds the GIL at a time.
- explanation-04: Each process gets its own interpreter and its own GIL.
- explanation-04: Running a task that might crash, leak memory, or hang in a separate process contains the damage.
- explanation-04: Processes have separate memory spaces enforced by the OS via virtual memory and the MMU.
- explanation-04: Browsers run tabs and renderers in separate processes rather than threads for sandboxing.
- explanation-04: Processes can be distributed across machines.
- explanation-04: Processes can run under different resource limits such as cgroups and ulimits.
- explanation-04: Process-based architecture maps naturally to microservices and worker-pool architectures.
- explanation-04: Threads generally win when tasks are I/O-bound, such as waiting on network or disk.
- explanation-04: For I/O-bound tasks, the GIL or lock is not the bottleneck.
- explanation-05: Global variables, active stack frames, and static fields are examples of garbage collection roots.
- explanation-05: Accumulated unreachable-but-retained objects cause memory usage to grow unbounded over time.
- explanation-05: A leak in a garbage-collected language is not about forgetting to call free().
- explanation-05: Listener leaks are especially common with observer patterns, DOM event listeners, and subscriptions to long-lived singletons.
- explanation-05: Closures capturing more than intended are a frequent cause of memory leaks.
- explanation-05: Thread-locals that outlive their thread pool's task lifecycle are a frequent cause of memory leaks.
- explanation-06: An APM tool can quickly show where time is going.
- explanation-06: A rough estimate of the read/write ratio can be derived from logs or query counts.
- explanation-06: Database bottlenecks can be caused by missing indexes, full table scans, or over-fetching data.
- explanation-07: A single well-tuned Postgres instance can comfortably handle multi-terabyte databases with proper indexing, vacuuming, and hardware.
- explanation-07: The real constraint on a database may be disk size, write throughput (IOPS), CPU/query load, or connection count.
- explanation-07: Cheaper alternatives to sharding include indexing, native Postgres table partitioning, vertical scaling, read replicas, connection pooling, and archiving old data.
- explanation-07: These cheaper alternatives often provide 10-50x headroom before sharding is needed.
- explanation-07: Locking in a shard key before understanding real access patterns is the number one cause of painful re-sharding later.
- explanation-07: Foreign keys do not work across shards, and distributed transactions are required.
- explanation-07: Monitoring should cover disk growth, query latency percentiles, and connection saturation.
- explanation-08: The actual benefit depends on how hot the code path is.
- explanation-08: Migrating to a binary format touches the whole API surface.
- explanation-08: Schemas, client compatibility, and debugging tooling all become more expensive with binary formats.
- summarization-01: Each button's tooltip shows the button's keyboard shortcut.
- summarization-01: The app now starts up roughly 40% faster.
- summarization-02: Staging intentionally uses smaller connection pools than production.
- summarization-02: The pool size reduction caused connection pool exhaustion.
- summarization-02: The configuration review checklist does not check other environment-sensitive settings.
- summarization-05: Ben is assigned to prepare the runbook for migration night.
- summarization-05: A migration night is planned.
- summarization-07: No relevant memory was found for this task.
- summarization-07: The task is a self-contained summarization task.
- summarization-07: A new request batcher was tested against the current request batcher.
- summarization-07: The test ran for six hours.

Added facts (styled only):

- code-review-01: The tool invoked is bash.
- code-review-01: The command runs `cat` on the file /var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-config-pairs-7y1ab910/projects/-private-var-folders-tt-jh9lk8gs6-sfn5fhz4rp7pch0000gn-T-style-pairs-370xicac/memory/MEMORY.md
- code-review-01: The command redirects stderr to /dev/null with 2>/dev/null.
- code-review-01: The command falls back to echoing 'no memory file' if the cat fails.
- code-review-01: The command's stated description is 'Check memory index for relevant context'.
- code-review-01: The targeted file is named MEMORY.md.
- code-review-01: The targeted file resides in a directory named 'memory'.
- code-review-01: The memory directory path referenced is under a temporary folder named style-config-pairs-7y1ab910.
- code-review-01: MEMORY.md is described as a memory index.
- code-review-02: Without error handling, failures surface as confusing downstream errors rather than a clear one.
- code-review-02: The promise chain currently has no return value.
- code-review-02: In the fixed version the function returns a plain string.
- code-review-02: The corrected version throws `new Error(`Failed to load profile: ${res.status}`)` when `res.ok` is false.
- code-review-03: Passing `status = "' OR '1'='1"` causes the query to return every row.
- code-review-03: The code has two issues besides the SQL injection.
- code-review-03: The function has no handling for `cursor.execute` failing.
- code-review-03: `cursor.execute` can fail due to a bad connection or a locked table.
- code-review-03: A try/except is worth adding unless callers already handle exceptions from this layer.
- code-review-04: CPython's GIL makes each bytecode operation atomic.
- code-review-05: The worst problem is that a failed `cd` leaves the script deleting files in the wrong directory.
- code-review-05: `$1` is unquoted in the script.
- code-review-05: If no `.log` files exist, `gzip` fails on a nonexistent file named `*.log`.
- code-review-06: Nested dicts and lists that are not touched by the merge remain shared by reference with the original `base` or `override` objects.
- code-review-06: A brand-new nested dict introduced by `override` is also shared by reference.
- code-review-06: The reference-sharing bug is easy to miss because the recursive case appears to produce fresh dicts while the non-recursive cases do not.
- code-review-06: `merge_settings` does not validate that `base` and `override` are dicts.
- code-review-06: Missing input validation causes failures to surface as bare `AttributeError` or `TypeError` deep in the recursion, far from the triggering call.
- code-review-06: `merge_settings` has unbounded recursion depth, so deeply nested settings could hit Python's recursion limit.
- code-review-06: The recursion limit issue is minor and probably not a practical concern for typical settings structures.
- code-review-06: The two 'likely intentional' items are the ones the author would confirm with stakeholders before changing the code.
- code-review-07: The helper hides failures more than it retries them.
- code-review-07: Five problems stand out in the helper, plus one likely bug in the control flow.
- code-review-07: The delay was almost certainly meant to be `1000 * (i + 1)`.
- code-review-07: The narrow focus on `err.status` (429 and 5xx) suggests the helper was written specifically for an HTTP client.
- code-review-07: The helper intentionally treats 429 and 5xx as the only retryable cases.
- code-review-07: Scoping retries to 429 and 5xx is not unreasonable.
- code-review-07: The two defects should be fixed before trusting the helper in new call sites.
- code-review-07: Unseen callers may already depend on the current buggy behavior.
- code-review-07: Changing the behavior requires first looking at who calls the function.
- code-review-08: os.remove and os.path.getmtime can raise FileNotFoundError, PermissionError, or IsADirectoryError.
- code-review-08: A broken symlink between listing and acting raises an error.
- code-review-08: clean() is never called in the file.
- code-review-08: Running the file as written does nothing.
- code-review-08: The scheduler should be confirmed to import the module and call clean() directly rather than expecting a __main__ guard.
- code-review-08: If the cap's asymmetry between junk cleanup and aged-file cleanup is intentional, it should be documented; otherwise it is a bug.
- code-review-08: The cap does not sort by mtime.
- code-review-08: When a run hits the 500 limit, which files get skipped depends on whatever order os.listdir returns.
- code-review-08: Files skipped at the cap are not selected oldest-first.
- code-review-08: If the backlog regularly exceeds 500 per run, some files could stay indefinitely rather than eventually clearing.
- debugging-02: `setInterval` invokes a regular `function` callback with `this` set to `undefined`.
- debugging-02: Class bodies run in strict mode.
- debugging-04: The file contains a non-ASCII byte with value 0xc3 at position 512.
- debugging-05: In the fixed version, `tags = list(tags) if tags is not None else ["draft"]` produces a new list per call.
- debugging-06: The incident was not caused by a database outage.
- debugging-07: Four workers compete for CPU and DB connections.
- debugging-07: Connection pool exhaustion is a plausible cause.
- debugging-07: Four workers can starve a small DB connection pool.
- debugging-07: Pool starvation can cause a write to retry, queue, or silently use a stale read connection.
- debugging-07: The seed/digest code path can be grepped for async elements such as background jobs, queues, caches with TTL, or ORM sessions not flushed or committed synchronously.
- debugging-07: A shared database across xdist workers is an isolation leak independent of timing.
- debugging-07: Adding such diagnostic logging is cheap to add and easy to remove once a repro exists.
- debugging-08: Two independent memory leaks, rather than one, best explain the observed pattern.
- debugging-08: One leak is a per-webhook-request leak.
- debugging-08: Memory growth tracks campaign traffic.
- debugging-08: Memory usage never drains overnight.
- debugging-08: Something tied to request handling registers per request and outlives the request.
- debugging-08: A leaking per-request object could be a listener, thread-local, callback, or promise chain.
- debugging-08: Heap growth rate can be plotted against webhook QPS across several weeks to test the per-request hypothesis.
- debugging-08: Linear tracking between heap growth rate and webhook QPS supports a per-request leak.
- debugging-08: Taking two heap histograms an hour apart on a busy instance and diffing them identifies the class whose count grows with traffic.
- debugging-08: `jmap -histo` is one way to capture a heap histogram.
- debugging-08: The second leak is traffic-independent.
- debugging-08: The canary instance receives no webhooks.
- debugging-08: The canary instance's memory still grows despite receiving no webhooks.
- debugging-08: A second leak source runs regardless of request volume.
- debugging-08: The traffic-independent leak is likely caused by scheduled or background work.
- debugging-08: Timers or cron jobs that re-register listeners on each run are a possible traffic-independent leak source.
- debugging-08: Unbounded metric label cardinality is a possible traffic-independent leak source.
- debugging-08: A connection pool that never shrinks is a possible traffic-independent leak source.
- debugging-08: Thread accumulation is a possible traffic-independent leak source.
- debugging-08: Off-heap buffers are a possible leak source and are not covered by the heap bound.
- debugging-08: Profiling the canary alone over several hours can isolate the traffic-independent leak.
- debugging-08: Thread count, old-gen occupancy after full GCs in GC logs, and metrics/registry collection sizes are the metrics to watch on the canary.
- debugging-08: The cache is a secondary suspect rather than the main one.
- debugging-08: The cache's bound has not changed.
- debugging-08: The cache bound may be on entry count rather than bytes.
- debugging-08: If average entry size grew as product payloads got richer, a fixed entry-count bound no longer caps memory.
- debugging-08: Cache eviction may not actually free the evicted object graph.
- debugging-08: Taking a heap dump and tracing GC roots on evicted-cache-entry classes reveals whether a listener or index still holds a reference.
- debugging-08: The possibility that the pattern is delayed GC rather than a leak should be ruled out.
- debugging-08: Triggering or waiting for a full GC during a quiet night and checking whether old-gen occupancy drops tests the delayed-GC explanation.
- debugging-08: Usage never returns to baseline even overnight.
- debugging-08: The fact that usage never returns to baseline overnight probably already rules out delayed GC.
- debugging-08: Confirming a full-GC drop rules out GC scheduling as an explanation before hunting retained objects.
- explanation-01: Most general-purpose hash maps use chaining for simplicity.
- explanation-01: Rust's HashMap uses open addressing.
- explanation-02: In the optimistic locking example, an e-commerce product table has a `version` column.
- explanation-02: In the example, two admins load the same product to edit its price.
- explanation-02: The application detects the conflict and asks the second admin to reload and retry.
- explanation-02: Web apps and REST APIs are examples of workloads suited to optimistic locking.
- explanation-02: In the pessimistic locking example, a bank transfer runs `SELECT * FROM accounts WHERE id = ? FOR UPDATE` on both the sender and receiver accounts before debiting and crediting.
- explanation-03: Overwhelming a router buffer causes a burst of dropped packets and a slow recovery.
- explanation-03: The receiver-advertised window acts as a ceiling on the congestion window.
- explanation-03: Slow start is called 'slow' only in comparison to sending all data at once, and it actually ramps up quickly.
- explanation-04: A GUI updating shared state is an example of a workload suited to threads.
- explanation-05: A UI component subscribing to a global event bus is an example of one object registering a listener on another.
- explanation-06: Adding a cache before profiling can hide the real problem instead of fixing it.
- explanation-06: A cache does nothing for slowness caused by lock contention.
- explanation-06: Skipping straight to a cache is a common trap.
- explanation-06: Adding a cache feels like progress.
- explanation-07: Growth rate matters more than current size in deciding whether to shard.
- explanation-07: 200 GB with modest, linear growth can be handled by vertical scaling for years.
- explanation-07: A database doubling every few months changes the sharding calculus quickly.
- explanation-07: Cheaper alternatives to sharding for storage limits include bigger disks, archiving cold data, and columnar compression.
- explanation-07: Someone must own sharding's operational burden indefinitely.
- explanation-07: A low-cardinality or skewed shard key creates hot shards.
- explanation-07: Hot shards recreate the bottleneck that sharding was meant to avoid.
- explanation-07: The payoff of sharding, headroom for growth, may not be needed for years.
- explanation-07: Concrete triggers should be set for when to shard, such as write IOPS exceeding a threshold or storage crossing 1.5 TB.
- explanation-08: Two unmeasured factors decide the outcome.
- explanation-08: If JSON encoding/decoding is 5% of request latency, a 10x faster parser shaves off only about 4.5% of overall latency.
- explanation-08: A ~4.5% overall latency reduction is barely noticeable.
- explanation-08: This tradeoff is an instance of Amdahl's law.
- explanation-08: You cannot speed up a step that isn't the bottleneck.
- explanation-08: Protobuf, msgpack, and Avro are binary formats.
- explanation-08: Binary formats typically produce payloads 20-50% smaller than JSON.
- explanation-08: Binary format parsers commonly run 2-10x faster than JSON parsers on CPU-bound benchmarks.
- explanation-08: Those speed and size figures come from isolated microbenchmarks rather than a specific service.
- explanation-08: If payloads are already small or clients are on fast internal networks, the payload size reduction won't matter.
- summarization-01: The app starts up to 40% faster.
- summarization-02: Recovery from the outage was fast.
- summarization-02: A rollback occurred at 09:48.
- summarization-02: The priority now is fixing the two structural gaps rather than the response speed.
- summarization-04: The reporter clicked the PDF export button several more times.
- summarization-04: Four identical "export failed" error banners appear.
- summarization-04: The bug was reproduced by two different users.
- summarization-08: Six participants completed the field-mapping step unaffected.

### classic-concise

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 21 | 15 | 0.714 | 20 | 4 |
| code-review-02 | 23 | 10 | 0.435 | 14 | 1 |
| code-review-03 | 21 | 8 | 0.381 | 15 | 5 |
| code-review-04 | 22 | 11 | 0.5 | 14 | 0 |
| code-review-05 | 31 | 24 | 0.774 | 37 | 8 |
| code-review-06 | 38 | 29 | 0.763 | 43 | 12 |
| code-review-07 | 37 | 22 | 0.595 | 22 | 5 |
| code-review-08 | 36 | 31 | 0.861 | 40 | 9 |
| debugging-01 | 7 | 7 | 1.0 | 6 | 0 |
| debugging-02 | 9 | 6 | 0.667 | 11 | 3 |
| debugging-03 | 9 | 9 | 1.0 | 8 | 0 |
| debugging-04 | 14 | 8 | 0.571 | 7 | 0 |
| debugging-05 | 16 | 15 | 0.938 | 12 | 0 |
| debugging-06 | 40 | 24 | 0.6 | 33 | 15 |
| debugging-07 | 29 | 16 | 0.552 | 31 | 13 |
| debugging-08 | 5 | 0 | 0.0 | 37 | 37 |
| explanation-01 | 32 | 20 | 0.625 | 25 | 3 |
| explanation-02 | 27 | 24 | 0.889 | 20 | 2 |
| explanation-03 | 32 | 20 | 0.625 | 33 | 5 |
| explanation-04 | 39 | 30 | 0.769 | 26 | 4 |
| explanation-05 | 23 | 18 | 0.783 | 11 | 0 |
| explanation-06 | 25 | 20 | 0.8 | 19 | 2 |
| explanation-07 | 27 | 18 | 0.667 | 29 | 6 |
| explanation-08 | 13 | 10 | 0.769 | 16 | 7 |
| summarization-01 | 5 | 4 | 0.8 | 5 | 0 |
| summarization-02 | 15 | 12 | 0.8 | 16 | 5 |
| summarization-03 | 14 | 13 | 0.929 | 12 | 0 |
| summarization-04 | 13 | 13 | 1.0 | 14 | 1 |
| summarization-05 | 11 | 9 | 0.818 | 8 | 0 |
| summarization-06 | 14 | 13 | 0.929 | 12 | 0 |
| summarization-07 | 18 | 15 | 0.833 | 15 | 2 |
| summarization-08 | 19 | 14 | 0.737 | 13 | 1 |

Median fraction: 0.769 over 32 scored pairs.

Median additions: 2.5 over 32 scored pairs.

Lost facts:

- code-review-01: The function performs no validation of `name`.
- code-review-01: An empty string, `None`, or a wrong type for `name` all pass through unchecked.
- code-review-01: If `roles` already contains "member", it gets added again because there is no deduplication.
- code-review-01: The suggested fix builds a new list with `roles + ["member"]` instead of mutating the caller's list.
- code-review-01: The suggested fix only adds "member" when it is not already in `roles`.
- code-review-01: Exceptions should be allowed to propagate, or specific exception types should be caught, rather than using a bare `except`.
- code-review-02: Mixing `async`/`await` with `.then()` inconsistently defeats the purpose of the promise chain.
- code-review-02: The inconsistent mixing of `async` and `.then()` makes the race condition bug easy to miss.
- code-review-02: Network failures or non-JSON responses will produce an unhandled promise rejection.
- code-review-02: On an error response, `res.json()` may throw or return an error payload that gets treated as a valid profile.
- code-review-02: A function declared `async` always returns a `Promise`.
- code-review-02: Callers must `await` or `.then()` the function's result regardless of the fix.
- code-review-02: As written, the returned promise resolves to a thrown error rather than the name.
- code-review-02: The code has no null or shape validation on the fetched data.
- code-review-02: There is no check that `data` has a `name` property.
- code-review-02: An API could return an error object such as `{ error: "not found" }`.
- code-review-02: The fixed version throws an `Error` with the message `Failed to load user ${userId}: ${res.status}` when `res.ok` is false.
- code-review-02: The fixed version awaits `res.json()` to obtain `profile`.
- code-review-02: The fixed version returns `profile.name.toUpperCase()`.
- code-review-03: A caller can pass `customer_name = "x' OR '1'='1"` to read or modify arbitrary data.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: A customer name containing a single quote, such as `O'Brien`, breaks the query syntactically.
- code-review-03: The single-quote bug causes errors even without malicious intent.
- code-review-03: The query has no LIMIT clause.
- code-review-03: Without a LIMIT, the query could return unbounded rows for a common customer name.
- code-review-03: Returning unbounded rows can cause memory and performance issues.
- code-review-03: Placeholder syntax depends on the database driver.
- code-review-03: psycopg2 and MySQLdb use `%s` as the placeholder.
- code-review-03: sqlite3 uses `?` as the placeholder.
- code-review-03: With parameterized queries, the driver handles escaping.
- code-review-03: With parameterized queries, the SQL structure cannot be altered by input.
- code-review-03: Using parameterized queries fixes both the injection risk and the quote-breaking bug in one change.
- code-review-04: The `reset` method is not atomic, though to a lesser extent than `increment`.
- code-review-04: Dropping an increment this way is called a lost update.
- code-review-04: A single `self.value += 1` would not be safe in general either.
- code-review-04: `+=` on an `int` is still a read-modify-write operation at the bytecode level.
- code-review-04: In CPython, `+=` narrows the race window but does not eliminate it.
- code-review-04: An increment can be lost immediately after a reset.
- code-review-04: There is no thread-safe way for callers to read `value` to get a consistent snapshot.
- code-review-04: Reading `counter.value` directly from another thread while it is being mutated is not guaranteed safe outside CPython's GIL guarantees for a single attribute read.
- code-review-04: Relying on GIL semantics for correctness is fragile and implementation-specific.
- code-review-04: Reading the value safely from other threads requires wrapping the read in the same lock, such as in a `get()` method.
- code-review-04: Attribute access without a lock relies on CPython/GIL implementation details rather than a documented guarantee.
- code-review-05: The unquoted `cd $BACKUP_DIR` is subject to word splitting and globbing.
- code-review-05: The stderr error from `ls *.log` with no matches is noisy but not fatal.
- code-review-05: Because globbing is not disabled, if no .tmp files exist the literal string `*.tmp` is passed to `rm -rf`.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` causes a harmless 'no such file' error.
- code-review-05: Running gzip on a file that already has a .gz counterpart prompts for overwrite confirmation.
- code-review-05: In a non-interactive or cron context, the gzip overwrite prompt can hang or silently fail depending on gzip's behavior.
- code-review-05: `gzip -f` should be used explicitly to avoid the overwrite prompt.
- code-review-06: There are no relevant saved memory entries or preferences for this task.
- code-review-06: JSON Merge Patch (RFC 7396) uses the convention that `None`/null deletes a key.
- code-review-06: Overwriting when only the override value is a dict is arguably correct behavior.
- code-review-06: The lack of cycle protection is low priority and almost certainly not deliberate.
- code-review-06: Some merge utilities do merge lists rather than replacing them.
- code-review-06: Merging conventions for settings vary widely between codebases.
- code-review-06: An empty dict in `override`, such as `{"key": {}}`, results in `merge_settings(merged[key], {})` returning `merged[key]` unchanged.
- code-review-06: An empty dict override is a no-op rather than a 'clear this sub-dict' operation.
- code-review-06: The type-check bug (#3) is the most urgent fix because it can crash in production.
- code-review-07: Immediately retrying a struggling server on 5xx is the worse case to leave without backoff.
- code-review-07: The differing backoff treatment reads more like an oversight than a considered choice.
- code-review-07: The delay computed on the last loop iteration is wasted because the loop exits immediately afterward with no further attempt.
- code-review-07: The backoff is unbounded.
- code-review-07: The semantics of the `attempts` parameter are ambiguous.
- code-review-07: `attempts = 3` means 3 total calls, not 3 retries following an initial attempt.
- code-review-07: Some callers may assume `attempts` means retries-after-failure and therefore receive one fewer call than expected.
- code-review-07: Nobody knows the history of this code.
- code-review-07: If `attempts` is less than or equal to 0, the loop body never runs and `fn` is never called.
- code-review-07: If `attempts` is less than or equal to 0, the wrapped function silently returns undefined.
- code-review-07: The `attempts <= 0` case is probably not exercised by real callers but is a landmine if someone passes a dynamic value.
- code-review-07: 5xx retrying without backoff and `attempts` meaning total calls are ambiguous as to whether they were deliberate.
- code-review-07: The null/undefined inconsistency, the wasted last-iteration delay, and non-HTTP errors being treated like a legitimate empty result are almost certainly accidental.
- code-review-07: The biggest practical risk is that a caller doing `if (result) {...}` or accessing `result.someField` cannot tell whether nothing was returned because of a real bug or because of a handled failure.
- code-review-07: The indistinguishable-failure issue should be fixed first, before the backoff issues.
- code-review-08: If enough tmp/part files are deleted early in the loop, the cap blocks legitimate old-file cleanup for the rest of the run.
- code-review-08: The user said they did not set up the schedule.
- code-review-08: Misconfigured `ROOT` or clock skew could make every file look old.
- code-review-08: Treating `tmp-`/`.part` files as always safe to delete regardless of age may be a deliberate assumption.
- code-review-08: The unconditional `.part`/`tmp-` deletion and the unhandled directory crash are the two issues most likely to cause real incidents.
- debugging-02: Because `setInterval` calls the callback as a plain function, `this` inside a regular function callback is the global object (`window`/`globalThis`), not the `Timer` instance.
- debugging-02: In that case `this.seconds` is `undefined`.
- debugging-02: `undefined + 1` evaluates to `NaN`.
- debugging-04: The byte 0xc3 is the start of a UTF-8 multi-byte sequence.
- debugging-04: The byte 0xc3 likely begins an accented character such as é, à, or ü.
- debugging-04: Any byte greater than or equal to 0x80 raises `UnicodeDecodeError` under the `ascii` codec.
- debugging-04: Encoding can be detected at runtime using the `chardet` library.
- debugging-04: Encoding can be detected at runtime using the `charset-normalizer` library.
- debugging-04: Runtime encoding detection is appropriate when files may use different encodings.
- debugging-05: A prior call can come from another test, from setup code, or from the same test running more than once via a fixture.
- debugging-06: The failure is a connection pool exhaustion issue rather than a code bug in the export job itself.
- debugging-06: The waits end exactly at the 30-second timeout ceiling.
- debugging-06: Unreleased connections on error are common with unhandled exceptions in analytics jobs.
- debugging-06: A leak tied to a rare analytics query or edge-case dataset fits a once-a-week failure cadence.
- debugging-06: The database's own max_connections limit may be the actual bottleneck rather than the application pool.
- debugging-06: If the database connection limit is the bottleneck, both services' pools could report healthy while failing to obtain a physical connection.
- debugging-06: One failure occurred at 02:14:07 on 2026-07-29.
- debugging-06: Cross-referencing analytics logs at 02:14:07 on 2026-07-29 would confirm or rule out the analytics-overlap hypothesis.
- debugging-06: Logging connection checkout and checkin with a query tag or caller identity reveals who owned the pool at exhaustion time.
- debugging-06: Caller-identity logging for connections is cheap to add and highly diagnostic.
- debugging-06: Checking DB-side pg_stat_activity history or logging can distinguish a real database connection limit from an app-level pool limit.
- debugging-06: Increasing pool size or adding wait-timeout backoff with jitter is a mitigation, not a root-cause fix.
- debugging-06: Such mitigation reduces failure frequency and buys time to instrument.
- debugging-06: Isolating the export job to its own pool or connection budget is possible if the database can support it.
- debugging-06: Separate connection pools per service is often the long-term fix for two services sharing one pool.
- debugging-06: The log lines surrounding the failure are missing, so further log analysis is unlikely to reveal what else was happening.
- debugging-07: No relevant memory was found for this project or codebase.
- debugging-07: The working directory is fresh with no prior context on this codebase.
- debugging-07: A digest query filtering broadly rather than by a seeded-test-owned ID can pick up rows belonging to another test.
- debugging-07: Shared cleanup or truncation logic running concurrently can cause missing events.
- debugging-07: When two workers share a test database, a TRUNCATE or teardown from another test can fire between the seed and the assertion and wipe one of the three events.
- debugging-07: A LIMIT combined with an unstable or missing ORDER BY can non-deterministically truncate or exclude events under concurrent load.
- debugging-07: If failures stop at single-worker execution, that confirms the issue is parallel-worker-related shared state rather than a pure timing bug in the code under test.
- debugging-07: pytest-xdist supports worker_id-scoped databases or schemas to give each worker its own test database.
- debugging-07: A single test database shared across workers is the prime suspect for the flake.
- debugging-07: A consistently missing last-inserted event points to a race, while a randomly missing event points to cross-test contamination.
- debugging-07: Inspecting the digest query for LIMIT, missing ORDER BY, or time-window/status filters is a five-minute code read.
- debugging-07: Inspecting the digest query can immediately confirm or eliminate the ordering/LIMIT and time-window hypotheses.
- debugging-07: Checking DB fixture isolation and the digest query's filtering logic are both quick to inspect and would explain the intermittent under-count without reproducing the failure.
- debugging-08: The speaker intends to check whether actual code exists to ground the discussion in.
- debugging-08: The Bash tool is invoked.
- debugging-08: The command executed is `ls -la /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac`.
- debugging-08: The path /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac is the target of the listing command.
- debugging-08: The stated description of the command is that it lists working directory contents.
- explanation-01: There are far more possible keys than buckets in a hash map.
- explanation-01: A hash map that does not handle collisions will overwrite or lose data.
- explanation-01: Insert in separate chaining hashes the key and appends to the bucket's list, first checking if the key already exists in order to update rather than duplicate.
- explanation-01: Linear probing tries the next index, then the next, and so on.
- explanation-01: Quadratic probing tries index + 1², index + 2², index + 3², and so on.
- explanation-01: Double hashing uses a second hash function to decide the step size.
- explanation-01: Deletion in chaining is simple because the entry is just removed from the list.
- explanation-01: Chaining's worst case is O(n) per bucket if the hash function is bad.
- explanation-01: Clustering in open addressing can cause long probe sequences.
- explanation-01: Open addressing tends to win on raw performance for small, primitive keys such as integers and short strings.
- explanation-01: Chaining is simpler to reason about and handles high load factors more gracefully.
- explanation-01: Chaining is easier to implement correctly, especially deletion.
- explanation-02: Optimistic locking avoids holding locks during slow operations such as user think-time between read and write.
- explanation-02: Pessimistic locking fits high-contention, short-lived critical sections where correctness matters more than throughput.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-03: A network path might be a fast local link or a congested trans-continental route through routers with limited buffer space.
- explanation-03: Overwhelming a router's buffer causes a burst of packet loss, retransmissions, and wasted bandwidth.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The initial cwnd is now typically 10 segments per RFC 6928.
- explanation-03: Congestion avoidance growth is typically additive, at +1 segment per RTT.
- explanation-03: Exponential growth is efficient because linear growth from a small starting point could take a very long time to ramp up to the available bandwidth on a fast link.
- explanation-03: Linear growth from a small starting point would waste capacity on a fast link.
- explanation-03: Exponential growth means slow start will overshoot and cause a loss event fairly soon after starting.
- explanation-03: Overshooting and causing a loss event during slow start is expected and intentional.
- explanation-03: After a loss event, TCP backs off and moves into the congestion avoidance phase.
- explanation-03: Moving to congestion avoidance prevents TCP from repeatedly hitting the capacity ceiling at full speed.
- explanation-04: A process is an independent instance of a running program.
- explanation-04: All threads in a process share the same memory address space, heap, and file descriptors.
- explanation-04: Switching between threads is cheaper than switching between processes.
- explanation-04: Thread communication requires careful synchronization with locks and mutexes to avoid race conditions.
- explanation-04: Processes communicate via IPC mechanisms such as pipes, sockets, and shared memory.
- explanation-04: Processes have separate memory spaces enforced by the OS via virtual memory and the MMU.
- explanation-04: Processes can be distributed across machines.
- explanation-04: Process-based architecture maps naturally to microservices and worker-pool architectures.
- explanation-04: Using processes for tasks that don't share much data eliminates race conditions and deadlocks by construction, because there is no shared memory to corrupt.
- explanation-05: Global variables, active stack frames, and static fields are examples of garbage collection roots.
- explanation-05: Accumulated unreachable-but-retained objects cause memory usage to grow unbounded over time.
- explanation-05: A leak in a garbage-collected language is not about forgetting to call free().
- explanation-05: Listener leaks are especially common with observer patterns, DOM event listeners, and subscriptions to long-lived singletons.
- explanation-05: Thread-locals that outlive their thread pool's task lifecycle are a frequent cause of memory leaks.
- explanation-06: An APM tool can quickly show where time is going.
- explanation-06: Database bottlenecks can be caused by missing indexes, full table scans, or over-fetching data.
- explanation-06: A query fix or an index can sometimes give the same speedup as a cache with far less complexity.
- explanation-06: A cache genuinely helps when the data can tolerate being slightly stale, on the order of seconds to minutes.
- explanation-06: The recommendation is to spend a day profiling and measuring the read/write mix before committing to a caching layer.
- explanation-07: A single well-tuned Postgres instance can comfortably handle multi-terabyte databases with proper indexing, vacuuming, and hardware.
- explanation-07: Disk growth per month and query latency trends can be tracked and extrapolated.
- explanation-07: Examples of shard keys include tenant_id and user_id.
- explanation-07: Cheaper alternatives to sharding include indexing, native Postgres table partitioning, vertical scaling, read replicas, connection pooling, and archiving old data.
- explanation-07: These cheaper alternatives often provide 10-50x headroom before sharding is needed.
- explanation-07: Foreign keys do not work across shards, and distributed transactions are required.
- explanation-07: Some database failure modes, such as autovacuum falling behind on huge tables and index bloat, creep up slowly and appear fine until they are not.
- explanation-07: Postgres-native partitioning is cheap, somewhat reversible, and significantly delays the sharding decision.
- explanation-07: Monitoring should cover disk growth, query latency percentiles, and connection saturation.
- explanation-08: Protobuf and msgpack are binary formats.
- explanation-08: A binary format typically reduces payload size.
- explanation-08: Migrating to a binary format touches the whole API surface.
- summarization-01: Each button's tooltip shows the button's keyboard shortcut.
- summarization-02: A deployment on the prior evening reduced the checkout service's database connection pool size from 50 to 5.
- summarization-02: The pool size reduction caused connection pool exhaustion.
- summarization-02: The incident produced an error rate of approximately 12%.
- summarization-03: Synchronous thumbnail generation currently blocks web workers.
- summarization-05: Ada is assigned to run the payments database migration dry run.
- summarization-05: Ada is assigned to confirm with the mobile team's lead whether the mobile team has been informed about the API deprecation.
- summarization-06: The on-call engineer suspects connection-pool exhaustion in the payments client.
- summarization-07: No relevant memory was found for this task.
- summarization-07: The task is a self-contained summarization task.
- summarization-07: A new request batcher was tested against the current request batcher.
- summarization-08: The abandonment is a real, observed outcome (firm on behavior).
- summarization-08: It is not yet confirmed whether the progress bar problem is purely a perception/UI issue.
- summarization-08: The progress bar cause warrants follow-up investigation.
- summarization-08: A few participant comments suggested admins and regular users may want different default settings.
- summarization-08: Non-use of the template gallery could instead mean these particular customers already had templates.

Added facts (styled only):

- code-review-01: The code has four real problems.
- code-review-01: The proposed fix copies the roles argument with `list(roles)` before appending.
- code-review-01: The proposed fix catches `Exception` instead of using a bare `except`.
- code-review-01: The proposed fix returns `True` on successful insert and `False` on exception.
- code-review-02: The corrected implementation throws an `Error` with the message `Failed to load profile: ${res.status}` when `res.ok` is false.
- code-review-03: The columns that are needed should be named explicitly in the query.
- code-review-03: The code has no error handling around the query.
- code-review-03: `cursor.execute` can fail due to a bad connection or a syntax error.
- code-review-03: When the query fails, the exception propagates with no context about which lookup failed.
- code-review-03: A typo in `status` silently returns zero rows rather than raising an error.
- code-review-05: The script assigns `BACKUP_DIR=$1` without quoting.
- code-review-05: The `-r` flag is pointless for files matching `*.tmp` unless directories can match that glob.
- code-review-05: `rm -rf` performs a silent, forceful delete.
- code-review-05: In bash, the equivalent option is `set -euo pipefail`.
- code-review-05: The `nullglob` option would make an unmatched glob expand to nothing.
- code-review-05: POSIX sh does not have the `nullglob` option.
- code-review-05: If no `*.log` files exist, the loop body may run once with the literal string `*.log`.
- code-review-05: Running the loop with the literal string `*.log` causes `gzip` to fail on a nonexistent file.
- code-review-06: The list-replacement behavior is inconsistent with the dict-merge behavior and is undocumented.
- code-review-06: A defensive cycle check is worthwhile if input is untrusted.
- code-review-06: The return type of merge_settings is not guaranteed to match the input type.
- code-review-06: dict(base) accepts any mapping.
- code-review-06: The recursive call in merge_settings always produces a plain dict.
- code-review-06: If base is an OrderedDict or custom mapping subclass, that type information is lost on nested keys.
- code-review-06: merge_settings uses merged.pop(key, None), which swallows deletion of a key that was never present.
- code-review-06: There is no way for an outside caller to tell whether a deletion in merge_settings actually removed anything.
- code-review-06: The inability to detect no-op deletions could matter for logging or debugging merge behavior.
- code-review-06: The two type-mismatch cases should either both raise or neither should raise.
- code-review-06: The recommended next step is to write tests pinning down whether None-as-delete and list-replace-not-merge are intended, before touching call sites.
- code-review-06: The recommendation includes switching to copy.deepcopy(base) or a proper recursive copy unless no caller mutates nested values afterward.
- code-review-07: If null or undefined is thrown, accessing err.status throws inside the catch block.
- code-review-07: The exception raised by accessing err.status on null or undefined is not handled and propagates out of withRetry.
- code-review-07: The propagating exception is inconsistent with withRetry's behavior of resolving to null elsewhere.
- code-review-07: Multiple callers retrying in lockstep after a shared rate-limit event will collide again at 1s, 2s, and 3s intervals.
- code-review-07: The callers of withRetry are unknown and cannot be inspected.
- code-review-08: `os.listdir(ROOT)` crashes if `ROOT` is missing.
- code-review-08: `os.remove` and `os.path.getmtime` crash on a permission error.
- code-review-08: `os.path.getmtime` works on directories.
- code-review-08: `os.listdir` does not return entries sorted by mtime.
- code-review-08: `os.listdir` ordering is filesystem-dependent and effectively arbitrary.
- code-review-08: The 500-file cap does not select the oldest files; it removes whichever 500 old files come first in directory order.
- code-review-08: The script has no dry-run mode.
- code-review-08: Without documented intent, there is no way to confirm the policy values or catch regressions if someone changes them.
- code-review-08: The remaining issues are worth confirming with whoever owns the retention policy before making changes.
- debugging-02: Class bodies run in strict mode.
- debugging-02: Because of strict mode, `this` inside that callback is `undefined`.
- debugging-02: `this.seconds += 1` throws `TypeError: Cannot read properties of undefined (reading 'seconds')`.
- debugging-06: Connection leaks accumulate over the course of a run.
- debugging-06: Because leaks accumulate over a run, failures could occur on any batch.
- debugging-06: If worker count or concurrency scaled up via autoscaling or a new deploy, the pool limit may now be undersized for peak load.
- debugging-06: Export and analytics jobs may occasionally overlap due to jitter in cron or scheduler timing.
- debugging-06: Scheduling overlap from jitter would cause spikes only on some nights.
- debugging-06: The failures occur between 02:13 and 02:15.
- debugging-06: A hook or scheduled snapshot can dump pg_stat_activity at the time the pool exhausts.
- debugging-06: pg_stat_activity provides active and idle connection counts, the longest-running query, and which service owns each connection.
- debugging-06: Auditing exception paths and retry logic can reveal connection leaks in the export code.
- debugging-06: Every acquire should have a matching release or close, including inside except blocks.
- debugging-06: Exact start times of the export job and analytics job can be compared across several nights to detect creeping overlap.
- debugging-06: The export job can be run against a test database while replaying analytics-like load concurrently.
- debugging-06: Synthetic reproduction is more reliable than waiting for the weekly failure.
- debugging-06: Correlating timestamps with analytics activity and capturing DB-side connection state are cheap diagnostic steps.
- debugging-06: Those first two steps will likely reveal within a few failures whether the cause is contention, a leak, or a config issue.
- debugging-07: The race could stem from a missing await, an async task fired without being joined, or a queue/worker that batches events and hasn't flushed.
- debugging-07: The test never fails when run serially and fails roughly 10% of the time under 4-way parallel execution.
- debugging-07: Examples of non-unique keys include a fixed user ID, a global counter, and an unpartitioned event store.
- debugging-07: Serial local runs are fast enough to always stay inside the digest time window.
- debugging-07: If seeding and reading use different DB connections and the seed isn't committed before the read, the read can miss the last write.
- debugging-07: Contention from parallel workers increases the chance of the read landing on a stale snapshot.
- debugging-07: The failing test is test_digest_contains_all_events in tests/test_notifications.py.
- debugging-07: Hardcoded IDs, class-scoped fixtures, and module-level lists or singletons are forms of shared state that may not be unique per test run.
- debugging-07: pytest-rerunfailures is a rerun-on-failure plugin.
- debugging-07: Knowing which event is missing is the single most useful piece of information currently being discarded.
- debugging-07: CI runners that are CPU or memory constrained under 4x parallelism can cause timeouts or slow I/O.
- debugging-07: Timeouts or slow I/O can make an otherwise-correct async wait too short under load.
- debugging-07: The recommended starting points are reproducing locally under load and capturing which event is missing.
- debugging-08: The four clues point to two separate memory leaks stacked on top of each other rather than a single bug.
- debugging-08: The canary instance is the key clue for diagnosing the problem.
- debugging-08: Memory growth on the canary without webhooks combined with faster growth with webhooks indicates a baseline leak plus a traffic-driven leak.
- debugging-08: A baseline leak independent of webhooks would explain the canary's memory growth.
- debugging-08: A scheduler or background job that accumulates state is a candidate cause of a baseline leak.
- debugging-08: Unbounded metric-tag cardinality is a candidate cause of a baseline leak.
- debugging-08: Thread-local values never cleared on a reused thread pool are a candidate cause of a baseline leak.
- debugging-08: A logging or metrics buffer is a candidate cause of a baseline leak.
- debugging-08: Taking two heap dumps on the canary, morning and evening, and diffing them can identify a baseline leak.
- debugging-08: Eclipse MAT is a tool that can diff heap dumps.
- debugging-08: jhat has a heap dump comparison view.
- debugging-08: `jcmd <pid> GC.class_histogram` can be run at two points and the instance counts per class diffed, as a starting point when no heap dump tooling exists.
- debugging-08: A webhook-driven leak additive to the baseline leak would explain faster growth with traffic and during campaigns.
- debugging-08: A listener or callback registered per webhook and never deregistered is a candidate cause of a webhook-driven leak.
- debugging-08: A dedupe or idempotency map keyed by webhook or event ID that is never pruned is a candidate cause of a webhook-driven leak.
- debugging-08: Per-request objects retained by a static collection are a candidate cause of a webhook-driven leak.
- debugging-08: If a webhook-driven leak is the cause, daily memory growth rate should be roughly linear in webhook request volume.
- debugging-08: async-profiler and JFR are allocation profilers.
- debugging-08: Running an allocation profiler during a high-traffic hour and a low-traffic hour and comparing top retained-size allocation sites can identify a webhook-driven leak.
- debugging-08: The cache's configured bound has not been changed.
- debugging-08: If a cache bounds entry count rather than bytes, campaigns introducing more or larger product records will increase resident memory even with the entry count capped.
- debugging-08: Whether cache evictions are actually firing should be checked.
- debugging-08: Average entry size and total cache bytes should be logged over time, not just entry count.
- debugging-08: Over a day, cache evictions should equal insertions minus current size.
- debugging-08: If evictions lag insertions, something such as a listener closure or a strong reference held elsewhere is keeping evicted entries alive.
- debugging-08: Memory usage never returns to baseline overnight, across multiple full GCs.
- debugging-08: The failure of usage to return to baseline across multiple full GCs argues against the explanation that the growth is merely GC lag.
- debugging-08: The GC-lag explanation should be confirmed directly rather than assumed.
- debugging-08: GC logs can be used to inspect old-gen occupancy immediately after each full GC.
- debugging-08: If old-gen occupancy after full GCs climbs monotonically overnight with no traffic, it is a real leak rather than fragmentation.
- debugging-08: If nothing appears in heap analysis, the growth may be off-heap or native rather than in the heap.
- debugging-08: Comparing process RSS to reported heap usage can reveal off-heap growth.
- debugging-08: If RSS grows while heap usage stays flat, `-XX:NativeMemoryTracking=summary` should be enabled and thread count and direct-buffer pools tracked over time.
- debugging-08: Investigations #1 and #4 are cheap, requiring only two heap dumps and a GC log grep.
- debugging-08: Investigations #1 and #4 will determine whether the issue is a real leak or GC behavior.
- debugging-08: Investigations #1 and #4 will determine whether the leak exists with zero webhook traffic.
- debugging-08: The result of investigations #1 and #4 determines whether profiling should focus on the cache path or the webhook handling path.
- explanation-01: Open addressing is preferable when memory locality matters and the load factor stays below about 0.7.
- explanation-01: Most general-purpose hash maps use chaining.
- explanation-01: Rust's HashMap uses open addressing.
- explanation-02: Example use cases for optimistic locking include web apps editing user profiles, CMS documents, and shopping carts.
- explanation-02: Example use cases for pessimistic locking include bank transfers, inventory decrement during a flash sale, and seat booking.
- explanation-03: A new TCP connection does not know how many other flows share the link.
- explanation-03: A new TCP connection does not know where the bottleneck sits.
- explanation-03: Slow start also applies after a loss event resets the sending rate.
- explanation-03: Each round trip generates acknowledgments for every segment sent.
- explanation-03: The name 'slow start' refers only to the cautious starting point, not the pace of growth.
- explanation-04: Creating a process requires a fresh address space and copied resources.
- explanation-04: Browsers use separate processes per tab for fault isolation.
- explanation-04: Ruby MRI serializes thread execution with a global interpreter lock.
- explanation-04: Process-level sandboxing provides separate memory and separate permissions.
- explanation-06: If writes dominate, indexing, batching, and query optimization are better places to look than caching.
- explanation-06: Adding a cache adds complexity, including cache invalidation, staleness, and another system to operate.
- explanation-07: A database's growth may be concentrated in one table (such as events, logs, or sessions) while the rest stays static.
- explanation-07: Sharding an entire database because one table is hot is the wrong fix.
- explanation-07: Cloud instances now offer multi-terabyte RAM and tens of terabytes of fast storage.
- explanation-07: Partitioning can serve as the seam along which a database is later sharded.
- explanation-07: The recommended approach is to instrument now by tracking table growth rates, write QPS, and vacuum/replication health.
- explanation-07: The recommended approach includes setting explicit thresholds for when to shard, such as a specific data size or sustained writes per second.
- explanation-08: Serialization rarely dominates request time.
- explanation-08: Network I/O, database calls, and business logic usually consume most of a request's time budget.
- explanation-08: If serialization is 5% of request time, halving it saves 2.5% of request time.
- explanation-08: A 2.5% savings does not justify the cost of migrating to a binary format.
- explanation-08: Migrating to a binary format means losing human-readable payloads.
- explanation-08: Serialization is likely to be a small share of request time.
- explanation-08: Serializing huge payloads at high QPS is an example of serialization being a large share of request time.
- summarization-02: Detection and response for the incident were fast.
- summarization-02: Page-to-resolution took 34 minutes.
- summarization-02: The page was sent at 09:21.
- summarization-02: The rollback completed at 09:48.
- summarization-02: The team has not yet fixed the root cause.
- summarization-04: Four clicks of "Export PDF" produce four error banners.
- summarization-07: The recommendation is to profile memory before trusting the tail-latency numbers.
- summarization-07: The recommendation is to reproduce the crash before trusting the tail-latency numbers.
- summarization-08: The progress bar issue is worth fixing.

### developer-docs

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 21 | 18 | 0.857 | 19 | 2 |
| code-review-02 | 23 | 14 | 0.609 | 16 | 2 |
| code-review-03 | 21 | 0 | 0.0 | 2 | 1 |
| code-review-04 | 22 | 14 | 0.636 | 21 | 7 |
| code-review-05 | 31 | 26 | 0.839 | 29 | 5 |
| code-review-06 | 38 | 23 | 0.605 | 25 | 7 |
| code-review-07 | 37 | 0 | 0.0 | 5 | 5 |
| code-review-08 | 36 | 28 | 0.778 | 39 | 14 |
| debugging-01 | 7 | 7 | 1.0 | 9 | 0 |
| debugging-02 | 9 | 7 | 0.778 | 11 | 2 |
| debugging-03 | 9 | 9 | 1.0 | 12 | 0 |
| debugging-04 | 14 | 14 | 1.0 | 15 | 3 |
| debugging-05 | 16 | 14 | 0.875 | 18 | 1 |
| debugging-06 | 40 | 28 | 0.7 | 37 | 10 |
| debugging-07 | 29 | 18 | 0.621 | 21 | 6 |
| debugging-08 | 5 | 0 | 0.0 | 36 | 36 |
| explanation-01 | 32 | 21 | 0.656 | 29 | 2 |
| explanation-02 | 27 | 25 | 0.926 | 26 | 0 |
| explanation-03 | 32 | 21 | 0.656 | 29 | 4 |
| explanation-04 | 39 | 31 | 0.795 | 39 | 5 |
| explanation-05 | 23 | 18 | 0.783 | 13 | 2 |
| explanation-06 | 25 | 16 | 0.64 | 19 | 3 |
| explanation-07 | 27 | 17 | 0.63 | 22 | 4 |
| explanation-08 | 13 | 10 | 0.769 | 15 | 4 |
| summarization-01 | 5 | 5 | 1.0 | 11 | 6 |
| summarization-02 | 15 | 9 | 0.6 | 10 | 3 |
| summarization-03 | 14 | 14 | 1.0 | 12 | 0 |
| summarization-04 | 13 | 13 | 1.0 | 14 | 4 |
| summarization-05 | 11 | 10 | 0.909 | 10 | 0 |
| summarization-06 | 14 | 14 | 1.0 | 13 | 0 |
| summarization-07 | 18 | 16 | 0.889 | 16 | 0 |
| summarization-08 | 19 | 17 | 0.895 | 22 | 2 |

Median fraction: 0.78 over 32 scored pairs.

Median additions: 3.0 over 32 scored pairs.

Lost facts:

- code-review-01: A bare `except:` silently swallows real bugs, such as `db` being `None`, a malformed `name`, or a network error.
- code-review-01: If `roles` already contains "member", it gets added again because there is no deduplication.
- code-review-01: The suggested fix only adds "member" when it is not already in `roles`.
- code-review-02: Mixing `async`/`await` with `.then()` inconsistently defeats the purpose of the promise chain.
- code-review-02: The inconsistent mixing of `async` and `.then()` makes the race condition bug easy to miss.
- code-review-02: A function declared `async` always returns a `Promise`.
- code-review-02: Callers must `await` or `.then()` the function's result regardless of the fix.
- code-review-02: As written, the returned promise resolves to a thrown error rather than the name.
- code-review-02: The code has no null or shape validation on the fetched data.
- code-review-02: There is no check that `data` has a `name` property.
- code-review-02: An API could return an error object such as `{ error: "not found" }`.
- code-review-02: The fixed version throws an `Error` with the message `Failed to load user ${userId}: ${res.status}` when `res.ok` is false.
- code-review-03: The code concatenates `customer_name` and `status` directly into the query string.
- code-review-03: Concatenating untrusted input into the query creates a SQL injection vulnerability.
- code-review-03: A caller can pass `customer_name = "x' OR '1'='1"` to read or modify arbitrary data.
- code-review-03: SQL injection can let a caller break out of the query entirely.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: A customer name containing a single quote, such as `O'Brien`, breaks the query syntactically.
- code-review-03: The single-quote bug causes errors even without malicious intent.
- code-review-03: `SELECT *` is fragile when the table schema changes.
- code-review-03: If columns are added or reordered, callers relying on positional access to `fetchall()` results will silently break.
- code-review-03: `SELECT *` fetches unneeded columns.
- code-review-03: The code does not validate that `status` is one of the expected enum values such as `'pending'` or `'shipped'`.
- code-review-03: The query has no LIMIT clause.
- code-review-03: Without a LIMIT, the query could return unbounded rows for a common customer name.
- code-review-03: Returning unbounded rows can cause memory and performance issues.
- code-review-03: The fix is to use parameterized queries with placeholders instead of string concatenation.
- code-review-03: Placeholder syntax depends on the database driver.
- code-review-03: psycopg2 and MySQLdb use `%s` as the placeholder.
- code-review-03: sqlite3 uses `?` as the placeholder.
- code-review-03: With parameterized queries, the driver handles escaping.
- code-review-03: With parameterized queries, the SQL structure cannot be altered by input.
- code-review-03: Using parameterized queries fixes both the injection risk and the quote-breaking bug in one change.
- code-review-04: The `reset` method is not atomic, though to a lesser extent than `increment`.
- code-review-04: A single `self.value += 1` would not be safe in general either.
- code-review-04: `+=` on an `int` is still a read-modify-write operation at the bytecode level.
- code-review-04: In CPython, `+=` narrows the race window but does not eliminate it.
- code-review-04: An increment can be lost immediately after a reset.
- code-review-04: Reading `counter.value` directly from another thread while it is being mutated is not guaranteed safe outside CPython's GIL guarantees for a single attribute read.
- code-review-04: Relying on GIL semantics for correctness is fragile and implementation-specific.
- code-review-04: Attribute access without a lock relies on CPython/GIL implementation details rather than a documented guarantee.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` causes a harmless 'no such file' error.
- code-review-05: Without error handling, the script prints 'Cleaned' as if everything succeeded.
- code-review-05: In a non-interactive or cron context, the gzip overwrite prompt can hang or silently fail depending on gzip's behavior.
- code-review-05: `gzip -f` should be used explicitly to avoid the overwrite prompt.
- code-review-05: The 'Cleaned' message is printed unconditionally even if earlier steps failed, giving a false sense of success.
- code-review-06: There are no relevant saved memory entries or preferences for this task.
- code-review-06: JSON Merge Patch (RFC 7396) uses the convention that `None`/null deletes a key.
- code-review-06: The None-as-delete behavior is an undocumented API decision.
- code-review-06: Overwriting when only the override value is a dict is arguably correct behavior.
- code-review-06: The asymmetric type check suggests the type-check logic was not fully thought through.
- code-review-06: Some merge utilities do merge lists rather than replacing them.
- code-review-06: Merging conventions for settings vary widely between codebases.
- code-review-06: An empty dict in `override`, such as `{"key": {}}`, results in `merge_settings(merged[key], {})` returning `merged[key]` unchanged.
- code-review-06: An empty dict override is a no-op rather than a 'clear this sub-dict' operation.
- code-review-06: The function lacks a name/docstring stating its 'settings' semantics.
- code-review-06: Nothing in the code states whether it implements JSON-Merge-Patch-like semantics or bespoke semantics.
- code-review-06: The None-as-delete behavior specifically matches RFC 7396.
- code-review-06: The author probably consciously implemented the RFC 7396 pattern but did not document or fully finish it.
- code-review-06: The type-check bug (#3) is the most urgent fix because it can crash in production.
- code-review-06: The shallow-copy aliasing bug (#1) is the most dangerous latent bug because it can silently corrupt `base`.
- code-review-07: On any error that is not a 429 status or a status of 500 or greater, the function returns null instead of rethrowing.
- code-review-07: Callers cannot distinguish a legitimate null return value from a failed call.
- code-review-07: Programmer bugs inside `fn`, such as a TypeError from a null reference, are silently converted into a null return rather than surfacing.
- code-review-07: The silent-null behavior could be an intentional 'fail soft' convention inherited from the original library.
- code-review-07: An undocumented fail-soft convention is dangerous.
- code-review-07: The function uses two different failure signals: null and undefined.
- code-review-07: If the retryable branches for 429 or 5xx exhaust the loop without hitting a return, the function falls off the end and implicitly returns undefined.
- code-review-07: The non-retryable branch explicitly returns null.
- code-review-07: Exhausted retries return undefined while other failures return null.
- code-review-07: The null versus undefined inconsistency is almost certainly accidental rather than deliberate.
- code-review-07: A 429 response triggers a delay of `1000 * i` milliseconds before retrying.
- code-review-07: A 5xx response is retried immediately with no delay.
- code-review-07: Immediately retrying a struggling server on 5xx is the worse case to leave without backoff.
- code-review-07: The differing backoff treatment could be deliberate, treating 5xx as probably transient and 429 as requiring a cooldown.
- code-review-07: The differing backoff treatment reads more like an oversight than a considered choice.
- code-review-07: Because the delay is `1000 * i`, the first retry occurs when i equals 0 and waits 0 milliseconds, providing no backoff on the first 429.
- code-review-07: The delay computed on the last loop iteration is wasted because the loop exits immediately afterward with no further attempt.
- code-review-07: The backoff is linear rather than exponential, despite appearing intended to ramp up.
- code-review-07: The backoff is unbounded.
- code-review-07: The backoff has no jitter, creating a thundering herd risk when many callers retry in lockstep after a shared rate limit.
- code-review-07: The code assumes `err.status` exists.
- code-review-07: Non-HTTP errors such as network failures, thrown strings, and bugs have no `.status` property.
- code-review-07: For errors without a status, both `undefined === 429` and `undefined >= 500` evaluate to false.
- code-review-07: Errors without a status fall through to the branch that silently returns null.
- code-review-07: Anything that is not a recognized HTTP error is treated identically to a successful call that returned no data.
- code-review-07: The semantics of the `attempts` parameter are ambiguous.
- code-review-07: `attempts = 3` means 3 total calls, not 3 retries following an initial attempt.
- code-review-07: Some callers may assume `attempts` means retries-after-failure and therefore receive one fewer call than expected.
- code-review-07: Nobody knows the history of this code.
- code-review-07: If `attempts` is less than or equal to 0, the loop body never runs and `fn` is never called.
- code-review-07: If `attempts` is less than or equal to 0, the wrapped function silently returns undefined.
- code-review-07: The `attempts <= 0` case is probably not exercised by real callers but is a landmine if someone passes a dynamic value.
- code-review-07: Returning null instead of throwing on non-retryable errors is plausibly a deliberate library convention.
- code-review-07: 5xx retrying without backoff and `attempts` meaning total calls are ambiguous as to whether they were deliberate.
- code-review-07: The null/undefined inconsistency, the wasted last-iteration delay, and non-HTTP errors being treated like a legitimate empty result are almost certainly accidental.
- code-review-07: The biggest practical risk is that a caller doing `if (result) {...}` or accessing `result.someField` cannot tell whether nothing was returned because of a real bug or because of a handled failure.
- code-review-07: The indistinguishable-failure issue should be fixed first, before the backoff issues.
- code-review-08: The script has no handling for directories.
- code-review-08: `os.listdir` returns all entries, including subdirectories.
- code-review-08: `os.remove` raises `IsADirectoryError` when given a directory.
- code-review-08: The script does not catch `IsADirectoryError`.
- code-review-08: An uncaught directory error crashes the whole `clean()` call.
- code-review-08: The 500 cap was presumably intended to bound the run's total deletions.
- code-review-08: The 45-day retention window is undocumented.
- code-review-08: The unconditional `.part`/`tmp-` deletion and the unhandled directory crash are the two issues most likely to cause real incidents.
- debugging-02: Because `setInterval` calls the callback as a plain function, `this` inside a regular function callback is the global object (`window`/`globalThis`), not the `Timer` instance.
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` inside it is an alternative fix.
- debugging-05: A prior call can come from another test, from setup code, or from the same test running more than once via a fixture.
- debugging-05: In the fixed code, `make_post` has signature `make_post(title, tags=None)` and sets `tags = list(DEFAULT_TAGS)` when `tags is None`.
- debugging-06: The waits end exactly at the 30-second timeout ceiling.
- debugging-06: A code path that acquires a connection but fails to release it on error causes leaks.
- debugging-06: Unreleased connections on error are common with unhandled exceptions in analytics jobs.
- debugging-06: A leak tied to a rare analytics query or edge-case dataset fits a once-a-week failure cadence.
- debugging-06: If the database connection limit is the bottleneck, both services' pools could report healthy while failing to obtain a physical connection.
- debugging-06: One failure occurred at 02:14:07 on 2026-07-29.
- debugging-06: Cross-referencing analytics logs at 02:14:07 on 2026-07-29 would confirm or rule out the analytics-overlap hypothesis.
- debugging-06: Checking DB-side pg_stat_activity history or logging can distinguish a real database connection limit from an app-level pool limit.
- debugging-06: Such mitigation reduces failure frequency and buys time to instrument.
- debugging-06: Isolating the export job to its own pool or connection budget is possible if the database can support it.
- debugging-06: Separate connection pools per service is often the long-term fix for two services sharing one pool.
- debugging-06: The log lines surrounding the failure are missing, so further log analysis is unlikely to reveal what else was happening.
- debugging-07: No relevant memory was found for this project or codebase.
- debugging-07: The working directory is fresh with no prior context on this codebase.
- debugging-07: Shared cleanup or truncation logic running concurrently can cause missing events.
- debugging-07: When two workers share a test database, a TRUNCATE or teardown from another test can fire between the seed and the assertion and wipe one of the three events.
- debugging-07: If the seed and the digest read use different DB connections or transactions and the isolation level is not read-committed, the read can observe only 2 of the 3 committed rows.
- debugging-07: Connection pooling that reuses a stale connection can cause a read to miss committed rows.
- debugging-07: If the digest is scoped by a time window and the test does not control the clock, a slow CI run can push an event's timestamp outside the window.
- debugging-07: pytest-xdist supports worker_id-scoped databases or schemas to give each worker its own test database.
- debugging-07: A single test database shared across workers is the prime suspect for the flake.
- debugging-07: A consistently missing last-inserted event points to a race, while a randomly missing event points to cross-test contamination.
- debugging-07: Inspecting the digest query for LIMIT, missing ORDER BY, or time-window/status filters is a five-minute code read.
- debugging-08: The speaker intends to check whether actual code exists to ground the discussion in.
- debugging-08: The Bash tool is invoked.
- debugging-08: The command executed is `ls -la /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac`.
- debugging-08: The path /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac is the target of the listing command.
- debugging-08: The stated description of the command is that it lists working directory contents.
- explanation-01: There are far more possible keys than buckets in a hash map.
- explanation-01: A hash map that does not handle collisions will overwrite or lose data.
- explanation-01: The collection in a separate chaining bucket is usually a linked list, and sometimes a tree.
- explanation-01: Quadratic probing tries index + 1², index + 2², index + 3², and so on.
- explanation-01: Chaining degrades gracefully even above a load factor of 1.0 because buckets just grow.
- explanation-01: Open addressing must keep the load factor well below 1.0 and needs resizing sooner.
- explanation-01: Chaining's worst case is O(n) per bucket if the hash function is bad.
- explanation-01: Clustering in open addressing can cause long probe sequences.
- explanation-01: Open addressing tends to win on raw performance for small, primitive keys such as integers and short strings.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Python's dict uses open addressing.
- explanation-02: Optimistic locking avoids holding locks during slow operations such as user think-time between read and write.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-03: A network path might be a fast local link or a congested trans-continental route through routers with limited buffer space.
- explanation-03: Congestion collapse was a real problem on the early internet in the late 1980s.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The initial cwnd was historically 1 segment.
- explanation-03: The initial cwnd is now typically 10 segments per RFC 6928.
- explanation-03: Congestion avoidance growth is typically additive, at +1 segment per RTT.
- explanation-03: Exponential growth means slow start will overshoot and cause a loss event fairly soon after starting.
- explanation-03: Overshooting and causing a loss event during slow start is expected and intentional.
- explanation-03: After a loss event, TCP backs off and moves into the congestion avoidance phase.
- explanation-03: Moving to congestion avoidance prevents TCP from repeatedly hitting the capacity ceiling at full speed.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Switching between threads is cheaper than switching between processes.
- explanation-04: Thread communication requires careful synchronization with locks and mutexes to avoid race conditions.
- explanation-04: Process creation cost is high because the OS allocates a new address space.
- explanation-04: Processes have separate memory spaces enforced by the OS via virtual memory and the MMU.
- explanation-04: Processes can be distributed across machines.
- explanation-04: Process-based architecture maps naturally to microservices and worker-pool architectures.
- explanation-04: Using processes for tasks that don't share much data eliminates race conditions and deadlocks by construction, because there is no shared memory to corrupt.
- explanation-05: Global variables, active stack frames, and static fields are examples of garbage collection roots.
- explanation-05: A leak in a garbage-collected language is not about forgetting to call free().
- explanation-05: Listener leaks are especially common with observer patterns, DOM event listeners, and subscriptions to long-lived singletons.
- explanation-05: Closures capturing more than intended are a frequent cause of memory leaks.
- explanation-05: Thread-locals that outlive their thread pool's task lifecycle are a frequent cause of memory leaks.
- explanation-06: If slowness comes from slow queries, N+1 calls, network latency, or CPU-bound code, adding a cache will not fix it.
- explanation-06: Deciding to add a cache without knowing the actual bottleneck is the real risk, not the cache itself.
- explanation-06: Time in an API request can go to the database, an external API call, serialization, or business logic.
- explanation-06: A simple timer or logging around each step can quickly show where time is going.
- explanation-06: An APM tool can quickly show where time is going.
- explanation-06: A rough estimate of the read/write ratio can be derived from logs or query counts.
- explanation-06: Database bottlenecks can be caused by missing indexes, full table scans, or over-fetching data.
- explanation-06: A cache genuinely helps when the data can tolerate being slightly stale, on the order of seconds to minutes.
- explanation-06: The recommendation is to spend a day profiling and measuring the read/write mix before committing to a caching layer.
- explanation-07: The real constraint on a database may be disk size, write throughput (IOPS), CPU/query load, or connection count.
- explanation-07: Sharding mainly provides write scalability and removes single-node disk ceilings.
- explanation-07: Examples of shard keys include tenant_id and user_id.
- explanation-07: Cheaper alternatives to sharding include indexing, native Postgres table partitioning, vertical scaling, read replicas, connection pooling, and archiving old data.
- explanation-07: These cheaper alternatives often provide 10-50x headroom before sharding is needed.
- explanation-07: Foreign keys do not work across shards, and distributed transactions are required.
- explanation-07: Staying single-instance too long risks hitting walls such as disk exhaustion, replication lag, or vacuum failing to keep up on huge tables.
- explanation-07: Some database failure modes, such as autovacuum falling behind on huge tables and index bloat, creep up slowly and appear fine until they are not.
- explanation-07: Postgres-native partitioning is cheap, somewhat reversible, and significantly delays the sharding decision.
- explanation-07: Monitoring should cover disk growth, query latency percentiles, and connection saturation.
- explanation-08: The actual benefit depends on how hot the code path is.
- explanation-08: Migrating to a binary format touches the whole API surface.
- explanation-08: Schemas, client compatibility, and debugging tooling all become more expensive with binary formats.
- summarization-02: A deployment on the prior evening reduced the checkout service's database connection pool size from 50 to 5.
- summarization-02: Staging intentionally uses smaller connection pools than production.
- summarization-02: The pool size reduction caused connection pool exhaustion.
- summarization-02: The incident produced an error rate of approximately 12%.
- summarization-02: The incident lasted approximately 34 minutes.
- summarization-02: The incident ran from 09:14 to 09:48 UTC.
- summarization-05: Ada's migration dry run is due before Thursday.
- summarization-07: No relevant memory was found for this task.
- summarization-07: The task is a self-contained summarization task.
- summarization-08: The progress bar cause warrants follow-up investigation.
- summarization-08: The recommendation is to prioritize investigating the progress bar issue because of its abandonment impact.

Added facts (styled only):

- code-review-01: No memory index file was found for the project.
- code-review-01: There is no prior saved context on this project.
- code-review-02: The function has four problems.
- code-review-02: Because the `.json()` result is not returned, the caller cannot get the profile data even if the timing worked out.
- code-review-03: The read_file MCP tool was called.
- code-review-04: A caller cannot safely read the count for a decision such as incrementing and then acting if a threshold was crossed.
- code-review-04: A read and a later action cannot be made atomic from outside the class.
- code-review-04: The proposed fix renames the attribute to `_value`.
- code-review-04: The proposed fix adds a read-only `value` property.
- code-review-04: In the fixed version, all access to the counter value goes through the lock.
- code-review-04: Compound operations such as 'increment and return the new value' should be added as a dedicated method rather than exposing separate read and write calls.
- code-review-04: Combining separate read and write calls from outside the class would still be a race.
- code-review-05: Line 4 is the most dangerous line in the script.
- code-review-05: `$BACKUP_DIR` and `$f` are unquoted on lines 2, 3, 6, and 8.
- code-review-05: `rm -rf *.tmp` gives no feedback if the glob doesn't match.
- code-review-05: The lack of feedback from `rm` is expected behavior with the `-f` flag.
- code-review-05: The `-f` flag hides typos in the removal pattern.
- code-review-06: When `override` introduces a nested dict under a key not already present in `merged`, that dict is assigned by reference rather than copied.
- code-review-06: The function has no guard against non-dict input.
- code-review-06: If `override` is `None` or not a dict, `.items()` fails with a generic `AttributeError` rather than a clear error message.
- code-review-06: The same lack of input validation applies to `base` if it is not dict-like.
- code-review-06: Supporting an explicit `None` value would require changing the sentinel, for example to a dedicated `DELETE` marker.
- code-review-06: A dict in `base` can be replaced entirely by a scalar in `override`.
- code-review-06: With `base = {"x": {"a": 1}}` and `override = {"x": 5}`, the result is `{"x": 5}`.
- code-review-07: The speaker is reading the memory index.
- code-review-07: The purpose of reading the memory index is to find relevant prior guidance.
- code-review-07: The memory index is read before reviewing.
- code-review-07: The speaker will check the memory index only once.
- code-review-07: After checking the memory index, the speaker will give the review directly.
- code-review-08: A single PermissionError would abort the entire run.
- code-review-08: getmtime raises an exception on broken symlinks.
- code-review-08: A broken symlink would abort the entire run.
- code-review-08: Whether anyone is notified of an aborted run depends on how the scheduler is configured.
- code-review-08: os.listdir returns files in arbitrary, OS-dependent order, not sorted by age.
- code-review-08: The condition removed < 500 does not cap the 500 oldest files; it caps whatever 500 files the filesystem returns first.
- code-review-08: Different files would be deleted on ext4 versus APFS versus a network filesystem.
- code-review-08: The 500 cap was presumably meant to limit the cutoff-based deletions specifically.
- code-review-08: The removed return value is unused — there is no metric emission and no log line.
- code-review-08: Because the removed return value is unused, you would never notice if the 500 cap is being hit regularly.
- code-review-08: Regularly hitting the 500 cap would signal that something upstream is producing too much garbage.
- code-review-08: ROOT is hardcoded and not configurable via environment variable or argument.
- code-review-08: The hardcoded ROOT makes the script hard to test against a staging directory.
- code-review-08: The script has no dry-run mode.
- debugging-02: When a function is called without a receiver, `this` is `undefined` in strict mode.
- debugging-02: The arrow function is the more common fix than explicit binding.
- debugging-04: The problematic byte 0xc3 is at position 512 in the file.
- debugging-04: errors="replace" substitutes the character � for each undecodable byte.
- debugging-04: errors="replace" should only be used when exact byte-for-byte fidelity does not matter.
- debugging-05: Other tests also call make_post without a tags argument.
- debugging-06: The error is a pool timeout, not a query timeout.
- debugging-06: A pool timeout means the export job is waiting for a connection slot rather than for a slow query.
- debugging-06: A leaked pool recovers after a restart.
- debugging-06: Pool state logs can be compared against the timestamps of past failures.
- debugging-06: PostgreSQL's pg_stat_activity shows what is holding connections and for how long.
- debugging-06: MySQL's SHOW PROCESSLIST shows what is holding connections and for how long.
- debugging-06: The past failures occurred near 02:00-02:15 UTC.
- debugging-06: A slow upward drift in checked-out connections that resets after a restart indicates a leak rather than contention.
- debugging-06: Temporarily raising the pool size is a diagnostic step rather than a fix.
- debugging-06: Raising the pool size and observing whether failures disappear indicates whether pool exhaustion is the real bottleneck or a symptom of something upstream such as slow queries.
- debugging-07: A digest can undercount because of a race on a shared counter.
- debugging-07: If events use a shared ID space, timestamp, or fixed key instead of a worker-specific or test-specific identifier, two workers can collide and one write can overwrite another.
- debugging-07: Serial runs on a developer machine avoid all four listed failure causes.
- debugging-07: Test isolation can be checked by confirming each test uses a unique tenant, user, or namespace for its events.
- debugging-07: Running CI with '-n 1', then '-n 2', then '-n 4' over several runs each bisects by worker count.
- debugging-07: Reproducing the parallelism effect locally is the fastest way to confirm whether parallelism is the actual variable.
- debugging-08: Taking a heap histogram is the fastest way to separate the five proposed causes of the memory growth.
- debugging-08: None of the four existing observations is sufficient to fully diagnose the problem from the outside.
- debugging-08: `jmap -histo` can be used to take heap snapshots.
- debugging-08: JFR is an alternative to `jmap -histo` for capturing heap snapshots.
- debugging-08: Two heap snapshots taken a few hours apart on an idle instance can be diffed by object counts per class.
- debugging-08: A class whose object count keeps growing with zero traffic pinpoints the leak.
- debugging-08: One plausible cause is a second, unbounded data structure sitting next to the bounded cache.
- debugging-08: Examples of such an unbounded structure include a dedup set, a callback/listener map, or a metrics map keyed by product or campaign ID.
- debugging-08: A second unbounded structure would explain growth on the traffic-free canary, growth that survives quiet nights, and why the unchanged cache bound doesn't help.
- debugging-08: Diffing two heap histograms taken hours apart on an idle instance identifies the leak site as the class with a steadily rising count.
- debugging-08: Another plausible cause is that cache entries grow in size while the entry count stays bounded.
- debugging-08: Another plausible cause is that eviction doesn't fully release references, due to lingering listeners or strong references held elsewhere.
- debugging-08: The cache bound has not changed.
- debugging-08: Campaign-week payloads may be larger than normal payloads.
- debugging-08: Eviction bugs are a common failure mode for size-bounded caches.
- debugging-08: Cache byte size, not just entry count, should be logged over time.
- debugging-08: Average cache entry size should be compared between campaign weeks and quiet weeks.
- debugging-08: Evicted cache entries should be confirmed to have no remaining strong references.
- debugging-08: Another plausible cause is webhook-specific accumulation via an idempotency/dedup set, a retry queue, or a subscription callback that is never pruned.
- debugging-08: The canary instance receives no webhooks.
- debugging-08: The canary instance grows more slowly than other instances.
- debugging-08: Campaign weeks have higher webhook volume and faster memory growth.
- debugging-08: Daily webhook volume can be correlated with daily growth rate across instances.
- debugging-08: The webhook handler can be instrumented to log the size of any in-memory structure it touches.
- debugging-08: Another plausible cause is an off-heap or native memory leak from direct buffers, image/asset processing for product data, or native libraries.
- debugging-08: Native allocations are not visible in the heap and are not cleared by normal GC.
- debugging-08: A native leak would explain growth that survives quiet nights and growth on the canary.
- debugging-08: Process RSS can be compared to JVM heap used using `-XX:NativeMemoryTracking` or `pmap`.
- debugging-08: A growing gap between process RSS and JVM heap used indicates a native memory leak.
- debugging-08: Another plausible cause is a thread or connection leak from unclosed sockets, growing thread pools, or resources opened per request or webhook.
- debugging-08: Background jobs on the canary would explain why it still leaks slowly under a thread or connection leak.
- debugging-08: Live thread count and open file descriptor/connection count can be tracked over the week.
- debugging-08: A steady climb in thread or connection count matching the memory graph indicates a thread or connection leak.
- debugging-08: No heap profile has been collected yet.
- debugging-08: The histogram diff is a five-minute check.
- debugging-08: The histogram diff will likely point directly at one of the other four causes.
- explanation-01: The load factor is the ratio of entries to array size.
- explanation-01: Chaining suits maps where you cannot predict how full the table will get.
- explanation-03: When a TCP connection starts, the sender does not know how many other connections share the path.
- explanation-03: Flooding routers along the path causes packet loss and congestion for every connection on that link.
- explanation-03: On packet loss, the sender lowers ssthresh and cwnd.
- explanation-03: After packet loss, the sender either restarts slow start or enters congestion avoidance, depending on the TCP variant.
- explanation-04: In Python or Ruby, only one thread runs Python bytecode at a time.
- explanation-04: Memory, CPU, and file descriptor limits cannot be capped per thread.
- explanation-04: Erlang's BEAM uses independent restart of workers at the process level.
- explanation-04: Application servers like Gunicorn and PM2 use the model of independently restarting failed workers.
- explanation-04: Communicating between processes through IPC is slower and uses more memory than sharing memory directly between threads.
- explanation-05: A cache keyed by user session that never expires entries holds onto session data long after the session ends.
- explanation-05: A global event bus is an example of a long-lived object that components register listeners on.
- explanation-06: A cache adds operational overhead because it means running and monitoring another system.
- explanation-06: Redis and Memcached are examples of cache systems.
- explanation-06: A cache can go down or return stale data, which must be handled.
- explanation-07: Sharding solves a working set that no longer fits in memory.
- explanation-07: A wrong shard key causes hot shards and cross-shard queries later.
- explanation-07: Storage nearing the limits of backup and maintenance windows is an example of a hard limit.
- explanation-07: Write latency degrading under load is an example of a hard limit.
- explanation-08: Any performance number given without measurements would be a guess rather than an estimate.
- explanation-08: Binary formats gain the most on data with many small numeric fields.
- explanation-08: The gain from binary formats shrinks on text-heavy payloads.
- explanation-08: Smaller payloads help more on constrained connections than on fast internal links.
- summarization-01: The release includes a build tooling update.
- summarization-01: The release includes a session module refactor.
- summarization-01: The release includes a telemetry batching change.
- summarization-01: The build tooling update, session module refactor, and telemetry batching change are internal and do not affect app behavior.
- summarization-01: The build tooling update, session module refactor, and telemetry batching change were omitted from the release notes.
- summarization-01: The task is a one-off summarization task that needs no prior context.
- summarization-02: Detection and response during the incident were fast.
- summarization-02: The page fired 7 minutes after the errors started.
- summarization-02: The rollback resolved the issue within 34 minutes of the page.
- summarization-04: The reporter clicked Export (PDF) several times.
- summarization-04: The expected result is that the PDF downloads.
- summarization-04: The expected result is that the PDF matches the working CSV export for the same report.
- summarization-04: Four identical "export failed" error banners appear.
- summarization-08: Finding 2 is characterized as tentative.
- summarization-08: The template gallery observation needs follow-up before it is called a finding.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 21 | 16 | 0.762 | 26 | 4 |
| code-review-02 | 23 | 13 | 0.565 | 21 | 3 |
| code-review-03 | 21 | 12 | 0.571 | 20 | 7 |
| code-review-04 | 22 | 0 | 0.0 | 4 | 4 |
| code-review-05 | 31 | 22 | 0.71 | 29 | 5 |
| code-review-06 | 38 | 28 | 0.737 | 28 | 8 |
| code-review-07 | 37 | 25 | 0.676 | 39 | 11 |
| code-review-08 | 36 | 22 | 0.611 | 39 | 15 |
| debugging-01 | 7 | 7 | 1.0 | 8 | 0 |
| debugging-02 | 9 | 7 | 0.778 | 12 | 1 |
| debugging-03 | 9 | 9 | 1.0 | 13 | 1 |
| debugging-04 | 14 | 13 | 0.929 | 15 | 6 |
| debugging-05 | 16 | 15 | 0.938 | 15 | 2 |
| debugging-06 | 40 | 0 | 0.0 | 10 | 10 |
| debugging-07 | 29 | 14 | 0.483 | 23 | 8 |
| debugging-08 | 5 | 0 | 0.0 | 29 | 29 |
| explanation-01 | 32 | 18 | 0.562 | 24 | 0 |
| explanation-02 | 27 | 19 | 0.704 | 28 | 1 |
| explanation-03 | 32 | 17 | 0.531 | 17 | 1 |
| explanation-04 | 39 | 27 | 0.692 | 30 | 2 |
| explanation-05 | 23 | 17 | 0.739 | 14 | 1 |
| explanation-06 | 25 | 23 | 0.92 | 30 | 3 |
| explanation-07 | 27 | 16 | 0.593 | 26 | 5 |
| explanation-08 | 13 | 9 | 0.692 | 21 | 11 |
| summarization-01 | 5 | 5 | 1.0 | 6 | 0 |
| summarization-02 | 15 | 11 | 0.733 | 17 | 0 |
| summarization-03 | 14 | 14 | 1.0 | 13 | 0 |
| summarization-04 | 13 | 13 | 1.0 | 11 | 1 |
| summarization-05 | 11 | 10 | 0.909 | 11 | 1 |
| summarization-06 | 14 | 14 | 1.0 | 14 | 1 |
| summarization-07 | 18 | 16 | 0.889 | 16 | 1 |
| summarization-08 | 19 | 17 | 0.895 | 25 | 2 |

Median fraction: 0.735 over 32 scored pairs.

Median additions: 2.0 over 32 scored pairs.

Lost facts:

- code-review-01: If `roles` already contains "member", it gets added again because there is no deduplication.
- code-review-01: The `True`/`False` return value does not distinguish between "insert failed," "db not configured," and "bad input."
- code-review-01: Conflating failure modes in the return value makes the function hard to use and debug.
- code-review-01: The suggested fix raises `ValueError("db is required")` when `db` is `None`.
- code-review-01: The suggested fix only adds "member" when it is not already in `roles`.
- code-review-02: Mixing `async`/`await` with `.then()` inconsistently defeats the purpose of the promise chain.
- code-review-02: The inconsistent mixing of `async` and `.then()` makes the race condition bug easy to miss.
- code-review-02: Network failures or non-JSON responses will produce an unhandled promise rejection.
- code-review-02: On an error response, `res.json()` may throw or return an error payload that gets treated as a valid profile.
- code-review-02: A function declared `async` always returns a `Promise`.
- code-review-02: Callers must `await` or `.then()` the function's result regardless of the fix.
- code-review-02: An API could return an error object such as `{ error: "not found" }`.
- code-review-02: The fixed version throws an `Error` with the message `Failed to load user ${userId}: ${res.status}` when `res.ok` is false.
- code-review-02: The fixed version awaits `res.json()` to obtain `profile`.
- code-review-02: The fixed version returns `profile.name.toUpperCase()`.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: A customer name containing a single quote, such as `O'Brien`, breaks the query syntactically.
- code-review-03: The single-quote bug causes errors even without malicious intent.
- code-review-03: The query has no LIMIT clause.
- code-review-03: Without a LIMIT, the query could return unbounded rows for a common customer name.
- code-review-03: Returning unbounded rows can cause memory and performance issues.
- code-review-03: With parameterized queries, the driver handles escaping.
- code-review-03: With parameterized queries, the SQL structure cannot be altered by input.
- code-review-03: Using parameterized queries fixes both the injection risk and the quote-breaking bug in one change.
- code-review-04: The `increment` method is not atomic.
- code-review-04: The `reset` method is not atomic, though to a lesser extent than `increment`.
- code-review-04: The `Counter` class has no locking at all.
- code-review-04: Concurrent use of `Counter` from multiple threads is unsafe.
- code-review-04: In `increment`, `current = self.value` and `self.value = current + 1` are two separate steps.
- code-review-04: Two threads can both read the same `current` value and both write `current + 1`, silently dropping one increment.
- code-review-04: Dropping an increment this way is called a lost update.
- code-review-04: A single `self.value += 1` would not be safe in general either.
- code-review-04: `+=` on an `int` is still a read-modify-write operation at the bytecode level.
- code-review-04: In CPython, `+=` narrows the race window but does not eliminate it.
- code-review-04: There is no `threading.Lock` or similar primitive guarding access to `self.value`.
- code-review-04: Without a synchronization primitive, nothing prevents the described thread interleaving.
- code-review-04: `reset` can run concurrently with `increment`'s read/write pair.
- code-review-04: A reset can be immediately overwritten by an in-flight increment that read the old value before the reset happened.
- code-review-04: An increment can be lost immediately after a reset.
- code-review-04: The class provides no atomic method for reading the current value.
- code-review-04: There is no thread-safe way for callers to read `value` to get a consistent snapshot.
- code-review-04: Reading `counter.value` directly from another thread while it is being mutated is not guaranteed safe outside CPython's GIL guarantees for a single attribute read.
- code-review-04: Relying on GIL semantics for correctness is fragile and implementation-specific.
- code-review-04: The fix is to add a `threading.Lock` to `Counter.__init__` and guard `increment` and `reset` with `with self._lock`.
- code-review-04: Reading the value safely from other threads requires wrapping the read in the same lock, such as in a `get()` method.
- code-review-04: Attribute access without a lock relies on CPython/GIL implementation details rather than a documented guarantee.
- code-review-05: The stderr error from `ls *.log` with no matches is noisy but not fatal.
- code-review-05: Because globbing is not disabled, if no .tmp files exist the literal string `*.tmp` is passed to `rm -rf`.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` causes a harmless 'no such file' error.
- code-review-05: Without error handling, the script prints 'Cleaned' as if everything succeeded.
- code-review-05: Running gzip on a file that already has a .gz counterpart prompts for overwrite confirmation.
- code-review-05: In a non-interactive or cron context, the gzip overwrite prompt can hang or silently fail depending on gzip's behavior.
- code-review-05: `gzip -f` should be used explicitly to avoid the overwrite prompt.
- code-review-05: The 'Cleaned' message is printed unconditionally even if earlier steps failed, giving a false sense of success.
- code-review-05: The script does not validate that BACKUP_DIR is actually a directory before using it.
- code-review-06: There are no relevant saved memory entries or preferences for this task.
- code-review-06: JSON Merge Patch (RFC 7396) uses the convention that `None`/null deletes a key.
- code-review-06: Replacing lists rather than merging them is standard and reasonable behavior.
- code-review-06: Some merge utilities do merge lists rather than replacing them.
- code-review-06: Merging conventions for settings vary widely between codebases.
- code-review-06: An empty dict in `override`, such as `{"key": {}}`, results in `merge_settings(merged[key], {})` returning `merged[key]` unchanged.
- code-review-06: An empty dict override is a no-op rather than a 'clear this sub-dict' operation.
- code-review-06: The function lacks a name/docstring stating its 'settings' semantics.
- code-review-06: The None-as-delete behavior specifically matches RFC 7396.
- code-review-06: The author probably consciously implemented the RFC 7396 pattern but did not document or fully finish it.
- code-review-07: Immediately retrying a struggling server on 5xx is the worse case to leave without backoff.
- code-review-07: The differing backoff treatment could be deliberate, treating 5xx as probably transient and 429 as requiring a cooldown.
- code-review-07: The delay computed on the last loop iteration is wasted because the loop exits immediately afterward with no further attempt.
- code-review-07: The semantics of the `attempts` parameter are ambiguous.
- code-review-07: `attempts = 3` means 3 total calls, not 3 retries following an initial attempt.
- code-review-07: Some callers may assume `attempts` means retries-after-failure and therefore receive one fewer call than expected.
- code-review-07: Nobody knows the history of this code.
- code-review-07: If `attempts` is less than or equal to 0, the loop body never runs and `fn` is never called.
- code-review-07: If `attempts` is less than or equal to 0, the wrapped function silently returns undefined.
- code-review-07: The `attempts <= 0` case is probably not exercised by real callers but is a landmine if someone passes a dynamic value.
- code-review-07: 5xx retrying without backoff and `attempts` meaning total calls are ambiguous as to whether they were deliberate.
- code-review-07: The null/undefined inconsistency, the wasted last-iteration delay, and non-HTTP errors being treated like a legitimate empty result are almost certainly accidental.
- code-review-08: If an export is actively being written, the script will delete that live file mid-write.
- code-review-08: Unconditional deletion of in-progress `.part`/`tmp-` files is the most dangerous issue because it causes data loss rather than mere cleanup.
- code-review-08: The script has no partial-progress logging.
- code-review-08: The 500-item cap and the `removed` counter conflate two unrelated deletion policies.
- code-review-08: The `removed` counter is incremented by both deletion branches.
- code-review-08: If enough tmp/part files are deleted early in the loop, the cap blocks legitimate old-file cleanup for the rest of the run.
- code-review-08: The script has no logging or audit trail.
- code-review-08: There is no record of which files were deleted, when, or why.
- code-review-08: The lack of logging makes any resulting incident hard to diagnose after the fact.
- code-review-08: The module-import cutoff is harmless if the script is re-invoked as a fresh process each run, such as under plain cron.
- code-review-08: The user said they did not set up the schedule.
- code-review-08: Misconfigured `ROOT` or clock skew could make every file look old.
- code-review-08: Deleting `.part` files without a minimum age threshold risks racing an in-progress writer.
- code-review-08: The unconditional `.part`/`tmp-` deletion and the unhandled directory crash are the two issues most likely to cause real incidents.
- debugging-02: `setInterval(function () { ... }.bind(this), 1000)` is an alternative fix.
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` inside it is an alternative fix.
- debugging-04: Encoding can be detected at runtime using the `charset-normalizer` library.
- debugging-05: A prior call can come from another test, from setup code, or from the same test running more than once via a fixture.
- debugging-06: The failure is a connection pool exhaustion issue rather than a code bug in the export job itself.
- debugging-06: The failing batch number varies between occurrences.
- debugging-06: The export job shares a database with an analytics service.
- debugging-06: The waits end exactly at the 30-second timeout ceiling.
- debugging-06: The observed pattern points to resource contention rather than a deterministic logic error.
- debugging-06: The analytics service may saturate the shared connection pool at certain times.
- debugging-06: Scheduled analytics queries such as hourly or nightly rollups can spike concurrent connection usage.
- debugging-06: An analytics connection spike can starve the export job whenever the two overlap.
- debugging-06: The varying batch number is consistent with a cause that depends on wall-clock timing rather than job progress.
- debugging-06: The pool size may be too small for the combined peak load.
- debugging-06: Export, analytics, and other consumers may exceed pool_size plus max_overflow only under specific conditions.
- debugging-06: A slow analytics query holding a connection longer than usual is one such condition.
- debugging-06: A connection leak in one of the services could be the cause.
- debugging-06: A code path that acquires a connection but fails to release it on error causes leaks.
- debugging-06: Unreleased connections on error are common with unhandled exceptions in analytics jobs.
- debugging-06: A connection leak slowly shrinks the effective pool until it is exhausted.
- debugging-06: A leak tied to a rare analytics query or edge-case dataset fits a once-a-week failure cadence.
- debugging-06: A long-running or blocking query holding connections could be the cause.
- debugging-06: A lock wait or large analytics query holding a transaction open causes other connections to queue behind it.
- debugging-06: The database's own max_connections limit may be the actual bottleneck rather than the application pool.
- debugging-06: If the database connection limit is the bottleneck, both services' pools could report healthy while failing to obtain a physical connection.
- debugging-06: Correlating failure timestamps with the analytics job schedule and logs can narrow down the cause.
- debugging-06: Failures clustering around analytics batch windows or its cron schedule would be a strong signal.
- debugging-06: One failure occurred at 02:14:07 on 2026-07-29.
- debugging-06: Cross-referencing analytics logs at 02:14:07 on 2026-07-29 would confirm or rule out the analytics-overlap hypothesis.
- debugging-06: Pool metrics to export include checked-out count, wait queue length, and max pool size.
- debugging-06: Pool metrics should be sampled every few seconds and sent to monitoring.
- debugging-06: With pool metrics in place, the next failure would reveal exactly what was holding connections.
- debugging-06: Logging connection checkout and checkin with a query tag or caller identity reveals who owned the pool at exhaustion time.
- debugging-06: Caller-identity logging for connections is cheap to add and highly diagnostic.
- debugging-06: Checking DB-side pg_stat_activity history or logging can distinguish a real database connection limit from an app-level pool limit.
- debugging-06: Pool usage trending upward over days indicates a leak.
- debugging-06: A sudden spike in pool usage indicates contention.
- debugging-06: Increasing pool size or adding wait-timeout backoff with jitter is a mitigation, not a root-cause fix.
- debugging-06: Such mitigation reduces failure frequency and buys time to instrument.
- debugging-06: Isolating the export job to its own pool or connection budget is possible if the database can support it.
- debugging-06: Separate connection pools per service is often the long-term fix for two services sharing one pool.
- debugging-06: The failure is currently unreproducible.
- debugging-06: Instrumentation with pool metrics and caller tagging is the fastest path to an answer.
- debugging-06: The log lines surrounding the failure are missing, so further log analysis is unlikely to reveal what else was happening.
- debugging-07: No relevant memory was found for this project or codebase.
- debugging-07: The working directory is fresh with no prior context on this codebase.
- debugging-07: Shared cleanup or truncation logic running concurrently can cause missing events.
- debugging-07: When two workers share a test database, a TRUNCATE or teardown from another test can fire between the seed and the assertion and wipe one of the three events.
- debugging-07: Async/eventual-consistency races are a very common cause of intermittent under-counting.
- debugging-07: A LIMIT combined with an unstable or missing ORDER BY can non-deterministically truncate or exclude events under concurrent load.
- debugging-07: If the seed and the digest read use different DB connections or transactions and the isolation level is not read-committed, the read can observe only 2 of the 3 committed rows.
- debugging-07: Connection pooling that reuses a stale connection can cause a read to miss committed rows.
- debugging-07: If failures stop at single-worker execution, that confirms the issue is parallel-worker-related shared state rather than a pure timing bug in the code under test.
- debugging-07: pytest-xdist supports worker_id-scoped databases or schemas to give each worker its own test database.
- debugging-07: A single test database shared across workers is the prime suspect for the flake.
- debugging-07: A consistently missing last-inserted event points to a race, while a randomly missing event points to cross-test contamination.
- debugging-07: Inspecting the digest query for LIMIT, missing ORDER BY, or time-window/status filters is a five-minute code read.
- debugging-07: Inspecting the digest query can immediately confirm or eliminate the ordering/LIMIT and time-window hypotheses.
- debugging-07: Checking DB fixture isolation and the digest query's filtering logic are both quick to inspect and would explain the intermittent under-count without reproducing the failure.
- debugging-08: The speaker intends to check whether actual code exists to ground the discussion in.
- debugging-08: The Bash tool is invoked.
- debugging-08: The command executed is `ls -la /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac`.
- debugging-08: The path /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac is the target of the listing command.
- debugging-08: The stated description of the command is that it lists working directory contents.
- explanation-01: A hash map that does not handle collisions will overwrite or lose data.
- explanation-01: The collection in a separate chaining bucket is usually a linked list, and sometimes a tree.
- explanation-01: Insert in separate chaining hashes the key and appends to the bucket's list, first checking if the key already exists in order to update rather than duplicate.
- explanation-01: Quadratic probing tries index + 1², index + 2², index + 3², and so on.
- explanation-01: Double hashing uses a second hash function to decide the step size.
- explanation-01: Chaining has worse cache performance because linked list nodes are scattered in memory.
- explanation-01: Open addressing has better cache performance because data is packed in a contiguous array.
- explanation-01: Chaining degrades gracefully even above a load factor of 1.0 because buckets just grow.
- explanation-01: Open addressing must keep the load factor well below 1.0 and needs resizing sooner.
- explanation-01: Chaining's worst case is O(n) per bucket if the hash function is bad.
- explanation-01: Clustering in open addressing can cause long probe sequences.
- explanation-01: Open addressing tends to win on raw performance for small, primitive keys such as integers and short strings.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Python's dict uses open addressing.
- explanation-02: A user editing their profile is an example workload suited to optimistic locking.
- explanation-02: Optimistic locking avoids holding locks during slow operations such as user think-time between read and write.
- explanation-02: Pessimistic locking sometimes prevents others from even reading the locked row.
- explanation-02: SELECT ... FOR UPDATE locks the row so a concurrent transfer can't read or modify the same balance until the first transaction commits or rolls back.
- explanation-02: Inventory decrement for a limited-stock item at checkout is an example use case for pessimistic locking.
- explanation-02: Pessimistic locking avoids wasted retries.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-02: Money and limited inventory are examples where the cost of a failed or retried transaction is high.
- explanation-03: A network path might be a fast local link or a congested trans-continental route through routers with limited buffer space.
- explanation-03: Overwhelming a router's buffer causes a burst of packet loss, retransmissions, and wasted bandwidth.
- explanation-03: This phenomenon is called congestion collapse.
- explanation-03: Congestion collapse was a real problem on the early internet in the late 1980s.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The initial cwnd was historically 1 segment.
- explanation-03: The initial cwnd is now typically 10 segments per RFC 6928.
- explanation-03: Congestion avoidance growth is typically additive, at +1 segment per RTT.
- explanation-03: Exponential growth is efficient because linear growth from a small starting point could take a very long time to ramp up to the available bandwidth on a fast link.
- explanation-03: Linear growth from a small starting point would waste capacity on a fast link.
- explanation-03: Exponential growth means slow start will overshoot and cause a loss event fairly soon after starting.
- explanation-03: Overshooting and causing a loss event during slow start is expected and intentional.
- explanation-03: After a loss event, TCP backs off and moves into the congestion avoidance phase.
- explanation-03: Moving to congestion avoidance prevents TCP from repeatedly hitting the capacity ceiling at full speed.
- explanation-04: A process has its own memory address space, file descriptors, and OS resources.
- explanation-04: All threads in a process share the same memory address space, heap, and file descriptors.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Thread communication requires careful synchronization with locks and mutexes to avoid race conditions.
- explanation-04: Each process gets its own interpreter and its own GIL.
- explanation-04: Processes have separate memory spaces enforced by the OS via virtual memory and the MMU.
- explanation-04: Processes can be distributed across machines.
- explanation-04: Processes can run under different resource limits such as cgroups and ulimits.
- explanation-04: Process-based architecture maps naturally to microservices and worker-pool architectures.
- explanation-04: Using processes for tasks that don't share much data eliminates race conditions and deadlocks by construction, because there is no shared memory to corrupt.
- explanation-04: Threads generally win when tasks are I/O-bound, such as waiting on network or disk.
- explanation-04: For I/O-bound tasks, the GIL or lock is not the bottleneck.
- explanation-05: Global variables, active stack frames, and static fields are examples of garbage collection roots.
- explanation-05: Accumulated unreachable-but-retained objects cause memory usage to grow unbounded over time.
- explanation-05: Event handlers often capture a reference to an object, such as `this` or a closure over local state.
- explanation-05: Listener leaks are especially common with observer patterns, DOM event listeners, and subscriptions to long-lived singletons.
- explanation-05: Closures capturing more than intended are a frequent cause of memory leaks.
- explanation-05: Thread-locals that outlive their thread pool's task lifecycle are a frequent cause of memory leaks.
- explanation-06: Deciding to add a cache without knowing the actual bottleneck is the real risk, not the cache itself.
- explanation-06: An APM tool can quickly show where time is going.
- explanation-07: The real constraint on a database may be disk size, write throughput (IOPS), CPU/query load, or connection count.
- explanation-07: If reads dominate the workload, read replicas or caching solve most scaling problems without changing the data model.
- explanation-07: Cheaper alternatives to sharding include indexing, native Postgres table partitioning, vertical scaling, read replicas, connection pooling, and archiving old data.
- explanation-07: These cheaper alternatives often provide 10-50x headroom before sharding is needed.
- explanation-07: Foreign keys do not work across shards, and distributed transactions are required.
- explanation-07: Sharding reduces team velocity.
- explanation-07: Staying single-instance too long risks hitting walls such as disk exhaustion, replication lag, or vacuum failing to keep up on huge tables.
- explanation-07: Some database failure modes, such as autovacuum falling behind on huge tables and index bloat, creep up slowly and appear fine until they are not.
- explanation-07: Postgres supports native table partitioning.
- explanation-07: Postgres-native partitioning is cheap, somewhat reversible, and significantly delays the sharding decision.
- explanation-07: Monitoring should cover disk growth, query latency percentiles, and connection saturation.
- explanation-08: A binary format typically reduces payload size.
- explanation-08: The actual benefit depends on how hot the code path is.
- explanation-08: Migrating to a binary format touches the whole API surface.
- explanation-08: Schemas, client compatibility, and debugging tooling all become more expensive with binary formats.
- summarization-02: A deployment on the prior evening reduced the checkout service's database connection pool size from 50 to 5.
- summarization-02: Staging intentionally uses smaller connection pools than production.
- summarization-02: The configuration review checklist does not check other environment-sensitive settings.
- summarization-02: The gap in the review checklist allowed the change to be merged without scrutiny.
- summarization-05: Ada is assigned to confirm with the mobile team's lead whether the mobile team has been informed about the API deprecation.
- summarization-07: No relevant memory was found for this task.
- summarization-07: Apart from the median latency drop and the memory increase, everything else is uncertain.
- summarization-08: It is not yet confirmed whether the progress bar problem is purely a perception/UI issue.
- summarization-08: The progress bar cause warrants follow-up investigation.

Added facts (styled only):

- code-review-01: The problems are listed in order of severity.
- code-review-01: The mutable default argument can be fixed by using `roles=None` and setting `roles = roles or []` inside the function.
- code-review-01: The exception should be logged before returning `False`.
- code-review-01: Problems 1 through 3 should be fixed first.
- code-review-02: Without `await`, the `async` keyword adds nothing useful in this function.
- code-review-02: Only network errors cause a `fetch` promise to reject.
- code-review-02: The fixed version throws an `Error` when `data.name` is missing.
- code-review-03: The memory contained nothing specific to this task.
- code-review-03: Only the needed columns should be listed in the query.
- code-review-03: The function has no error handling.
- code-review-03: If cursor.execute() fails, the exception propagates with no context about what the function was doing.
- code-review-03: Bad connections and lock timeouts are examples of failures cursor.execute() can raise.
- code-review-03: The function has no type hints.
- code-review-03: Adding type hints such as cursor: Cursor, customer_name: str, status: str would make the function's contract clearer.
- code-review-04: The speaker will check their memory for saved preferences.
- code-review-04: The memory check happens before the review is performed.
- code-review-04: A memory index file named MEMORY.md is located at /var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-config-pairs-7y1ab910/projects/-private-var-folders-tt-jh9lk8gs6-sfn5fhz4rp7pch0000gn-T-style-pairs-370xicac/memory/MEMORY.md
- code-review-04: The speaker reads that MEMORY.md file.
- code-review-05: `$1`, `$BACKUP_DIR`, and `$f` are all used without quotes in the script.
- code-review-05: If no `.log` files exist, the literal string `*.log` is passed to `gzip`, causing another error.
- code-review-05: `set -e` has quirks around loops and conditionals.
- code-review-05: The `-r` (recursive) flag is not needed for a `*.tmp` glob unless matching directories are expected.
- code-review-05: Dropping `-r` from `rm` reduces the blast radius if something unexpected matches.
- code-review-06: The crash on a dict value overridden by a non-dict value is the most serious issue in `merge_settings`.
- code-review-06: If a key exists only in `override` and its value is a dict, that dict is inserted into `merged` by reference.
- code-review-06: Mutating `merged[key]` for such an aliased dict would also change the original `override` dict.
- code-review-06: The dict-replaces-plain-value behavior is a deliberate default reflecting 'override takes priority'.
- code-review-06: The function performs no input validation.
- code-review-06: If `base` is not dict-like, `dict(base)` may fail unexpectedly.
- code-review-06: Bugs #2 and #3 could cause hard-to-trace mutation bugs elsewhere in the codebase.
- code-review-06: The recommended order of work is to write tests pinning down current behavior, especially the `None`-deletes-key rule, then fix bug #1 because it is an outright crash.
- code-review-07: The helper function has one serious bug and several risky design choices.
- code-review-07: The intended backoff expression was probably 1000 * (i + 1).
- code-review-07: Treating rate limits and server errors as retryable is a common and reasonable retry policy.
- code-review-07: Rate limits and server errors are often transient.
- code-review-07: Client errors like 400 or 404 usually are not transient.
- code-review-07: The retry policy of retrying 429 and 5xx is defensible.
- code-review-07: Returning null on a fatal error could be an intentional contract but is undocumented.
- code-review-07: Waiting 1000 * i milliseconds is simple and might be intentional.
- code-review-07: The recommendation is to always rethrow, or wrap and rethrow, the original error when giving up instead of returning null or undefined.
- code-review-07: The recommendation is to fix the backoff to 1000 * (i + 1) and apply a delay to the 5xx path as well.
- code-review-07: Errors without a .status property are usually bugs rather than HTTP failures and should propagate.
- code-review-08: The module is loaded once, and the schedule likely keeps the process alive or reloads it rarely.
- code-review-08: The cutoff calculation should be moved inside clean().
- code-review-08: A file can disappear between listdir() and the check due to another process, a symlink, or a concurrent run.
- code-review-08: Symlinks and directories aren't handled by the script.
- code-review-08: os.listdir() does not guarantee sorted order.
- code-review-08: Which files survive when the cap is hit is essentially random from run to run.
- code-review-08: Continuing to iterate after the cap is hit is wasted work but not a correctness bug by itself.
- code-review-08: 45 days is a normal export-retention period.
- code-review-08: Matching on a tmp- prefix and a .part suffix is a common pattern for files that are always safe to delete regardless of age.
- code-review-08: Treating tmp-/.part files as exempt from the cutoff and the cap is probably intentional.
- code-review-08: Recommended fix: compute the cutoff inside clean(), not at module load.
- code-review-08: Recommended fix: apply the 500-item cap to all deletions and break out of the loop once it is hit.
- code-review-08: Recommended fix: sort os.listdir() results, for example oldest-first by mtime, before applying the cap.
- code-review-08: Sorting the listing before applying the cap makes which files get removed predictable.
- code-review-08: Recommended items 2-4 are the priority because they can crash silently or delete more than intended.
- debugging-02: In strict mode, `this` in that callback is `undefined` instead of the global object.
- debugging-03: This is a common off-by-one error.
- debugging-04: The error message reports byte 0xc3 at position 512.
- debugging-04: "é" and "ñ" are examples of characters whose UTF-8 encoding begins with the lead byte 0xc3.
- debugging-04: "ignore" is another accepted value for open's errors parameter.
- debugging-04: The chardet library provides a detect function that guesses a file's encoding from its bytes.
- debugging-04: chardet.detect returns a result containing an "encoding" key.
- debugging-04: Opening a file in "rb" mode reads it as bytes.
- debugging-05: When the full suite is run, other tests that call `make_post` earlier have already appended `"post"` to the shared list.
- debugging-05: With the fix, no test can leak state into another test.
- debugging-06: The assistant is checking whether the current working directory contains the export job's code.
- debugging-06: Determining whether the working directory has the export job's code could confirm which cause applies.
- debugging-06: A bash tool call is issued to search the filesystem.
- debugging-06: The command uses `find` starting from the current directory with a maximum depth of 3.
- debugging-06: The search is restricted to regular files.
- debugging-06: The search matches files with the extensions .py, .yml, .yaml, .json, .toml, and .conf.
- debugging-06: The extension matching is case-insensitive (uses -iname).
- debugging-06: Errors from the find command are suppressed by redirecting stderr to /dev/null.
- debugging-06: The command output is limited to the first 50 lines via `head -50`.
- debugging-06: The stated purpose of the command is to look for project files related to the export job.
- debugging-07: If tests share a database connection pool of limited size, a busy CI run under four workers can cause a transaction to commit late or roll back unexpectedly.
- debugging-07: Running the full suite locally with four workers in a loop of 50-100 times can confirm whether parallelism is the trigger.
- debugging-07: Most CI runners allow artifacts to be enabled per job or per test.
- debugging-07: Hardcoded IDs, filenames, queue names, or 'current time' calls that aren't unique per test are the most common root cause of this symptom.
- debugging-07: The correct fix for an ingestion/digest race is to change the real code to wait on completion rather than permanently keeping the retry in the test.
- debugging-07: The failing test is named test_digest_contains_all_events.
- debugging-07: If the suspect test still fails when run many times in parallel with itself, the bug lies in the test or digest logic rather than cross-test contamination.
- debugging-07: Reproducing the failure under four parallel workers locally is the recommended first step.
- debugging-08: A cache described as "size-bounded" often bounds by entry count or a rough byte estimate rather than actual retained memory.
- debugging-08: If product data payloads grow to include more fields, larger images, or campaign-specific data, each cache entry uses more memory even when the entry count limit is unchanged.
- debugging-08: A cache's actual heap footprint can be logged over time, separately from entry count.
- debugging-08: A heap histogram can be used to sum retained size for cache entry classes.
- debugging-08: Measured cache memory use can be compared against the cache's configured bound.
- debugging-08: The canary instance receives no webhook traffic.
- debugging-08: The canary instance still grows in memory use.
- debugging-08: At least one leak source is unrelated to webhooks.
- debugging-08: Scheduled jobs and background sync are examples of components that are always active.
- debugging-08: Memory growth is faster during marketing campaigns.
- debugging-08: Faster growth during marketing campaigns suggests a second leak source tied to webhook or campaign-driven traffic.
- debugging-08: Event listeners, request-scoped objects, and session data are possible sources of uncleaned memory.
- debugging-08: Heap growth rate on the canary can be compared against a normal instance under matching non-webhook load.
- debugging-08: Heap dumps taken before and after a campaign burst can be diffed by object counts per class.
- debugging-08: Caches may use soft references or weak references.
- debugging-08: An LRU list can remove a map entry while leaving listeners, timers, or thread-locals attached to the evicted object.
- debugging-08: Cache entries can outlive their cache slot if other structures still reference them.
- debugging-08: A manual eviction sweep can be forced, followed immediately by a heap dump.
- debugging-08: A heap dump can show whether evicted objects are still reachable and reveal their reference chain to garbage collection roots.
- debugging-08: Memory growth that survives quiet nights and never returns to baseline could be off-heap memory.
- debugging-08: Connection pool buffers, native library allocations, and thread pools are possible sources of off-heap growth.
- debugging-08: Thread pools can grow under load and not shrink back.
- debugging-08: No heap profile currently exists for the system.
- debugging-08: RSS stands for resident set size.
- debugging-08: If RSS grows faster than the runtime heap, the growth is off-heap.
- debugging-08: `pmap` and `jcmd VM.native_memory` can isolate native allocations.
- debugging-08: Taking a heap profile is the highest-value next step given that none exists.
- debugging-08: The recommended approach is to take one heap dump mid-week after a few days of growth and one right after a restart, then diff retained size by class.
- debugging-08: Diffing heap dumps by retained size per class would confirm or rule out most of the listed causes directly.
- explanation-02: A wiki page edit is an example of optimistic locking.
- explanation-03: Packet pile-up and loss can happen when many connections share the same network.
- explanation-04: Strong security boundaries matter when running untrusted code, such as browser extensions or plugins.
- explanation-04: Web servers often run worker processes that can be restarted individually if they hang or leak memory, without affecting other workers.
- explanation-05: Leaks from forgotten listeners are especially common in long-running apps such as web pages or servers, where listeners pile up over time.
- explanation-06: Database logs or a query analyzer can be used to find the slowest queries.
- explanation-06: Cache invalidation is one of the hardest problems in software.
- explanation-06: The read-to-write numbers and slowest endpoints should be brought back to the team.
- explanation-07: A single well-tuned PostgreSQL instance can often handle tens of thousands of writes per second, depending on workload.
- explanation-07: Re-sharding later is much harder than sharding the first time.
- explanation-07: It is hard to return to a single instance once application code assumes many shards.
- explanation-07: Choosing a shard key in advance lets schema and queries be shard-ready before sharding happens.
- explanation-07: A concrete threshold such as 80% of disk capacity or write latency exceeding a set value can be used as a trigger to start a sharding project.
- explanation-08: A binary format will likely help performance.
- explanation-08: Payload size determines whether switching to a binary format matters at all.
- explanation-08: If JSON payloads are small (a few KB), network and application logic dominate request time.
- explanation-08: With small payloads, a binary format will barely improve performance.
- explanation-08: If payloads are large (hundreds of KB or more), the savings from a binary format could be real.
- explanation-08: If serialization takes 5% of a request, a 10x faster format saves about 4.5% of total time.
- explanation-08: If serialization takes 40% of a request, a faster format could cut request time nearly in half.
- explanation-08: Payload sizes can be measured by logging or sampling request and response sizes in production across a range of endpoints.
- explanation-08: Most languages have built-in profilers.
- explanation-08: Serialization calls can be wrapped with timers to measure their duration.
- explanation-08: A benchmark can serialize and deserialize a representative payload with both the current JSON library and a candidate binary format for comparison.
- summarization-04: The problem occurs on two different machines.
- summarization-05: The listed action items came out of Monday's sprint planning.
- summarization-06: No relevant memory was found.
- summarization-07: The summary is one paragraph written for the team lead.
- summarization-08: The progress bar finding is characterized as tentative but worth acting on.
- summarization-08: The admin-versus-user settings preference is not strong enough to report as a finding.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 21 | 19 | 0.905 | 20 | 1 |
| code-review-02 | 23 | 15 | 0.652 | 19 | 1 |
| code-review-03 | 21 | 10 | 0.476 | 22 | 8 |
| code-review-04 | 22 | 14 | 0.636 | 20 | 0 |
| code-review-05 | 31 | 16 | 0.516 | 22 | 0 |
| code-review-06 | 38 | 0 | 0.0 | 4 | 2 |
| debugging-01 | 7 | 7 | 1.0 | 8 | 1 |
| debugging-02 | 9 | 8 | 0.889 | 14 | 1 |
| debugging-03 | 9 | 9 | 1.0 | 8 | 0 |
| debugging-04 | 14 | 13 | 0.929 | 17 | 3 |
| debugging-05 | 16 | 15 | 0.938 | 16 | 0 |
| debugging-06 | 40 | 17 | 0.425 | 33 | 9 |
| debugging-08 | 5 | 0 | 0.0 | 31 | 31 |
| explanation-01 | 32 | 21 | 0.656 | 26 | 0 |
| explanation-02 | 27 | 18 | 0.667 | 28 | 3 |
| explanation-03 | 32 | 18 | 0.562 | 22 | 4 |
| explanation-04 | 39 | 23 | 0.59 | 27 | 3 |
| explanation-05 | 23 | 16 | 0.696 | 14 | 0 |
| explanation-06 | 25 | 15 | 0.6 | 16 | 0 |
| explanation-07 | 27 | 20 | 0.741 | 25 | 7 |
| summarization-01 | 5 | 5 | 1.0 | 5 | 0 |
| summarization-02 | 15 | 7 | 0.467 | 9 | 3 |
| summarization-03 | 14 | 13 | 0.929 | 13 | 0 |
| summarization-04 | 13 | 11 | 0.846 | 11 | 0 |
| summarization-05 | 11 | 10 | 0.909 | 8 | 0 |
| summarization-08 | 19 | 0 | 0.0 | 0 | 0 |

Median fraction: 0.661 over 26 scored pairs.

Median additions: 1.0 over 26 scored pairs.

Lost facts:

- code-review-01: Conflating failure modes in the return value makes the function hard to use and debug.
- code-review-01: The suggested fix builds a new list with `roles + ["member"]` instead of mutating the caller's list.
- code-review-02: Mixing `async`/`await` with `.then()` inconsistently defeats the purpose of the promise chain.
- code-review-02: The inconsistent mixing of `async` and `.then()` makes the race condition bug easy to miss.
- code-review-02: A function declared `async` always returns a `Promise`.
- code-review-02: Callers must `await` or `.then()` the function's result regardless of the fix.
- code-review-02: The code has no null or shape validation on the fetched data.
- code-review-02: There is no check that `data` has a `name` property.
- code-review-02: An API could return an error object such as `{ error: "not found" }`.
- code-review-02: The fixed version throws an `Error` with the message `Failed to load user ${userId}: ${res.status}` when `res.ok` is false.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: A customer name containing a single quote, such as `O'Brien`, breaks the query syntactically.
- code-review-03: The single-quote bug causes errors even without malicious intent.
- code-review-03: `SELECT *` fetches unneeded columns.
- code-review-03: The query has no LIMIT clause.
- code-review-03: Without a LIMIT, the query could return unbounded rows for a common customer name.
- code-review-03: Returning unbounded rows can cause memory and performance issues.
- code-review-03: psycopg2 and MySQLdb use `%s` as the placeholder.
- code-review-03: With parameterized queries, the driver handles escaping.
- code-review-03: With parameterized queries, the SQL structure cannot be altered by input.
- code-review-03: Using parameterized queries fixes both the injection risk and the quote-breaking bug in one change.
- code-review-04: The `reset` method is not atomic, though to a lesser extent than `increment`.
- code-review-04: A single `self.value += 1` would not be safe in general either.
- code-review-04: `+=` on an `int` is still a read-modify-write operation at the bytecode level.
- code-review-04: In CPython, `+=` narrows the race window but does not eliminate it.
- code-review-04: An increment can be lost immediately after a reset.
- code-review-04: Reading `counter.value` directly from another thread while it is being mutated is not guaranteed safe outside CPython's GIL guarantees for a single attribute read.
- code-review-04: Relying on GIL semantics for correctness is fragile and implementation-specific.
- code-review-04: Attribute access without a lock relies on CPython/GIL implementation details rather than a documented guarantee.
- code-review-05: With an empty BACKUP_DIR, `cd $BACKUP_DIR` becomes a plain `cd`, which changes to $HOME.
- code-review-05: After cd'ing to $HOME, the script would run `rm -rf *.tmp` in the user's home directory.
- code-review-05: Parsing `ls` output breaks on filenames with spaces, newlines, or glob characters.
- code-review-05: If no .log files exist, `ls *.log` prints a 'No such file or directory' error to stderr.
- code-review-05: The stderr error from `ls *.log` with no matches is noisy but not fatal.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` causes a harmless 'no such file' error.
- code-review-05: The script does not use `set -e` or `set -u`.
- code-review-05: Without error handling, the script prints 'Cleaned' as if everything succeeded.
- code-review-05: Failures of `gzip $f`, such as disk full or permission denied, are not checked.
- code-review-05: Running gzip on a file that already has a .gz counterpart prompts for overwrite confirmation.
- code-review-05: In a non-interactive or cron context, the gzip overwrite prompt can hang or silently fail depending on gzip's behavior.
- code-review-05: `gzip -f` should be used explicitly to avoid the overwrite prompt.
- code-review-05: The 'Cleaned' message is printed unconditionally even if earlier steps failed, giving a false sense of success.
- code-review-05: The script lacks `set -u` to catch typos and undefined variables.
- code-review-05: In the suggested fix, `[ -e "$f" ] || continue` handles the case where the glob matches nothing.
- code-review-06: There are no relevant saved memory entries or preferences for this task.
- code-review-06: `dict(base)` performs a shallow copy.
- code-review-06: If `override` does not touch a nested dict key, `merged[key]` remains the same object as `base[key]`.
- code-review-06: Because of shallow-copy aliasing, later mutation of a shared nested dict also changes `base`.
- code-review-06: The shallow-copy aliasing is a classic shallow-copy bug.
- code-review-06: The shallow-copy aliasing is likely not intentional.
- code-review-06: In the code, `None` in `override` always means delete the key.
- code-review-06: There is no way to explicitly set a setting's value to `None` via the override.
- code-review-06: Passing `None` is unconditionally interpreted as 'remove this key'.
- code-review-06: The None-as-delete behavior could be intentional, following a common merge/patch convention.
- code-review-06: JSON Merge Patch (RFC 7396) uses the convention that `None`/null deletes a key.
- code-review-06: The None-as-delete behavior is an undocumented API decision.
- code-review-06: The recursive merge only triggers when the value from `base` is a dict.
- code-review-06: The type of `override`'s value is never checked.
- code-review-06: The `isinstance(merged[key], dict)` check inspects `merged[key]` (from base), not `value` (from override).
- code-review-06: If `base[key]` is a dict but `override[key]` is not a dict, the code recurses and crashes when `.items()` is called on a non-dict such as a string.
- code-review-06: If `base[key]` is not a dict but `override[key]` is a dict, the code performs a plain overwrite instead of merging.
- code-review-06: Overwriting when only the override value is a dict is arguably correct behavior.
- code-review-06: The asymmetric type check suggests the type-check logic was not fully thought through.
- code-review-06: The type-check issue is a genuine bug rather than deliberate design.
- code-review-06: A robust implementation would also check `isinstance(value, dict)` or handle the type mismatch explicitly.
- code-review-06: The code has no cycle protection.
- code-review-06: Circular references in `base` or `override` cause infinite recursion.
- code-review-06: The lack of cycle protection is low priority and almost certainly not deliberate.
- code-review-06: Lists in `override` fully replace lists in `base` rather than being concatenated or merged.
- code-review-06: Replacing lists rather than merging them is standard and reasonable behavior.
- code-review-06: Some merge utilities do merge lists rather than replacing them.
- code-review-06: Merging conventions for settings vary widely between codebases.
- code-review-06: An empty dict in `override`, such as `{"key": {}}`, results in `merge_settings(merged[key], {})` returning `merged[key]` unchanged.
- code-review-06: An empty dict override is a no-op rather than a 'clear this sub-dict' operation.
- code-review-06: The function lacks a name/docstring stating its 'settings' semantics.
- code-review-06: Nothing in the code states whether it implements JSON-Merge-Patch-like semantics or bespoke semantics.
- code-review-06: The None-as-delete behavior specifically matches RFC 7396.
- code-review-06: The author probably consciously implemented the RFC 7396 pattern but did not document or fully finish it.
- code-review-06: Recursive merging of nested dicts is intentional and is the point of the function.
- code-review-06: The type-check bug (#3) is the most urgent fix because it can crash in production.
- code-review-06: The shallow-copy aliasing bug (#1) is the most dangerous latent bug because it can silently corrupt `base`.
- code-review-06: The None-as-delete behavior (#2) should be confirmed with stakeholders before changing, since removing it could break intended delete-via-`None` behavior.
- debugging-02: `setInterval(function () { ... }.bind(this), 1000)` is an alternative fix.
- debugging-04: Encoding can be detected at runtime using the `charset-normalizer` library.
- debugging-05: A prior call can come from another test, from setup code, or from the same test running more than once via a fixture.
- debugging-06: The waits end exactly at the 30-second timeout ceiling.
- debugging-06: Export, analytics, and other consumers may exceed pool_size plus max_overflow only under specific conditions.
- debugging-06: A connection leak in one of the services could be the cause.
- debugging-06: A code path that acquires a connection but fails to release it on error causes leaks.
- debugging-06: Unreleased connections on error are common with unhandled exceptions in analytics jobs.
- debugging-06: A connection leak slowly shrinks the effective pool until it is exhausted.
- debugging-06: A leak tied to a rare analytics query or edge-case dataset fits a once-a-week failure cadence.
- debugging-06: The database's own max_connections limit may be the actual bottleneck rather than the application pool.
- debugging-06: If the database connection limit is the bottleneck, both services' pools could report healthy while failing to obtain a physical connection.
- debugging-06: One failure occurred at 02:14:07 on 2026-07-29.
- debugging-06: Cross-referencing analytics logs at 02:14:07 on 2026-07-29 would confirm or rule out the analytics-overlap hypothesis.
- debugging-06: Pool metrics should be sampled every few seconds and sent to monitoring.
- debugging-06: With pool metrics in place, the next failure would reveal exactly what was holding connections.
- debugging-06: Caller-identity logging for connections is cheap to add and highly diagnostic.
- debugging-06: Checking DB-side pg_stat_activity history or logging can distinguish a real database connection limit from an app-level pool limit.
- debugging-06: Pool usage trending upward over days indicates a leak.
- debugging-06: A sudden spike in pool usage indicates contention.
- debugging-06: Such mitigation reduces failure frequency and buys time to instrument.
- debugging-06: Isolating the export job to its own pool or connection budget is possible if the database can support it.
- debugging-06: Separate connection pools per service is often the long-term fix for two services sharing one pool.
- debugging-06: The failure is currently unreproducible.
- debugging-06: Instrumentation with pool metrics and caller tagging is the fastest path to an answer.
- debugging-06: The log lines surrounding the failure are missing, so further log analysis is unlikely to reveal what else was happening.
- debugging-08: The speaker intends to check whether actual code exists to ground the discussion in.
- debugging-08: The Bash tool is invoked.
- debugging-08: The command executed is `ls -la /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac`.
- debugging-08: The path /private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-pairs-370xicac is the target of the listing command.
- debugging-08: The stated description of the command is that it lists working directory contents.
- explanation-01: There are far more possible keys than buckets in a hash map.
- explanation-01: The collection in a separate chaining bucket is usually a linked list, and sometimes a tree.
- explanation-01: Insert in separate chaining hashes the key and appends to the bucket's list, first checking if the key already exists in order to update rather than duplicate.
- explanation-01: Chaining has worse cache performance because linked list nodes are scattered in memory.
- explanation-01: Open addressing has better cache performance because data is packed in a contiguous array.
- explanation-01: Open addressing must keep the load factor well below 1.0 and needs resizing sooner.
- explanation-01: Chaining's worst case is O(n) per bucket if the hash function is bad.
- explanation-01: Clustering in open addressing can cause long probe sequences.
- explanation-01: Open addressing tends to win on raw performance for small, primitive keys such as integers and short strings.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Python's dict uses open addressing.
- explanation-02: A user editing their profile is an example workload suited to optimistic locking.
- explanation-02: A document editor with occasional concurrent edits is an example workload suited to optimistic locking.
- explanation-02: Optimistic locking avoids holding locks during slow operations such as user think-time between read and write.
- explanation-02: Pessimistic locking sometimes prevents others from even reading the locked row.
- explanation-02: SELECT ... FOR UPDATE locks the row so a concurrent transfer can't read or modify the same balance until the first transaction commits or rolls back.
- explanation-02: Pessimistic locking fits high-contention, short-lived critical sections where correctness matters more than throughput.
- explanation-02: Inventory decrement for a limited-stock item at checkout is an example use case for pessimistic locking.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-02: Money and limited inventory are examples where the cost of a failed or retried transaction is high.
- explanation-03: A network path might be a fast local link or a congested trans-continental route through routers with limited buffer space.
- explanation-03: This phenomenon is called congestion collapse.
- explanation-03: Congestion collapse was a real problem on the early internet in the late 1980s.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The initial cwnd was historically 1 segment.
- explanation-03: The initial cwnd is now typically 10 segments per RFC 6928.
- explanation-03: Congestion avoidance growth is typically additive, at +1 segment per RTT.
- explanation-03: Exponential growth is efficient because linear growth from a small starting point could take a very long time to ramp up to the available bandwidth on a fast link.
- explanation-03: Linear growth from a small starting point would waste capacity on a fast link.
- explanation-03: Exponential growth means slow start will overshoot and cause a loss event fairly soon after starting.
- explanation-03: Overshooting and causing a loss event during slow start is expected and intentional.
- explanation-03: After a loss event, TCP backs off and moves into the congestion avoidance phase.
- explanation-03: Moving to congestion avoidance prevents TCP from repeatedly hitting the capacity ceiling at full speed.
- explanation-04: A process has its own memory address space, file descriptors, and OS resources.
- explanation-04: All threads in a process share the same memory address space, heap, and file descriptors.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Switching between threads is cheaper than switching between processes.
- explanation-04: Thread communication requires careful synchronization with locks and mutexes to avoid race conditions.
- explanation-04: Process creation cost is high because the OS allocates a new address space.
- explanation-04: Processes communicate via IPC mechanisms such as pipes, sockets, and shared memory.
- explanation-04: Only one thread holds the GIL at a time.
- explanation-04: Each process gets its own interpreter and its own GIL.
- explanation-04: A separate process can be killed and restarted without affecting the rest of the system.
- explanation-04: Processes have separate memory spaces enforced by the OS via virtual memory and the MMU.
- explanation-04: Processes can be distributed across machines.
- explanation-04: Processes can be restarted independently.
- explanation-04: Processes can run under different resource limits such as cgroups and ulimits.
- explanation-04: Process-based architecture maps naturally to microservices and worker-pool architectures.
- explanation-04: Using processes for tasks that don't share much data eliminates race conditions and deadlocks by construction, because there is no shared memory to corrupt.
- explanation-05: If a reference chain exists from a root to an object, the garbage collector treats that object as live.
- explanation-05: Global variables, active stack frames, and static fields are examples of garbage collection roots.
- explanation-05: Accumulated unreachable-but-retained objects cause memory usage to grow unbounded over time.
- explanation-05: A leak in a garbage-collected language is not about forgetting to call free().
- explanation-05: Listener leaks are especially common with observer patterns, DOM event listeners, and subscriptions to long-lived singletons.
- explanation-05: Closures capturing more than intended are a frequent cause of memory leaks.
- explanation-05: Thread-locals that outlive their thread pool's task lifecycle are a frequent cause of memory leaks.
- explanation-06: Adding a cache can add complexity and bugs, such as stale data and invalidation issues.
- explanation-06: Deciding to add a cache without knowing the actual bottleneck is the real risk, not the cache itself.
- explanation-06: Time in an API request can go to the database, an external API call, serialization, or business logic.
- explanation-06: A simple timer or logging around each step can quickly show where time is going.
- explanation-06: An APM tool can quickly show where time is going.
- explanation-06: Database bottlenecks can be caused by missing indexes, full table scans, or over-fetching data.
- explanation-06: A query fix or an index can sometimes give the same speedup as a cache with far less complexity.
- explanation-06: A cache genuinely helps when the data can tolerate being slightly stale, on the order of seconds to minutes.
- explanation-06: A cache does not help or hurts when writes are frequent, because you pay to update the database and also invalidate or update the cache.
- explanation-06: The recommendation is to spend a day profiling and measuring the read/write mix before committing to a caching layer.
- explanation-07: Examples of shard keys include tenant_id and user_id.
- explanation-07: Cheaper alternatives to sharding include indexing, native Postgres table partitioning, vertical scaling, read replicas, connection pooling, and archiving old data.
- explanation-07: These cheaper alternatives often provide 10-50x headroom before sharding is needed.
- explanation-07: Foreign keys do not work across shards, and distributed transactions are required.
- explanation-07: Some database failure modes, such as autovacuum falling behind on huge tables and index bloat, creep up slowly and appear fine until they are not.
- explanation-07: Postgres supports native table partitioning.
- explanation-07: Postgres-native partitioning is cheap, somewhat reversible, and significantly delays the sharding decision.
- summarization-02: A deployment on the prior evening reduced the checkout service's database connection pool size from 50 to 5.
- summarization-02: Staging intentionally uses smaller connection pools than production.
- summarization-02: The pool size reduction caused connection pool exhaustion.
- summarization-02: The incident produced an error rate of approximately 12%.
- summarization-02: The incident lasted approximately 34 minutes.
- summarization-02: The incident ran from 09:14 to 09:48 UTC.
- summarization-02: The configuration review checklist does not check other environment-sensitive settings.
- summarization-02: The gap in the review checklist allowed the change to be merged without scrutiny.
- summarization-03: Synchronous thumbnail generation currently blocks web workers.
- summarization-04: Nothing happens initially after selecting the PDF export option.
- summarization-04: The bug was reproduced on the latest version of Firefox.
- summarization-05: Ada is assigned to confirm with the mobile team's lead whether the mobile team has been informed about the API deprecation.
- summarization-08: The import flow research study had 8 participants.
- summarization-08: All 8 participants found the field-mapping step.
- summarization-08: 6 of 8 participants completed the field-mapping step unassisted.
- summarization-08: The field-mapping redesign is effective, with the finding rated as firm.
- summarization-08: 3 of 8 participants encountered an apparently stuck progress bar on large files.
- summarization-08: 2 of those 3 participants abandoned the import.
- summarization-08: The uploads actually did complete despite the progress bar appearing stuck.
- summarization-08: The abandonment is a real, observed outcome (firm on behavior).
- summarization-08: It is not yet confirmed whether the progress bar problem is purely a perception/UI issue.
- summarization-08: The progress bar cause warrants follow-up investigation.
- summarization-08: A few participant comments suggested admins and regular users may want different default settings.
- summarization-08: With n=8, the admin vs. regular-user preference difference cannot be sized or confirmed as a broader pattern.
- summarization-08: No participant used the new template gallery.
- summarization-08: Non-use of the template gallery could indicate a discoverability problem.
- summarization-08: Non-use of the template gallery could instead mean these particular customers already had templates.
- summarization-08: The cause of the template gallery non-use is unclear.
- summarization-08: The recommendation is to treat the field-mapping finding as validated.
- summarization-08: The recommendation is to prioritize investigating the progress bar issue because of its abandonment impact.
- summarization-08: The recommendation is that findings on admin/user defaults and template gallery usage need a larger or more targeted sample before acting.

Added facts (styled only):

- code-review-01: The suggested fix copies `roles` with `list(roles)`, avoiding the side effect on the caller's list.
- code-review-02: The `async` keyword has no effect in this function.
- code-review-03: A value like `'; DROP TABLE orders; --` can delete data.
- code-review-03: The columns that are needed should be listed explicitly.
- code-review-03: The function has no error handling.
- code-review-03: If `cursor.execute` fails, the function raises an unhandled exception.
- code-review-03: It must be decided whether the caller handles execution failure or whether the function catches it.
- code-review-03: The function has no type hints.
- code-review-03: Type hints for `cursor`, `customer_name`, and `status` improve readability.
- code-review-03: Type hints catch errors early.
- code-review-06: The 'skill' tool was invoked with the command 'auto-memory'.
- code-review-06: The 'skill' tool was invoked with the command 'auto-memory' a second time.
- debugging-01: The corrected `get_url` function returns the f-string `f"http://{cfg['host']}:{cfg['port']}/api"`.
- debugging-02: Inside a regular function called by setInterval, `this` is the global object, or undefined in strict mode.
- debugging-04: The errors="replace" argument to open() skips bad bytes.
- debugging-04: The errors="ignore" argument to open() skips bad bytes.
- debugging-04: Byte 0xc3 is common in UTF-8.
- debugging-06: The retry makes the problem worse.
- debugging-06: A retry occurred at 02:14:08.
- debugging-06: The retry hit the same exhausted pool 33 seconds after the original failure.
- debugging-06: The retry does not solve the root cause.
- debugging-06: The retry only adds more pressure to an already full pool.
- debugging-06: If failures stop after increasing the pool size, this confirms a capacity problem.
- debugging-06: If failures continue after increasing the pool size, this points to a stuck query or lock instead.
- debugging-06: The retry logic should be checked to ensure the retry does not run right after the first failure.
- debugging-06: A short backoff can let the pool recover before the retry.
- debugging-08: The evidence points away from a simple cache overflow.
- debugging-08: The clues show a real memory leak.
- debugging-08: The leak has two sources.
- debugging-08: One leak source is linked to webhook traffic.
- debugging-08: One leak source exists without webhook traffic.
- debugging-08: The cache bound has not changed in a year.
- debugging-08: Memory still grows despite the unchanged cache bound.
- debugging-08: An evicted cache entry can stay alive if another part of the code still holds a reference to it.
- debugging-08: Listeners, callbacks, and secondary indexes are examples of code that can hold references to evicted cache entries.
- debugging-08: If the count of cached-object types exceeds the cache bound, another structure holds old entries.
- debugging-08: The canary instance receives no webhook traffic.
- debugging-08: The canary instance's memory still grows.
- debugging-08: Memory growth survives quiet nights.
- debugging-08: Garbage collection does not reclaim the leaked memory later.
- debugging-08: In Node, a 'MaxListenersExceededWarning' in the logs can indicate a listener leak.
- debugging-08: In Java, `jmap -histo:live` produces a class histogram that can be compared across runs.
- debugging-08: Memory growth is faster in campaign weeks.
- debugging-08: Canary instances with no webhook traffic grow slower than instances that receive webhooks.
- debugging-08: The webhook-correlated growth points to a leak inside the webhook handling path, in addition to the baseline leak.
- debugging-08: Cache entries have different sizes.
- debugging-08: Cache entries are added and evicted often during campaigns.
- debugging-08: Cache churn can fragment the memory allocator.
- debugging-08: Allocator fragmentation causes free memory to sit unused instead of being reused.
- debugging-08: Memory fragmentation would explain why quiet nights do not lower memory usage.
- debugging-08: If heap size stays flat but RSS grows, the allocator holds unused memory rather than the application.
- debugging-08: Some caches, TLS libraries, and buffer pools store data outside the managed heap.
- debugging-08: Off-heap growth does not show up in a heap dump.
- debugging-08: A growing gap between heap-reported memory and total process memory (RSS) points to native memory growth.
- debugging-08: Native buffer pools, TLS session caches, and connection pools may have no eviction of their own.
- debugging-08: The heap dump comparisons in points 1 and 2 give the clearest answer with the least guesswork.
- debugging-08: The webhook load test in point 3 should be run only if the heap dumps do not show a clear cause.
- explanation-02: The assistant has no stored memory about this topic.
- explanation-02: Under optimistic locking, the application must retry after a failed write.
- explanation-02: In the example, an `accounts` table has a `version` column.
- explanation-03: Slow start lets the sender find the available capacity without a burst of loss.
- explanation-03: After a packet loss, the sender reduces the congestion window and adjusts ssthresh.
- explanation-03: The network's signal is a lost packet or a drop in throughput.
- explanation-03: The name "slow start" refers only to the small initial window, not to the growth speed.
- explanation-04: A process can contain one thread or many threads.
- explanation-04: The main difference between processes and threads is memory.
- explanation-04: A thread crash can bring down the whole process because all threads share memory.
- explanation-07: A slow growth rate leaves time before action is required.
- explanation-07: A fast growth rate requires a plan immediately, but not sharding yet.
- explanation-07: Sharding does not fix a slow query or a missing index.
- explanation-07: A wrong shard key causes hot shards.
- explanation-07: Distributed transactions add failure modes.
- explanation-07: Backup and restore times grow with data size.
- explanation-07: Long restore times increase downtime during an incident.
- summarization-02: The team paged the on-call engineer 7 minutes after the first error.
- summarization-02: The team completed the rollback in 27 minutes.
- summarization-02: The incident response worked well.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### clarity-flow

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 2 | 1 | 0 | 1 | 1.0 |
| code-review-03 | 1 | 0 | 0 | 1 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-06 | 11 | 6 | 0 | 5 | 1.0 |
| code-review-07 | 13 | 7 | 2 | 4 | 0.778 |
| code-review-08 | 11 | 8 | 2 | 1 | 0.8 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 4 | 4 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| debugging-06 | 12 | 1 | 1 | 10 | 0.5 |
| debugging-07 | 14 | 11 | 2 | 1 | 0.846 |
| debugging-08 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 1 | 2 | 0 | 0.333 |
| explanation-02 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-03 | 4 | 0 | 1 | 3 | 0.0 |
| explanation-04 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-06 | 3 | 1 | 1 | 1 | 0.5 |
| explanation-07 | 2 | 1 | 1 | 0 | 0.5 |
| explanation-08 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-06 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-07 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-08 | 3 | 3 | 0 | 0 | 1.0 |

Claims: 98 over 32 judged pairs: 54 hedged, 15 certain, 29 absent.

Median survival: 0.8 over 19 scored pairs.

Claims that became certain:

- code-review-05: If the `cd` fails and the script keeps running in the original working directory, executing `rm -rf *.tmp` there could potentially delete the wrong files.
- code-review-07: The lack of jitter risks a thundering herd if many callers retry in lockstep after a shared rate limit.
- code-review-07: I'd flag the caller's inability to distinguish a real bug from a handled failure as the first thing to fix if you touch this file.
- code-review-08: Between os.listdir and os.path.getmtime/os.remove, another process (or a concurrent/overlapping run of this same job) could delete the file first, raising FileNotFoundError and killing the whole run.
- code-review-08: The 500 cap doesn't actually bound total deletions the way it probably should.
- debugging-06: This looks like a connection pool exhaustion issue, not a code bug in the export job itself.
- debugging-07: If the test database is shared across workers rather than one per worker, that is the prime suspect.
- debugging-07: If adding a short poll-until-3-events makes the flake disappear, that strongly confirms an eventual-consistency race rather than data loss.
- explanation-01: In open addressing, you usually mark a deleted slot with a special "deleted" tombstone.
- explanation-01: As a rule of thumb, open addressing tends to win on raw performance for small, primitive keys (integers, short strings) because it keeps data in cache-friendly contiguous memory.
- explanation-02: Pessimistic locking locks the row as soon as you read it, so no one else can modify (or sometimes even read) it until you're done.
- explanation-03: Slow start's job is to quickly ramp up from zero to roughly the right neighborhood of the network's capacity.
- explanation-04: Threads generally win when tasks are I/O-bound (waiting on network/disk, where the GIL/lock isn't the bottleneck), need frequent low-latency communication, or when the overhead of process creation and IPC serialization would dominate the actual work.
- explanation-06: Adding a cache can add complexity/bugs (stale data, invalidation issues) for no benefit if the slowness isn't from repeated reads of the same data hitting the database
- explanation-07: Postgres-native partitioning for your largest/fastest-growing tables is cheap and reversible-ish.

### classic-concise

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-03 | 1 | 0 | 0 | 1 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-06 | 11 | 9 | 0 | 2 | 1.0 |
| code-review-07 | 13 | 7 | 1 | 5 | 0.875 |
| code-review-08 | 11 | 7 | 3 | 1 | 0.7 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 4 | 2 | 1 | 1 | 0.667 |
| debugging-05 | 1 | 0 | 1 | 0 | 0.0 |
| debugging-06 | 12 | 7 | 1 | 4 | 0.875 |
| debugging-07 | 14 | 8 | 1 | 5 | 0.889 |
| debugging-08 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 1 | 2 | 0 | 0.333 |
| explanation-02 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-03 | 4 | 0 | 2 | 2 | 0.0 |
| explanation-04 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-06 | 3 | 2 | 0 | 1 | 1.0 |
| explanation-07 | 2 | 1 | 1 | 0 | 0.5 |
| explanation-08 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-06 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-07 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-08 | 3 | 3 | 0 | 0 | 1.0 |

Claims: 98 over 32 judged pairs: 55 hedged, 18 certain, 25 absent.

Median survival: 0.667 over 19 scored pairs.

Claims that became certain:

- code-review-02: If the user doesn't exist (404) or the server errors (500), `res.json()` will still attempt to run and may throw or return an error payload that gets treated as a valid profile.
- code-review-05: If the `cd` fails and the script keeps running in the original working directory, executing `rm -rf *.tmp` there could potentially delete the wrong files.
- code-review-07: The lack of jitter risks a thundering herd if many callers retry in lockstep after a shared rate limit.
- code-review-08: The six issues listed are likely bugs.
- code-review-08: The interaction between the 500-item cap and the two deletion policies is almost certainly not what was intended, even if each half is deliberate individually.
- code-review-08: The 500 cap doesn't actually bound total deletions the way it probably should.
- debugging-04: Switching the hardcoded "ascii" to "utf-8" is almost certainly the real fix here.
- debugging-05: By the time this test runs in the full suite, `DEFAULT_TAGS` might be `["draft", "post", "post"]` or similar.
- debugging-06: Pool usage trending upward over days before the weekly failure would indicate a leak, while a sudden spike would indicate contention.
- debugging-07: If adding a short poll-until-3-events makes the flake disappear, that strongly confirms an eventual-consistency race rather than data loss.
- explanation-01: Each bucket usually holds a linked list, though sometimes a tree.
- explanation-01: In open addressing, you usually mark a deleted slot with a special "deleted" tombstone.
- explanation-02: Pessimistic locking locks the row as soon as you read it, so no one else can modify (or sometimes even read) it until you're done.
- explanation-03: Every time the sender receives an ACK, it increases cwnd — roughly by one segment per ACK.
- explanation-03: Slow start's job is to quickly ramp up from zero to roughly the right neighborhood of the network's capacity.
- explanation-04: Threads generally win when tasks are I/O-bound (waiting on network/disk, where the GIL/lock isn't the bottleneck), need frequent low-latency communication, or when the overhead of process creation and IPC serialization would dominate the actual work.
- explanation-07: Postgres-native partitioning for your largest/fastest-growing tables is cheap and reversible-ish.
- explanation-08: A binary format (protobuf, msgpack, etc.) typically saves on serialization/deserialization CPU time and payload size.

### developer-docs

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-03 | 1 | 0 | 0 | 1 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 2 | 0 | 0 | 1.0 |
| code-review-06 | 11 | 7 | 0 | 4 | 1.0 |
| code-review-07 | 13 | 0 | 0 | 13 | n/a |
| code-review-08 | 11 | 7 | 4 | 0 | 0.636 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 4 | 4 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 0 | 1 | 0 | 0.0 |
| debugging-06 | 12 | 7 | 1 | 4 | 0.875 |
| debugging-07 | 14 | 9 | 1 | 4 | 0.9 |
| debugging-08 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 2 | 1 | 0 | 0.667 |
| explanation-02 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-03 | 4 | 0 | 2 | 2 | 0.0 |
| explanation-04 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-06 | 3 | 1 | 2 | 0 | 0.333 |
| explanation-07 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-08 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-06 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-07 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-08 | 3 | 3 | 0 | 0 | 1.0 |

Claims: 98 over 32 judged pairs: 51 hedged, 16 certain, 31 absent.

Median survival: 0.771 over 18 scored pairs.

Claims that became certain:

- code-review-02: If the user doesn't exist (404) or the server errors (500), `res.json()` will still attempt to run and may throw or return an error payload that gets treated as a valid profile.
- code-review-08: The six issues listed are likely bugs.
- code-review-08: Between os.listdir and os.path.getmtime/os.remove, another process (or a concurrent/overlapping run of this same job) could delete the file first, raising FileNotFoundError and killing the whole run.
- code-review-08: The 500 cap doesn't actually bound total deletions the way it probably should.
- code-review-08: Bug #1 (unconditional deletion of .part/tmp- files) and #2 (unhandled directories crashing the run) are the ones most likely to cause real incidents.
- debugging-05: By the time this test runs in the full suite, `DEFAULT_TAGS` might be `["draft", "post", "post"]` or similar.
- debugging-06: Pool usage trending upward over days before the weekly failure would indicate a leak, while a sudden spike would indicate contention.
- debugging-07: If adding a short poll-until-3-events makes the flake disappear, that strongly confirms an eventual-consistency race rather than data loss.
- explanation-01: As a rule of thumb, open addressing tends to win on raw performance for small, primitive keys (integers, short strings) because it keeps data in cache-friendly contiguous memory.
- explanation-02: Pessimistic locking locks the row as soon as you read it, so no one else can modify (or sometimes even read) it until you're done.
- explanation-03: Every time the sender receives an ACK, it increases cwnd — roughly by one segment per ACK.
- explanation-03: Slow start's job is to quickly ramp up from zero to roughly the right neighborhood of the network's capacity.
- explanation-04: Threads generally win when tasks are I/O-bound (waiting on network/disk, where the GIL/lock isn't the bottleneck), need frequent low-latency communication, or when the overhead of process creation and IPC serialization would dominate the actual work.
- explanation-06: Adding a cache can add complexity/bugs (stale data, invalidation issues) for no benefit if the slowness isn't from repeated reads of the same data hitting the database
- explanation-06: If the data doesn't confirm read-heavy plus repeated queries, you might add real complexity while the actual bottleneck stays unsolved
- explanation-07: These cheaper levers (indexing, partitioning, vertical scaling, read replicas, connection pooling, archiving) are far cheaper than sharding and often buy you 10-50x before sharding is needed.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 2 | 0 | 2 | 0 | 0.0 |
| code-review-03 | 1 | 0 | 0 | 1 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 1 | 0 | 1 | 1.0 |
| code-review-06 | 11 | 7 | 0 | 4 | 1.0 |
| code-review-07 | 13 | 8 | 1 | 4 | 0.889 |
| code-review-08 | 11 | 6 | 3 | 2 | 0.667 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 4 | 4 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| debugging-06 | 12 | 0 | 0 | 12 | n/a |
| debugging-07 | 14 | 9 | 1 | 4 | 0.9 |
| debugging-08 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 1 | 2 | 0 | 0.333 |
| explanation-02 | 2 | 0 | 2 | 0 | 0.0 |
| explanation-03 | 4 | 1 | 2 | 1 | 0.333 |
| explanation-04 | 1 | 0 | 0 | 1 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-06 | 3 | 3 | 0 | 0 | 1.0 |
| explanation-07 | 2 | 0 | 0 | 2 | n/a |
| explanation-08 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-06 | 4 | 4 | 0 | 0 | 1.0 |
| summarization-07 | 4 | 3 | 1 | 0 | 0.75 |
| summarization-08 | 3 | 3 | 0 | 0 | 1.0 |

Claims: 98 over 32 judged pairs: 52 hedged, 14 certain, 32 absent.

Median survival: 0.95 over 16 scored pairs.

Claims that became certain:

- code-review-02: If the user doesn't exist (404) or the server errors (500), `res.json()` will still attempt to run and may throw or return an error payload that gets treated as a valid profile.
- code-review-02: Even if the fetch succeeded, there's no check that `data` has a `name` property — the API could return an error object like `{ error: "not found" }`.
- code-review-07: I'd flag the caller's inability to distinguish a real bug from a handled failure as the first thing to fix if you touch this file.
- code-review-08: The six issues listed are likely bugs.
- code-review-08: Between os.listdir and os.path.getmtime/os.remove, another process (or a concurrent/overlapping run of this same job) could delete the file first, raising FileNotFoundError and killing the whole run.
- code-review-08: The 500 cap doesn't actually bound total deletions the way it probably should.
- debugging-07: If adding a short poll-until-3-events makes the flake disappear, that strongly confirms an eventual-consistency race rather than data loss.
- explanation-01: Each bucket usually holds a linked list, though sometimes a tree.
- explanation-01: In open addressing, you usually mark a deleted slot with a special "deleted" tombstone.
- explanation-02: Pessimistic locking locks the row as soon as you read it, so no one else can modify (or sometimes even read) it until you're done.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-03: Every time the sender receives an ACK, it increases cwnd — roughly by one segment per ACK.
- explanation-03: Slow start's job is to quickly ramp up from zero to roughly the right neighborhood of the network's capacity.
- summarization-07: Apart from the measured 18% median latency drop and the 60 MB per-worker memory increase, everything else in the comparison is uncertain.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 2 | 1 | 0 | 1 | 1.0 |
| code-review-03 | 1 | 0 | 0 | 1 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 1 | 0 | 1 | 1.0 |
| code-review-06 | 11 | 0 | 0 | 11 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 4 | 1 | 3 | 0 | 0.25 |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| debugging-06 | 12 | 6 | 2 | 4 | 0.75 |
| debugging-08 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 0 | 2 | 1 | 0.0 |
| explanation-02 | 2 | 0 | 2 | 0 | 0.0 |
| explanation-03 | 4 | 0 | 2 | 2 | 0.0 |
| explanation-04 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-06 | 3 | 2 | 0 | 1 | 1.0 |
| explanation-07 | 2 | 0 | 0 | 2 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-08 | 3 | 0 | 0 | 3 | n/a |

Claims: 51 over 26 judged pairs: 12 hedged, 12 certain, 27 absent.

Median survival: 0.5 over 10 scored pairs.

Claims that became certain:

- debugging-04: The non-ASCII byte 0xc3 is likely the start of a UTF-8 sequence for an accented character such as é, à, or ü.
- debugging-04: The encoding that actually matches the file is most likely UTF-8.
- debugging-04: Switching the hardcoded "ascii" to "utf-8" is almost certainly the real fix here.
- debugging-06: If failures cluster around analytics' own batch windows or its cron schedule, that would be a strong signal.
- debugging-06: Cross-referencing analytics' logs at 02:14:07 on 2026-07-29 would confirm or rule this out.
- explanation-01: Each bucket usually holds a linked list, though sometimes a tree.
- explanation-01: In open addressing, you usually mark a deleted slot with a special "deleted" tombstone.
- explanation-02: Pessimistic locking locks the row as soon as you read it, so no one else can modify (or sometimes even read) it until you're done.
- explanation-02: Pessimistic locking risks blocking, deadlocks, and reduced concurrency if locks are held too long.
- explanation-03: Every time the sender receives an ACK, it increases cwnd — roughly by one segment per ACK.
- explanation-03: Slow start's job is to quickly ramp up from zero to roughly the right neighborhood of the network's capacity.
- explanation-04: Threads generally win when tasks are I/O-bound (waiting on network/disk, where the GIL/lock isn't the bottleneck), need frequent low-latency communication, or when the overhead of process creation and IPC serialization would dominate the actual work.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 619, measured: 619.
Mean duration: 14701 ms. Mean wall: 21996 ms. Mean startup: 7295 ms.

## Harness spend

A stored call row holds the token counts of its call: the
uncached input, cache-write input, cache-read input, and
output tokens. The cache-read share is the cache-read total
over the whole input total.

Calls: 619, measured: 619.
Input tokens: 1238 uncached, 1188924 cache write, 1268754 cache read. Output tokens: 621652.
Cache-read share: 0.516.

## Warnings

- technical-simplified/explanation-08: the pair failed the gate, excluded
- technical-simplified/code-review-07: the pair failed the gate, excluded
- technical-simplified/summarization-06: the pair failed the gate, excluded
- technical-simplified/summarization-07: the pair failed the gate, excluded
- technical-simplified/debugging-07: the pair failed the gate, excluded
- technical-simplified/code-review-08: the pair failed the gate, excluded
