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

Judge: opus. Judged on 2026-08-05T05:54:55+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 44 | 35 | 0.795 | 23 | 3 |
| code-review-02 | 22 | 17 | 0.773 | 21 | 0 |
| code-review-03 | 24 | 17 | 0.708 | 25 | 8 |
| code-review-04 | 21 | 14 | 0.667 | 23 | 2 |
| code-review-05 | 38 | 24 | 0.632 | 27 | 4 |
| debugging-01 | 7 | 7 | 1.0 | 8 | 1 |
| debugging-02 | 12 | 10 | 0.833 | 16 | 1 |
| debugging-03 | 12 | 12 | 1.0 | 15 | 0 |
| debugging-04 | 13 | 7 | 0.538 | 14 | 6 |
| debugging-05 | 16 | 15 | 0.938 | 17 | 0 |
| explanation-01 | 35 | 25 | 0.714 | 27 | 2 |
| explanation-02 | 22 | 15 | 0.682 | 24 | 5 |
| explanation-03 | 25 | 18 | 0.72 | 20 | 2 |
| explanation-04 | 32 | 16 | 0.5 | 34 | 5 |
| explanation-05 | 14 | 12 | 0.857 | 14 | 1 |
| summarization-01 | 7 | 7 | 1.0 | 5 | 0 |
| summarization-02 | 13 | 12 | 0.923 | 20 | 9 |
| summarization-03 | 14 | 14 | 1.0 | 12 | 0 |
| summarization-04 | 11 | 9 | 0.818 | 13 | 0 |
| summarization-05 | 9 | 9 | 1.0 | 6 | 0 |

Median fraction: 0.806 over 20 scored pairs.

Median additions: 1.5 over 20 scored pairs.

Lost facts:

- code-review-01: The mutable default argument is a classic Python gotcha.
- code-review-01: When `roles` is passed in, `.append` mutates the caller's list in place.
- code-review-01: A caller likely does not expect their list to change as a side effect.
- code-review-01: Nothing in the function prevents duplicate users.
- code-review-01: A boolean return means the caller cannot distinguish "insert failed", "db is None", and "duplicate user".
- code-review-01: The function has no type hints.
- code-review-01: The contract of the function is unclear.
- code-review-01: The `roles` parameter is presumably `list[str]`.
- code-review-01: Handling errors at the call site makes failures visible.
- code-review-02: Because it never awaits, the function does not actually behave asynchronously.
- code-review-02: Marking a function `async` without using `await` defeats the purpose of the `async` keyword.
- code-review-02: An error response body parsed as JSON may lack a `name` field.
- code-review-02: The code does not validate `userId`.
- code-review-02: If `userId` is `undefined` or `null`, the request silently becomes `/api/users/undefined`.
- code-review-03: Any input containing a single quote breaks out of the string literal in the query.
- code-review-03: psycopg2 and MySQLdb use `%s` as the placeholder.
- code-review-03: The `status` parameter presumably comes from a fixed set of values such as `pending` and `shipped`.
- code-review-03: An invalid or misspelled `status` fails silently by returning zero rows instead of raising a clear error.
- code-review-03: The function does not handle the 'no results' case.
- code-review-03: The function returns an empty list with no distinction between no results and an error.
- code-review-03: The empty-list return may be acceptable depending on the caller, but the intended contract is worth confirming.
- code-review-04: In the fixed class, `__init__` sets `self._value` to 0 and creates `self._lock` as a `threading.Lock()`.
- code-review-04: In the fixed class, `increment` executes `self._value += 1` inside a `with self._lock:` block.
- code-review-04: In the fixed class, `reset` sets `self._value = 0` inside a `with self._lock:` block.
- code-review-04: In the fixed class, `value` is a `@property` that returns `self._value` while holding the lock.
- code-review-04: The fix renames the counter state from a public `value` attribute to a private `_value` attribute.
- code-review-04: Callers can read and write the public `value` attribute directly, bypassing any locking added inside the class.
- code-review-04: Making `value` a lock-protected property closes the direct-access hole.
- code-review-05: If no `.tmp` files exist, `*.tmp` is passed literally to `rm -rf`
- code-review-05: `sh` does not have `nullglob`-like behavior
- code-review-05: `rm -rf` on a nonexistent file only errors, which is harmless here
- code-review-05: With no `.log` matches, the command substitution captures nothing useful or the literal string, depending on the shell
- code-review-05: The script prints "Cleaned" regardless of actual success
- code-review-05: The script does not check that `gzip` succeeded for each file, so a per-file failure is neither stopped nor reported
- code-review-05: `echo Cleaned $BACKUP_DIR` always prints, even if nothing was cleaned or errors occurred
- code-review-05: No exit code reflects failure
- code-review-05: There is a potential race condition if the script runs concurrently with something writing new `.log` or `.tmp` files
- code-review-05: The race condition is minor for a cleanup script
- code-review-05: The suggested rewrite uses `BACKUP_DIR=${1:?Usage: $0 BACKUP_DIR}` to require the argument
- code-review-05: The suggested rewrite uses `rm -f -- *.tmp 2>/dev/null || true`
- code-review-05: The `-r` (recursive) flag is not needed for matching plain files by extension
- code-review-05: Using `-r` suggests unintended recursion into directories named `*.tmp`
- debugging-02: An alternative fix is to call `.bind(this)` on the callback function.
- debugging-02: An alternative fix is to capture `const self = this;` before the callback and use `self.seconds` inside it.
- debugging-04: Omitting the encoding argument makes open() use the platform default encoding.
- debugging-04: Specifying UTF-8 explicitly is safer than relying on the platform default.
- debugging-04: If the file's actual encoding is unknown or untrusted, the encoding should be detected first.
- debugging-04: The charset-normalizer library can detect a file's encoding.
- debugging-04: An alternative is to open the file in binary mode and count occurrences of b"\n".
- debugging-04: Counting newline bytes in binary mode avoids decoding the text at all.
- debugging-05: In the fixed code, the body sets `tags = list(tags) if tags is not None else list(DEFAULT_TAGS)`.
- explanation-01: A hash map's array has a fixed number of slots.
- explanation-01: There are infinitely many possible keys.
- explanation-01: The collection held in a chaining slot is usually a linked list.
- explanation-01: Chaining allows a load factor above 1, meaning more entries than slots.
- explanation-01: Open addressing needs resizing sooner than chaining.
- explanation-01: Most general-purpose hash map implementations use chaining.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Performance-critical implementations use open addressing.
- explanation-01: Python's dict uses open addressing.
- explanation-01: Rust's HashMap uses open addressing.
- explanation-02: In the example, an orders table has a version column.
- explanation-02: In the example, the application reads version = 5 and updates with UPDATE orders SET status = 'shipped', version = 6 WHERE id = 42 AND version = 5.
- explanation-02: Optimistic locking fits when transactions are long-lived, such as a user editing a form for minutes.
- explanation-02: Optimistic locking fits in a distributed or stateless setup where holding a database lock across a network round trip is expensive.
- explanation-02: The pessimistic example uses BEGIN; SELECT * FROM accounts WHERE id = 42 FOR UPDATE; then deducts the balance and commits.
- explanation-02: Pessimistic locking fits when the critical section is short so lock hold time stays small.
- explanation-02: Short, high-contention critical sections favor pessimistic locking.
- explanation-03: Congestion collapse was a real problem on the early internet.
- explanation-03: The initial congestion window was historically 1 segment.
- explanation-03: The initial congestion window is now typically 10 segments, about 14KB, per RFC 6928.
- explanation-03: Each round-trip's worth of data generates that many ACKs.
- explanation-03: Congestion avoidance uses slower, linear growth.
- explanation-03: On packet loss the sender backs off, often resetting ssthresh to half the current window and shrinking cwnd.
- explanation-03: Slow start finds a sustainable sending rate without requiring routers to explicitly tell senders their fair share.
- explanation-04: A process is an independent execution unit with its own memory address space, file descriptors, and OS-level resources.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Processes are heavier to spawn than threads because a new address space and resource tables must be created.
- explanation-04: Sharing memory between threads carries the risk of race conditions.
- explanation-04: IPC is slower and more explicit than shared-memory communication between threads.
- explanation-04: Both processes and threads are scheduled by the OS.
- explanation-04: Threads are typically lighter to context-switch than processes because much of the state, such as memory mappings, is shared.
- explanation-04: Web servers such as Nginx and Gunicorn's process workers spawn a process per request or worker so one bad request cannot crash the whole server.
- explanation-04: Ruby's MRI historically had a global interpreter lock.
- explanation-04: Threads cannot be sandboxed independently of each other.
- explanation-04: Browsers put each tab or origin in a separate process partly for security and privilege separation.
- explanation-04: Separate processes allow components to be restarted, killed, or scaled independently via OS process management.
- explanation-04: A supervisor can restart a crashed worker process.
- explanation-04: Processes use more memory than threads because resources are duplicated.
- explanation-04: Communication between processes is slower because it requires serialization and IPC instead of direct memory access.
- explanation-04: Threads are the right choice when work is CPU-parallel, trusted, and needs fast shared-state access.
- explanation-05: Examples of long-lived collections include a global dictionary and an event-listener registry.
- explanation-05: An example of a callback capturing large objects is a closure holding a DOM node or a big buffer.
- summarization-02: The production DB connection pool was set to 5 instead of 50.
- summarization-04: The issue was reproduced on the latest version of Firefox on the reporter's laptop.
- summarization-04: The issue was reproduced on Chrome on a colleague's machine.

Added facts (styled only):

- code-review-01: Bad input passes through the function until the database call fails.
- code-review-01: A safer version calls `db.insert({"name": name, "roles": roles})` inside a `try` block and returns `True` on success.
- code-review-01: A safer version catches `DatabaseError`, logs the error with `logging.error`, and returns `False`.
- code-review-03: The input customer_name = "x' OR '1'='1" would return every row in the table.
- code-review-03: What an injection attack can do depends on the database permissions.
- code-review-03: Most database drivers use %s as the parameter placeholder.
- code-review-03: Listing only the needed columns avoids wasted data transfer.
- code-review-03: The function has no error handling.
- code-review-03: A database error will raise an unhandled exception with no context for the caller.
- code-review-03: Bad connections and invalid status values are examples of database errors.
- code-review-03: For a large result set, fetchall() could use a lot of memory.
- code-review-04: Code that reads `counter.value` from a different thread can see a value that is being written at that same moment.
- code-review-04: A reader can still read a stale value that a concurrent `increment` is about to change.
- code-review-05: The script's most serious problem is that if `cd` fails, the script continues and runs `rm -rf` in the wrong directory.
- code-review-05: The variables `$1`, `$BACKUP_DIR`, and `$f` are all unquoted in the script.
- code-review-05: The missing `*.log` check is not dangerous but is noisy and easy to miss.
- code-review-05: The suggested fix checks `[ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]` and exits with status 1 after printing an error to standard error.
- debugging-01: The fix is to change `Port` to `port` on line 4.
- debugging-02: The `NaN` result is stored back into `this.seconds`.
- debugging-04: The byte 0xc3 at position 512 is not valid ASCII.
- debugging-04: The ascii codec only accepts bytes from 0 to 127.
- debugging-04: UTF-8 handles plain ASCII text.
- debugging-04: Adding errors="replace" prevents a bad byte from crashing the line count.
- debugging-04: errors="ignore" is an alternative to errors="replace".
- debugging-04: A function count_lines(path) can open the file with open(path, encoding="utf-8", errors="replace") and return sum(1 for _ in f).
- explanation-01: The load factor is the fraction of filled slots.
- explanation-01: You rarely need to pick a collision strategy yourself unless you are building a hash map from scratch or optimizing for a specific memory or performance constraint.
- explanation-02: In the pessimistic transfer example, you subtract from one account, add to the other, then commit.
- explanation-02: An online store product page edited by a store admin is an example of optimistic locking.
- explanation-02: In the optimistic example, the product row has a version column.
- explanation-02: In the optimistic example, the row is read at version 5, the description is edited, and an UPDATE sets version to 6 with a WHERE clause requiring version = 5.
- explanation-02: Pessimistic locking risks deadlocks if multiple transactions lock rows in different orders.
- explanation-03: The congestion window is the amount of data a sender can send before waiting for an acknowledgment.
- explanation-03: An acknowledgment is a confirmation that the data arrived.
- explanation-04: Use more processes than threads when you want to scale across machines, not just cores.
- explanation-04: A process-based design, such as a worker that reads from a queue, tends to map cleanly onto multiple machines.
- explanation-04: A process-based design maps cleanly onto multiple machines because each worker is self-contained.
- explanation-04: Shared memory does not exist across machines.
- explanation-04: An example of a good thread use case is one thread handling a task while other threads read the results without copying them.
- explanation-05: Examples of event sources include a UI element, an event bus, and a subscription.
- summarization-02: The low pool size exhausted database connections.
- summarization-02: The exhausted connections caused checkout errors.
- summarization-02: About 12% of requests hit checkout errors.
- summarization-02: The page went out 7 minutes after the errors began.
- summarization-02: The rollback finished 34 minutes after the page went out.
- summarization-02: Total impact time was about 34 minutes.
- summarization-02: The impact ran from 09:14 to 09:48 UTC.
- summarization-02: A suggested fix is to rename or separate the staging and production templates.
- summarization-02: Renaming or separating the templates would prevent future mix-ups.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 44 | 35 | 0.795 | 27 | 2 |
| code-review-02 | 22 | 15 | 0.682 | 17 | 3 |
| code-review-03 | 24 | 11 | 0.458 | 20 | 8 |
| code-review-04 | 21 | 11 | 0.524 | 19 | 2 |
| code-review-05 | 38 | 25 | 0.658 | 33 | 1 |
| debugging-01 | 7 | 7 | 1.0 | 8 | 0 |
| debugging-02 | 12 | 11 | 0.917 | 14 | 1 |
| debugging-03 | 12 | 12 | 1.0 | 12 | 0 |
| debugging-05 | 16 | 15 | 0.938 | 18 | 0 |
| explanation-02 | 22 | 15 | 0.682 | 21 | 1 |
| explanation-04 | 32 | 19 | 0.594 | 38 | 6 |
| explanation-05 | 14 | 12 | 0.857 | 10 | 0 |
| summarization-01 | 7 | 7 | 1.0 | 5 | 0 |
| summarization-03 | 14 | 14 | 1.0 | 14 | 0 |
| summarization-04 | 11 | 9 | 0.818 | 15 | 1 |
| summarization-05 | 9 | 7 | 0.778 | 5 | 0 |

Median fraction: 0.806 over 16 scored pairs.

Median additions: 1.0 over 16 scored pairs.

Lost facts:

- code-review-01: The mutable default argument is a classic Python gotcha.
- code-review-01: A bare `except:` catches everything, including `KeyboardInterrupt` and `SystemExit`.
- code-review-01: Nothing in the function prevents duplicate users.
- code-review-01: Nothing in the function prevents invalid roles.
- code-review-01: A boolean return means the caller cannot distinguish "insert failed", "db is None", and "duplicate user".
- code-review-01: The function has no type hints.
- code-review-01: The contract of the function is unclear.
- code-review-01: The `roles` parameter is presumably `list[str]`.
- code-review-01: Nothing documents or enforces the expected types of `roles` and `db`.
- code-review-02: The code throws `TypeError: Cannot read properties of undefined (reading 'name')`.
- code-review-02: The function will essentially always throw.
- code-review-02: An error response body parsed as JSON may lack a `name` field.
- code-review-02: The code does not validate the shape of the response.
- code-review-02: Nothing guards against `data` being `null`, missing `name`, or `name` not being a string before calling `.toUpperCase()`.
- code-review-02: The code does not validate `userId`.
- code-review-02: If `userId` is `undefined` or `null`, the request silently becomes `/api/users/undefined`.
- code-review-03: Any input containing a single quote breaks out of the string literal in the query.
- code-review-03: An attacker exploiting the injection can read, modify, or delete arbitrary data.
- code-review-03: SQL injection is the critical issue in this code, and the other problems are secondary.
- code-review-03: Placeholder syntax depends on the database driver.
- code-review-03: psycopg2 and MySQLdb use `%s` as the placeholder.
- code-review-03: sqlite3 uses `?` as the placeholder.
- code-review-03: With `SELECT *`, callers may break silently on schema migrations.
- code-review-03: The `status` parameter presumably comes from a fixed set of values such as `pending` and `shipped`.
- code-review-03: The code does not check that `status` is one of the allowed values.
- code-review-03: An invalid or misspelled `status` fails silently by returning zero rows instead of raising a clear error.
- code-review-03: The function does not handle the 'no results' case.
- code-review-03: The function returns an empty list with no distinction between no results and an error.
- code-review-03: The empty-list return may be acceptable depending on the caller, but the intended contract is worth confirming.
- code-review-04: A single attribute assignment is atomic under the GIL.
- code-review-04: Because attribute assignment is atomic, `reset` on its own will not corrupt the value.
- code-review-04: When a `reset` lands mid-increment, the increment overwrites the reset with `old_value + 1`, silently discarding it.
- code-review-04: In the fixed class, `__init__` sets `self._value` to 0 and creates `self._lock` as a `threading.Lock()`.
- code-review-04: In the fixed class, `increment` executes `self._value += 1` inside a `with self._lock:` block.
- code-review-04: In the fixed class, `reset` sets `self._value = 0` inside a `with self._lock:` block.
- code-review-04: In the fixed class, `value` is a `@property` that returns `self._value` while holding the lock.
- code-review-04: The fix renames the counter state from a public `value` attribute to a private `_value` attribute.
- code-review-04: Callers can read and write the public `value` attribute directly, bypassing any locking added inside the class.
- code-review-04: Making `value` a lock-protected property closes the direct-access hole.
- code-review-05: `rm -rf` on a nonexistent file only errors, which is harmless here
- code-review-05: If no `.log` files exist, `*.log` is passed literally to `ls`, which prints an error to stderr
- code-review-05: With no `.log` matches, the command substitution captures nothing useful or the literal string, depending on the shell
- code-review-05: No exit code reflects failure
- code-review-05: There is a potential race condition if the script runs concurrently with something writing new `.log` or `.tmp` files
- code-review-05: The race condition is minor for a cleanup script
- code-review-05: The suggested rewrite uses `set -eu`
- code-review-05: The suggested rewrite uses `BACKUP_DIR=${1:?Usage: $0 BACKUP_DIR}` to require the argument
- code-review-05: The suggested rewrite uses `rm -f -- *.tmp 2>/dev/null || true`
- code-review-05: The suggested rewrite calls `gzip -- "$f"`
- code-review-05: The key fixes are quoting all variable expansions, validating the argument, checking `cd` succeeded, avoiding `ls` in the loop, guarding against the no-match glob case, and using `set -eu`
- code-review-05: The `-r` (recursive) flag is not needed for matching plain files by extension
- code-review-05: Using `-r` suggests unintended recursion into directories named `*.tmp`
- debugging-02: When a plain function is called as a regular callback, `this` is undefined in strict mode or class context.
- debugging-05: In the fixed code, the body sets `tags = list(tags) if tags is not None else list(DEFAULT_TAGS)`.
- explanation-02: In the example, an orders table has a version column.
- explanation-02: In the example, the application reads version = 5 and updates with UPDATE orders SET status = 'shipped', version = 6 WHERE id = 42 AND version = 5.
- explanation-02: Optimistic locking fits when transactions are long-lived, such as a user editing a form for minutes.
- explanation-02: Optimistic locking fits in a distributed or stateless setup where holding a database lock across a network round trip is expensive.
- explanation-02: The pessimistic example uses BEGIN; SELECT * FROM accounts WHERE id = 42 FOR UPDATE; then deducts the balance and commits.
- explanation-02: Pessimistic locking fits when the critical section is short so lock hold time stays small.
- explanation-02: Long-lived operations, or high concurrency with rare actual conflicts, favor optimistic locking.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Because threads share memory, passing data between threads is just pointer access.
- explanation-04: Sharing memory between threads carries the risk of race conditions.
- explanation-04: Both processes and threads are scheduled by the OS.
- explanation-04: Threads are typically lighter to context-switch than processes because much of the state, such as memory mappings, is shared.
- explanation-04: Web servers such as Nginx and Gunicorn's process workers spawn a process per request or worker so one bad request cannot crash the whole server.
- explanation-04: Languages with a global interpreter lock let only one thread execute bytecode at a time, even on multiple cores.
- explanation-04: CPython has a global interpreter lock (the GIL).
- explanation-04: Ruby's MRI historically had a global interpreter lock.
- explanation-04: Multiple processes sidestep a global interpreter lock because each process has its own interpreter instance.
- explanation-04: Processes can run under different users, with different permissions, or in different sandboxes such as containers or seccomp filters.
- explanation-04: Separate processes allow components to be restarted, killed, or scaled independently via OS process management.
- explanation-04: A supervisor can restart a crashed worker process.
- explanation-05: Examples of long-lived collections include a global dictionary and an event-listener registry.
- explanation-05: An example of a callback capturing large objects is a closure holding a DOM node or a big buffer.
- summarization-04: The issue was reproduced on the latest version of Firefox on the reporter's laptop.
- summarization-04: The issue was reproduced on Chrome on a colleague's machine.
- summarization-05: Ada will run the payments database migration dry run.
- summarization-05: Chen will continue the search indexing work.

Added facts (styled only):

- code-review-01: The function has six problems.
- code-review-01: The corrected version raises `ValueError("name must not be empty")` when `name` is falsy.
- code-review-02: The function has five problems.
- code-review-02: The useless async keyword hides the real problem, because the function looks like it waits for the fetch but does not.
- code-review-02: If the fetch call fails, the error stays silent.
- code-review-03: Retrieving every column wastes bandwidth.
- code-review-03: The function does not check that `customer_name` and `status` are non-empty or well-formed.
- code-review-03: If `cursor.execute` fails, the function raises an unhandled exception.
- code-review-03: An unhandled exception leaves the caller without a clear error.
- code-review-03: A query returning a large number of rows can exhaust memory.
- code-review-03: A parameterized query sends the values separately from the SQL text.
- code-review-03: With a parameterized query, the database treats the values as data rather than as code.
- code-review-03: Treating the values as data stops SQL injection.
- code-review-04: There is no atomic operation in the code.
- code-review-04: The method has two separate byte-code operations with a thread switch possible between them.
- code-review-05: The script does not check that the argument is a directory.
- debugging-02: The arrow function is the simplest of the three fixes.
- explanation-02: Web applications with many readers and few writers are a common case for optimistic locking.
- explanation-04: A memory leak in one process cannot affect another process.
- explanation-04: A process-based design maps to a distributed system.
- explanation-04: Each process communicates through messages, not through shared memory.
- explanation-04: A process-based design ports well from one machine to a cluster.
- explanation-04: Processes help when tasks must scale across multiple machines.
- explanation-04: Plugins, codecs, and third-party libraries are common causes of freezes or crashes.
- summarization-04: The reproduction requires clicking the export button, then the PDF option.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-02 | 2 | 1 | 1 | 0 | 0.5 |
| code-review-03 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 3 | 0 | 1 | 2 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 1 | 1 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-01 | 2 | 1 | 0 | 1 | 1.0 |
| explanation-02 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-03 | 4 | 1 | 1 | 2 | 0.5 |
| explanation-04 | 4 | 1 | 1 | 2 | 0.5 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.5 over 12 scored pairs.

Claims that became certain:

- code-review-01: `roles` is presumably `list[str]`, and `db` presumably has an `.insert` method, but nothing documents or enforces this.
- code-review-02: The function will essentially always throw.
- code-review-03: Callers of `SELECT *` get columns they didn't ask for and may break silently on schema migrations.
- code-review-05: If no .log files exist, the literal `*.log` passed to `ls` means `$(...)` captures nothing useful, or possibly the literal string, depending on the shell, so the loop either does nothing or tries to gzip a nonexistent file named `*.log`
- debugging-05: In the full suite, another test likely calls `make_post` first (or this test itself is order-dependent across runs), so the list has already been mutated.
- explanation-02: The check for whether the data changed since you read it is usually done via a version number or timestamp.
- explanation-03: Slow start is essentially a probing mechanism: start small, ramp up quickly, and use packet loss (or explicit congestion signals) as feedback to find a sustainable sending rate.
- explanation-04: As a rule of thumb, threads are the right choice when work is CPU-parallel, trusted, and needs fast shared-state access, and processes when isolation is needed.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-02 | 2 | 0 | 2 | 0 | 0.0 |
| code-review-03 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 3 | 0 | 1 | 2 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-02 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-04 | 4 | 2 | 2 | 0 | 0.5 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-03 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 9 scored pairs.

Claims that became certain:

- code-review-01: The caller likely doesn't expect their list to change as a side effect when `roles` is passed in and `.append` mutates it in place.
- code-review-02: The function will essentially always throw.
- code-review-02: A 404/500 error body would still be parsed as "success" JSON, potentially without a `name` field.
- code-review-03: Callers of `SELECT *` get columns they didn't ask for and may break silently on schema migrations.
- code-review-05: If no .log files exist, the literal `*.log` passed to `ls` means `$(...)` captures nothing useful, or possibly the literal string, depending on the shell, so the loop either does nothing or tries to gzip a nonexistent file named `*.log`
- explanation-02: The check for whether the data changed since you read it is usually done via a version number or timestamp.
- explanation-04: Threads are typically lighter to context-switch than processes, since much of the state (memory mappings) is shared.
- explanation-04: As a rule of thumb, threads are the right choice when work is CPU-parallel, trusted, and needs fast shared-state access, and processes when isolation is needed.
- summarization-01: A crash could occur when opening settings during a file upload.

## Warnings

- technical-simplified/explanation-01: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
