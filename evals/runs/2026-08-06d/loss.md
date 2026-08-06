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

Judge: opus. Judged on 2026-08-06T09:14:27+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 32 | 23 | 0.719 | 28 | 3 |
| code-review-02 | 20 | 16 | 0.8 | 19 | 2 |
| code-review-03 | 28 | 21 | 0.75 | 19 | 6 |
| code-review-04 | 22 | 12 | 0.545 | 16 | 0 |
| code-review-05 | 39 | 31 | 0.795 | 34 | 3 |
| debugging-01 | 7 | 7 | 1.0 | 9 | 1 |
| debugging-02 | 13 | 9 | 0.692 | 14 | 1 |
| debugging-03 | 8 | 8 | 1.0 | 8 | 0 |
| debugging-04 | 13 | 7 | 0.538 | 13 | 3 |
| debugging-05 | 22 | 20 | 0.909 | 12 | 0 |
| explanation-01 | 36 | 30 | 0.833 | 39 | 2 |
| explanation-02 | 30 | 26 | 0.867 | 25 | 4 |
| explanation-03 | 36 | 21 | 0.583 | 28 | 1 |
| explanation-04 | 41 | 24 | 0.585 | 29 | 1 |
| explanation-05 | 17 | 17 | 1.0 | 16 | 3 |
| summarization-01 | 6 | 5 | 0.833 | 6 | 0 |
| summarization-02 | 9 | 5 | 0.556 | 17 | 6 |
| summarization-03 | 12 | 12 | 1.0 | 12 | 1 |
| summarization-04 | 14 | 11 | 0.786 | 11 | 0 |
| summarization-05 | 10 | 10 | 1.0 | 9 | 1 |

Median fraction: 0.798 over 20 scored pairs.

Median additions: 1.0 over 20 scored pairs.

Lost facts:

- code-review-01: Nothing in the function prevents duplicate users or empty names.
- code-review-01: The function has no duplicate-role check.
- code-review-01: The function does too much and has poor separation of concerns.
- code-review-01: The function silently mixes validation, mutation, and persistence.
- code-review-01: Mixing validation, mutation, and persistence makes the function hard to test or reason about failure modes.
- code-review-01: The fixed version copies `roles` with `list(roles)` when `roles` is truthy, and otherwise uses an empty list.
- code-review-01: The fixed version appends "member" only if "member" is not already in `roles`.
- code-review-01: The fixed version lets real errors propagate.
- code-review-01: Specific exceptions, such as `db`-related ones, can be caught at the call site.
- code-review-02: Calling `res.json()` on an error response body may fail or return unexpected data.
- code-review-02: Because `res.ok` is not checked, a failed request still tries to parse JSON and proceed as if it succeeded.
- code-review-02: The code assumes `data` and `profile` have a `.name` property without checking.
- code-review-02: A malformed API response would throw because the response shape is not validated.
- code-review-03: An input value like `'; DROP TABLE orders; --` can exploit the concatenation.
- code-review-03: SQL injection lets an attacker destroy arbitrary data.
- code-review-03: The `status` parameter presumably comes from a fixed set of values such as "pending" and "shipped".
- code-review-03: Whether to catch and log exceptions or let them propagate depends on the caller's needs.
- code-review-03: String equality on `customer_name` and `status` may fail to match due to case differences.
- code-review-03: String equality on `customer_name` and `status` may fail to match due to whitespace differences.
- code-review-03: Case-sensitivity behavior in string comparison depends on the database collation.
- code-review-04: The read and the write in `increment()` are two separate bytecode operations.
- code-review-04: The GIL only guarantees that each individual bytecode instruction runs atomically.
- code-review-04: The GIL can switch threads between the read and the write in `increment()`.
- code-review-04: A `reset()` can occur between `increment()`'s read and write, causing the in-flight increment to overwrite the reset with `1` instead of leaving it at `0`.
- code-review-04: Using `self.value += 1` would not fix the race condition.
- code-review-04: `self.value += 1` is still a non-atomic read-modify-write operation under the hood.
- code-review-04: The design relies on undocumented GIL behavior rather than explicit synchronization.
- code-review-04: The correctness of the single-write cases is only accidentally OK because of the GIL.
- code-review-04: The code's correctness would not hold up on a free-threaded (no-GIL) CPython build or another Python implementation.
- code-review-04: No lock is exposed for callers who need to perform compound atomic operations such as reading and resetting together.
- code-review-05: `cd "$BACKUP_DIR" || exit 1` is the recommended way to make `cd` failure fatal.
- code-review-05: In most shells, `cd ""` changes to `$HOME`.
- code-review-05: A missing argument causes the script to silently `rm -rf` `*.tmp` in the user's home directory.
- code-review-05: The script should check `[ -n "$1" ] && [ -d "$1" ]` before proceeding.
- code-review-05: With zero matches, `ls` prints an error to stderr.
- code-review-05: If there are no `*.log` files, the `ls` inside `$(...)` errors to stderr.
- code-review-05: The suggested rewrite checks `[ -d "$BACKUP_DIR" ]` and exits 1 with an error on stderr otherwise.
- code-review-05: The suggested rewrite loops over `*.tmp` and `*.log` globs directly, guarding each with `[ -e "$f" ]`.
- debugging-02: The global object is `window` in browsers or `globalThis` generally.
- debugging-02: The resulting `NaN` is assigned back to `this.seconds`.
- debugging-02: Calling `.bind(this)` on the function expression is an alternative fix.
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` is an alternative fix.
- debugging-04: The actual encoding is usually UTF-8.
- debugging-04: Passing `errors="replace"` or `errors="ignore"` to `open` prevents decoding from failing.
- debugging-04: The encoding of a file can be detected programmatically.
- debugging-04: `chardet` and `charset-normalizer` are libraries that detect file encoding.
- debugging-04: Counting lines does not require decoding the file's contents.
- debugging-04: Opening the file in binary mode with `open(path, "rb")` is the simplest robust fix for counting lines.
- debugging-05: In the full suite the list becomes ["draft", "post", "post"], failing the equality check.
- debugging-05: The fix builds a new list inside the function with list(DEFAULT_TAGS) when tags is None.
- explanation-01: Open addressing lookup follows the probe sequence until it finds the key or hits an empty slot.
- explanation-01: Hitting an empty slot during an open addressing lookup means the key is not present.
- explanation-01: Deletion in open addressing usually requires tombstone markers.
- explanation-01: Go's map uses open addressing.
- explanation-01: Open addressing requires careful tuning, including resizing before the table gets too full.
- explanation-01: Open addressing tables are usually resized at around 70-75% load factor.
- explanation-02: Pessimistic locking suits workflows where retrying a failed transaction is costly or user-facing.
- explanation-02: Editing a document or profile record is an example use case for optimistic locking.
- explanation-02: Updating a shopping cart is an example use case for optimistic locking.
- explanation-02: Holding locks carries throughput and deadlock costs.
- explanation-03: When a TCP connection starts, the sender has no knowledge of the path to the receiver, including link speeds, how many other connections share the links, and how much router buffering exists.
- explanation-03: If a TCP sender sent data limited only by the receiver's buffer, it could send faster than the network can carry.
- explanation-03: Routers queue excess packets and drop packets once their queues fill up.
- explanation-03: Dropped packets cause retransmissions, which wastes bandwidth.
- explanation-03: Congestion collapse is a state where most traffic on a link is retransmissions of dropped packets and almost no data gets through.
- explanation-03: Congestion collapse actually occurred on the early internet in the mid-1980s.
- explanation-03: The mid-1980s congestion collapse motivated the development of TCP congestion control.
- explanation-03: Slow start is also used after certain events, such as a timeout.
- explanation-03: Historically, a connection began slow start with a cwnd of 1 segment.
- explanation-03: Increasing cwnd by one segment per round-trip would take a very long time to reach a reasonable rate on a fast, high-latency path.
- explanation-03: ssthresh is usually based on the last known safe rate from before congestion was last detected.
- explanation-03: In congestion avoidance, cwnd grows roughly linearly, adding about one segment per round-trip.
- explanation-03: On detecting loss, TCP lowers ssthresh to roughly half the window size that caused the loss.
- explanation-03: Guessing a fixed safe rate is too conservative and wastes bandwidth.
- explanation-03: Sending as fast as possible is too aggressive and causes congestion collapse.
- explanation-04: A process has its own file descriptors.
- explanation-04: A process has its own OS-level resources.
- explanation-04: All threads in a process share the same file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state.
- explanation-04: Nginx uses multiple worker processes.
- explanation-04: Postgres uses multiple processes per connection.
- explanation-04: OS-level permission boundaries such as different users, seccomp filters, and capabilities can be enforced between processes.
- explanation-04: One thread cannot be sandboxed differently from another thread in the same process because they share everything.
- explanation-04: Ruby historically had a GIL.
- explanation-04: Each process gets its own interpreter and lock.
- explanation-04: Processes can be killed, restarted, or scaled independently by the OS or a supervisor without coordinating with other components.
- explanation-04: systemd, Kubernetes, and supervisord are supervisors that can manage process lifecycles.
- explanation-04: Microservices and container-based architectures favor process-level separation.
- explanation-04: Shared memory only exists within a single machine.
- explanation-04: Processes have heavier context switches than threads.
- explanation-04: Processes have higher memory overhead than threads because each process has its own address space.
- summarization-01: Cold start time has been reduced by approximately 40%.
- summarization-02: The connection pool size that shipped to production was 5 instead of the intended 50.
- summarization-02: A 10x reduction in connection pool size went unnoticed until it caused an outage.
- summarization-02: The time from page to rollback was 34 minutes.
- summarization-02: The time from error onset to page was 7 minutes.
- summarization-04: After choosing the PDF option, nothing happens initially.
- summarization-04: One error banner appears per click, so four clicks produce four banners.
- summarization-04: The bug was reproduced on different machines.

Added facts (styled only):

- code-review-01: The fixed version computes `roles = (roles or []) + ["member"]`.
- code-review-01: The fixed version calls `db.insert({"name": name, "roles": roles})` inside a `try` block and returns `True` on success.
- code-review-01: The fixed version catches `ConnectionError`, logs the error with the user's name, and returns `False`.
- code-review-02: The code has four problems.
- code-review-02: Without a `.catch()`, failures would produce an unhandled promise rejection instead of a clear error.
- code-review-03: With parameterized queries, the database driver inserts the values safely.
- code-review-03: The psycopg2 driver uses `%s` as its placeholder.
- code-review-03: Pulling every column wastes bandwidth.
- code-review-03: If the query fails, `cursor.execute` raises an exception with no context about what went wrong.
- code-review-03: The function name `find_orders` does not indicate that it filters by customer and status.
- code-review-03: A more specific function name would let readers understand what the function does without checking its arguments.
- code-review-05: With an empty BACKUP_DIR, `cd $BACKUP_DIR` fails and the script continues running in its starting directory.
- code-review-05: When the loop runs with the literal `*.log`, gzip fails with a "no such file" error.
- code-review-05: `set -u` catches unset variables.
- debugging-01: The corrected function get_url(cfg) returns the f-string "http://{cfg['host']}:{cfg['port']}/api".
- debugging-02: In strict mode, `this` inside a regular function is `undefined`.
- debugging-04: The error identifies byte 0xc3 at position 512.
- debugging-04: ASCII is a subset of UTF-8.
- debugging-04: Because ASCII is a subset of UTF-8, opening with UTF-8 works for both plain ASCII files and files with non-ASCII characters.
- explanation-01: Load factor refers to the number of entries per slot.
- explanation-01: Most general-purpose hash map implementations use chaining.
- explanation-02: In the version-column example, an update of a product read at version 3 includes `WHERE version = 3` in its query.
- explanation-02: If no other party changed the row, the versioned update succeeds and the version becomes 4.
- explanation-02: If another party already updated the row, the `WHERE version = 3` clause matches no rows.
- explanation-02: While a row is locked with `SELECT ... FOR UPDATE`, no other transaction can read or modify the balance at the same time.
- explanation-03: Ten segments is roughly 14KB.
- explanation-04: Web browsers run each tab, or each site, in its own process for security reasons.
- explanation-05: A program with a memory leak uses more and more memory over time.
- explanation-05: Increasing memory use from a leak can slow a program down.
- explanation-05: Increasing memory use from a leak can crash a program.
- summarization-02: The deployment copied a database connection pool size from the staging template.
- summarization-02: Staging intentionally uses low configuration values.
- summarization-02: About 12% of requests experienced checkout errors.
- summarization-02: The team detected the issue at 09:14 UTC.
- summarization-02: On-call was paged at 09:21.
- summarization-02: The issue was fixed at 09:48.
- summarization-03: Generating thumbnails during upload currently ties up web workers.
- summarization-05: Ada is to run the payments database migration dry run.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 32 | 24 | 0.75 | 26 | 0 |
| code-review-02 | 20 | 14 | 0.7 | 14 | 1 |
| code-review-03 | 28 | 22 | 0.786 | 16 | 2 |
| code-review-04 | 22 | 14 | 0.636 | 23 | 6 |
| code-review-05 | 39 | 30 | 0.769 | 31 | 8 |
| debugging-01 | 7 | 7 | 1.0 | 9 | 3 |
| debugging-02 | 13 | 9 | 0.692 | 11 | 1 |
| debugging-03 | 8 | 6 | 0.75 | 8 | 0 |
| debugging-05 | 22 | 20 | 0.909 | 14 | 0 |
| explanation-01 | 36 | 16 | 0.444 | 22 | 1 |
| explanation-02 | 30 | 26 | 0.867 | 27 | 5 |
| explanation-03 | 36 | 17 | 0.472 | 22 | 2 |
| explanation-05 | 17 | 16 | 0.941 | 11 | 1 |
| summarization-01 | 6 | 5 | 0.833 | 5 | 2 |
| summarization-02 | 9 | 6 | 0.667 | 13 | 4 |
| summarization-03 | 12 | 12 | 1.0 | 13 | 1 |
| summarization-04 | 14 | 11 | 0.786 | 13 | 1 |
| summarization-05 | 10 | 10 | 1.0 | 8 | 2 |

Median fraction: 0.778 over 18 scored pairs.

Median additions: 1.5 over 18 scored pairs.

Lost facts:

- code-review-01: Errors swallowed by the bare except could include an `AttributeError` if `db` is `None`, a DB connection error, or a validation error.
- code-review-01: Nothing in the function prevents duplicate users or empty names.
- code-review-01: Mutating the caller's list in place is a surprising side effect for the caller.
- code-review-01: The function does too much and has poor separation of concerns.
- code-review-01: The function silently mixes validation, mutation, and persistence.
- code-review-01: Mixing validation, mutation, and persistence makes the function hard to test or reason about failure modes.
- code-review-01: The fixed version copies `roles` with `list(roles)` when `roles` is truthy, and otherwise uses an empty list.
- code-review-01: The fixed version doesn't mutate the caller's list.
- code-review-02: The `async` keyword makes the function return a Promise.
- code-review-02: The promise returned by the function rejects immediately due to the crash rather than resolving after the fetch completes.
- code-review-02: The fixed version awaits the fetch call.
- code-review-02: The fixed version checks the response status via `res.ok` and throws an `Error` including `res.status` when the response is not OK.
- code-review-02: The fixed version lets errors propagate as a rejected promise.
- code-review-02: Callers of the fixed version can handle errors with `try/catch` or `.catch()`.
- code-review-03: Whether to catch and log exceptions or let them propagate depends on the caller's needs.
- code-review-03: The code has no LIMIT or pagination.
- code-review-03: Without a LIMIT, a customer with many orders causes the function to return everything at once.
- code-review-03: String equality on `customer_name` and `status` may fail to match due to case differences.
- code-review-03: String equality on `customer_name` and `status` may fail to match due to whitespace differences.
- code-review-03: Case-sensitivity behavior in string comparison depends on the database collation.
- code-review-04: `increment()` reads `self.value` into a local variable `current` and then writes `current + 1` back to `self.value`.
- code-review-04: The GIL only guarantees that each individual bytecode instruction runs atomically.
- code-review-04: Using `self.value += 1` would not fix the race condition.
- code-review-04: `self.value += 1` is still a non-atomic read-modify-write operation under the hood.
- code-review-04: The design relies on undocumented GIL behavior rather than explicit synchronization.
- code-review-04: The correctness of the single-write cases is only accidentally OK because of the GIL.
- code-review-04: The code's correctness would not hold up on a free-threaded (no-GIL) CPython build or another Python implementation.
- code-review-04: No lock is exposed for callers who need to perform compound atomic operations such as reading and resetting together.
- code-review-05: The script should check `[ -n "$1" ] && [ -d "$1" ]` before proceeding.
- code-review-05: `cd $BACKUP_DIR` breaks on paths containing spaces or glob characters.
- code-review-05: Unquoted `$BACKUP_DIR` is subject to word splitting and pathname expansion.
- code-review-05: With zero matches, the literal `*.log` is left unless nullglob-like behavior applies.
- code-review-05: The script does not check whether the `.log` or `.tmp` globs matched anything.
- code-review-05: If there are no `*.tmp` files, `rm -rf *.tmp` errors.
- code-review-05: The error from `rm -rf *.tmp` with no matches is harmless but noisy.
- code-review-05: The suggested rewrite checks `[ -d "$BACKUP_DIR" ]` and exits 1 with an error on stderr otherwise.
- code-review-05: The suggested rewrite loops over `*.tmp` and `*.log` globs directly, guarding each with `[ -e "$f" ]`.
- debugging-02: The global object is `window` in browsers or `globalThis` generally.
- debugging-02: The resulting `NaN` is assigned back to `this.seconds`.
- debugging-02: Calling `.bind(this)` on the function expression is an alternative fix.
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` is an alternative fix.
- debugging-03: With `len(values) = 4` and `window = 2`, the original loop skips the final window `[3, 4]`.
- debugging-03: `moving_sum([1, 2, 3, 4], 2)` returns `[3, 5, 7]`.
- debugging-05: In the full suite the list becomes ["draft", "post", "post"], failing the equality check.
- debugging-05: The fix builds a new list inside the function with list(DEFAULT_TAGS) when tags is None.
- explanation-01: There are usually more possible keys than array slots in a hash map.
- explanation-01: Separate chaining is simple to implement.
- explanation-01: Deletion in separate chaining is easy because the entry is just removed from the list.
- explanation-01: Worst-case lookup in separate chaining degrades to O(n) when too many keys pile up in one bucket.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Quadratic probing spreads out clusters better than linear probing.
- explanation-01: Double hashing uses a second hash function to determine the step size.
- explanation-01: Open addressing has better cache locality because everything is in one contiguous array with no pointer chasing.
- explanation-01: Deletion in open addressing is trickier because emptying a slot could break the probe chain for other keys.
- explanation-01: Deletion in open addressing usually requires tombstone markers.
- explanation-01: Chaining has memory overhead per entry from pointers, while open addressing is compact and cache-friendly.
- explanation-01: Chaining has worse cache performance than open addressing due to pointer chasing.
- explanation-01: Chaining is more forgiving and simpler to reason about than open addressing.
- explanation-01: Chaining is common in general-purpose libraries.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Open addressing is faster in practice when memory locality matters and the load factor is kept low.
- explanation-01: Python's dict uses open addressing.
- explanation-01: Go's map uses open addressing.
- explanation-01: Open addressing requires careful tuning, including resizing before the table gets too full.
- explanation-01: Open addressing tables are usually resized at around 70-75% load factor.
- explanation-02: Seat and inventory reservation systems are example use cases for pessimistic locking.
- explanation-02: Editing a document or profile record is an example use case for optimistic locking.
- explanation-02: Updating a shopping cart is an example use case for optimistic locking.
- explanation-02: Holding locks carries throughput and deadlock costs.
- explanation-03: When a TCP connection starts, the sender has no knowledge of the path to the receiver, including link speeds, how many other connections share the links, and how much router buffering exists.
- explanation-03: If a TCP sender sent data limited only by the receiver's buffer, it could send faster than the network can carry.
- explanation-03: Dropped packets cause retransmissions, which wastes bandwidth.
- explanation-03: Congestion collapse is a state where most traffic on a link is retransmissions of dropped packets and almost no data gets through.
- explanation-03: Congestion collapse actually occurred on the early internet in the mid-1980s.
- explanation-03: The mid-1980s congestion collapse motivated the development of TCP congestion control.
- explanation-03: Slow start is also used after certain events, such as a timeout.
- explanation-03: Historically, a connection began slow start with a cwnd of 1 segment.
- explanation-03: Modern TCP implementations often start with a cwnd of around 10 segments.
- explanation-03: The name 'slow start' is somewhat ironic because the window starts tiny but ramps up fast.
- explanation-03: Increasing cwnd by one segment per round-trip would take a very long time to reach a reasonable rate on a fast, high-latency path.
- explanation-03: ssthresh is usually based on the last known safe rate from before congestion was last detected.
- explanation-03: In congestion avoidance, cwnd grows roughly linearly, adding about one segment per round-trip.
- explanation-03: On detecting loss, TCP cuts cwnd back down.
- explanation-03: On detecting loss, TCP lowers ssthresh to roughly half the window size that caused the loss.
- explanation-03: Lowering ssthresh after loss makes future slow start and congestion avoidance phases start from a more conservative estimate.
- explanation-03: Guessing a fixed safe rate is too conservative and wastes bandwidth.
- explanation-03: Sending as fast as possible is too aggressive and causes congestion collapse.
- explanation-03: Slow start lets each connection ramp up exponentially to quickly find a reasonable operating point while backing off promptly on signs of overshoot.
- explanation-05: UI event handlers, observers, and pub/sub subscriptions are examples of callbacks that can leak.
- summarization-01: Cold start time has been reduced by approximately 40%.
- summarization-02: The connection pool size that shipped to production was 5 instead of the intended 50.
- summarization-02: A 10x reduction in connection pool size went unnoticed until it caused an outage.
- summarization-02: The time from page to rollback was 34 minutes.
- summarization-04: One error banner appears per click, so four clicks produce four banners.
- summarization-04: The bug was reproduced on the latest version of Firefox.
- summarization-04: The bug was reproduced on different machines.

Added facts (styled only):

- code-review-02: The `async` keyword has no effect in this function.
- code-review-03: `%s` is the parameter placeholder for MySQL and psycopg2.
- code-review-03: The correct placeholder should be confirmed in the database driver's documentation.
- code-review-04: Callers must read `self.value` directly because there is no `get` method.
- code-review-04: Reading `self.value` directly is not safe.
- code-review-04: The fixed `Counter.__init__` sets `self._value` to 0 and `self._lock` to a `threading.Lock()`.
- code-review-04: The fixed `increment` performs `self._value += 1` while holding `self._lock`.
- code-review-04: The fixed `reset` sets `self._value` to 0 while holding `self._lock`.
- code-review-04: The fixed `get` returns `self._value` while holding `self._lock`.
- code-review-05: Using `for f in *.log` avoids an unneeded extra process.
- code-review-05: If no file matches *.log, the loop body does not run.
- code-review-05: The error message printed when no *.log file matches can confuse the user.
- code-review-05: Without `set -u`, use of an unset variable does not raise an error.
- code-review-05: Parsing ls output and the unquoted $f in gzip are high-risk problems.
- code-review-05: The missing check for existing *.log files and the missing `set -e`/`set -u` are medium-risk problems.
- code-review-05: A suggested fix uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` and `cd "$BACKUP_DIR" || exit 1`.
- code-review-05: The suggested fix uses `rm -f -- *.tmp`, a `for f in *.log` loop with an `[ -e "$f" ] || continue` guard, and `gzip -- "$f"`.
- debugging-01: The config dictionary is {"host": "localhost", "port": 8080}.
- debugging-01: The function get_url takes a parameter named cfg.
- debugging-01: The code calls print(get_url(config)).
- debugging-02: In strict mode, `this` inside the callback is `undefined`.
- explanation-01: Two keys must not share one slot in a hash map.
- explanation-02: In the example, a table named `products` has a column named `version`.
- explanation-02: In the example, a user reads a product row with `version = 3`.
- explanation-02: In the example, the update query is `UPDATE products SET price = 20, version = 4 WHERE id = 1 AND version = 3;`.
- explanation-02: If another user changed the row first, the row's `version` is no longer 3.
- explanation-02: Under pessimistic locking, the database can also block concurrent reads, depending on the lock type.
- explanation-03: The event of routers filling buffers and dropping packets is called congestion.
- explanation-03: Congestion causes delay and packet loss for every connection that uses the same path.
- explanation-05: In a memory leak, memory use grows over time even though the garbage collector runs.
- summarization-01: Each button's tooltip shows that button's keyboard shortcut.
- summarization-01: The app starts up to 40% faster.
- summarization-02: The page went out at 09:21.
- summarization-02: The rollback finished at 09:48.
- summarization-02: The rollback finished 27 minutes after the page went out.
- summarization-02: The team's response time was good.
- summarization-03: Thumbnail generation currently uses web workers.
- summarization-04: A second user sees the same failure on Chrome.
- summarization-05: Ada is assigned to run the payments database migration dry run.
- summarization-05: The payments database migration dry run is due before Thursday.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-02 | 1 | 0 | 0 | 1 | n/a |
| code-review-03 | 3 | 1 | 0 | 2 | 1.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 7 | 1 | 2 | 4 | 0.333 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 0 | 1 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 1.0 over 5 scored pairs.

Claims that became certain:

- code-review-01: The listed issues are ordered roughly in order of severity.
- explanation-03: Modern TCP implementations often start with a congestion window of around 10 segments.
- explanation-03: On each ACK confirming delivered data, the sender increases cwnd roughly by one segment per ACK.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-03 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 1 | 0 | 0 | 1 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 7 | 2 | 2 | 3 | 0.5 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 0 | 1 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 3 scored pairs.

Claims that became certain:

- code-review-02: `res.json()` on an error body may fail or return unexpected data
- code-review-03: `status` presumably comes from a fixed set of values (e.g. "pending", "shipped")
- explanation-03: On each ACK confirming delivered data, the sender increases cwnd roughly by one segment per ACK.
- explanation-03: By the time it enters congestion avoidance, the sender has a rough estimate of the network's capacity.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 167, measured: 167.
Mean duration: 11342 ms. Mean wall: 25884 ms. Mean startup: 14541 ms.

## Warnings

- technical-simplified/explanation-04: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- completeness:reverse:9f3a7b0ceb018a29e4aa2838d95b871ec2cc9061b8acaa7081a55090eb6ba541: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-loss-_v4m5i9t","session_id":"5f6350f5-00f6-4579-bb88-03b74388ee16","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","clea
