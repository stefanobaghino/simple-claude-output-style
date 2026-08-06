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

Judge: opus. Judged on 2026-08-06T06:55:20+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 26 | 20 | 0.769 | 26 | 4 |
| code-review-02 | 12 | 10 | 0.833 | 22 | 4 |
| code-review-03 | 23 | 18 | 0.783 | 26 | 7 |
| code-review-04 | 28 | 18 | 0.643 | 17 | 0 |
| code-review-05 | 26 | 18 | 0.692 | 35 | 5 |
| debugging-01 | 8 | 8 | 1.0 | 9 | 0 |
| debugging-02 | 14 | 12 | 0.857 | 20 | 0 |
| debugging-03 | 8 | 8 | 1.0 | 12 | 3 |
| debugging-04 | 12 | 10 | 0.833 | 12 | 1 |
| debugging-05 | 18 | 15 | 0.833 | 15 | 2 |
| explanation-01 | 39 | 24 | 0.615 | 30 | 0 |
| explanation-02 | 21 | 21 | 1.0 | 27 | 2 |
| explanation-03 | 40 | 24 | 0.6 | 25 | 2 |
| explanation-04 | 48 | 30 | 0.625 | 27 | 2 |
| explanation-05 | 16 | 15 | 0.938 | 18 | 3 |
| summarization-01 | 6 | 6 | 1.0 | 5 | 1 |
| summarization-02 | 15 | 12 | 0.8 | 15 | 4 |
| summarization-03 | 15 | 14 | 0.933 | 16 | 0 |
| summarization-04 | 13 | 10 | 0.769 | 12 | 0 |
| summarization-05 | 9 | 9 | 1.0 | 12 | 0 |

Median fraction: 0.833 over 20 scored pairs.

Median additions: 2.0 over 20 scored pairs.

Lost facts:

- code-review-01: The mutable default argument is a classic Python footgun.
- code-review-01: Returning `True`/`False` loses information.
- code-review-01: With a boolean return value, callers cannot distinguish cases such as "user already exists," "db down," and "bad input."
- code-review-01: `roles.append("member")` mutates the list the caller passed in, as a side effect.
- code-review-01: Mutating the caller's list is surprising if the caller reuses that list elsewhere.
- code-review-01: In the fixed version, exceptions from `db.insert` are not caught.
- code-review-02: The function returns `undefined` immediately, wrapped in a resolved promise because it is declared `async`.
- code-review-02: If the API response does not include a `name` field, `.toUpperCase()` will throw even after the async bug is fixed.
- code-review-03: A stacked or statement-terminating payload may be possible depending on the database driver.
- code-review-03: The code has no input validation.
- code-review-03: Nothing in the code stops `status` from being an unexpected or invalid value.
- code-review-03: Lack of input validation is a correctness concern independent of SQL injection.
- code-review-03: The issues other than the SQL injection are minor or contextual.
- code-review-04: With enough concurrent threads, the final count can be far below the number of `increment()` calls.
- code-review-04: There is no atomic way to read `value`.
- code-review-04: Reading `value` while other threads are mid-increment provides no consistency guarantee.
- code-review-04: There is no lock-protected getter, so callers cannot obtain a coherent snapshot relative to other operations.
- code-review-04: Relying on GIL semantics is fragile and non-obvious.
- code-review-04: GIL-based atomicity behavior is not guaranteed across Python implementations.
- code-review-04: Free-threaded Python builds do not have a GIL.
- code-review-04: PyPy is an example of a Python implementation with different GIL-related behavior.
- code-review-04: The fixed version exposes `value` as a property that acquires the lock before returning `self._value`.
- code-review-04: The lock makes `increment`, `reset`, and reads mutually exclusive.
- code-review-05: If `$1` is empty, the unquoted `cd $BACKUP_DIR` becomes a plain `cd` command.
- code-review-05: A plain `cd` with no argument changes to `$HOME`.
- code-review-05: If `$1` is empty, the script deletes `*.tmp` files in `$HOME`.
- code-review-05: The variables `$1`, `$BACKUP_DIR`, and `$f` are all unquoted in the script.
- code-review-05: Parsing `ls` output mangles glob characters.
- code-review-05: With no matching files, `ls` errors.
- code-review-05: The script does not check `rm` and `gzip` for failure.
- code-review-05: The script always prints "Cleaned" even if operations failed.
- debugging-02: Binding a regular function with `.bind(this)` is an alternative fix.
- debugging-02: Capturing `this` beforehand in a variable such as `const self = this;` and using `self.seconds` inside the callback is an alternative fix.
- debugging-04: Using errors="replace" is reasonable when only counting lines, because exact content is not needed.
- debugging-04: Using errors="ignore" silently drops invalid bytes.
- debugging-05: Running the test alone makes it the only call ever made to make_post.
- debugging-05: The extra appended tags cause the equality assertion in the test to fail.
- debugging-05: A module imported multiple times in ways that reuse state can also cause the shared list to carry extra tags.
- explanation-01: The internal array of a hash map is called the bucket array.
- explanation-01: Collisions are inevitable once a hash map has enough entries, because the array has a limited number of slots.
- explanation-01: The collection in a chaining bucket is usually a linked list, and sometimes a tree or dynamic array.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Quadratic probing spreads entries out more and reduces clustering.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Open addressing needs resizing sooner than chaining.
- explanation-01: Open addressing is more subtle, involving clustering behavior, tombstones, and resize timing.
- explanation-01: A low load factor for open addressing means below roughly 70%.
- explanation-01: Chaining is common in general-purpose libraries.
- explanation-01: Java's HashMap uses chaining, with a switch to trees for long chains.
- explanation-01: Python's dict uses open addressing.
- explanation-01: Developers rarely implement collision handling themselves.
- explanation-01: Understanding collision handling explains why hash maps recommend keeping the load factor below a threshold.
- explanation-01: Resizing, which rehashes entries into a bigger array, is necessary as a hash map grows.
- explanation-03: A sender at connection start does not know how many routers the path crosses.
- explanation-03: A sender at connection start does not know the speed of the slowest link on the path.
- explanation-03: A sender at connection start does not know how much other traffic is competing for the path's bandwidth.
- explanation-03: Dropped packets get retransmitted.
- explanation-03: Retransmissions add more traffic to an already overloaded path, worsening the problem.
- explanation-03: Unchecked congestion can spiral into 'congestion collapse'.
- explanation-03: In congestion collapse, the network is busy but almost no data gets through successfully.
- explanation-03: Slow start is also used after certain recovery events.
- explanation-03: The congestion window is abbreviated `cwnd`.
- explanation-03: The initial congestion window was historically 1 segment.
- explanation-03: The initial congestion window is now typically 2–10 segments.
- explanation-03: Congestion avoidance uses linear growth.
- explanation-03: Congestion avoidance fine-tunes the sending rate around the estimated capacity.
- explanation-03: 'Slow start' is called slow only relative to the older approach of sending a full window's worth of data immediately with no ramp-up.
- explanation-03: Incrementing by one segment at a time would take many RTTs to reach a reasonable sending rate.
- explanation-03: Most connections are not actually competing with much congestion.
- explanation-04: A process has its own file descriptors.
- explanation-04: A process has its own OS resources.
- explanation-04: All threads in a process share the same file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state, including its program counter.
- explanation-04: Threads are cheaper to create and switch than processes because there is less state to duplicate or isolate.
- explanation-04: Process creation cost is high because the OS allocates a new address space.
- explanation-04: Process context switches are more expensive because they involve MMU/page table swaps.
- explanation-04: Job workers often use multiple processes.
- explanation-04: CPU-bound Python work uses the multiprocessing module to get real parallelism across cores.
- explanation-04: In Python, threads only help with I/O-bound concurrency.
- explanation-04: Processes can be given separate memory limits.
- explanation-04: Processes can be distributed across machines more naturally than threads.
- explanation-04: Threads are inherently tied to one process on one machine.
- explanation-04: Threads sharing memory requires locks or mutexes to avoid race conditions.
- explanation-04: Race conditions are a class of hard-to-debug concurrency bugs.
- explanation-04: A game engine's render and physics threads sharing a scene graph is an example of tasks sharing large amounts of data frequently.
- explanation-04: Threads are better when many lightweight concurrent units are needed, such as handling thousands of I/O-bound connections.
- explanation-05: A long-lived collection stays reachable, often because it is held by a long-lived object or a global.
- summarization-02: Detection-to-resolution took 34 minutes.
- summarization-02: The incident was detected at 09:14.
- summarization-02: The deploy had no automated guardrail.
- summarization-03: Under the proposal, the upload endpoint would return a placeholder URL immediately.
- summarization-04: After selecting PDF export, nothing happens initially.
- summarization-04: The error banners provide no additional error details.
- summarization-04: The bug was reproduced on the latest version of Firefox.

Added facts (styled only):

- code-review-01: The function has five problems.
- code-review-01: The fix for the mutable default is to use `roles=None` and set `roles = roles or []` inside the function.
- code-review-01: The corrected version raises `ValueError("name is required")` when `name` is falsy.
- code-review-01: The corrected version catches `Exception`, logs an error with `logging.error`, and returns `False`.
- code-review-02: Marking a function `async` suggests the author intended to use `await`.
- code-review-02: Without error handling, the user gets a raw exception with no useful message.
- code-review-02: Parsing an error page as JSON fails in a confusing way.
- code-review-02: The fixed version throws an `Error` with a message including the user ID and response status when `res.ok` is false.
- code-review-03: Libraries like psycopg2 and mysql-connector use %s as the parameter placeholder.
- code-review-03: A customer name containing an apostrophe, such as O'Brien, closes the quote early and causes a SQL syntax error.
- code-review-03: Parameterized queries also fix the apostrophe syntax error problem.
- code-review-03: Options for error handling include catching and re-raising with more information, or letting the caller handle it deliberately.
- code-review-03: The function has no type hints or docstring.
- code-review-03: Adding a type hint for cursor and a short docstring would help future readers understand what's expected.
- code-review-03: The missing type hints and docstring are a minor issue.
- code-review-05: With an empty `BACKUP_DIR`, `cd $BACKUP_DIR` fails.
- code-review-05: That `gzip` failure is not obvious from reading the script.
- code-review-05: The rewrite changes `rm -rf` to `rm -f` because `*.tmp` matches files, not directories.
- code-review-05: The `-r` flag is not needed for removing files.
- code-review-05: Removing `-r` lowers the risk if the glob ever matches something unexpected.
- debugging-03: Those iterations cover the windows [1, 2] and [2, 3].
- debugging-03: The corrected code gives the windows [1, 2], [2, 3], and [3, 4].
- debugging-03: `moving_sum([1, 2, 3, 4], 2)` returns [3, 5, 7] with the fix applied.
- debugging-04: UTF-8 covers most other text.
- debugging-05: In the fixed code, DEFAULT_TAGS is defined as ["draft"].
- debugging-05: In the fixed function, if tags is None, tags is set to list(DEFAULT_TAGS).
- explanation-02: Pessimistic locking fits when a transaction needs several steps and another process must not intervene between them.
- explanation-02: A product catalog that many people browse but few edit at the same time is an example use case for optimistic locking.
- explanation-03: The slow start threshold value is set from past experience with that connection.
- explanation-03: After a packet loss or reaching the threshold, TCP switches to a growth pattern called congestion avoidance.
- explanation-04: Web servers often run each user request in its own process for fault isolation.
- explanation-04: Sandboxed plugins run as separate processes.
- explanation-05: A leaking program uses more and more memory over time.
- explanation-05: Growing memory use from a leak can slow a program down.
- explanation-05: Growing memory use from a leak can crash a program.
- summarization-01: The ten most-used actions now have keyboard shortcuts.
- summarization-02: Errors began at 09:14 UTC.
- summarization-02: The on-call engineer was paged at 09:21 UTC.
- summarization-02: The on-call engineer was paged 7 minutes after errors began.
- summarization-02: The rollback finished at 09:48.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 26 | 23 | 0.885 | 20 | 1 |
| code-review-02 | 12 | 11 | 0.917 | 17 | 2 |
| code-review-03 | 23 | 19 | 0.826 | 16 | 3 |
| code-review-04 | 28 | 17 | 0.607 | 16 | 0 |
| code-review-05 | 26 | 20 | 0.769 | 29 | 1 |
| debugging-01 | 8 | 7 | 0.875 | 8 | 0 |
| debugging-02 | 14 | 11 | 0.786 | 12 | 1 |
| debugging-03 | 8 | 7 | 0.875 | 9 | 0 |
| debugging-04 | 12 | 6 | 0.5 | 10 | 1 |
| debugging-05 | 18 | 17 | 0.944 | 13 | 1 |
| explanation-01 | 39 | 14 | 0.359 | 22 | 3 |
| explanation-02 | 21 | 19 | 0.905 | 22 | 4 |
| explanation-04 | 48 | 30 | 0.625 | 21 | 1 |
| explanation-05 | 16 | 16 | 1.0 | 10 | 0 |
| summarization-01 | 6 | 6 | 1.0 | 5 | 1 |
| summarization-03 | 15 | 15 | 1.0 | 13 | 0 |
| summarization-04 | 13 | 12 | 0.923 | 11 | 1 |
| summarization-05 | 9 | 9 | 1.0 | 8 | 0 |

Median fraction: 0.88 over 18 scored pairs.

Median additions: 1.0 over 18 scored pairs.

Lost facts:

- code-review-01: The mutable default argument is a classic Python footgun.
- code-review-01: `roles.append("member")` mutates the list the caller passed in, as a side effect.
- code-review-01: Mutating the caller's list is surprising if the caller reuses that list elsewhere.
- code-review-02: The function returns `undefined` immediately, wrapped in a resolved promise because it is declared `async`.
- code-review-03: A stacked or statement-terminating payload may be possible depending on the database driver.
- code-review-03: `SELECT *` is fragile.
- code-review-03: `SELECT *` breaks if columns are added or reordered.
- code-review-03: A bad connection or syntax error can cause `cursor.execute` to raise.
- code-review-04: The lost-update problem gets worse under higher load.
- code-review-04: With enough concurrent threads, the final count can be far below the number of `increment()` calls.
- code-review-04: A plain `self.value` read is safe from tearing.
- code-review-04: Python attribute reads are atomic.
- code-review-04: Relying on GIL semantics is fragile and non-obvious.
- code-review-04: Individual bytecode operations are atomic under CPython's GIL.
- code-review-04: The combination of a read operation and a write operation is not atomic under the GIL.
- code-review-04: GIL-based atomicity behavior is not guaranteed across Python implementations.
- code-review-04: Free-threaded Python builds do not have a GIL.
- code-review-04: PyPy is an example of a Python implementation with different GIL-related behavior.
- code-review-04: The fixed version exposes `value` as a property that acquires the lock before returning `self._value`.
- code-review-05: `cd` can fail due to a bad path, insufficient permissions, or `$1` being unset.
- code-review-05: Writing `cd "$BACKUP_DIR" || exit 1` fixes the silent `cd` failure.
- code-review-05: The variables `$1`, `$BACKUP_DIR`, and `$f` are all unquoted in the script.
- code-review-05: With no matching files, `ls` errors.
- code-review-05: With no matching files, `rm -f` silently ignores the literal pattern.
- code-review-05: The script always prints "Cleaned" even if operations failed.
- debugging-01: The mismatch between 'port' and 'Port' raises a KeyError.
- debugging-02: When a plain function is called in strict mode or in a class, `this` is `undefined`.
- debugging-02: Binding a regular function with `.bind(this)` is an alternative fix.
- debugging-02: Capturing `this` beforehand in a variable such as `const self = this;` and using `self.seconds` inside the callback is an alternative fix.
- debugging-03: At i = 2 with window 2, the window is `[3, 4]`.
- debugging-04: The byte 0xc3 is likely the start of a UTF-8 multi-byte sequence, such as for 'é' or 'ü'.
- debugging-04: With encoding="ascii", any file containing accented characters, curly quotes, or other non-ASCII text will fail.
- debugging-04: UTF-8 is a superset compatible with ASCII text.
- debugging-04: Pure-ASCII files still work correctly when opened with UTF-8 encoding.
- debugging-04: Using errors="replace" is reasonable when only counting lines, because exact content is not needed.
- debugging-04: Using errors="ignore" silently drops invalid bytes.
- debugging-05: A module imported multiple times in ways that reuse state can also cause the shared list to carry extra tags.
- explanation-01: The internal array of a hash map is called the bucket array.
- explanation-01: Collisions are inevitable once a hash map has enough entries, because the array has a limited number of slots.
- explanation-01: Collisions are expected behavior that every hash map implementation must handle, not a bug.
- explanation-01: The collection in a chaining bucket is usually a linked list, and sometimes a tree or dynamic array.
- explanation-01: Linear probing tries index+1, index+2, index+3, and so on until an empty slot is found.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Quadratic probing spreads entries out more and reduces clustering.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Chaining has poor cache performance because linked list nodes are scattered in memory.
- explanation-01: Open addressing has good cache performance because data stays in one contiguous array.
- explanation-01: Open addressing needs resizing sooner than chaining.
- explanation-01: Deletion under chaining is simple: just remove the node.
- explanation-01: Deletion under open addressing is trickier because emptying a slot breaks probe chains for other keys.
- explanation-01: Deletion under open addressing usually requires a tombstone marker.
- explanation-01: Chaining is simpler to reason about than open addressing.
- explanation-01: Open addressing is more subtle, involving clustering behavior, tombstones, and resize timing.
- explanation-01: Open addressing tends to win when raw speed and cache locality matter and the load factor can be kept low.
- explanation-01: A low load factor for open addressing means below roughly 70%.
- explanation-01: Chaining is more forgiving and simpler to implement and debug.
- explanation-01: Java's HashMap uses chaining, with a switch to trees for long chains.
- explanation-01: Python's dict uses open addressing.
- explanation-01: Developers rarely implement collision handling themselves.
- explanation-01: Understanding collision handling explains why hash maps recommend keeping the load factor below a threshold.
- explanation-01: Resizing, which rehashes entries into a bigger array, is necessary as a hash map grows.
- explanation-01: Both chaining and open addressing get slower as buckets fill up.
- explanation-02: Pessimistic locking risks deadlocks and blocking if locks are held too long.
- explanation-02: Under high contention, optimistic locking causes wasted work and repeated retries.
- explanation-04: A process has its own file descriptors.
- explanation-04: A process has its own OS resources.
- explanation-04: All threads in a process share the same file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state, including its program counter.
- explanation-04: Switching threads is cheaper than switching processes.
- explanation-04: Threads are cheaper to create and switch than processes because there is less state to duplicate or isolate.
- explanation-04: Communication between processes requires IPC such as pipes, sockets, or shared memory.
- explanation-04: Process context switching costs more than thread context switching.
- explanation-04: Process context switches are more expensive because they involve MMU/page table swaps.
- explanation-04: Web servers often use multiple processes so one bad request or task cannot corrupt shared state or bring down the whole system.
- explanation-04: Browsers often run each tab as a separate process.
- explanation-04: Job workers often use multiple processes.
- explanation-04: Browsers isolate site content in separate processes partly for security and sandboxing reasons.
- explanation-04: Processes can be given separate memory limits.
- explanation-04: Threads sharing memory requires locks or mutexes to avoid race conditions.
- explanation-04: Race conditions are a class of hard-to-debug concurrency bugs.
- explanation-04: A game engine's render and physics threads sharing a scene graph is an example of tasks sharing large amounts of data frequently.
- summarization-04: The bug is reproduced by clicking the Export button and selecting PDF.

Added facts (styled only):

- code-review-01: The corrected version raises `ValueError("name is required")` when `name` is falsy.
- code-review-02: The unused `async` marking hides the timing bug.
- code-review-02: The `res.json()` call fails if the response is not valid JSON.
- code-review-03: A value like `x' OR '1'='1` causes the query to return every row.
- code-review-03: `%s` is the parameter placeholder for MySQL and psycopg2.
- code-review-03: Wrapping the `cursor.execute` call in a try block provides a clear error message to the caller.
- code-review-05: If no .tmp files match, rm receives the literal string `*.tmp` and prints an error.
- debugging-02: When setInterval calls a normal function, `this` becomes the global object rather than the Timer instance.
- debugging-04: The file contains the byte 0xc3 at position 512.
- debugging-05: In the fixed version, make_post checks whether tags is None and assigns list(DEFAULT_TAGS) if so.
- explanation-01: Chaining stays fast even when the hash map is nearly full.
- explanation-01: Most general-purpose hash maps use chaining.
- explanation-01: Most general-purpose hash maps use chaining because performance stays steady under load.
- explanation-02: Optimistic locking checks a version number or timestamp before it writes.
- explanation-02: Web apps with many reads and few write conflicts are a good fit for optimistic locking.
- explanation-02: In bank transfers and inventory systems, a lost update can cause direct financial loss.
- explanation-02: Pessimistic locking is the choice when correctness matters more than throughput.
- explanation-04: Each process gets its own Python interpreter and its own global lock.
- summarization-01: The app now has keyboard shortcuts for the ten most used actions.
- summarization-04: Clicking the PDF export button several more times produces four identical "export failed" error banners.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 4 | 4 | 0 | 0 | 1.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-01 | 3 | 1 | 2 | 0 | 0.333 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 5 | 2 | 1 | 2 | 0.667 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 0 | 1 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 1.0 over 5 scored pairs.

Claims that became certain:

- explanation-01: Deletion under open addressing usually needs a "tombstone" marker, since emptying the slot outright would break probe chains for other keys.
- explanation-01: Open addressing tends to win when you care about raw speed and cache locality and can keep the load factor low (below roughly 70%).
- explanation-03: The name "slow start" is a bit of a misnomer.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 4 | 2 | 1 | 1 | 0.667 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-01 | 3 | 0 | 1 | 2 | 0.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.334 over 4 scored pairs.

Claims that became certain:

- code-review-03: `SELECT *` pulls more data than is likely needed.
- debugging-05: Any subsequent test (or even the same test run twice) sees `["draft", "post", "post"]` or worse, depending on run order and other tests calling `make_post`.
- explanation-01: Each bucket in chaining holds a small collection — usually a linked list, sometimes a tree or dynamic array.

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
