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

Judge: opus. Judged on 2026-08-06T06:58:36+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 26 | 24 | 0.923 | 21 | 2 |
| code-review-02 | 13 | 10 | 0.769 | 13 | 0 |
| code-review-03 | 20 | 13 | 0.65 | 22 | 2 |
| code-review-04 | 16 | 11 | 0.688 | 23 | 3 |
| code-review-05 | 31 | 25 | 0.806 | 36 | 5 |
| debugging-01 | 7 | 7 | 1.0 | 9 | 0 |
| debugging-02 | 18 | 13 | 0.722 | 13 | 2 |
| debugging-03 | 11 | 11 | 1.0 | 8 | 1 |
| debugging-04 | 13 | 8 | 0.615 | 11 | 2 |
| debugging-05 | 19 | 18 | 0.947 | 20 | 0 |
| explanation-01 | 31 | 24 | 0.774 | 27 | 0 |
| explanation-02 | 22 | 17 | 0.773 | 34 | 6 |
| explanation-03 | 36 | 25 | 0.694 | 25 | 2 |
| explanation-04 | 38 | 24 | 0.632 | 29 | 0 |
| explanation-05 | 21 | 17 | 0.81 | 18 | 3 |
| summarization-01 | 6 | 6 | 1.0 | 6 | 1 |
| summarization-02 | 15 | 11 | 0.733 | 16 | 5 |
| summarization-03 | 13 | 12 | 0.923 | 12 | 0 |
| summarization-04 | 13 | 13 | 1.0 | 15 | 3 |
| summarization-05 | 10 | 10 | 1.0 | 13 | 2 |

Median fraction: 0.79 over 20 scored pairs.

Median additions: 2.0 over 20 scored pairs.

Lost facts:

- code-review-01: Mutating the caller's list is a side effect the caller did not request, and is surprising and hard to trace.
- code-review-01: Returning only `True`/`False` discards error context such as a stack trace, a validation message, or an inserted ID.
- code-review-02: The code does not handle the case where the `name` field is missing from the API response.
- code-review-02: If the API response lacks a `name` field, calling `.toUpperCase()` throws.
- code-review-02: The minimal fix is to `await fetch(`/api/users/${userId}`)`, throw an Error including the user ID and `res.status` when `res.ok` is false, `await res.json()`, and return `profile.name.toUpperCase()`.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: `SELECT *` wastes bandwidth for wide tables.
- code-review-03: sqlite3, psycopg2, and pymysql all support parameterized queries.
- code-review-03: The code does not check that `customer_name` and `status` are non-empty strings, of correct type, or within expected length or enum.
- code-review-03: `status` presumably should be one of a fixed set of values.
- code-review-03: sqlite3 uses `?` placeholders instead of `%s`.
- code-review-03: The remaining issues (`SELECT *`, validation, error handling, pagination) are judgment calls depending on how the function is used.
- code-review-04: The lost-increment race can occur even without the GIL releasing mid-expression.
- code-review-04: Splitting the read-modify-write into two separate statements makes the race window larger.
- code-review-04: Without an explicit accessor and lock, callers can observe torn or stale counter values.
- code-review-04: Exposing the count through a `@property` that acquires the lock makes reads synchronized.
- code-review-04: Making `increment`, `reset`, and reads mutually exclusive ensures no updates are lost and readers never see stale or torn values.
- code-review-05: If no `*.log` files exist, the `ls *.log` version prints an `ls` error to stderr.
- code-review-05: The `ls *.log` version can behave unpredictably depending on the shell and the `ls` implementation.
- code-review-05: The empty-glob case can alternatively be handled with `compgen` or `nullglob` equivalents.
- code-review-05: Without `-f`, rerunning gzip on a directory with existing `.gz` files will hang waiting for confirmation or fail, depending on the gzip version and tty.
- code-review-05: Using `#!/bin/sh` means relying only on POSIX sh features.
- code-review-05: The `for f in $(ls *.log)` construct is more of a bash idiom, creating a mismatch between intent and interpreter.
- debugging-02: Inside the callback, `this` is `undefined`.
- debugging-02: Class bodies are in strict mode by default in JavaScript.
- debugging-02: Because `this` is undefined, `this.seconds` evaluates to `undefined`.
- debugging-02: Calling `.bind(this)` on a regular function callback is an alternative fix.
- debugging-02: Capturing `this` in a variable such as `const self = this;` before the callback is an alternative fix.
- debugging-04: Python source files are UTF-8 today.
- debugging-04: Most text files today are UTF-8.
- debugging-04: A file that is not valid UTF-8 could be Latin-1 or mixed encodings.
- debugging-04: Using errors="replace" still counts lines correctly.
- debugging-04: Decoding errors do not affect newline detection.
- debugging-05: The test can also fail if the test module is imported or collected multiple times.
- explanation-01: Because the underlying array has a finite number of slots, collisions are eventually inevitable by the pigeonhole principle.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Double hashing uses a second hash function to compute the probe step size.
- explanation-01: In the worst case, separate chaining degrades to a list traversal per bucket.
- explanation-01: Open addressing can suffer from clustering, where probes pile up near occupied slots.
- explanation-01: Clustering degrades open addressing performance badly when the load factor is high.
- explanation-01: Open addressing needs the load factor kept lower for good performance, often resizing around 0.7.
- explanation-02: SELECT ... FOR UPDATE locks the selected row.
- explanation-02: A row locked with SELECT ... FOR UPDATE cannot be read-for-update or modified by another transaction until the locking transaction commits or rolls back.
- explanation-02: Pessimistic locking fits short transactions, because blocking is brief.
- explanation-02: Editing a document is an example use case for optimistic locking.
- explanation-02: Optimistic locking fits long-running transactions or user-facing edits, where holding a database lock for the whole duration would be wasteful or impossible.
- explanation-03: When a TCP connection starts, the sender does not know how many other connections are sharing the path's bandwidth.
- explanation-03: When a TCP connection starts, the sender does not know how much buffering exists in routers along the path.
- explanation-03: If many connections send too fast at once, the network can enter congestion collapse.
- explanation-03: Congestion collapse is a state where so much traffic is retransmitted lost data that almost no useful data gets through.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: Historically, the initial cwnd was 1 segment.
- explanation-03: RFC 6928 specifies the initial congestion window of around 10 segments.
- explanation-03: In congestion avoidance, cwnd grows roughly linearly, at about one segment per RTT.
- explanation-03: The sender uses congestion avoidance because it believes it is close to the network's actual capacity and wants to probe more cautiously.
- explanation-03: Exponential search is an efficient way to close in on the right order of magnitude when the sender starts with almost no information.
- explanation-03: Slow start hands off to the linear growth of congestion avoidance once the sender is in the right neighborhood of capacity.
- explanation-04: A process has its own memory address space, file descriptors, and OS-level resources.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, and message queues.
- explanation-04: The operating system mediates inter-process communication.
- explanation-04: Each thread has its own stack and instruction pointer.
- explanation-04: Chrome isolates risky or untrusted work into separate processes.
- explanation-04: Nginx uses separate worker processes.
- explanation-04: systemd is a supervisor that isolates work into separate processes.
- explanation-04: Erlang/OTP-style architectures isolate risky or untrusted work into separate processes.
- explanation-04: Older versions of Ruby have a global interpreter lock.
- explanation-04: Processes can be further restricted with different privilege levels, sandboxes, or containers.
- explanation-04: Resource limits include memory limits and CPU quotas via cgroups or ulimits.
- explanation-04: OS resource limits cannot be applied to a single thread.
- explanation-04: Processes generalize to distributed systems across separate machines in a way threads do not.
- explanation-04: Architecting with processes and message-passing/IPC from the start makes later scaling out a smaller leap than scaling out a shared-memory multithreaded design.
- explanation-05: Memory is unreachable when no live reference chain from GC roots reaches it.
- explanation-05: The reference in a listener leak can go in either direction between the listener and the object.
- explanation-05: Closures capturing large scopes unintentionally are a frequent cause of memory leaks.
- explanation-05: Static or global variables accumulating references over time are a frequent cause of memory leaks.
- summarization-02: The config review checklist does not check other environment-sensitive values.
- summarization-02: The incident was paged out 7 minutes after detection.
- summarization-02: The incident was resolved in 34 minutes.
- summarization-02: Recommended preventive measures are separating or clearly differentiating the config templates and adding pool size to the review checklist.
- summarization-03: A worker pool would generate the real thumbnails and update the record afterward.

Added facts (styled only):

- code-review-01: The function has five problems.
- code-review-01: Error handling should be added back only for a specific failure case, such as retrying on a connection error.
- code-review-03: SQL placeholder syntax varies by database driver, including `%s`, `?`, and `:name`.
- code-review-03: A bad connection or a lock timeout can cause `cursor.execute` to fail.
- code-review-04: A race condition of this kind is also called a 'lost update'.
- code-review-04: A write at the end of increment() can overwrite a reset that occurred during the increment.
- code-review-04: A reset that is overwritten can leave the counter at 6 immediately after the reset, which is incorrect.
- code-review-05: The `for f in *.log` loop with no matching files would try to `gzip` a file literally named `*.log`.
- code-review-05: Gzipping a literally named `*.log` file causes a "no such file" error.
- code-review-05: Unmatched globs can be guarded against with `set -- *.log; [ -e "$1" ] || continue`.
- code-review-05: `set -u` makes a shell script error on unset variables.
- code-review-05: The script prints "Cleaned" regardless of what actually happened.
- debugging-02: When setInterval calls a regular function, `this` refers to the global object.
- debugging-02: The NaN value is logged every second.
- debugging-03: `moving_sum([1, 2, 3, 4], 2)` returns `[3, 5, 7]`.
- debugging-04: UTF-8 covers plain ASCII text.
- debugging-04: UTF-8 covers most non-English text.
- explanation-02: In the example, two coworkers open the same product listing at version 5 in an inventory system.
- explanation-02: In the example, the first user changes the price and saves, and the database updates the record to version 6.
- explanation-02: In a bank transfer, the system locks both account rows for the duration of the transaction.
- explanation-02: Locking both account rows prevents any other transaction from withdrawing from either account until the transfer finishes.
- explanation-02: Locking both accounts prevents a double-spend, where two transfers read the same starting balance and overdraw the account.
- explanation-02: The risks of pessimistic locking are slower throughput and possible deadlocks.
- explanation-03: Congestion is expensive to recover from.
- explanation-03: On packet loss, TCP cuts its rate back and adjusts ssthresh to remember the point where trouble started.
- explanation-05: A leaking program uses more and more memory over time.
- explanation-05: Growing memory use can slow a program down or crash it.
- explanation-05: Code can retain references to unneeded memory either on purpose or by accident.
- summarization-01: Each button's tooltip displays that button's keyboard shortcut.
- summarization-02: The deploy copied a database connection pool size from the staging template into production.
- summarization-02: The incorrect pool size caused the connection pool to run out.
- summarization-02: The pool exhaustion led to errors for 12% of checkout requests.
- summarization-02: The team was paged about the issue at 09:21.
- summarization-02: The team rolled back the deploy by 09:48.
- summarization-04: Nothing happens immediately after choosing PDF.
- summarization-04: After repeated clicks, four identical "export failed" error banners appear.
- summarization-04: The expected behavior matches how CSV export works for the same report.
- summarization-05: A sprint planning meeting took place on Monday.
- summarization-05: The listed action items come from Monday's sprint planning.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 26 | 21 | 0.808 | 29 | 5 |
| code-review-02 | 13 | 12 | 0.923 | 20 | 0 |
| code-review-03 | 20 | 10 | 0.5 | 16 | 2 |
| code-review-04 | 16 | 10 | 0.625 | 18 | 1 |
| code-review-05 | 31 | 17 | 0.548 | 27 | 3 |
| debugging-01 | 7 | 7 | 1.0 | 9 | 0 |
| debugging-02 | 18 | 12 | 0.667 | 14 | 2 |
| debugging-03 | 11 | 10 | 0.909 | 9 | 0 |
| debugging-04 | 13 | 6 | 0.462 | 11 | 2 |
| debugging-05 | 19 | 16 | 0.842 | 14 | 0 |
| explanation-01 | 31 | 16 | 0.516 | 22 | 0 |
| explanation-02 | 22 | 19 | 0.864 | 22 | 3 |
| explanation-04 | 38 | 20 | 0.526 | 27 | 3 |
| explanation-05 | 21 | 14 | 0.667 | 11 | 0 |
| summarization-01 | 6 | 6 | 1.0 | 5 | 0 |
| summarization-02 | 15 | 8 | 0.533 | 14 | 2 |
| summarization-03 | 13 | 12 | 0.923 | 13 | 0 |
| summarization-04 | 13 | 12 | 0.923 | 11 | 1 |
| summarization-05 | 10 | 8 | 0.8 | 8 | 0 |

Median fraction: 0.8 over 19 scored pairs.

Median additions: 1 over 19 scored pairs.

Lost facts:

- code-review-01: Mutating the caller's list is a side effect the caller did not request, and is surprising and hard to trace.
- code-review-01: Returning only `True`/`False` discards error context such as a stack trace, a validation message, or an inserted ID.
- code-review-01: The proposed fix appends "member" only if it is not already in `roles`.
- code-review-01: The proposed fix lets exceptions from `db.insert` propagate instead of hiding them.
- code-review-01: Letting real exceptions propagate allows callers to catch the errors they actually need to handle.
- code-review-02: The minimal fix is to `await fetch(`/api/users/${userId}`)`, throw an Error including the user ID and `res.status` when `res.ok` is false, `await res.json()`, and return `profile.name.toUpperCase()`.
- code-review-03: If the database permits multi-statement execution, an attacker could drop tables via this injection.
- code-review-03: SQL injection is the OWASP #1 vulnerability class.
- code-review-03: `cursor.execute` accepts a params tuple or dict in essentially every Python DB driver.
- code-review-03: sqlite3, psycopg2, and pymysql all support parameterized queries.
- code-review-03: The code performs no input validation on `customer_name` or `status`.
- code-review-03: The code does not check that `customer_name` and `status` are non-empty strings, of correct type, or within expected length or enum.
- code-review-03: `status` presumably should be one of a fixed set of values.
- code-review-03: The query has no `LIMIT` or pagination.
- code-review-03: Without a limit, the query could return massive result sets for common names or statuses.
- code-review-03: The remaining issues (`SELECT *`, validation, error handling, pagination) are judgment calls depending on how the function is used.
- code-review-04: The lost-increment race can occur even without the GIL releasing mid-expression.
- code-review-04: Splitting the read-modify-write into two separate statements makes the race window larger.
- code-review-04: Writing `self.value += 1` has the same race condition as the two-statement version.
- code-review-04: `+=` on an integer attribute is a non-atomic load-modify-store in Python bytecode.
- code-review-04: Collapsing the increment to a single line does not fix the race condition.
- code-review-04: Exposing the count through a `@property` that acquires the lock makes reads synchronized.
- code-review-05: An unquoted empty variable expands to nothing.
- code-review-05: A bare `cd` with no argument changes the current directory to $HOME.
- code-review-05: If BACKUP_DIR is empty, the script runs `rm -rf *.tmp` and gzips `*.log` in the user's home directory instead of the intended backup directory.
- code-review-05: In POSIX sh, if no files match a glob, the glob does not expand and is left as the literal string.
- code-review-05: If no `*.tmp` files exist, `rm -rf *.tmp` errors harmlessly on a nonexistent file.
- code-review-05: If no `*.log` files exist, the `ls *.log` version prints an `ls` error to stderr.
- code-review-05: The `ls *.log` version can behave unpredictably depending on the shell and the `ls` implementation.
- code-review-05: The empty-glob case can be guarded with `[ -e "$f" ] || continue` inside the loop.
- code-review-05: The empty-glob case can alternatively be handled with `compgen` or `nullglob` equivalents.
- code-review-05: The `gzip` call in the script has no `-f` flag.
- code-review-05: Without `-f`, rerunning gzip on a directory with existing `.gz` files will hang waiting for confirmation or fail, depending on the gzip version and tty.
- code-review-05: The script's shebang is `#!/bin/sh`.
- code-review-05: Using `#!/bin/sh` means relying only on POSIX sh features.
- code-review-05: The `for f in $(ls *.log)` construct is more of a bash idiom, creating a mismatch between intent and interpreter.
- debugging-02: setInterval invokes its callback as a plain function call.
- debugging-02: Inside the callback, `this` is `undefined`.
- debugging-02: Class bodies are in strict mode by default in JavaScript.
- debugging-02: Because `this` is undefined, `this.seconds` evaluates to `undefined`.
- debugging-02: Calling `.bind(this)` on a regular function callback is an alternative fix.
- debugging-02: Capturing `this` in a variable such as `const self = this;` before the callback is an alternative fix.
- debugging-03: The buggy code skips the last window, `[3, 4]`.
- debugging-04: Any byte greater than or equal to 0x80 breaks decoding under the ascii encoding.
- debugging-04: Python source files are UTF-8 today.
- debugging-04: Most text files today are UTF-8.
- debugging-04: A file that is not valid UTF-8 could be Latin-1 or mixed encodings.
- debugging-04: errors="ignore" is an alternative to errors="replace".
- debugging-04: Using errors="replace" still counts lines correctly.
- debugging-04: Decoding errors do not affect newline detection.
- debugging-05: The test can also fail if the test module is imported or collected multiple times.
- debugging-05: The fixed code is: def make_post(title, tags=None): if tags is None: tags = list(DEFAULT_TAGS); tags.append("post"); return {"title": title, "tags": tags}.
- debugging-05: The fix copies DEFAULT_TAGS on each call instead of mutating the shared module-level list.
- explanation-01: Because the underlying array has a finite number of slots, collisions are eventually inevitable by the pigeonhole principle.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Double hashing uses a second hash function to compute the probe step size.
- explanation-01: Open addressing is more cache-friendly and requires no extra pointers.
- explanation-01: Open addressing can suffer from clustering, where probes pile up near occupied slots.
- explanation-01: Clustering degrades open addressing performance badly when the load factor is high.
- explanation-01: Deletion in separate chaining is simple, requiring only removal from the list.
- explanation-01: Deletion in open addressing is trickier because naive removal breaks probe chains.
- explanation-01: Open addressing deletion usually requires tombstone markers.
- explanation-01: Open addressing needs the load factor kept lower for good performance, often resizing around 0.7.
- explanation-01: Chaining is simpler and more forgiving as the map fills up but pays a memory and cache cost per entry.
- explanation-01: Open addressing is faster in practice due to better cache locality and no pointer chasing.
- explanation-01: Open addressing is more sensitive to load factor and deletion complexity.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Python's dict uses open addressing.
- explanation-02: Pessimistic locking fits short transactions, because blocking is brief.
- explanation-02: Editing a document is an example use case for optimistic locking.
- explanation-02: Optimistic locking fits long-running transactions or user-facing edits, where holding a database lock for the whole duration would be wasteful or impossible.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, and message queues.
- explanation-04: The operating system mediates inter-process communication.
- explanation-04: Each thread has its own stack and instruction pointer.
- explanation-04: A crashing thread can take down the entire process and all other threads in it.
- explanation-04: A crashing process can be restarted independently.
- explanation-04: Chrome isolates risky or untrusted work into separate processes.
- explanation-04: Nginx uses separate worker processes.
- explanation-04: systemd is a supervisor that isolates work into separate processes.
- explanation-04: Erlang/OTP-style architectures isolate risky or untrusted work into separate processes.
- explanation-04: Older versions of Ruby have a global interpreter lock.
- explanation-04: Multiple processes each get their own interpreter and GIL.
- explanation-04: Threads offer no security protection because shared memory means a shared vulnerability surface.
- explanation-04: A component that needs to be killed, restarted, or resource-capped independently must be its own process.
- explanation-04: Resource limits include memory limits and CPU quotas via cgroups or ulimits.
- explanation-04: OS resource limits cannot be applied to a single thread.
- explanation-04: Architecting with processes and message-passing/IPC from the start makes later scaling out a smaller leap than scaling out a shared-memory multithreaded design.
- explanation-04: Processes cost more than threads in memory overhead per process.
- explanation-04: IPC is slower and more complex than shared-memory access.
- explanation-05: Memory is unreachable when no live reference chain from GC roots reaches it.
- explanation-05: Caches without a TTL, size limit, or removal on invalidation cause entries to leak.
- explanation-05: The reference in a listener leak can go in either direction between the listener and the object.
- explanation-05: Listener leaks are classic in UI code.
- explanation-05: A UI component that adds itself as a listener to a long-lived global emitter and is never removed stays reachable longer than it should.
- explanation-05: Closures capturing large scopes unintentionally are a frequent cause of memory leaks.
- explanation-05: Static or global variables accumulating references over time are a frequent cause of memory leaks.
- summarization-02: The config review checklist does not check other environment-sensitive values.
- summarization-02: The incident was paged out 7 minutes after detection.
- summarization-02: The incident was resolved in 34 minutes.
- summarization-02: Detection-to-recovery for the incident was fast.
- summarization-02: The incident response worked as intended.
- summarization-02: The fix should focus on prevention rather than on the incident process.
- summarization-02: Recommended preventive measures are separating or clearly differentiating the config templates and adding pool size to the review checklist.
- summarization-03: Under the proposal, uploads would return a placeholder thumbnail URL immediately.
- summarization-04: The bug is reproduced by clicking the "Export" button and choosing PDF.
- summarization-05: Ada is assigned to run the payments database migration dry run.
- summarization-05: Ada is assigned to check with the mobile team's lead about whether they were informed of the API deprecation.

Added facts (styled only):

- code-review-01: The recommended fix for the bare `except` is to use `except Exception as e` and log the error.
- code-review-01: The function does not check whether the user already exists before inserting.
- code-review-01: In the corrected version, `name` defaults are validated and a `ValueError` is raised if `name` is empty or not a string.
- code-review-01: In the corrected version, `db.insert({"name": name, "roles": roles})` is called inside a `try` block.
- code-review-01: In the corrected version, `except Exception as e` prints a failure message including the name and error, then returns `False`.
- code-review-03: The needed columns should be listed explicitly instead of using `SELECT *`.
- code-review-03: A customer name such as `O'Brien` breaks the query even without a deliberate attack.
- code-review-04: In the fixed code, `increment`, `reset`, and `get` each acquire the lock via a `with` statement.
- code-review-05: The unchecked `cd` exit status is the biggest risk in the script.
- code-review-05: Without `set -u`, undefined variables do not cause an error.
- code-review-05: The unquoted variable in the final `echo` is a minor issue.
- debugging-02: Inside the normal-function callback, `this` points to the global object.
- debugging-02: The global object has no `seconds` property.
- debugging-04: errors="replace" substitutes a placeholder character for each bad byte.
- debugging-04: With errors="replace", the caller must verify the resulting count is still correct for their case.
- explanation-02: A user reads a row with `version = 3`.
- explanation-02: The update statement is `UPDATE products SET price = 20, version = 4 WHERE id = 1 AND version = 3;`.
- explanation-02: If another process already changed the row, `version` is no longer 3.
- explanation-04: Threads are cheaper to switch between than processes.
- explanation-04: Processes cost more to create and switch between than threads.
- explanation-04: Threads should be used when tasks must share data quickly and safely.
- summarization-02: The wrong pool size exhausted the database pool.
- summarization-02: The exhausted pool caused errors for 12% of checkout requests.
- summarization-04: Clicking the PDF export button multiple times produces one "export failed" banner per click.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 4 | 1 | 2 | 1 | 0.333 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 0 | 0 | 2 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 0 | 2 | 1 | 0.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 2 | 1 | 1 | 0 | 0.5 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.333 over 5 scored pairs.

Claims that became certain:

- code-review-01: The `name` argument could be `None`, empty, or the wrong type, since nothing validates it before it reaches the DB.
- code-review-03: If the DB permits multi-statement execution, a caller passing an injected `customer_name` may be able to drop tables.
- code-review-03: `SELECT *` pulls every column, including ones the caller may not need.
- explanation-01: Open addressing can suffer from clustering (probes piling up near occupied slots), degrading badly if the load factor is high
- explanation-01: Deletion under open addressing usually needs "tombstone" markers, since naive removal breaks probe chains
- summarization-03: Effort is estimated at two weeks for one engineer.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 4 | 0 | 1 | 3 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 0 | 0 | 2 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 1 | 1 | 0 | 0.5 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 3 | 0 | 2 | 1 | 0.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 2 | 1 | 1 | 0 | 0.5 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 5 scored pairs.

Claims that became certain:

- code-review-01: The `name` argument could be `None`, empty, or the wrong type, since nothing validates it before it reaches the DB.
- code-review-03: `SELECT *` pulls every column, including ones the caller may not need.
- debugging-04: The non-ASCII byte 0xc3 in the file is likely part of a UTF-8 encoded character such as é or ü.
- explanation-01: Open addressing can suffer from clustering (probes piling up near occupied slots), degrading badly if the load factor is high
- explanation-01: Open addressing needs the load factor kept lower — often resized around 0.7 — for good performance
- summarization-03: There is a risk of a visible delay before real thumbnails appear during high load.

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
