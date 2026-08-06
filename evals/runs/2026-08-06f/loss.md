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

Judge: opus. Judged on 2026-08-06T09:15:58+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 36 | 24 | 0.667 | 22 | 3 |
| code-review-02 | 18 | 15 | 0.833 | 23 | 2 |
| code-review-03 | 30 | 18 | 0.6 | 21 | 7 |
| code-review-04 | 23 | 15 | 0.652 | 20 | 6 |
| code-review-05 | 34 | 24 | 0.706 | 33 | 8 |
| debugging-01 | 6 | 6 | 1.0 | 8 | 1 |
| debugging-02 | 17 | 11 | 0.647 | 14 | 3 |
| debugging-03 | 13 | 13 | 1.0 | 11 | 0 |
| debugging-04 | 10 | 7 | 0.7 | 10 | 2 |
| debugging-05 | 22 | 19 | 0.864 | 12 | 0 |
| explanation-01 | 40 | 24 | 0.6 | 31 | 3 |
| explanation-02 | 25 | 18 | 0.72 | 25 | 4 |
| explanation-03 | 29 | 19 | 0.655 | 28 | 4 |
| explanation-04 | 36 | 27 | 0.75 | 24 | 4 |
| explanation-05 | 14 | 13 | 0.929 | 13 | 2 |
| summarization-01 | 6 | 6 | 1.0 | 5 | 0 |
| summarization-02 | 10 | 9 | 0.9 | 17 | 4 |
| summarization-03 | 13 | 13 | 1.0 | 12 | 1 |
| summarization-04 | 18 | 14 | 0.778 | 13 | 0 |
| summarization-05 | 9 | 8 | 0.889 | 8 | 0 |

Median fraction: 0.764 over 20 scored pairs.

Median additions: 2.5 over 20 scored pairs.

Lost facts:

- code-review-01: Mutable default arguments are a classic Python footgun.
- code-review-01: The function performs no input validation.
- code-review-01: The `name` parameter is not checked for type or emptiness.
- code-review-01: Nothing prevents `add_user(None)` or `add_user("")` from proceeding to the DB call.
- code-review-01: The function has no docstring and no type hints.
- code-review-01: The missing docstring/type hints issue is minor.
- code-review-01: The function's contract is undocumented, including what `roles` should contain, what `db` needs to implement, and what exceptions are expected.
- code-review-01: A fixed version can raise `ValueError("name is required")` when `name` is falsy.
- code-review-01: A fixed version can copy the input with `roles = list(roles)` before appending.
- code-review-01: A fixed version can append `"member"` only if it is not already in `roles`.
- code-review-01: The fixed version calls `db.insert({"name": name, "roles": roles})` and returns `True`.
- code-review-01: The fixed version avoids duplicate roles.
- code-review-02: Discarding the rest of the profile data is probably not what a function named `loadProfile` should do.
- code-review-02: A corrected version awaits `fetch(`/api/users/${userId}`)`, throws an `Error` with the status if `res.ok` is false, awaits `res.json()`, and returns the profile.
- code-review-02: If the intent was to return the uppercased name, it should be done explicitly and `profile.name` should be validated to exist first.
- code-review-03: An input like `'; DROP TABLE orders; --` would break out of the string literal in the query.
- code-review-03: Breaking out of the string literal lets an attacker destroy arbitrary data.
- code-review-03: sqlite3 uses `?` as its parameter placeholder.
- code-review-03: psycopg2 uses `%s` as its parameter placeholder.
- code-review-03: mysql-connector uses `%s` as its parameter placeholder.
- code-review-03: The function does not check that `status` is one of the expected or allowed values before querying the database.
- code-review-03: The lack of error handling may be acceptable depending on context.
- code-review-03: There is no indication that the absence of error handling is intentional.
- code-review-03: The exact string match means callers must pass exact values, with no trimming or case-insensitive matching.
- code-review-03: The case and whitespace sensitivity is unstated behavior.
- code-review-03: The SQL injection is the only issue that needs fixing before the code ships.
- code-review-03: The remaining issues are minor or stylistic.
- code-review-04: The GIL guarantees that each individual attribute read or write is atomic.
- code-review-04: The GIL does not guarantee atomicity for a read and write pair taken together.
- code-review-04: With concurrent callers, the increment implementation reliably drops increments.
- code-review-04: The docstring claims the class is used from multiple threads.
- code-review-04: An increment can silently apply on top of a stale pre-reset value and get overwritten.
- code-review-04: The class provides no atomic compound operations for callers.
- code-review-04: Even with `increment` and `reset` fixed internally, there is no way to do a safe read-modify-write from outside the class.
- code-review-04: Examples of unsupported compound operations are 'increment and return the new value' and 'increment only if below some limit'.
- code-review-05: Running `cd ""` fails.
- code-review-05: The unchecked `cd` is the most dangerous bug in the script.
- code-review-05: With an unexpanded glob, `rm -rf` tries to remove a file literally named `*.tmp`, which just produces an error.
- code-review-05: Unexpected .tmp files, such as someone's in-progress work, are silently destroyed by the script.
- code-review-05: `echo Cleaned $BACKUP_DIR` is unquoted, which is a minor issue.
- code-review-05: The absence of `set -e`/`set -u` is largely why the unchecked `cd` is so dangerous.
- code-review-05: `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` provides a required-argument check.
- code-review-05: Using `--` guards against filenames starting with `-`.
- code-review-05: The suggested fix drops `-r` from `rm` because `*.tmp` shouldn't match directories.
- code-review-05: `-r` should be used with `rm` only if removing tmp directories is intended.
- debugging-02: A callback defined inside a class body runs in strict mode.
- debugging-02: Class bodies are always strict mode.
- debugging-02: In strict mode, a function called without a receiver gets `this === undefined`.
- debugging-02: In the strict-mode case, `this.seconds += 1` throws a TypeError: Cannot read properties of undefined (reading 'seconds').
- debugging-02: `setInterval(function () {...}.bind(this), 1000)` is an equivalent alternative fix.
- debugging-02: Capturing `const self = this;` before the callback and using `self` inside is an equivalent alternative fix.
- debugging-04: If the file is not UTF-8, the actual encoding can be detected and used instead.
- debugging-04: Opening the file in binary mode with "rb" avoids decoding entirely.
- debugging-04: Iterating over a file opened in binary mode yields lines, so summing 1 per iteration counts the file's lines.
- debugging-05: The fix also avoids a second bug.
- debugging-05: Even with a fresh default, passing in a caller's own list would still mutate that caller's list.
- debugging-05: Callers who pass explicit lists should be aware that append mutates in place.
- explanation-01: The underlying array of a hash map is called the bucket array.
- explanation-01: Collisions are inevitable once there are enough entries, because the array has a limited number of slots.
- explanation-01: Collisions are expected behavior, not a bug.
- explanation-01: The collection in a separate chaining bucket is usually a linked list, and sometimes a tree or dynamic array.
- explanation-01: Deleting entries is easy with separate chaining.
- explanation-01: Separate chaining lookups can get slow if one bucket accumulates many entries.
- explanation-01: Separate chaining has worst-case O(n) lookup if the hash function is bad.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Quadratic probing spreads out clusters better than linear probing.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Deletion is trickier in open addressing because emptying a slot might break a probe chain.
- explanation-01: Open addressing deletion often uses tombstones.
- explanation-01: Open addressing performance can degrade sharply as the table fills up, due to clustering.
- explanation-01: Deletion is easy with chaining and awkward with open addressing, which needs tombstones.
- explanation-01: Java's HashMap converts buckets to trees when they get large, giving O(log n) worst case.
- explanation-01: absl::flat_hash_map is a C++ implementation that uses open addressing.
- explanation-02: Pessimistic locking fits expensive-to-retry operations.
- explanation-02: Pessimistic locking fits short critical sections.
- explanation-02: Inventory decrement at checkout during a flash sale is an example use case for pessimistic locking.
- explanation-02: Pessimistic locking trades throughput for correctness guarantees and simplicity of reasoning.
- explanation-02: Optimistic locking fits long-lived transactions, such as a user editing a form for minutes.
- explanation-02: Collaborative document editing is an example use case for optimistic locking.
- explanation-02: REST APIs updating a resource via ETag/If-Match are an example use case for optimistic locking.
- explanation-03: There is no fixed answer for how fast TCP can send, because every path through the internet is different and changes over time.
- explanation-03: Slow start is also used after a period of idleness or after loss.
- explanation-03: Historically the initial congestion window was a few packets.
- explanation-03: Modern TCP implementations often start with a congestion window of around 10.
- explanation-03: cwnd grows by roughly one packet's worth for each ACK received.
- explanation-03: Congestion avoidance typically uses linear growth instead of exponential growth.
- explanation-03: The number of RTTs slow start needs to reach a target window size is log₂ of the target size.
- explanation-03: Slow start is essentially an additive-then-multiplicative search: ramp up aggressively until loss occurs, then back off and grow more conservatively.
- explanation-03: Slow start lets TCP automatically adapt to wildly different network conditions, such as a fast datacenter link and a congested home internet connection.
- explanation-03: TCP adapts to different network conditions without either side needing to know the other's characteristics in advance.
- explanation-04: A process has its own file descriptors and OS-level resources.
- explanation-04: The operating system schedules and protects processes separately.
- explanation-04: Threads in the same process share open files and other resources.
- explanation-04: Each thread has its own stack and register state.
- explanation-04: Threads must coordinate using locks and mutexes to avoid race conditions.
- explanation-04: Inter-process communication requires explicit mechanisms such as pipes, sockets, or shared memory.
- explanation-04: Inter-thread communication happens through shared memory but needs synchronization.
- explanation-04: Processes can run under different users or permissions.
- explanation-04: Using processes eliminates whole classes of data races and deadlocks that affect multithreaded code.
- explanation-05: A global event bus and a DOM element are examples of long-lived objects that callbacks can be registered on.
- summarization-02: The pool exhaustion caused approximately 12% error rates for checkout.
- summarization-04: The issue is reproduced by clicking the "Export" button and choosing the PDF option.
- summarization-04: The Reports page has an "Export" button.
- summarization-04: The Export button offers a PDF option.
- summarization-04: The issue was reproduced by two different users.
- summarization-05: The check with the mobile team lead concerns whether the mobile team was informed about the API deprecation.

Added facts (styled only):

- code-review-01: The function has five problems.
- code-review-01: The shared default list accumulates users across calls even though it is meant for one person.
- code-review-01: `roles + ["member"]` builds a new list instead of modifying the caller's list in place.
- code-review-02: Marking a function `async` without using `await` makes the `async` keyword misleading.
- code-review-02: The `async` keyword suggests the function waits for something.
- code-review-03: The function builds its SQL query by joining strings together with the `+` operator.
- code-review-03: A customer name of `x' OR '1'='1` would cause the query to return every row in the table.
- code-review-03: The function has no handling for missing matches or database errors.
- code-review-03: The caller may want to check for and handle the empty result case.
- code-review-03: The function does not check whether `customer_name` or `status` are the right type or a reasonable length before using them.
- code-review-03: Input type and length checks matter less once parameterized queries are used.
- code-review-03: It is worth confirming the caller cannot pass `None` or unexpected types.
- code-review-04: In the fixed code, `Counter.__init__` sets `self._value = 0` and `self._lock = threading.Lock()`.
- code-review-04: In the fixed code, `increment()` performs `self._value += 1` while holding the lock.
- code-review-04: In the fixed code, `reset()` sets `self._value = 0` while holding the lock.
- code-review-04: In the fixed code, `value` is a property that returns `self._value` while holding the lock.
- code-review-04: The attribute was renamed to `_value`.
- code-review-04: A locked `value` property was added.
- code-review-05: Failing to check that `cd` succeeded is known as the "cd or die" bug.
- code-review-05: The `-f` flag to `rm` silences errors.
- code-review-05: With `set -e` enabled, a failing `ls` in the loop could terminate the script.
- code-review-05: If a .gz file already exists, `gzip` skips the file, or prompts when run in a terminal.
- code-review-05: Nothing prevents passing `/` or `~` as the backup directory, causing files outside the intended folder to be deleted or compressed.
- code-review-05: The safer version exits with a usage message to stderr if the argument is empty or not a directory.
- code-review-05: The safer version uses `cd "$BACKUP_DIR" || exit 1`.
- code-review-05: The safer version calls `gzip -f -- "$f"`.
- debugging-01: The corrected function `get_url(cfg)` returns the f-string `f"http://{cfg['host']}:{cfg['port']}/api"`.
- debugging-02: When `setInterval` calls a regular function, `this` refers to the global object.
- debugging-02: In Node.js, `this` in that context is `globalThis` or the module wrapper.
- debugging-02: `this.seconds` inside the callback looks for a `seconds` property on the global object.
- debugging-04: The byte 0xc3 appears at position 512 in the file.
- debugging-04: UTF-8 covers ASCII plus many more characters.
- explanation-01: A key can be something like a name or a number.
- explanation-01: Chaining's performance stays steady even at high load.
- explanation-01: Most general-purpose hash maps use chaining.
- explanation-02: An optimistic locking example uses a `products` table with a `version` column.
- explanation-02: The example update statement is `UPDATE products SET stock = 10, version = version + 1 WHERE id = 42 AND version = 3;`.
- explanation-02: If another process already updated the row so that `version` is no longer 3, the example update affects zero rows.
- explanation-02: The pessimistic example is `BEGIN; SELECT * FROM accounts WHERE id = 42 FOR UPDATE; UPDATE accounts SET balance = balance - 100 WHERE id = 42; COMMIT;`.
- explanation-03: Routers dropping packets due to excess traffic is called congestion.
- explanation-03: The threshold that ends slow start is set from a past connection's experience.
- explanation-03: Slow start is a core part of how the internet avoids congestion collapse.
- explanation-03: Congestion collapse is a state where so many retransmissions happen after packet loss that the network gets clogged with wasted traffic.
- explanation-04: Threads are faster to switch between than processes.
- explanation-04: Browser tabs, plugins, and sandboxed scripts are examples of untrusted code.
- explanation-04: Ruby allows only one thread to run Ruby code at a time.
- explanation-04: Processes can be restarted, stopped, or moved to a different machine independently.
- explanation-05: During a memory leak, a program's memory use grows over time even though its workload has not grown.
- explanation-05: Forgotten listeners and callbacks are a frequent cause of leaks in long-running applications such as web pages and servers.
- summarization-02: Checkout errors started at 09:14 UTC.
- summarization-02: A rollback at 09:48 fixed the problem.
- summarization-02: The outage lasted 34 minutes.
- summarization-02: An automated guardrail that flags production values resembling staging defaults should be considered.
- summarization-03: Generating thumbnails during upload currently keeps web workers busy.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 36 | 30 | 0.833 | 24 | 1 |
| code-review-02 | 18 | 14 | 0.778 | 15 | 0 |
| code-review-03 | 30 | 20 | 0.667 | 17 | 6 |
| code-review-04 | 23 | 13 | 0.565 | 18 | 0 |
| code-review-05 | 34 | 20 | 0.588 | 27 | 2 |
| debugging-01 | 6 | 6 | 1.0 | 9 | 3 |
| debugging-02 | 17 | 11 | 0.647 | 13 | 0 |
| debugging-04 | 10 | 6 | 0.6 | 8 | 0 |
| debugging-05 | 22 | 19 | 0.864 | 16 | 1 |
| explanation-01 | 40 | 24 | 0.6 | 28 | 0 |
| explanation-02 | 25 | 19 | 0.76 | 22 | 5 |
| explanation-03 | 29 | 20 | 0.69 | 25 | 1 |
| explanation-04 | 36 | 24 | 0.667 | 30 | 2 |
| explanation-05 | 14 | 13 | 0.929 | 9 | 0 |
| summarization-01 | 6 | 5 | 0.833 | 5 | 1 |
| summarization-02 | 10 | 6 | 0.6 | 11 | 5 |
| summarization-03 | 13 | 13 | 1.0 | 13 | 1 |
| summarization-04 | 18 | 15 | 0.833 | 12 | 0 |
| summarization-05 | 9 | 7 | 0.778 | 9 | 1 |

Median fraction: 0.76 over 19 scored pairs.

Median additions: 1 over 19 scored pairs.

Lost facts:

- code-review-01: Mutable default arguments are a classic Python footgun.
- code-review-01: The function has no docstring and no type hints.
- code-review-01: The missing docstring/type hints issue is minor.
- code-review-01: The function's contract is undocumented, including what `roles` should contain, what `db` needs to implement, and what exceptions are expected.
- code-review-01: Whether to keep a `try/except` around `db.insert` depends on what `db` is and how the caller wants to handle failures.
- code-review-01: The decision about a `try/except` around `db.insert` is worth deciding explicitly rather than defaulting to swallow-everything.
- code-review-02: The function returns a transformed value instead of the profile.
- code-review-02: Calling `.toUpperCase()` on the name discards the rest of the profile data.
- code-review-02: Discarding the rest of the profile data is probably not what a function named `loadProfile` should do.
- code-review-02: A corrected version awaits `fetch(`/api/users/${userId}`)`, throws an `Error` with the status if `res.ok` is false, awaits `res.json()`, and returns the profile.
- code-review-03: psycopg2 uses `%s` as its parameter placeholder.
- code-review-03: mysql-connector uses `%s` as its parameter placeholder.
- code-review-03: The function does not check that `status` is one of the expected or allowed values before querying the database.
- code-review-03: The function has no error handling.
- code-review-03: A malformed query or database error will raise an uncaught exception.
- code-review-03: The lack of error handling may be acceptable depending on context.
- code-review-03: There is no indication that the absence of error handling is intentional.
- code-review-03: The exact string match means callers must pass exact values, with no trimming or case-insensitive matching.
- code-review-03: The case and whitespace sensitivity is unstated behavior.
- code-review-03: The SQL injection is the only issue that needs fixing before the code ships.
- code-review-04: With concurrent callers, the increment implementation reliably drops increments.
- code-review-04: The code uses no primitive such as `itertools.count` or `multiprocessing.Value` to guard shared state.
- code-review-04: The docstring claims the class is used from multiple threads.
- code-review-04: An increment can silently apply on top of a stale pre-reset value and get overwritten.
- code-review-04: The class provides no atomic compound operations for callers.
- code-review-04: Even with `increment` and `reset` fixed internally, there is no way to do a safe read-modify-write from outside the class.
- code-review-04: Examples of unsupported compound operations are 'increment and return the new value' and 'increment only if below some limit'.
- code-review-04: Callers reading `.value` directly get no consistency guarantee.
- code-review-04: Another thread could mutate `.value` immediately after a caller reads it.
- code-review-04: A consistent read requires adding a `get()` method that also takes `self._lock`.
- code-review-05: The script assigns BACKUP_DIR=$1 without quoting and without checking that the argument is set.
- code-review-05: Running `cd ""` fails.
- code-review-05: Unquoted `cd $BACKUP_DIR` is subject to word-splitting and globbing.
- code-review-05: With an unexpanded glob, `rm -rf` tries to remove a file literally named `*.tmp`, which just produces an error.
- code-review-05: The script has no confirmation or dry-run step.
- code-review-05: Unexpected .tmp files, such as someone's in-progress work, are silently destroyed by the script.
- code-review-05: Parsing `ls` output breaks on filenames with spaces, newlines, or glob characters.
- code-review-05: If no .log files exist, `ls *.log` prints an error to stderr.
- code-review-05: The script does not check whether gzip succeeded, so failures are not reported.
- code-review-05: `echo Cleaned $BACKUP_DIR` is unquoted, which is a minor issue.
- code-review-05: `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` provides a required-argument check.
- code-review-05: Using `--` guards against filenames starting with `-`.
- code-review-05: The suggested fix drops `-r` from `rm` because `*.tmp` shouldn't match directories.
- code-review-05: `-r` should be used with `rm` only if removing tmp directories is intended.
- debugging-02: A callback defined inside a class body runs in strict mode.
- debugging-02: Class bodies are always strict mode.
- debugging-02: In the strict-mode case, `this.seconds += 1` throws a TypeError: Cannot read properties of undefined (reading 'seconds').
- debugging-02: If the same pattern were used outside a class in non-strict/sloppy code, `this` would fall back to the global object instead of throwing.
- debugging-02: `setInterval(function () {...}.bind(this), 1000)` is an equivalent alternative fix.
- debugging-02: Capturing `const self = this;` before the callback and using `self` inside is an equivalent alternative fix.
- debugging-04: Accented characters such as "é" and "à" are examples of characters encoded as UTF-8 multi-byte sequences.
- debugging-04: If the file is not UTF-8, the actual encoding can be detected and used instead.
- debugging-04: Opening the file in binary mode with "rb" avoids decoding entirely.
- debugging-04: Iterating over a file opened in binary mode yields lines, so summing 1 per iteration counts the file's lines.
- debugging-05: The fix also avoids a second bug.
- debugging-05: Even with a fresh default, passing in a caller's own list would still mutate that caller's list.
- debugging-05: Callers who pass explicit lists should be aware that append mutates in place.
- explanation-01: The underlying array of a hash map is called the bucket array.
- explanation-01: Collisions are inevitable once there are enough entries, because the array has a limited number of slots.
- explanation-01: Collisions are expected behavior, not a bug.
- explanation-01: The collection in a separate chaining bucket is usually a linked list, and sometimes a tree or dynamic array.
- explanation-01: Separate chaining has worst-case O(n) lookup if the hash function is bad.
- explanation-01: Linear probing tries index+1, index+2, index+3, and so on.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Quadratic probing spreads out clusters better than linear probing.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Open addressing is often faster in practice for typical loads.
- explanation-01: Open addressing performance can degrade sharply as the table fills up, due to clustering.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Java's HashMap converts buckets to trees when they get large, giving O(log n) worst case.
- explanation-01: Python's dict uses open addressing.
- explanation-01: absl::flat_hash_map is a C++ implementation that uses open addressing.
- explanation-01: Both chaining and open addressing are valid, well-tested choices.
- explanation-02: Pessimistic locking fits short critical sections.
- explanation-02: Inventory decrement at checkout during a flash sale is an example use case for pessimistic locking.
- explanation-02: Pessimistic locking trades throughput for correctness guarantees and simplicity of reasoning.
- explanation-02: Optimistic locking fits long-lived transactions, such as a user editing a form for minutes.
- explanation-02: Collaborative document editing is an example use case for optimistic locking.
- explanation-02: REST APIs updating a resource via ETag/If-Match are an example use case for optimistic locking.
- explanation-03: Dropped packets trigger retransmissions and waste bandwidth.
- explanation-03: There is no fixed answer for how fast TCP can send, because every path through the internet is different and changes over time.
- explanation-03: Slow start is also used after a period of idleness or after loss.
- explanation-03: The congestion window (cwnd) is the amount of unacknowledged data a sender is allowed to have in flight at once.
- explanation-03: Historically the initial congestion window was a few packets.
- explanation-03: Modern TCP implementations often start with a congestion window of around 10.
- explanation-03: Congestion avoidance typically uses linear growth instead of exponential growth.
- explanation-03: Slow start is called 'slow' because it begins cautiously with a small window.
- explanation-03: Slow start is essentially an additive-then-multiplicative search: ramp up aggressively until loss occurs, then back off and grow more conservatively.
- explanation-04: Threads in the same process share open files and other resources.
- explanation-04: Each thread has its own stack and register state.
- explanation-04: Threads must coordinate using locks and mutexes to avoid race conditions.
- explanation-04: Inter-thread communication happens through shared memory but needs synchronization.
- explanation-04: Ruby historically had a Global Interpreter Lock.
- explanation-04: Processes can run under different users or permissions.
- explanation-04: Processes can be sandboxed independently.
- explanation-04: Browsers run each tab in its own process, sandboxed away from the rest of the browser.
- explanation-04: Separate processes make it trivial to kill, restart, or scale a component independently without affecting others.
- explanation-04: A supervisor can restart a crashed worker process.
- explanation-04: One thread cannot easily be restarted without restarting the whole process.
- explanation-04: Using processes eliminates whole classes of data races and deadlocks that affect multithreaded code.
- explanation-05: A global event bus and a DOM element are examples of long-lived objects that callbacks can be registered on.
- summarization-01: Cold start time has been reduced by approximately 40%.
- summarization-02: The staging config template intentionally uses smaller values than production.
- summarization-02: The copied template cut the database connection pool size from 50 to 5.
- summarization-02: The reduced connection pool was exhausted under load.
- summarization-02: The pool exhaustion caused approximately 12% error rates for checkout.
- summarization-04: The expected behavior is that a PDF file is generated and downloaded.
- summarization-04: The issue was reproduced on the latest version of Firefox.
- summarization-04: The issue was reproduced on different machines.
- summarization-05: The payments database migration dry run is due before Thursday.
- summarization-05: The check with the mobile team lead concerns whether the mobile team was informed about the API deprecation.

Added facts (styled only):

- code-review-01: The caller might not expect the passed-in list to be modified.
- code-review-03: The function has one severe problem and two minor problems.
- code-review-03: Passing customer_name = "x' OR '1'='1" returns all orders.
- code-review-03: The database driver escapes values in a parameterized query.
- code-review-03: The function does not check that customer_name and status are non-empty, which is a minor problem.
- code-review-03: The missing empty check is not critical because the parameterized query already blocks injection.
- code-review-03: An empty check can prevent a useless database call.
- code-review-05: The listed problems are ordered by risk.
- code-review-05: The suggested fix exits with status 1 and an error message on stderr when `$BACKUP_DIR` is empty or not a directory.
- debugging-01: The config dictionary is {"host": "localhost", "port": 8080}.
- debugging-01: The function get_url returns the f-string "http://{cfg['host']}:{cfg['port']}/api".
- debugging-01: The corrected code calls print(get_url(config)).
- debugging-05: With the fix, no call can change the list of another call.
- explanation-02: Under optimistic locking, when a write fails the application must retry.
- explanation-02: In the example, a user reads a row with `version = 3`.
- explanation-02: In the example, when the user saves the row, the update statement includes `WHERE id = 1 AND version = 3`.
- explanation-02: In the example, the update statement sets `version = 4`.
- explanation-02: A lost update in a financial transaction can cause real financial harm.
- explanation-03: The network path can include slow links, busy routers, and bandwidth shared with other connections.
- explanation-04: The operating system can switch between threads in one process faster than it can switch between processes.
- explanation-04: Switching between threads in one process is faster because the operating system does not need to swap the full memory space.
- summarization-01: The app starts up to 40% faster.
- summarization-02: Errors started at 09:14.
- summarization-02: The team paged at 09:21.
- summarization-02: The team took 7 minutes to page after the errors started.
- summarization-02: An earlier alert on pool size could reduce the time to page.
- summarization-02: There are currently no alerts for low database connection pool size.
- summarization-03: Currently, thumbnail generation ties up web workers.
- summarization-05: Chen's search indexing work and demo are due Friday.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-02 | 3 | 0 | 2 | 1 | 0.0 |
| code-review-03 | 2 | 0 | 0 | 2 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 5 | 1 | 0 | 4 | 1.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 1 | 1 | 0 | 0 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 5 | 0 | 3 | 2 | 0.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 4 | 1 | 0 | 3 | 1.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.5 over 6 scored pairs.

Claims that became certain:

- code-review-01: A fixed version would look something like the code shown (using `roles=None`/`db=None` defaults, raising `ValueError` for missing `db` and `name`, copying `roles`, and appending `"member"` only if not already present).
- code-review-02: The code will throw `TypeError: Cannot read properties of undefined (reading 'name')` almost every time.
- code-review-02: `res.json()` would still be called on an error response, potentially producing a malformed `profile`.
- explanation-01: Each bucket in separate chaining usually holds a linked list, and sometimes a tree or dynamic array
- explanation-01: Open addressing is often faster in practice for typical loads
- explanation-01: Open addressing performance can degrade sharply as the table fills up, and can fail if the table fills up

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-02 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-03 | 2 | 0 | 0 | 2 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 5 | 1 | 1 | 3 | 0.5 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 1 | 1 | 0 | 0 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 5 | 1 | 4 | 0 | 0.2 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 4 | 1 | 1 | 2 | 0.5 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.35 over 6 scored pairs.

Claims that became certain:

- code-review-01: A fixed version would look something like the code shown (using `roles=None`/`db=None` defaults, raising `ValueError` for missing `db` and `name`, copying `roles`, and appending `"member"` only if not already present).
- code-review-02: The code will throw `TypeError: Cannot read properties of undefined (reading 'name')` almost every time.
- code-review-05: If no `*.tmp` files exist, most shells will probably leave the glob unexpanded (as the literal string `*.tmp`), so `rm -rf` tries to remove a file literally named `*.tmp`.
- explanation-01: Each bucket in separate chaining usually holds a linked list, and sometimes a tree or dynamic array
- explanation-01: Open addressing is often faster in practice for typical loads
- explanation-01: With open addressing, deletion often requires using "tombstones" since emptying a slot might break a probe chain
- explanation-01: Open addressing performance can degrade sharply as the table fills up, and can fail if the table fills up
- explanation-03: Roughly, cwnd grows by one packet's worth for each ACK received.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 171, measured: 171.
Mean duration: 11268 ms. Mean wall: 28703 ms. Mean startup: 17434 ms.

## Warnings

- technical-simplified/debugging-03: the pair failed the gate, excluded
