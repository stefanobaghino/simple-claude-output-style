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

Judge: opus. Judged on 2026-08-05T21:07:58+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 27 | 27 | 1.0 | 34 | 3 |
| code-review-02 | 23 | 19 | 0.826 | 21 | 3 |
| code-review-03 | 26 | 13 | 0.5 | 17 | 4 |
| code-review-04 | 25 | 20 | 0.8 | 19 | 0 |
| code-review-05 | 33 | 26 | 0.788 | 42 | 9 |
| debugging-01 | 7 | 6 | 0.857 | 6 | 0 |
| debugging-02 | 8 | 8 | 1.0 | 14 | 0 |
| debugging-03 | 11 | 11 | 1.0 | 8 | 0 |
| debugging-04 | 15 | 12 | 0.8 | 19 | 4 |
| debugging-05 | 13 | 11 | 0.846 | 13 | 0 |
| explanation-01 | 30 | 19 | 0.633 | 27 | 2 |
| explanation-02 | 25 | 17 | 0.68 | 26 | 4 |
| explanation-03 | 39 | 26 | 0.667 | 27 | 3 |
| explanation-04 | 41 | 25 | 0.61 | 34 | 1 |
| explanation-05 | 19 | 15 | 0.789 | 16 | 3 |
| summarization-01 | 6 | 5 | 0.833 | 5 | 0 |
| summarization-02 | 15 | 12 | 0.8 | 16 | 4 |
| summarization-03 | 14 | 14 | 1.0 | 14 | 0 |
| summarization-04 | 14 | 11 | 0.786 | 10 | 0 |
| summarization-05 | 9 | 9 | 1.0 | 12 | 2 |

Median fraction: 0.8 over 20 scored pairs.

Median additions: 2.0 over 20 scored pairs.

Lost facts:

- code-review-02: The returned Promise resolves or rejects based on the synchronous throw rather than on the fetch result.
- code-review-02: The function does not validate the shape of the response.
- code-review-02: The function assumes `data` always has a `name` field.
- code-review-02: If the API returns something else, such as an error object, the `.toUpperCase()` call fails.
- code-review-03: Stacked or UNION-based payloads are a worse form of SQL injection attack.
- code-review-03: The sqlite3 module uses `?` placeholders instead of `%s`.
- code-review-03: The code has no error handling.
- code-review-03: `cursor.execute` can raise errors from a bad connection, a syntax error, or a constraint issue.
- code-review-03: Nothing in the code catches or surfaces execution errors meaningfully to the caller.
- code-review-03: There is a quoting bug independent of injection.
- code-review-03: A legitimate name containing a single quote, such as `O'Brien`, breaks the query even without malicious intent.
- code-review-03: `status` may be meant to be an enum-like set such as "pending", "shipped", or "cancelled".
- code-review-03: The function has no docstring or type hints.
- code-review-03: The missing docstring and type hints is a minor issue.
- code-review-03: The function signature gives no indication of expected types or return shape.
- code-review-03: The SQL injection is the critical, must-fix issue.
- code-review-03: All the other issues are secondary to the SQL injection.
- code-review-04: The class's `reset()` method is an unsynchronized read-modify-write operation.
- code-review-04: CPython has a GIL.
- code-review-04: The GIL only guarantees that individual bytecode operations are atomic.
- code-review-04: The GIL does not guarantee atomicity for multi-step sequences such as a read-modify-write.
- code-review-04: The proposed fix uses `threading.Lock` and a `with self._lock:` block in `increment()`, `reset()`, and a `value` property.
- code-review-05: `cd -- "$BACKUP_DIR"` is the correct form for the `cd` call.
- code-review-05: Parsing `ls` output breaks on filenames containing spaces or newlines.
- code-review-05: Parsing `ls` output mangles filenames containing glob characters.
- code-review-05: The script's `gzip` call lacks the `-f` flag and has no error reporting.
- code-review-05: If no `.log` files exist, the loop silently does nothing and gives no feedback.
- code-review-05: A safer rewrite uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` to require the argument.
- code-review-05: A safer rewrite calls `gzip -f -- "$f"`.
- debugging-01: The mismatched lookup raises a KeyError.
- debugging-04: A file might not be valid UTF-8, for example if it is Latin-1 or mixed encodings.
- debugging-04: Opening the file in binary mode with open(path, "rb") and counting b"\n" occurrences yields a line count.
- debugging-04: Counting newlines in binary mode sidesteps encoding issues entirely.
- debugging-05: In the fixed code, when `tags` is `None`, a new list is created via `list(DEFAULT_TAGS)`.
- debugging-05: `DEFAULT_TAGS` is module-level state.
- explanation-01: Collisions are inevitable because the array has a limited number of slots.
- explanation-01: Collisions are not a bug but expected behavior that every hash map must handle.
- explanation-01: The collection used in chaining is usually a linked list and sometimes a tree.
- explanation-01: Quadratic probing jumps by increasing steps at offsets index+1, index+4, index+9, and so on.
- explanation-01: Double hashing uses a second hash function to decide the step size.
- explanation-01: Open addressing degrades badly at high load, as probing gets expensive and resizing is needed sooner.
- explanation-01: Deletion under chaining is simple, requiring only removal from the list.
- explanation-01: Deletion under open addressing is tricky and requires tombstone markers so probing sequences don't break.
- explanation-01: Open addressing is more sensitive to the map filling up and requires more careful implementation, especially for deletes.
- explanation-01: Java's HashMap uses chaining with tree conversion for long chains.
- explanation-01: Go's map uses an open addressing variant.
- explanation-02: In SQL, `SELECT ... FOR UPDATE` locks the selected row.
- explanation-02: The `FOR UPDATE` clause prevents other transactions from reading-for-update or modifying the row until the current transaction commits.
- explanation-02: In the optimistic SQL pattern, 0 rows affected means someone else updated the record first, so the client must reload and retry.
- explanation-02: Inventory decrements where overselling is unacceptable are an example where pessimistic locking fits.
- explanation-02: Pessimistic locking carries a risk of deadlocks and blocking.
- explanation-02: CMS editing and most CRUD APIs are examples where optimistic locking fits.
- explanation-02: Distributed and web applications are examples where optimistic locking fits.
- explanation-02: Holding a database lock across a user's think-time is impractical in distributed/web apps.
- explanation-03: A network path may be a fast, uncongested link, or a slow link already shared by many other connections.
- explanation-03: Historically, the initial cwnd was 1 segment.
- explanation-03: Modern initial cwnd is typically 2 to 10 segments, depending on the TCP implementation.
- explanation-03: Congestion avoidance uses linear growth rather than exponential growth.
- explanation-03: After loss, depending on the algorithm, TCP may re-enter a modified slow start or drop into congestion avoidance.
- explanation-03: The name 'slow start' is ironic given how fast it grows the window.
- explanation-03: Starting at one full window with no ramp-up risks massive congestion collapse if many connections do it at once.
- explanation-03: Real congestion collapse incidents occurred on the early Internet in the 1980s.
- explanation-03: The 1980s congestion collapse incidents motivated the invention of congestion control.
- explanation-03: Growing the window linearly from the start would take too long to reach a reasonable sending rate on high-bandwidth paths.
- explanation-03: Linear growth from the start would waste capacity for many round trips.
- explanation-03: The network has no way to tell a TCP sender to slow down except by dropping packets.
- explanation-03: Packet loss is the network's only available signal for a sender to stop escalating its rate.
- explanation-04: A process has its own file descriptors and OS resources.
- explanation-04: Each process has its own heap, stack, and data segments.
- explanation-04: Threads in the same process share the same address space, heap, and most OS resources.
- explanation-04: Each thread gets its own stack and register state, including the program counter.
- explanation-04: nginx uses separate worker processes.
- explanation-04: systemd is a supervisor that isolates work into separate processes.
- explanation-04: Erlang/OTP-style architectures isolate risky or untrusted work into separate processes.
- explanation-04: Python's multiprocessing module can be used instead of threading to get real parallelism.
- explanation-04: Processes can run under different users, permissions, or sandboxes.
- explanation-04: A thread shares everything with other threads in its process.
- explanation-04: Browser tabs, plugins, and sandboxed compute are examples of untrusted code that may need isolation.
- explanation-04: Separate processes make it clean to restart, update, or scale a component independently.
- explanation-04: A worker pool of separate processes can be killed and respawned without affecting the parent.
- explanation-04: You cannot restart a single thread without tearing down the whole process.
- explanation-04: Locks create risk of deadlocks, race conditions, and subtle corruption.
- explanation-04: Handling separate client requests with no shared mutable state is an example of largely independent work.
- explanation-05: Live roots include globals, running closures, and caches.
- explanation-05: Eviction strategies include LRU, TTL, and size caps.
- explanation-05: Long-lived objects that callbacks are registered on include DOM nodes, event emitters, and global buses.
- explanation-05: A listener closes over its surrounding scope.
- summarization-01: App cold start is about 40% quicker.
- summarization-02: Paging happened at 09:21.
- summarization-02: The gap between errors starting and paging was 7 minutes.
- summarization-02: The incident response itself was solid.
- summarization-04: One error banner appears per click of the PDF export button.
- summarization-04: The issue was reproduced on the latest Firefox on macOS.
- summarization-04: The issue was reproduced on Chrome on a colleague's machine.

Added facts (styled only):

- code-review-01: Python creates the empty list for a default argument only once, when the function is defined.
- code-review-01: The code should catch a specific exception, such as the database library's own error type.
- code-review-01: The function does not check that roles contains valid values.
- code-review-02: Marking a function `async` only matters if you use `await` inside it or if you want it to return a promise.
- code-review-02: The `async` keyword hides the timing bug in this function.
- code-review-02: fetch only rejects on a network failure.
- code-review-03: The function has four problems.
- code-review-03: The query has no result limit.
- code-review-03: If many rows match, the function loads them all into memory at once.
- code-review-03: Adding a `LIMIT` clause or fetching rows in batches addresses the missing result limit when the table can grow large.
- code-review-05: `cd "$BACKUP_DIR" || { echo "Cannot cd to $BACKUP_DIR" >&2; exit 1; }` checks the `cd` result and exits on failure.
- code-review-05: `[ -z "$1" ]` can be used to test whether the first argument is missing.
- code-review-05: If no `.log` files exist, `for f in *.log` iterates once with the literal string `*.log`.
- code-review-05: POSIX `sh` has no `nullglob` option.
- code-review-05: `gzip` can fail because a file is already compressed, permission is denied, or the disk is full.
- code-review-05: `echo Cleaned $BACKUP_DIR` always prints, even if earlier commands failed.
- code-review-05: The unconditional success message gives false confidence that the cleanup worked.
- code-review-05: The rewrite uses `${1:-}` in the argument check.
- code-review-05: Recursive delete on a glob is worth avoiding unless specifically needed.
- debugging-04: UTF-8 can read plain ASCII text.
- debugging-04: Switching to UTF-8 will not break files that were pure ASCII before.
- debugging-04: Encoding detection can be done before opening the file.
- debugging-04: Using errors="replace" or errors="ignore" causes some characters to be lost or altered.
- explanation-01: Most general-purpose hash maps use chaining.
- explanation-01: Performance-critical hash map implementations use open addressing.
- explanation-02: In the support ticket example, the ticket table has a `version` column.
- explanation-02: If you read a ticket at version 5 and edit it, the database checks at save time that the version is still 5.
- explanation-02: If another agent saved a change and bumped the ticket to version 6, your save fails and you see an error asking you to reload and try again.
- explanation-02: Most web applications have rare conflicts because users edit different records most of the time.
- explanation-03: TCP must resend dropped packets.
- explanation-03: Resending dropped packets wastes bandwidth and slows things down for everyone sharing that network path.
- explanation-03: A connection resuming after a pause starts slower than an established, actively-flowing one.
- explanation-04: Threads are faster to switch between than processes.
- explanation-05: Wasted memory from leaks builds up over time.
- explanation-05: Accumulated leaked memory can slow down a program.
- explanation-05: Accumulated leaked memory can crash a program.
- summarization-02: A staging configuration value reached production and broke checkout.
- summarization-02: The production checkout service requires a connection pool size of 50.
- summarization-02: The deploy dropped the connection pool below what the checkout service needs.
- summarization-02: 12% of requests failed as a result of the incident.
- summarization-05: Ada is to run the payments database migration dry run before Thursday.
- summarization-05: There is a payments database migration planned.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 27 | 19 | 0.704 | 23 | 4 |
| code-review-02 | 23 | 18 | 0.783 | 21 | 4 |
| code-review-03 | 26 | 14 | 0.538 | 22 | 5 |
| code-review-04 | 25 | 16 | 0.64 | 23 | 5 |
| code-review-05 | 33 | 20 | 0.606 | 28 | 7 |
| debugging-01 | 7 | 6 | 0.857 | 8 | 2 |
| debugging-02 | 8 | 8 | 1.0 | 11 | 0 |
| debugging-03 | 11 | 11 | 1.0 | 9 | 0 |
| debugging-04 | 15 | 9 | 0.6 | 8 | 1 |
| debugging-05 | 13 | 12 | 0.923 | 15 | 0 |
| explanation-02 | 25 | 20 | 0.8 | 33 | 7 |
| explanation-03 | 39 | 24 | 0.615 | 25 | 2 |
| explanation-04 | 41 | 25 | 0.61 | 26 | 1 |
| explanation-05 | 19 | 13 | 0.684 | 14 | 0 |
| summarization-03 | 14 | 14 | 1.0 | 13 | 0 |
| summarization-04 | 14 | 9 | 0.643 | 12 | 1 |
| summarization-05 | 9 | 9 | 1.0 | 8 | 2 |

Median fraction: 0.704 over 17 scored pairs.

Median additions: 2 over 17 scored pairs.

Lost facts:

- code-review-01: `roles.append("member")` mutates whatever list object was passed in by the caller.
- code-review-01: Mutating the caller's list silently changes the caller's data as a side effect.
- code-review-01: The function has a `db=None` default but never checks whether `db` is None.
- code-review-01: If `db` isn't passed, `db.insert(...)` raises `AttributeError`.
- code-review-01: The function has no duplicate protection for the `"member"` role.
- code-review-01: The corrected version raises `ValueError("name is required")` when `name` is falsy.
- code-review-01: The corrected version raises `ValueError("db is required")` when `db` is None.
- code-review-01: The corrected version copies `roles` with `list(roles)` and appends `"member"` only if not already present.
- code-review-02: The error message is "Cannot read properties of undefined (reading 'name')".
- code-review-02: The function is declared `async` but never awaits anything.
- code-review-02: The `async` keyword is pointless as the function is written.
- code-review-02: The `async` keyword makes the function return a Promise.
- code-review-02: The returned Promise resolves or rejects based on the synchronous throw rather than on the fetch result.
- code-review-03: A value like `x' OR '1'='1` lets an attacker read or manipulate arbitrary data.
- code-review-03: Stacked or UNION-based payloads are a worse form of SQL injection attack.
- code-review-03: The sqlite3 module uses `?` placeholders instead of `%s`.
- code-review-03: `cursor.execute` can raise errors from a bad connection, a syntax error, or a constraint issue.
- code-review-03: There is a quoting bug independent of injection.
- code-review-03: A legitimate name containing a single quote, such as `O'Brien`, breaks the query even without malicious intent.
- code-review-03: `status` is not validated against allowed values.
- code-review-03: `status` may be meant to be an enum-like set such as "pending", "shipped", or "cancelled".
- code-review-03: There is no check that `status` is one of the allowed values before hitting the database.
- code-review-03: The function has no docstring or type hints.
- code-review-03: The missing docstring and type hints is a minor issue.
- code-review-03: The function signature gives no indication of expected types or return shape.
- code-review-04: The class's `reset()` method is an unsynchronized read-modify-write operation.
- code-review-04: CPython has a GIL.
- code-review-04: The GIL only guarantees that individual bytecode operations are atomic.
- code-review-04: The GIL does not guarantee atomicity for multi-step sequences such as a read-modify-write.
- code-review-04: The race condition is real and reproducible under load.
- code-review-04: The proposed fix uses `threading.Lock` and a `with self._lock:` block in `increment()`, `reset()`, and a `value` property.
- code-review-04: `itertools.count()` provides thread-safe increment via `next()`.
- code-review-04: `itertools.count()` and `multiprocessing.Value`-style atomics are alternatives when higher throughput than a lock is needed.
- code-review-04: A plain lock is the simplest correct fix for this class.
- code-review-05: `cd -- "$BACKUP_DIR"` is the correct form for the `cd` call.
- code-review-05: Parsing `ls` output mangles filenames containing glob characters.
- code-review-05: `gzip` will fail non-fatally and silently on a file that is already gzipped or unreadable.
- code-review-05: The script's `gzip` call lacks the `-f` flag and has no error reporting.
- code-review-05: If no `.log` files exist, `*.log` will not glob-expand absent nullglob-like behavior.
- code-review-05: If no `.log` files exist, the loop silently does nothing and gives no feedback.
- code-review-05: Combined with the missing argument validation and missing `cd` check, `rm -rf *.tmp` is the script's most dangerous line.
- code-review-05: A safer rewrite uses `set -eu`.
- code-review-05: A safer rewrite uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` to require the argument.
- code-review-05: A safer rewrite tests `[ -d "$BACKUP_DIR" ]` and exits with an error message to stderr otherwise.
- code-review-05: A safer rewrite uses `rm -f -- *.tmp` rather than `rm -rf *.tmp`.
- code-review-05: A safer rewrite iterates with `for f in *.log` and skips nonexistent entries with `[ -e "$f" ] || continue`.
- code-review-05: A safer rewrite calls `gzip -f -- "$f"`.
- debugging-01: The mismatched lookup raises a KeyError.
- debugging-04: Any byte greater than or equal to 0x80 causes an error when decoding with the ascii encoding.
- debugging-04: A file might not be valid UTF-8, for example if it is Latin-1 or mixed encodings.
- debugging-04: Encoding can be detected or negotiated using libraries such as chardet or charset-normalizer.
- debugging-04: Passing errors="ignore" to open is another permissive option.
- debugging-04: Opening the file in binary mode with open(path, "rb") and counting b"\n" occurrences yields a line count.
- debugging-04: Counting newlines in binary mode sidesteps encoding issues entirely.
- debugging-05: Run alone, the test sees the list start as `["draft"]` and become `["draft", "post"]`, which is the expected result.
- explanation-02: Inventory decrements where overselling is unacceptable are an example where pessimistic locking fits.
- explanation-02: Pessimistic locking carries a risk of deadlocks and blocking.
- explanation-02: CMS editing and most CRUD APIs are examples where optimistic locking fits.
- explanation-02: Distributed and web applications are examples where optimistic locking fits.
- explanation-02: Holding a database lock across a user's think-time is impractical in distributed/web apps.
- explanation-03: A network path may be a fast, uncongested link, or a slow link already shared by many other connections.
- explanation-03: Historically, the initial cwnd was 1 segment.
- explanation-03: Modern initial cwnd is typically 2 to 10 segments, depending on the TCP implementation.
- explanation-03: On packet loss, TCP shrinks the congestion window sharply.
- explanation-03: After loss, depending on the algorithm, TCP may re-enter a modified slow start or drop into congestion avoidance.
- explanation-03: The name 'slow start' is ironic given how fast it grows the window.
- explanation-03: The 'slow' in slow start refers to being more cautious than sending as much data as the receiver's window allows from the first packet.
- explanation-03: Sending at the full receiver window immediately ignores the state of the network between sender and receiver.
- explanation-03: Starting at one full window with no ramp-up risks massive congestion collapse if many connections do it at once.
- explanation-03: Real congestion collapse incidents occurred on the early Internet in the 1980s.
- explanation-03: The 1980s congestion collapse incidents motivated the invention of congestion control.
- explanation-03: Growing the window linearly from the start would take too long to reach a reasonable sending rate on high-bandwidth paths.
- explanation-03: Linear growth from the start would waste capacity for many round trips.
- explanation-03: The network has no way to tell a TCP sender to slow down except by dropping packets.
- explanation-03: Packet loss is the network's only available signal for a sender to stop escalating its rate.
- explanation-04: A process has its own file descriptors and OS resources.
- explanation-04: Each process has its own heap, stack, and data segments.
- explanation-04: Threads in the same process share the same address space, heap, and most OS resources.
- explanation-04: Each thread gets its own stack and register state, including the program counter.
- explanation-04: Chrome isolates risky or untrusted work into separate processes.
- explanation-04: nginx uses separate worker processes.
- explanation-04: systemd is a supervisor that isolates work into separate processes.
- explanation-04: Erlang/OTP-style architectures isolate risky or untrusted work into separate processes.
- explanation-04: Older Ruby MRI has a global interpreter lock.
- explanation-04: Python's multiprocessing module can be used instead of threading to get real parallelism.
- explanation-04: A thread shares everything with other threads in its process.
- explanation-04: Browser tabs, plugins, and sandboxed compute are examples of untrusted code that may need isolation.
- explanation-04: Threads sharing memory requires locks.
- explanation-04: Locks create risk of deadlocks, race conditions, and subtle corruption.
- explanation-04: For largely independent work, processes avoid an entire class of concurrency bugs by construction.
- explanation-04: Handling separate client requests with no shared mutable state is an example of largely independent work.
- explanation-05: A memory leak in a garbage-collected language is not a failure of the collector.
- explanation-05: A memory leak in a garbage-collected language is a bug in the program's own reference graph.
- explanation-05: Live roots include globals, running closures, and caches.
- explanation-05: Eviction strategies include LRU, TTL, and size caps.
- explanation-05: Long-lived objects that callbacks are registered on include DOM nodes, event emitters, and global buses.
- explanation-05: A listener closes over its surrounding scope.
- summarization-04: After clicking the PDF export option, nothing happens initially.
- summarization-04: One error banner appears per click of the PDF export button.
- summarization-04: The error banners give no additional details.
- summarization-04: The issue was reproduced on the latest Firefox on macOS.
- summarization-04: The issue was reproduced on Chrome on a colleague's machine.

Added facts (styled only):

- code-review-01: Hiding the real error makes it impossible to find bugs.
- code-review-01: The corrected version raises `ValueError` with the message "name must not be empty" when `name` is falsy.
- code-review-01: The corrected version raises `ValueError` with the message "db must not be None" when `db` is `None`.
- code-review-01: With the corrected version, the caller can catch specific exceptions and handle each case.
- code-review-02: The caller receives undefined instead of the profile name.
- code-review-02: A network failure will produce an unhandled promise rejection.
- code-review-02: A JSON parse error will produce an unhandled promise rejection.
- code-review-02: The suggested fix throws an Error when data.name is missing.
- code-review-03: The exception handling should either be delegated to the caller or handled with a try block in the function.
- code-review-03: The query has no result limit.
- code-review-03: The query can return many rows.
- code-review-03: Adding a `LIMIT` clause or paginating the results would bound the number of rows returned.
- code-review-03: A docstring should state the parameters, the return value, and the exceptions the function can raise.
- code-review-04: The fixed `Counter.__init__` creates a `threading.Lock` stored as `self._lock` and sets `self.value` to 0.
- code-review-04: In the fixed version, `increment` performs `self.value += 1` while holding `self._lock`.
- code-review-04: In the fixed version, `reset` sets `self.value` to 0 while holding `self._lock`.
- code-review-04: The fixed version adds a `get` method that returns `self.value` while holding `self._lock`.
- code-review-04: The `get` method lets callers avoid reading `self.value` outside the lock.
- code-review-05: Without `--`, `rm` can interpret a file name that starts with a dash as an option.
- code-review-05: If no `.log` files exist, `ls *.log` writes an error to standard error.
- code-review-05: Without error handling, the script continues after a failed step and can report success at the end despite a failure.
- code-review-05: If a user passes `/` or `.` as the path, `rm -rf *.tmp` can delete files outside the intended backup folder.
- code-review-05: Line 8 runs `echo Cleaned $BACKUP_DIR` without quoting `$BACKUP_DIR`.
- code-review-05: The unquoted variable in the echo on line 8 is a small risk in this script.
- code-review-05: The unquoted variable in the echo on line 8 is inconsistent with safe scripting practice.
- debugging-01: The config dictionary maps 'host' to 'localhost' and 'port' to 8080.
- debugging-01: The corrected code calls print(get_url(config)).
- debugging-04: The file has a non-ASCII byte at position 512.
- explanation-02: In the example, a `products` row has a `version` column.
- explanation-02: In the example, the row is read as `price = 10, version = 3`.
- explanation-02: In the example, the price is updated to 12 with the condition `WHERE id = 1 AND version = 3`.
- explanation-02: In the example, the update also sets `version = 4`.
- explanation-02: If another user updated the row first, the version is no longer 3.
- explanation-02: Under pessimistic locking, other transactions trying to read or write the same row must wait until the locking transaction commits or rolls back.
- explanation-02: Optimistic locking's lock timing is at write time, only on conflict.
- explanation-03: TCP slow start lets the sender find a safe sending rate without causing congestion first.
- explanation-03: When slow start ends, TCP moves into congestion avoidance.
- explanation-04: Switching between processes is more costly because the operating system must change the memory map.
- summarization-04: The app does not disable the export button while an export is running.
- summarization-05: Ada is assigned to run the dry run of the payments database migration.
- summarization-05: The dry run of the payments database migration is due before Thursday.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 0 | 0 | 0 | 0 | n/a |
| code-review-04 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 1 | 0 | 1 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 4 scored pairs.

Claims that became certain:

- code-review-04: If a `get_value()` were added (or callers read `.value` directly), it could observe a torn/inconsistent state relative to concurrent writers.
- explanation-03: When a packet is lost, TCP shrinks the window sharply and, depending on the algorithm, may re-enter a modified slow start or drop into congestion avoidance.
- summarization-04: The issue is likely not browser-specific, as suggested by reproduction on Firefox (latest) on macOS and Chrome on a colleague's machine.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 0 | 0 | 0 | 0 | n/a |
| code-review-04 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 0 | 1 | 1 | 0.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 2 | 0 | 1 | 1 | 0.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 4 scored pairs.

Claims that became certain:

- code-review-04: If a `get_value()` were added (or callers read `.value` directly), it could observe a torn/inconsistent state relative to concurrent writers.
- debugging-04: The byte 0xC3 suggests the file contains UTF-8-encoded text, e.g. a byte from a multi-byte UTF-8 sequence like an accented character.
- explanation-03: When a packet is lost, TCP shrinks the window sharply and, depending on the algorithm, may re-enter a modified slow start or drop into congestion avoidance.

## Warnings

- technical-simplified/summarization-01: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
- technical-simplified/explanation-01: the pair failed the gate, excluded
