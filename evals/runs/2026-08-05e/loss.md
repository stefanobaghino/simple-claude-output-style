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

Judge: opus. Judged on 2026-08-05T21:09:20+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 26 | 18 | 0.692 | 17 | 2 |
| code-review-02 | 20 | 17 | 0.85 | 21 | 3 |
| code-review-03 | 27 | 21 | 0.778 | 25 | 4 |
| code-review-04 | 20 | 10 | 0.5 | 22 | 0 |
| code-review-05 | 37 | 27 | 0.73 | 31 | 3 |
| debugging-01 | 7 | 7 | 1.0 | 7 | 0 |
| debugging-02 | 15 | 13 | 0.867 | 14 | 0 |
| debugging-03 | 11 | 11 | 1.0 | 13 | 0 |
| debugging-04 | 15 | 7 | 0.467 | 15 | 7 |
| debugging-05 | 19 | 16 | 0.842 | 16 | 1 |
| explanation-01 | 33 | 23 | 0.697 | 27 | 3 |
| explanation-02 | 22 | 22 | 1.0 | 31 | 2 |
| explanation-03 | 32 | 18 | 0.562 | 24 | 5 |
| explanation-04 | 33 | 21 | 0.636 | 34 | 0 |
| explanation-05 | 18 | 15 | 0.833 | 12 | 0 |
| summarization-01 | 5 | 5 | 1.0 | 5 | 0 |
| summarization-02 | 17 | 14 | 0.824 | 18 | 2 |
| summarization-03 | 13 | 13 | 1.0 | 13 | 0 |
| summarization-04 | 15 | 13 | 0.867 | 13 | 1 |
| summarization-05 | 9 | 9 | 1.0 | 7 | 1 |

Median fraction: 0.837 over 20 scored pairs.

Median additions: 1.0 over 20 scored pairs.

Lost facts:

- code-review-01: Mutating the caller's list is a side effect callers likely do not expect.
- code-review-01: If the caller reuses the passed list elsewhere, it will have been silently changed.
- code-review-01: The function implies no transaction or atomicity guarantee.
- code-review-01: Depending on what `db.insert` is, a partial failure state is not handled.
- code-review-01: Whether atomicity is a problem depends more on `db`'s implementation.
- code-review-01: A reasonable rewrite raises `ValueError("db is required")` when `db is None` and `ValueError("name is required")` when `name` is falsy.
- code-review-01: The rewrite copies the input with `roles = list(roles) if roles else []` and appends `"member"` only if it is not already present.
- code-review-01: As an alternative to propagating errors, specific exceptions such as `db`'s known error types can be caught at the call site.
- code-review-02: The userId is interpolated directly into the URL template string without sanitization.
- code-review-02: userId should be run through encodeURIComponent to safely handle special characters.
- code-review-02: If the API response does not include a name field, .toUpperCase() will throw.
- code-review-03: `status` presumably belongs to a fixed set of enum-like values
- code-review-03: An invalid `status` value should probably error early rather than return no rows
- code-review-03: The code calls `fetchall()` on potentially large result sets
- code-review-03: `fetchall()` loads all results into memory at once
- code-review-03: Pagination, `fetchmany`, or iterating the cursor are alternatives to `fetchall()` for large result sets
- code-review-03: The shape of returned rows (tuples vs dict-like) matters to callers
- code-review-04: In CPython, the GIL only guarantees that individual bytecode operations are atomic.
- code-review-04: The load, add, and store in `increment` compile to multiple bytecodes, so CPython can switch threads between them.
- code-review-04: The counter code is unsafe under free-threaded CPython and other implementations such as PyPy, where atomicity guarantees differ.
- code-review-04: Free-threaded CPython is designated 3.13t.
- code-review-04: The class provides no accessor method for reading the value, so callers read `counter.value` directly.
- code-review-04: In CPython, a single attribute read is atomic.
- code-review-04: Without an accessor, there is no single place to enforce consistency of the counter's contract.
- code-review-04: Guarding `increment`, `reset`, and reads with a `threading.Lock` makes them mutually exclusive.
- code-review-04: `itertools.count` is thread-safe in CPython because it is a C-implemented atomic counter.
- code-review-04: `multiprocessing.Value`-style atomics are an alternative to a lock.
- code-review-05: The unchecked `cd` before a recursive `rm -rf` is the most serious bug in the script.
- code-review-05: The recommended idiom is `cd "$DIR" || exit 1`.
- code-review-05: When `*.tmp` stays literal, `rm -rf` attempts to remove a file named `*.tmp` and produces an error.
- code-review-05: The error produced by the literal `*.tmp` is harmless in this script.
- code-review-05: The script should either target POSIX sh strictly or use `#!/usr/bin/env bash` if bash-specific features are wanted.
- code-review-05: `echo Cleaned $BACKUP_DIR` uses an unquoted variable.
- code-review-05: The "Cleaned" output is uninformative because it does not report how many files were compressed or deleted, or any failures.
- code-review-05: The suggested rewrite uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` to enforce an argument.
- code-review-05: The suggested rewrite loops over `*.tmp` and `*.log` with an `[ -e "$f" ]` existence test.
- code-review-05: The single highest-risk issue in the script is the unchecked `cd` preceding the recursive `rm -rf`.
- debugging-02: Calling .bind(this) on a regular-function callback is an alternative fix.
- debugging-02: Capturing `const self = this;` before the interval and referencing `self.seconds` inside the callback is an alternative fix.
- debugging-04: The file being opened contains a non-ASCII byte at byte offset 512.
- debugging-04: Passing errors="replace" to open() makes decoding more robust when the file's encoding is unknown or inconsistent.
- debugging-04: A file's encoding may be inconsistent, for example Latin-1 or UTF-8 depending on the source.
- debugging-04: errors="replace" or errors="ignore" prevents malformed bytes from crashing the operation.
- debugging-04: errors="replace" and errors="ignore" do not preserve the exact original text.
- debugging-04: Keeping encoding="ascii" is appropriate when strict validation that a file is ASCII is required.
- debugging-04: A UnicodeDecodeError is raised when decoding fails under the ascii encoding.
- debugging-04: The UnicodeDecodeError can be caught and handled or reported explicitly instead of being allowed to propagate.
- debugging-05: In the fixed code, tags is reassigned to tags + ["post"].
- debugging-05: The fix copies DEFAULT_TAGS on every call.
- debugging-05: Using + instead of .append avoids mutating the caller's tags list.
- explanation-01: The collection in a separate-chaining slot is usually a linked list, and sometimes a tree.
- explanation-01: Quadratic probing tries index + 1², index + 2², and so on.
- explanation-01: Quadratic probing spreads out clusters.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Separate chaining has worse cache performance because list nodes are scattered in memory.
- explanation-01: Deletion in open addressing usually needs a tombstone marker.
- explanation-01: Separate chaining degrades to an O(n) linked list scan if hashing is bad.
- explanation-01: Python and Rust's HashMap lean toward open addressing or variants of it.
- explanation-01: Chaining is the classic textbook implementation of collision handling.
- explanation-01: Java's HashMap historically used separate chaining.
- explanation-03: The TCP sender maintains a congestion window, abbreviated cwnd.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window protects the receiver from being overwhelmed.
- explanation-03: Historically, TCP connections started with a congestion window of 1 segment.
- explanation-03: Modern TCP typically starts with a congestion window of around 10 segments.
- explanation-03: RFC 6928 specifies the initial congestion window of about 10 segments.
- explanation-03: During slow start the send rate progresses roughly as 10 segments, then ~20, then ~40, then ~80.
- explanation-03: An ECN signal can end slow start in the same way as a packet loss.
- explanation-03: On detecting loss, cwnd is slashed and the connection moves into congestion avoidance.
- explanation-03: Congestion avoidance is a more conservative, linear growth mode.
- explanation-03: Congestion avoidance grows the window by roughly +1 segment per RTT.
- explanation-03: ssthresh stands for slow start threshold.
- explanation-03: ssthresh is often set from a previous congestion event on the same connection.
- explanation-03: Slow start hands off to an additive growth mode once it has found roughly where the network's limit is.
- explanation-04: A process has its own memory address space, file descriptors, and OS-level resources.
- explanation-04: Threads in the same process share the memory address space, open files, and other resources.
- explanation-04: Each thread has its own stack and instruction pointer.
- explanation-04: Thread communication requires synchronization mechanisms such as locks and mutexes to avoid race conditions.
- explanation-04: Chrome uses separate processes for fault isolation.
- explanation-04: Some web servers use per-request worker processes so a single bad request or tab cannot crash the whole system.
- explanation-04: Processes can be given separate resource quotas for CPU and memory via cgroups and ulimits.
- explanation-04: Processes can be scheduled and prioritized by the OS individually.
- explanation-04: Independent process scheduling and resource limits are useful for multi-tenant systems and for killing a runaway task cleanly.
- explanation-04: Processes can span multiple machines using IPC such as sockets.
- explanation-04: Threads cannot span multiple machines; they exist only within a single process on a single machine.
- explanation-04: Processes have a larger memory footprint and more OS overhead than threads.
- explanation-05: Caching results by request ID without removing old entries is an example of an unbounded cache leak.
- explanation-05: Global event buses, DOM elements, and observables are examples of long-lived objects that hold listeners.
- explanation-05: Callbacks often close over a large object graph.
- summarization-02: Errors began at 09:14.
- summarization-02: The total elapsed time from first errors to completed rollback was 34 minutes.
- summarization-02: The config review checklist likely omits other performance-critical settings as well.
- summarization-04: Clicking Export and choosing PDF results in nothing happening.
- summarization-04: Diagnosing the bug may require backend or console logs.

Added facts (styled only):

- code-review-01: The fix for the bare except is to catch a specific exception such as `except Exception as e` and log it.
- code-review-01: The function does not validate that `roles` contains valid role values before inserting.
- code-review-02: Marking a function async only matters if you use await inside it or you want it to return a promise.
- code-review-02: Wrapping the thrown error in a rejected promise hides the real problem.
- code-review-02: The rejection is silently dropped.
- code-review-03: The function builds its SQL query by joining strings with the + operator.
- code-review-03: The psycopg2 library uses %s as its query placeholder.
- code-review-03: The mysql-connector library uses %s as its query placeholder.
- code-review-03: If cursor.execute() fails, the error crashes the caller with no context.
- code-review-05: If no `.log` files exist, `ls *.log` fails with an error.
- code-review-05: The `-f` flag on `rm` suppresses errors and hides real errors.
- code-review-05: The suggested rewrite drops the `-r` flag from `rm` because `*.tmp` should only match files.
- debugging-04: A byte like 0xc3 indicates the file contains non-English characters.
- debugging-04: The failure occurs at the first non-ASCII character in the file.
- debugging-04: UTF-8 is the most common text encoding today.
- debugging-04: Opening a file in binary mode with "rb" avoids decoding entirely.
- debugging-04: Iterating a file opened in binary mode counts lines by newline bytes.
- debugging-04: Counting lines in binary mode requires no interpretation of the character encoding.
- debugging-04: Binary mode is a viable approach when a file may not be valid UTF-8 and only a line count is needed.
- debugging-05: In the fixed code, make_post appends "post" to tags and returns {"title": title, "tags": tags}.
- explanation-01: A slot in a hash map's internal array is also called a bucket.
- explanation-01: A hash map's internal array has a fixed number of slots but can hold many more keys.
- explanation-01: Chaining's performance stays steady when the map is nearly full, because each slot still just holds a short list.
- explanation-02: A single balance update is an example of a short transaction.
- explanation-02: The application detects a zero-row update and asks the user to reload and try again.
- explanation-03: Overloading a router or slow link causes lost packets and wasted bandwidth.
- explanation-03: Slow start is part of a broader idea called congestion control.
- explanation-03: Congestion control is the process TCP uses to avoid sending more data than the network can carry.
- explanation-03: After a packet loss, the sender may restart slow start from a lower point.
- explanation-03: Starting too slow would waste available bandwidth and make every connection slower than it needs to be.
- summarization-02: The shrunken connection pool caused errors for 12% of checkout requests.
- summarization-02: The team detected the errors at 09:14.
- summarization-04: The expected behavior is that the PDF downloads the same way the CSV export does for the same report.
- summarization-05: The listed items are action items from Monday's sprint planning.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 26 | 20 | 0.769 | 23 | 0 |
| code-review-02 | 20 | 17 | 0.85 | 17 | 1 |
| code-review-03 | 27 | 13 | 0.481 | 16 | 1 |
| code-review-04 | 20 | 9 | 0.45 | 15 | 0 |
| code-review-05 | 37 | 28 | 0.757 | 23 | 1 |
| debugging-01 | 7 | 7 | 1.0 | 10 | 0 |
| debugging-02 | 15 | 12 | 0.8 | 12 | 3 |
| debugging-03 | 11 | 11 | 1.0 | 10 | 0 |
| debugging-05 | 19 | 15 | 0.789 | 13 | 0 |
| explanation-01 | 33 | 19 | 0.576 | 21 | 2 |
| explanation-03 | 32 | 17 | 0.531 | 19 | 2 |
| explanation-04 | 33 | 21 | 0.636 | 31 | 4 |
| explanation-05 | 18 | 14 | 0.778 | 14 | 0 |
| summarization-01 | 5 | 5 | 1.0 | 5 | 0 |
| summarization-02 | 17 | 11 | 0.647 | 12 | 2 |
| summarization-03 | 13 | 13 | 1.0 | 13 | 0 |
| summarization-04 | 15 | 13 | 0.867 | 13 | 1 |
| summarization-05 | 9 | 9 | 1.0 | 8 | 0 |

Median fraction: 0.784 over 18 scored pairs.

Median additions: 0.5 over 18 scored pairs.

Lost facts:

- code-review-01: Mutating the caller's list is a side effect callers likely do not expect.
- code-review-01: If the caller reuses the passed list elsewhere, it will have been silently changed.
- code-review-01: The function implies no transaction or atomicity guarantee.
- code-review-01: Depending on what `db.insert` is, a partial failure state is not handled.
- code-review-01: Whether atomicity is a problem depends more on `db`'s implementation.
- code-review-01: As an alternative to propagating errors, specific exceptions such as `db`'s known error types can be caught at the call site.
- code-review-02: The async keyword makes the immediate throw become a rejected promise instead of a synchronous exception.
- code-review-02: userId should be run through encodeURIComponent to safely handle special characters.
- code-review-02: Callers of the corrected function should handle errors with try/catch or .catch().
- code-review-03: An input like `'; DROP TABLE orders; --` could exploit the SQL injection
- code-review-03: sqlite3 uses `?` placeholders instead of `%s`
- code-review-03: `SELECT *` is fragile and breaks silently if columns are added, reordered, or renamed
- code-review-03: `status` presumably belongs to a fixed set of enum-like values
- code-review-03: An invalid `status` value should probably error early rather than return no rows
- code-review-03: The code has no error handling
- code-review-03: `cursor.execute` can raise exceptions such as from a bad connection or lock timeout
- code-review-03: The code calls `fetchall()` on potentially large result sets
- code-review-03: `fetchall()` loads all results into memory at once
- code-review-03: Pagination, `fetchmany`, or iterating the cursor are alternatives to `fetchall()` for large result sets
- code-review-03: The function has no type hints
- code-review-03: The function has no docstring or return-type indication of the shape of returned rows
- code-review-03: The shape of returned rows (tuples vs dict-like) matters to callers
- code-review-03: The issues other than SQL injection are worth considering depending on how the function is used
- code-review-04: Under concurrent load, `Counter.value` will end up lower than the number of `increment()` calls made.
- code-review-04: In CPython, the GIL only guarantees that individual bytecode operations are atomic.
- code-review-04: The load, add, and store in `increment` compile to multiple bytecodes, so CPython can switch threads between them.
- code-review-04: The counter code is unsafe under free-threaded CPython and other implementations such as PyPy, where atomicity guarantees differ.
- code-review-04: Free-threaded CPython is designated 3.13t.
- code-review-04: The class provides no accessor method for reading the value, so callers read `counter.value` directly.
- code-review-04: In CPython, a single attribute read is atomic.
- code-review-04: Without an accessor, there is no single place to enforce consistency of the counter's contract.
- code-review-04: Guarding `increment`, `reset`, and reads with a `threading.Lock` makes them mutually exclusive.
- code-review-04: `itertools.count` is thread-safe in CPython because it is a C-implemented atomic counter.
- code-review-04: `multiprocessing.Value`-style atomics are an alternative to a lock.
- code-review-05: The unchecked `cd` before a recursive `rm -rf` is the most serious bug in the script.
- code-review-05: `rm -rf *.tmp` fails silently when no .tmp files exist.
- code-review-05: The error produced by the literal `*.tmp` is harmless in this script.
- code-review-05: The "Cleaned" message printed after a gzip failure is a misleading success message.
- code-review-05: The script relies on behavior that varies across sh implementations, such as glob handling in dash versus bash.
- code-review-05: The script should either target POSIX sh strictly or use `#!/usr/bin/env bash` if bash-specific features are wanted.
- code-review-05: The "Cleaned" output is uninformative because it does not report how many files were compressed or deleted, or any failures.
- code-review-05: The suggested rewrite uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` to enforce an argument.
- code-review-05: The single highest-risk issue in the script is the unchecked `cd` preceding the recursive `rm -rf`.
- debugging-02: In the buggy code, `this.seconds` evaluates to undefined.
- debugging-02: Calling .bind(this) on a regular-function callback is an alternative fix.
- debugging-02: Capturing `const self = this;` before the interval and referencing `self.seconds` inside the callback is an alternative fix.
- debugging-05: In the fixed code, when tags is None it is set to list(DEFAULT_TAGS).
- debugging-05: In the fixed code, tags is reassigned to tags + ["post"].
- debugging-05: The fix copies DEFAULT_TAGS on every call.
- debugging-05: Using + instead of .append avoids mutating the caller's tags list.
- explanation-01: There are usually far more possible keys than array slots in a hash map.
- explanation-01: The collection in a separate-chaining slot is usually a linked list, and sometimes a tree.
- explanation-01: Linear probing tries index + 1, index + 2, and so on until an empty slot is found.
- explanation-01: Quadratic probing tries index + 1², index + 2², and so on.
- explanation-01: Quadratic probing spreads out clusters.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Separate chaining has worse cache performance because list nodes are scattered in memory.
- explanation-01: Deletion in separate chaining is simple: remove the node from the list.
- explanation-01: Deletion in open addressing is trickier because removing a slot can break the probe chain for other entries.
- explanation-01: Deletion in open addressing usually needs a tombstone marker.
- explanation-01: Separate chaining degrades to an O(n) linked list scan if hashing is bad.
- explanation-01: Python and Rust's HashMap lean toward open addressing or variants of it.
- explanation-01: Chaining is the classic textbook implementation of collision handling.
- explanation-01: Java's HashMap historically used separate chaining.
- explanation-03: The TCP sender maintains a congestion window, abbreviated cwnd.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window protects the receiver from being overwhelmed.
- explanation-03: Historically, TCP connections started with a congestion window of 1 segment.
- explanation-03: Modern TCP typically starts with a congestion window of around 10 segments.
- explanation-03: RFC 6928 specifies the initial congestion window of about 10 segments.
- explanation-03: During slow start the send rate progresses roughly as 10 segments, then ~20, then ~40, then ~80.
- explanation-03: Slow start growth is self-limiting because it depends on real ACKs returning rather than a timer.
- explanation-03: An ECN signal can end slow start in the same way as a packet loss.
- explanation-03: On detecting loss, cwnd is slashed and the connection moves into congestion avoidance.
- explanation-03: Congestion avoidance is a more conservative, linear growth mode.
- explanation-03: Congestion avoidance grows the window by roughly +1 segment per RTT.
- explanation-03: ssthresh stands for slow start threshold.
- explanation-03: ssthresh is often set from a previous congestion event on the same connection.
- explanation-03: Slow start hands off to an additive growth mode once it has found roughly where the network's limit is.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, or files.
- explanation-04: Each thread has its own stack and instruction pointer.
- explanation-04: Thread communication requires synchronization mechanisms such as locks and mutexes to avoid race conditions.
- explanation-04: Chrome uses separate processes for fault isolation.
- explanation-04: Some web servers use per-request worker processes so a single bad request or tab cannot crash the whole system.
- explanation-04: Processes can be given separate resource quotas for CPU and memory via cgroups and ulimits.
- explanation-04: Processes can be scheduled and prioritized by the OS individually.
- explanation-04: Independent process scheduling and resource limits are useful for multi-tenant systems and for killing a runaway task cleanly.
- explanation-04: Processes can span multiple machines using IPC such as sockets.
- explanation-04: Threads cannot span multiple machines; they exist only within a single process on a single machine.
- explanation-04: Process-based isolation aligns naturally with architectures designed for horizontal scaling.
- explanation-04: Processes cost more to create and switch between than threads.
- explanation-05: Caching results by request ID without removing old entries is an example of an unbounded cache leak.
- explanation-05: Global event buses, DOM elements, and observables are examples of long-lived objects that hold listeners.
- explanation-05: Callbacks often close over a large object graph.
- explanation-05: The garbage collector guarantees it will clean up anything truly unreachable.
- summarization-02: Errors began at 09:14.
- summarization-02: Paging happened at 09:21.
- summarization-02: Rollback completed by 09:48.
- summarization-02: The total elapsed time from first errors to completed rollback was 34 minutes.
- summarization-02: Detection and response to the incident were fast.
- summarization-02: The incident response worked as intended.
- summarization-04: Clicking Export and choosing PDF results in nothing happening.
- summarization-04: Diagnosing the bug may require backend or console logs.

Added facts (styled only):

- code-review-02: The `async` keyword has no effect in this function.
- code-review-03: The database driver escapes parameterized values.
- code-review-05: The suggested fix checks the directory before changing into it.
- debugging-02: Class bodies always run in strict mode.
- debugging-02: Evaluating `this.seconds += 1` when `this` is `undefined` throws a TypeError.
- debugging-02: The same code produces `NaN` in a non-strict test but a TypeError inside a class.
- explanation-01: In chaining, each lookup needs an extra pointer.
- explanation-01: A load factor under 0.7 is an example of a low load factor.
- explanation-03: Dropped packets cause retransmissions and waste capacity.
- explanation-03: Congestion collapse is a state where the network spends most of its capacity on retransmissions instead of new data.
- explanation-04: A thread crash can bring down the whole process because all threads share the same memory.
- explanation-04: Shared memory avoids the cost of copying data between processes.
- explanation-04: Threads use less memory and start faster because they do not need a separate memory space.
- explanation-04: Threads are suitable for tasks that wait on I/O, such as network calls.
- summarization-02: Small pool values are intentionally correct in staging.
- summarization-02: Teams must not copy configuration templates between environments without checking for environment-specific values.
- summarization-04: The bug is not specific to one browser or machine.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 0 | 2 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 5 | 2 | 0 | 3 | 1.0 |
| code-review-04 | 1 | 0 | 0 | 1 | n/a |
| code-review-05 | 2 | 1 | 1 | 0 | 0.5 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 1 | 1 | 1 | 0.5 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 2 | 0 | 2 | 0 | 0.0 |
| explanation-03 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 0 | 1 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 2 | 1 | 0 | 1 | 1.0 |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.75 over 6 scored pairs.

Claims that became certain:

- code-review-05: If `cd` fails, the script keeps going and runs `rm -rf *.tmp` in whatever directory it happened to be in, likely the original CWD.
- debugging-04: The byte `0xc3` at offset 512 is likely part of a UTF-8 encoded character, such as an accented letter.
- explanation-02: Pessimistic locking assumes conflicts are likely, so it prevents them upfront.
- explanation-02: In optimistic locking, the check on write for whether the data changed since you read it is usually done via a version number or timestamp.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 0 | 2 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 5 | 0 | 1 | 4 | 0.0 |
| code-review-04 | 1 | 0 | 0 | 1 | n/a |
| code-review-05 | 2 | 0 | 1 | 1 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 2 | 0 | 1 | 1 | 0.0 |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 5 scored pairs.

Claims that became certain:

- code-review-03: `SELECT *` pulls more data than is likely needed.
- code-review-05: If `cd` fails, the script keeps going and runs `rm -rf *.tmp` in whatever directory it happened to be in, likely the original CWD.
- summarization-02: The config review checklist likely omits other performance-critical settings besides pool sizes.
- summarization-04: The issue is likely not browser-specific, since it reproduced on Firefox (latest) and Chrome on two different machines.

## Warnings

- technical-simplified/explanation-02: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
