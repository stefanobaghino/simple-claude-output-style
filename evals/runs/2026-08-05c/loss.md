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

Judge: opus. Judged on 2026-08-05T17:25:07+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 34 | 22 | 0.647 | 18 | 1 |
| code-review-02 | 15 | 13 | 0.867 | 21 | 2 |
| code-review-03 | 24 | 17 | 0.708 | 22 | 5 |
| code-review-04 | 23 | 19 | 0.826 | 21 | 2 |
| code-review-05 | 36 | 29 | 0.806 | 29 | 1 |
| debugging-01 | 7 | 7 | 1.0 | 10 | 1 |
| debugging-02 | 17 | 12 | 0.706 | 14 | 0 |
| debugging-03 | 9 | 9 | 1.0 | 11 | 0 |
| debugging-04 | 14 | 8 | 0.571 | 11 | 1 |
| debugging-05 | 15 | 15 | 1.0 | 11 | 0 |
| explanation-01 | 34 | 27 | 0.794 | 28 | 5 |
| explanation-02 | 23 | 20 | 0.87 | 23 | 1 |
| explanation-03 | 31 | 21 | 0.677 | 24 | 2 |
| explanation-04 | 35 | 22 | 0.629 | 29 | 2 |
| explanation-05 | 22 | 15 | 0.682 | 13 | 2 |
| summarization-01 | 7 | 7 | 1.0 | 5 | 0 |
| summarization-02 | 18 | 13 | 0.722 | 17 | 4 |
| summarization-03 | 13 | 13 | 1.0 | 15 | 0 |
| summarization-04 | 14 | 13 | 0.929 | 12 | 0 |
| summarization-05 | 9 | 9 | 1.0 | 10 | 3 |

Median fraction: 0.816 over 20 scored pairs.

Median additions: 1.0 over 20 scored pairs.

Lost facts:

- code-review-01: Nothing stops duplicate names from being inserted.
- code-review-01: Nothing stops invalid role values from being inserted.
- code-review-01: If a caller passes their own `roles` list, `add_user` mutates it in place by appending `"member"`.
- code-review-01: Mutating the caller's list can surprise the caller, since they did not ask for their list to be modified.
- code-review-01: There is no duplicate check for `"member"`.
- code-review-01: If `roles` already contains `"member"`, `"member"` gets added again.
- code-review-01: The return value conflates "user added" with "no exception occurred".
- code-review-01: The suggested fix defines `add_user(name, db, roles=None)` and sets `roles = []` when `roles is None`.
- code-review-01: The suggested fix builds a new list with `[*roles, "member"]` when `"member"` is not already in `roles`, otherwise copies with `list(roles)`.
- code-review-01: The suggested fix calls `db.insert({"name": name, "roles": roles})`.
- code-review-01: The recommendation is to drop the default for `db` and make it required.
- code-review-01: The recommendation is to not mutate the caller's list.
- code-review-02: The promise returned by the function rejects with the `TypeError` rather than resolving with a name
- code-review-02: A failed request or non-JSON body will produce an unhandled rejection or silently bad data
- code-review-03: The SQL injection lets an attacker modify arbitrary data.
- code-review-03: The code returns all rows unbounded because the query has no `LIMIT`.
- code-review-03: The absence of a `LIMIT` could result in huge result sets for common name and status combinations.
- code-review-03: The code has no type hints and no docstring.
- code-review-03: The missing type hints and docstring are a minor issue.
- code-review-03: Type hints and a docstring would help callers know the expected types and return shape.
- code-review-03: The SQL injection is the only issue that actually matters in this code.
- code-review-04: The GIL only protects individual bytecode operations, not sequences of them.
- code-review-04: That interleaving can produce a value of `1` right after a reset instead of `0`.
- code-review-04: Reading `self.value` for reporting is not guaranteed to reflect a consistent state relative to concurrent increments and resets.
- code-review-04: In CPython, a single attribute read or write is atomic.
- code-review-05: `rm -rf` on a literal unmatched glob errors out.
- code-review-05: The unmatched-glob error is harmless in this script because the literal filename likely does not exist.
- code-review-05: Unmatched globs are a common source of "rm: cannot remove" surprises and can cause problems with commands like mv and cp.
- code-review-05: The script does not check whether any files were actually processed.
- code-review-05: The script does not distinguish between "nothing to clean" and "cleaned N files."
- code-review-05: `echo Cleaned $BACKUP_DIR` is unquoted.
- code-review-05: The echo statement gives a false success message even if earlier commands silently failed, because there is no `set -e`.
- debugging-02: Class bodies always execute in strict mode
- debugging-02: Accessing `this.seconds` when `this` is `undefined` throws `TypeError: Cannot read properties of undefined (reading 'seconds')`
- debugging-02: In sloppy mode, the code silently sets `NaN` on the global object repeatedly instead of throwing
- debugging-02: `setInterval(function () { ... }.bind(this), 1000)` is an alternative fix
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` is an alternative fix
- debugging-04: UTF-8 is a safe default encoding choice.
- debugging-04: A file might not be valid UTF-8; it could be Latin-1 or a mix of unknown encodings.
- debugging-04: The encoding of a file can be detected using libraries such as chardet or charset-normalizer.
- debugging-04: For counting lines, decoding correctness does not matter, only where line breaks fall.
- debugging-04: Opening the file in binary mode with "rb" and counting iterated lines works for line counting.
- debugging-04: A byte-level approach to counting lines sidesteps encoding issues entirely.
- explanation-01: Quadratic probing and double hashing are open addressing probe sequences.
- explanation-01: Deletion in open addressing cannot simply clear a slot because that might break the probe chain for a later lookup.
- explanation-01: Open addressing implementations typically use a tombstone marker instead of leaving a deleted slot empty.
- explanation-01: Deletion in open addressing is awkward and needs tombstones.
- explanation-01: Python's dict uses a variant of open addressing.
- explanation-01: Rust's HashMap uses a variant of open addressing.
- explanation-01: Open addressing needs a good resize/rehash strategy to avoid performance cliffs as the array fills up.
- explanation-02: Conflicts in optimistic locking are detected via a version column, or a timestamp or hash, at update time.
- explanation-02: Pessimistic locking fits short critical sections where blocking briefly is cheaper than retrying.
- explanation-02: Optimistic locking fits long-lived transactions or user think-time between read and write.
- explanation-03: TCP guarantees reliable delivery.
- explanation-03: A sender that sends data as fast as the receiver's buffer allows can overwhelm a router or link along the path.
- explanation-03: If senders keep pushing harder during loss, the network can collapse into a state of high loss and low throughput.
- explanation-03: The state of high loss and low throughput is called congestion collapse.
- explanation-03: Congestion collapse was a real problem on the early internet in the 1980s.
- explanation-03: There is no direct feedback from routers about their queue depth.
- explanation-03: Congestion avoidance grows the congestion window linearly.
- explanation-03: A path might be a fast local link or a slow congested one across the world.
- explanation-03: Linear growth from a tiny window would take far too long to reach a link's actual capacity.
- explanation-03: Linear growth from a tiny window would waste bandwidth on fast paths.
- explanation-04: A process is an independent instance of a running program with its own memory address space, file descriptors, and OS-level resources.
- explanation-04: Threads in the same process share the same memory address space, open files, and other resources.
- explanation-04: Each thread has its own stack and instruction pointer.
- explanation-04: Context switching between processes is slower than context switching between threads.
- explanation-04: Nginx uses a process-per-worker model.
- explanation-04: Chrome uses a process-per-tab model.
- explanation-04: Ruby historically had a global interpreter lock.
- explanation-04: In Python, threads only help for I/O-bound work.
- explanation-04: Processes can be killed, restarted, resource-limited via cgroups or ulimit, or run on different machines without touching other processes.
- explanation-04: Threads cannot be relocated independently and die with their process.
- explanation-04: Threads sharing memory requires the use of locks.
- explanation-04: Locks bring races, deadlocks, and priority inversion.
- explanation-04: When work is naturally independent, processes sidestep synchronization complexity entirely at the cost of needing explicit IPC for parts that must communicate.
- explanation-05: Long-lived collections include caches, lists, maps, and static or global variables.
- explanation-05: An event-listener list where listeners are added but never unregistered is an example of an accumulating collection leak.
- explanation-05: A second common cause of leaks is closures or callbacks capturing more than they need.
- explanation-05: A closure or callback keeps a reference to its enclosing scope.
- explanation-05: If an enclosing scope contains a large object and the closure is stored somewhere long-lived, the large object stays reachable indefinitely through the closure's captured environment.
- explanation-05: Registering a closure as an event handler that is never removed is an example of storing a closure somewhere long-lived.
- explanation-05: A closure can retain a large object even if the closure only uses a small piece of the captured scope.
- summarization-02: The config review checklist does not cover other environment-sensitive values.
- summarization-02: Paging happened at 09:21, 7 minutes after errors began.
- summarization-02: Rollback completed at 09:48.
- summarization-02: Detection and response were fast.
- summarization-02: Fast detection and response alone are not enough to address the problem.
- summarization-04: Repeated clicks produce multiple stacked "export failed" error banners.

Added facts (styled only):

- code-review-01: Catching a specific exception, such as `except Exception as e`, and logging it is the recommended fix.
- code-review-02: `fetch` does not reject on HTTP error status codes such as 404 or 500.
- code-review-02: `fetch` rejects only on network failure.
- code-review-03: `%s` is the parameter placeholder for MySQL and psycopg2.
- code-review-03: Selecting every column wastes bandwidth.
- code-review-03: If the query fails, the exception propagates with no context about what the function was doing.
- code-review-03: `"pending"`, `"shipped"`, and `"cancelled"` are examples of expected status values.
- code-review-03: An invalid status will silently return zero rows rather than signaling an error.
- code-review-04: Losing updates in `increment` is the main bug.
- code-review-04: In an example where the value starts at 5, thread A reads 5, thread B reads 5, thread A writes 6, and thread B writes 6, so two calls to `increment` raise the value by only 1.
- code-review-05: `cd` fails if the target directory does not exist or the user lacks permission.
- debugging-01: The corrected function get_url(cfg) returns f"http://{cfg['host']}:{cfg['port']}/api".
- debugging-04: The error message points to byte 0xc3 at position 512.
- explanation-01: Chaining's performance stays steady when the hash map is nearly full.
- explanation-01: Most general-purpose hash maps use a form of chaining or a hybrid approach.
- explanation-01: Python's dict uses a form of chaining or a hybrid approach.
- explanation-01: Java's HashMap uses a form of chaining or a hybrid approach.
- explanation-01: Chaining tends to perform more predictably in real-world use.
- explanation-02: Under pessimistic locking, no one else can read or write the locked data until the lock is released.
- explanation-03: Router queues are limited in size.
- explanation-03: Once a router's queue fills up, the router must drop packets.
- explanation-04: Services are often split into separate processes or containers that a supervisor can restart independently if one fails.
- explanation-04: Threads are the right choice when tasks need to share data quickly and safely.
- explanation-05: In a garbage-collected language, a garbage collector runs in the background.
- explanation-05: Leaks from forgotten event listeners or callbacks are common in user interfaces and in long-running applications with event systems.
- summarization-02: The staging config value that reached production broke checkout.
- summarization-02: The incorrect pool setting caused the connection pool to run out.
- summarization-02: The pool exhaustion led to errors for about 12% of requests.
- summarization-02: The incident ran from 09:14 to 09:48 UTC.
- summarization-05: The text is a list of action items from a meeting.
- summarization-05: Ada is assigned to run the payments database migration dry run.
- summarization-05: Ada is assigned to check with the mobile team's lead about whether the mobile team knows about the API deprecation.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 34 | 21 | 0.618 | 25 | 7 |
| code-review-02 | 15 | 12 | 0.8 | 17 | 2 |
| code-review-03 | 24 | 17 | 0.708 | 20 | 4 |
| code-review-04 | 23 | 17 | 0.739 | 19 | 0 |
| code-review-05 | 36 | 23 | 0.639 | 24 | 2 |
| debugging-01 | 7 | 7 | 1.0 | 6 | 1 |
| debugging-02 | 17 | 10 | 0.588 | 14 | 1 |
| debugging-04 | 14 | 10 | 0.714 | 13 | 2 |
| debugging-05 | 15 | 14 | 0.933 | 13 | 0 |
| explanation-01 | 34 | 15 | 0.441 | 17 | 2 |
| explanation-02 | 23 | 17 | 0.739 | 26 | 5 |
| explanation-03 | 31 | 21 | 0.677 | 22 | 7 |
| explanation-04 | 35 | 19 | 0.543 | 27 | 2 |
| explanation-05 | 22 | 17 | 0.773 | 13 | 0 |
| summarization-01 | 7 | 6 | 0.857 | 6 | 0 |
| summarization-02 | 18 | 8 | 0.444 | 13 | 3 |
| summarization-03 | 13 | 12 | 0.923 | 13 | 0 |
| summarization-04 | 14 | 13 | 0.929 | 12 | 2 |
| summarization-05 | 9 | 9 | 1.0 | 9 | 2 |

Median fraction: 0.739 over 19 scored pairs.

Median additions: 2 over 19 scored pairs.

Lost facts:

- code-review-01: Nothing stops duplicate names from being inserted.
- code-review-01: Nothing stops invalid role values from being inserted.
- code-review-01: If a caller passes their own `roles` list, `add_user` mutates it in place by appending `"member"`.
- code-review-01: Mutating the caller's list can surprise the caller, since they did not ask for their list to be modified.
- code-review-01: There is no duplicate check for `"member"`.
- code-review-01: If `roles` already contains `"member"`, `"member"` gets added again.
- code-review-01: The return value conflates "user added" with "no exception occurred".
- code-review-01: The suggested fix defines `add_user(name, db, roles=None)` and sets `roles = []` when `roles is None`.
- code-review-01: The suggested fix builds a new list with `[*roles, "member"]` when `"member"` is not already in `roles`, otherwise copies with `list(roles)`.
- code-review-01: The recommendation is to drop the default for `db` and make it required.
- code-review-01: The recommendation is to not mutate the caller's list.
- code-review-01: The recommendation is to let exceptions propagate so the caller can see what went wrong.
- code-review-01: Alternatively, the recommendation is to catch a specific exception type if there is a known failure mode to handle.
- code-review-02: The promise returned by the function rejects with the `TypeError` rather than resolving with a name
- code-review-02: The code does not handle `profile.name` being missing or null
- code-review-02: If the API returns a payload without a `name` field, `.toUpperCase()` will throw
- code-review-03: The code has no error handling.
- code-review-03: A failed `cursor.execute` will raise an unhandled exception.
- code-review-03: A bad connection or a lock can cause `cursor.execute` to fail.
- code-review-03: The code has no type hints and no docstring.
- code-review-03: The missing type hints and docstring are a minor issue.
- code-review-03: Type hints and a docstring would help callers know the expected types and return shape.
- code-review-03: The SQL injection is the only issue that actually matters in this code.
- code-review-04: The increment race is a real risk even with Python's GIL.
- code-review-04: The GIL only protects individual bytecode operations, not sequences of them.
- code-review-04: That interleaving can produce a value of `1` right after a reset instead of `0`.
- code-review-04: The code has no atomic operation for reading the current value.
- code-review-04: Reading `self.value` for reporting is not guaranteed to reflect a consistent state relative to concurrent increments and resets.
- code-review-04: In CPython, a single attribute read or write is atomic.
- code-review-05: Unquoted $1 and $BACKUP_DIR are subject to word-splitting and globbing.
- code-review-05: A path starting with `-` (e.g. `-rf`) could be interpreted as a command option.
- code-review-05: `rm -rf` on a literal unmatched glob errors out.
- code-review-05: The unmatched-glob error is harmless in this script because the literal filename likely does not exist.
- code-review-05: Unmatched globs are a common source of "rm: cannot remove" surprises and can cause problems with commands like mv and cp.
- code-review-05: If no .log files exist, `*.log` is passed literally and `gzip` fails with "no such file."
- code-review-05: The script does not check whether any files were actually processed.
- code-review-05: The script does not distinguish between "nothing to clean" and "cleaned N files."
- code-review-05: The script lacks `--` before `gzip $f`.
- code-review-05: If a log filename starts with `-`, gzip will interpret it as a flag.
- code-review-05: `${1:?...}` requires an argument to be supplied.
- code-review-05: `--` guards against dash-prefixed filenames.
- code-review-05: The check `[ -e "$f" ]` prevents an empty glob match from being treated as a literal filename.
- debugging-02: Class bodies always execute in strict mode
- debugging-02: In strict mode, `this` inside such a callback is `undefined`
- debugging-02: Accessing `this.seconds` when `this` is `undefined` throws `TypeError: Cannot read properties of undefined (reading 'seconds')`
- debugging-02: In sloppy mode, the code silently sets `NaN` on the global object repeatedly instead of throwing
- debugging-02: The bug in both strict and sloppy cases is that the callback lost its binding to the Timer instance
- debugging-02: `setInterval(function () { ... }.bind(this), 1000)` is an alternative fix
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` is an alternative fix
- debugging-04: The encoding of a file can be detected using libraries such as chardet or charset-normalizer.
- debugging-04: errors="ignore" is another permissive error handling option.
- debugging-04: Opening the file in binary mode with "rb" and counting iterated lines works for line counting.
- debugging-04: A byte-level approach to counting lines sidesteps encoding issues entirely.
- debugging-05: In the fixed code, `make_post(title, tags=None)` sets `tags = list(DEFAULT_TAGS)` when `tags is None`.
- explanation-01: A hash map's array has finite size while the space of possible keys is much larger.
- explanation-01: Collisions are unavoidable in general due to the pigeonhole principle.
- explanation-01: Every hash map needs a strategy to handle collisions.
- explanation-01: The per-bucket collection in separate chaining is usually a linked list, and sometimes a tree or small array.
- explanation-01: Quadratic probing and double hashing are open addressing probe sequences.
- explanation-01: Deletion in open addressing cannot simply clear a slot because that might break the probe chain for a later lookup.
- explanation-01: Open addressing implementations typically use a tombstone marker instead of leaving a deleted slot empty.
- explanation-01: Open addressing is more cache-friendly and requires no extra pointers.
- explanation-01: Chaining can have a load factor exceeding 1.0 because buckets just grow.
- explanation-01: Open addressing must keep the load factor below 1.0 because the array cannot overflow.
- explanation-01: Deletion in chaining is simple, just removing from a list.
- explanation-01: Deletion in open addressing is awkward and needs tombstones.
- explanation-01: Chaining has worse cache behavior because it chases pointers around memory.
- explanation-01: Open addressing has better cache behavior because data is contiguous in the array.
- explanation-01: Open addressing is faster in practice at small-to-medium load factors because of CPU cache locality.
- explanation-01: Python's dict uses a variant of open addressing.
- explanation-01: Rust's HashMap uses a variant of open addressing.
- explanation-01: Open addressing needs a good resize/rehash strategy to avoid performance cliffs as the array fills up.
- explanation-01: Chaining pays a small constant-factor cost from pointer-chasing and per-node memory overhead.
- explanation-02: Conflicts in optimistic locking are detected via a version column, or a timestamp or hash, at update time.
- explanation-02: Pessimistic locking fits expensive-to-redo work.
- explanation-02: Pessimistic locking fits short critical sections where blocking briefly is cheaper than retrying.
- explanation-02: Seat reservations, inventory decrements, and financial transfers on hot accounts are examples suited to pessimistic locking.
- explanation-02: Optimistic locking fits long-lived transactions or user think-time between read and write.
- explanation-02: Editing a document or user profile is an example suited to optimistic locking, because two people rarely edit the same record at once.
- explanation-03: TCP guarantees reliable delivery.
- explanation-03: When packets are dropped, senders retransmit them.
- explanation-03: If senders keep pushing harder during loss, the network can collapse into a state of high loss and low throughput.
- explanation-03: The state of high loss and low throughput is called congestion collapse.
- explanation-03: Congestion collapse was a real problem on the early internet in the 1980s.
- explanation-03: There is no direct feedback from routers about their queue depth.
- explanation-03: Congestion avoidance grows the congestion window linearly.
- explanation-03: A path might be a fast local link or a slow congested one across the world.
- explanation-03: Linear growth from a tiny window would take far too long to reach a link's actual capacity.
- explanation-03: Linear growth from a tiny window would waste bandwidth on fast paths.
- explanation-04: One process cannot directly read another process's memory.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, and message queues.
- explanation-04: Each thread has its own stack and instruction pointer.
- explanation-04: Context switching between processes is slower than context switching between threads.
- explanation-04: Inter-process communication is explicit and slower than thread communication.
- explanation-04: Nginx uses a process-per-worker model.
- explanation-04: Chrome uses a process-per-tab model.
- explanation-04: Most browsers use a process-per-tab model.
- explanation-04: In a process-per-worker/tab model, one bad renderer or request does not kill the whole browser or server.
- explanation-04: Ruby historically had a global interpreter lock.
- explanation-04: In Python, threads only help for I/O-bound work.
- explanation-04: Processes can be killed, restarted, resource-limited via cgroups or ulimit, or run on different machines without touching other processes.
- explanation-04: Threads cannot be relocated independently and die with their process.
- explanation-04: Threads sharing memory requires the use of locks.
- explanation-04: Locks bring races, deadlocks, and priority inversion.
- explanation-04: When work is naturally independent, processes sidestep synchronization complexity entirely at the cost of needing explicit IPC for parts that must communicate.
- explanation-05: Long-lived collections include caches, lists, maps, and static or global variables.
- explanation-05: An event-listener list where listeners are added but never unregistered is an example of an accumulating collection leak.
- explanation-05: A second common cause of leaks is closures or callbacks capturing more than they need.
- explanation-05: A closure or callback keeps a reference to its enclosing scope.
- explanation-05: A closure can retain a large object even if the closure only uses a small piece of the captured scope.
- summarization-01: Keyboard shortcuts were added for the user's ten most-used actions.
- summarization-02: The staging template intentionally uses smaller values.
- summarization-02: The config review checklist does not cover other environment-sensitive values.
- summarization-02: Errors began at 09:14.
- summarization-02: Paging happened at 09:21, 7 minutes after errors began.
- summarization-02: Rollback completed at 09:48.
- summarization-02: Total impact duration was 34 minutes.
- summarization-02: Detection and response were fast.
- summarization-02: Fast detection and response alone are not enough to address the problem.
- summarization-02: The real fix is preventing the bad config from shipping in the first place.
- summarization-02: A proposed fix is adding pool size and other critical values to the review checklist.
- summarization-03: The proposed change eliminates that delay and worker congestion.
- summarization-04: The bug is reproduced by clicking the "Export" button and selecting the PDF option.

Added facts (styled only):

- code-review-01: The corrected version raises `ValueError` when `name` is empty.
- code-review-01: The corrected version raises `ValueError` when `db` is None.
- code-review-01: The corrected version checks `name` and `db` before using them.
- code-review-01: The corrected version uses `except Exception` instead of a bare `except`.
- code-review-01: The corrected version logs the error with `logging.error`.
- code-review-01: The corrected version returns `True` after a successful `db.insert` call.
- code-review-01: The corrected version returns `False` when an exception is caught.
- code-review-02: The current code returns undefined in practice rather than the profile name.
- code-review-02: The corrected version awaits res.json() and returns data.name.toUpperCase().
- code-review-03: A value like `' OR '1'='1` can cause data to be deleted.
- code-review-03: Returning too many rows can use too much memory.
- code-review-03: With parameterized queries, an unexpected status value returns zero rows.
- code-review-03: Validating input at the boundary would catch a typo early.
- code-review-05: If no `.log` files exist, `ls *.log` prints an error to standard error.
- code-review-05: The `ls *.log` error occurs because the shell does not expand the pattern when no matches exist.
- debugging-01: The corrected function get_url(cfg) returns the f-string "http://{cfg['host']}:{cfg['port']}/api".
- debugging-02: When setInterval calls a normal function, `this` becomes the global object rather than the Timer instance.
- debugging-04: The file has a non-ASCII byte at position 512.
- debugging-04: The replace error handler substitutes bad bytes with a placeholder character.
- explanation-01: Chaining stays fast even when the map is nearly full.
- explanation-01: Most standard libraries use chaining.
- explanation-02: When a user reads the row in the example, the version is 3.
- explanation-02: When the user saves in the example, the update statement includes `WHERE version = 3`.
- explanation-02: Double withdrawal from an account is an example of a conflict causing serious harm.
- explanation-02: Optimistic locking acquires locks at write time.
- explanation-02: Pessimistic locking is best suited to high contention and high risk of data loss.
- explanation-03: Routers filling their queues and dropping packets causes congestion.
- explanation-03: At the start of a connection, the sender sends only a few packets, often two to ten.
- explanation-03: In the first round trip, the sender sends two packets.
- explanation-03: In the second round trip, the sender sends four packets.
- explanation-03: In the third round trip, the sender sends eight packets.
- explanation-03: When the sender detects packet loss, TCP reduces the congestion window.
- explanation-03: When the sender detects packet loss, TCP can restart slow start from a small value.
- explanation-04: A process can contain one thread or many threads.
- explanation-04: A crash in one thread can corrupt shared memory and crash the whole process.
- summarization-02: An alert should be added for database connection pool use.
- summarization-02: A pool exhaustion alert can page the on-call engineer before the error rate rises.
- summarization-02: A pool exhaustion alert can reduce the seven-minute delay between incident start and page.
- summarization-04: After waiting a few seconds following the click, no export starts.
- summarization-04: Four "export failed" error banners appear at once.
- summarization-05: Ada is assigned to run the payments database migration dry run.
- summarization-05: Ada's payments migration dry run is due before Thursday.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 1 | 0 | 0 | 1 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 4 | 0 | 1 | 3 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 2 | 1 | 0 | 0.667 |
| debugging-05 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-01 | 4 | 1 | 1 | 2 | 0.5 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 2 | 1 | 0 | 1 | 1.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.5 over 5 scored pairs.

Claims that became certain:

- code-review-05: If `$1` is empty, unset, or contains spaces/globs, `cd` can fail silently or go somewhere unexpected.
- debugging-04: Since you only need a line count, `errors="replace"` (or even `errors="ignore"`) is often fine.
- debugging-05: By the time this test runs, DEFAULT_TAGS might be ["draft", "post", "post"] or similar, so the assertion fails.
- explanation-01: As a rule of thumb, open addressing is faster in practice for small-to-medium load factors because of CPU cache locality.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 1 | 1 | 0 | 0 | 1.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 4 | 0 | 1 | 3 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 2 | 1 | 0 | 0.667 |
| debugging-05 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-01 | 4 | 0 | 0 | 4 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 5 scored pairs.

Claims that became certain:

- code-review-05: If `$1` is empty, unset, or contains spaces/globs, `cd` can fail silently or go somewhere unexpected.
- debugging-04: Since you only need a line count, `errors="replace"` (or even `errors="ignore"`) is often fine.
- debugging-05: By the time this test runs, DEFAULT_TAGS might be ["draft", "post", "post"] or similar, so the assertion fails.
- explanation-03: If a sender just blasted data as fast as the receiver's buffer allowed, it could easily overwhelm a router or link somewhere in the middle of the path.

## Warnings

- technical-simplified/debugging-03: the pair failed the gate, excluded
