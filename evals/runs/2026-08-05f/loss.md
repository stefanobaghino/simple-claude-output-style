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

Judge: opus. Judged on 2026-08-05T21:12:18+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 33 | 27 | 0.818 | 27 | 1 |
| code-review-02 | 23 | 16 | 0.696 | 19 | 2 |
| code-review-03 | 20 | 14 | 0.7 | 15 | 3 |
| code-review-04 | 19 | 12 | 0.632 | 24 | 2 |
| code-review-05 | 28 | 24 | 0.857 | 28 | 5 |
| debugging-01 | 8 | 8 | 1.0 | 10 | 4 |
| debugging-02 | 12 | 8 | 0.667 | 11 | 0 |
| debugging-03 | 8 | 7 | 0.875 | 14 | 3 |
| debugging-04 | 11 | 8 | 0.727 | 12 | 4 |
| debugging-05 | 18 | 17 | 0.944 | 14 | 0 |
| explanation-01 | 34 | 24 | 0.706 | 27 | 0 |
| explanation-02 | 32 | 31 | 0.969 | 25 | 2 |
| explanation-03 | 28 | 14 | 0.5 | 19 | 1 |
| explanation-04 | 31 | 21 | 0.677 | 28 | 3 |
| explanation-05 | 17 | 15 | 0.882 | 16 | 2 |
| summarization-01 | 6 | 5 | 0.833 | 5 | 1 |
| summarization-02 | 13 | 8 | 0.615 | 12 | 4 |
| summarization-03 | 12 | 12 | 1.0 | 15 | 0 |
| summarization-04 | 12 | 11 | 0.917 | 12 | 1 |
| summarization-05 | 10 | 9 | 0.9 | 7 | 3 |

Median fraction: 0.825 over 20 scored pairs.

Median additions: 2.0 over 20 scored pairs.

Lost facts:

- code-review-01: The code should catch a specific exception, or at least `Exception`.
- code-review-01: The caught exception should ideally be logged.
- code-review-01: `db` should probably be a required parameter rather than defaulted to `None`.
- code-review-01: `roles` is not checked to be a list, so it could be any iterable or an entirely wrong type.
- code-review-01: Returning success/failure as `True`/`False` discards the actual error and useful information such as the inserted record's ID.
- code-review-01: In the corrected version, the insert is wrapped in a try block that catches `Exception` and logs an error before returning `False`.
- code-review-02: The `async` keyword makes a function return a Promise.
- code-review-02: Callers that await the function get the wrong result and wrong timing.
- code-review-02: A network failure, non-OK HTTP status, or JSON parse error will produce an unhandled rejection in the `.then` chain because nothing observes it.
- code-review-02: `fetch` rejects only on network failure.
- code-review-02: Calling `res.json()` on an error response, such as a 404 returning an HTML error page, will likely throw a JSON parse error.
- code-review-02: Calling `res.json()` on an error response may silently succeed with unexpected data such as `{error: "not found"}`.
- code-review-02: The corrected version checks `res.ok` and throws an Error containing the user ID and status when the response is not OK.
- code-review-03: Stacked queries could allow worse attacks, depending on the database driver.
- code-review-03: The same string concatenation causes a correctness bug in addition to the security issue.
- code-review-03: Any legitimate input value containing a single quote breaks the query with a syntax error.
- code-review-03: A customer name such as `O'Brien` would break the query.
- code-review-03: Parameterized queries also eliminate the single-quote quoting bug.
- code-review-03: The database driver handles escaping and type binding correctly.
- code-review-04: CPython has a GIL.
- code-review-04: The GIL only protects individual bytecode instructions, not multi-step sequences.
- code-review-04: The increment race is real in CPython despite the GIL.
- code-review-04: The class documents no memory barrier or visibility guarantee.
- code-review-04: A minimal fix is to guard `increment`, `reset`, and reading `value` with a `threading.Lock`.
- code-review-04: A bare attribute read is safe in CPython.
- code-review-04: Locking the read of `value` keeps the thread-safety contract explicit and portable.
- code-review-05: The `rm -rf *.tmp` command has no `-i` or confirmation flag and no scoping safeguard.
- code-review-05: If no `.log` files exist, `ls *.log` prints an error to stderr.
- code-review-05: If no `.log` files exist, `$(ls *.log)` expands to nothing and the loop body never runs.
- code-review-05: `nullglob` is not part of POSIX sh.
- debugging-02: When a function is called as a plain function in strict mode or inside a class, `this` is `undefined`.
- debugging-02: Class bodies execute in strict mode.
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` is an alternative fix.
- debugging-02: Calling `.bind(this)` on the function passed to `setInterval` is an alternative fix.
- debugging-03: The fixed `moving_sum(values, window)` initializes an empty list `sums`, loops `for i in range(len(values) - window + 1)`, appends `sum(values[i : i + window])` to `sums`, and returns `sums`.
- debugging-04: errors="replace" substitutes the replacement character '�' for malformed bytes.
- debugging-04: errors="replace" can produce an inaccurate line count if bad bytes corrupt line boundaries.
- debugging-04: Opening the file in binary mode ("rb") and counting line separators gives an exact count regardless of the file's encoding.
- debugging-05: Running the same test twice can mutate `DEFAULT_TAGS`.
- explanation-01: The collection in a separate chaining slot is usually a linked list and sometimes a tree.
- explanation-01: Linear probing tries index+1, index+2, index+3, and so on.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Double hashing uses a second hash function to compute the step size.
- explanation-01: Open addressing lookups follow the same probe sequence until they find the key or an empty slot.
- explanation-01: An empty slot encountered during an open addressing lookup signals that the key is not present.
- explanation-01: Open addressing's worst case can degrade to scanning large clusters of the array.
- explanation-01: Open addressing is popular in performance-critical systems.
- explanation-01: Many general-purpose language implementations default to chaining.
- explanation-01: Java's HashMap defaults to chaining.
- explanation-02: Typical pessimistic locking use cases are short transactions on hot rows and banking transfers.
- explanation-03: Slow start is also used after some loss events.
- explanation-03: TCP tracks a congestion window, abbreviated cwnd.
- explanation-03: The congestion window is the amount of unacknowledged data a sender is allowed to have in flight at once.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The congestion window reflects the sender's estimate of what the network can handle.
- explanation-03: Historically the initial congestion window was 1 segment.
- explanation-03: Under current RFCs the initial congestion window is typically 2 to 10 segments.
- explanation-03: Each time the sender receives an ACK confirming successful delivery, it increases cwnd by roughly one segment.
- explanation-03: A larger congestion window means more segments in flight and thus more ACKs coming back.
- explanation-03: Congestion avoidance grows the congestion window more conservatively than slow start, typically linearly instead of exponentially.
- explanation-03: The slow start threshold is called ssthresh.
- explanation-03: ssthresh is a remembered estimate from a previous congestion event.
- explanation-03: When ssthresh is reached, TCP switches to the slower, linear growth phase to avoid repeating the same overshoot.
- explanation-04: A process has its own memory address space, file descriptors, and OS-level resources.
- explanation-04: Communication between processes requires explicit IPC such as pipes, sockets, or shared memory.
- explanation-04: Threads in the same process share the same memory address space, heap, and file descriptors.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Chrome runs each tab as a separate process so that one crashing tab does not crash the whole browser.
- explanation-04: Processes can be started, stopped, restarted, or scaled independently, including across machines via a process manager or orchestrator.
- explanation-04: Independent process lifecycles fit worker pools, microservices, and supervisor patterns such as restarting a crashed worker.
- explanation-04: Restarting an individual unit of work is much harder with threads without restarting the whole program.
- explanation-04: Inter-process communication is explicit via message-passing.
- explanation-04: Processes have higher memory overhead than threads because of their separate address spaces.
- explanation-05: Examples of such callbacks include UI event handlers, observers, and pub/sub subscribers.
- explanation-05: An unremoved listener often keeps a whole closure's captured scope alive.
- summarization-01: Cold start time was reduced by roughly 40%.
- summarization-02: The staging and production config templates live in the same directory.
- summarization-02: The staging and production config templates have similar names.
- summarization-02: The time from page to rollback was 34 minutes.
- summarization-02: The gap between deploy and detection was approximately 9 or more hours.
- summarization-02: The deploy-to-detection gap spanned overnight.
- summarization-04: Clicking the PDF export option produces no visible result; the export fails silently.
- summarization-05: Ada is to confirm that the mobile team was informed about the API deprecation.

Added facts (styled only):

- code-review-01: The fixed version raises `ValueError("name is required")` when `name` is falsy.
- code-review-02: `fetch` does not throw on its own when the network request fails or the server returns an error status such as 404 or 500.
- code-review-02: The original code silently swallows fetch errors.
- code-review-03: Returning all matching rows at once can use a lot of memory and slow down the database.
- code-review-03: The function does not validate that `status` is one of the expected values, such as "pending", "shipped", or "canceled".
- code-review-03: An unexpected `status` value should raise an error early rather than fail silently or return no rows.
- code-review-04: The `increment` method performs three separate steps.
- code-review-04: In that reset race, `value` ends at 1 instead of 0.
- code-review-05: The script leaves `$1`, `$BACKUP_DIR`, and `$f` unquoted.
- code-review-05: In that case `rm -rf *.tmp` attempts to remove a file named `*.tmp` and prints an error.
- code-review-05: The unmatched-glob case is not itself destructive.
- code-review-05: `*.tmp` matches only files, not directories, so the `-r` flag on `rm` is not needed.
- code-review-05: Using `rm -f` instead of `rm -rf` removes the risk of recursively deleting a directory whose name ends in `.tmp`.
- debugging-01: The dictionary `config` has a lowercase key `"port"`.
- debugging-01: Line 4 looks up `cfg['Port']` with a capital P.
- debugging-01: In the corrected code, `config` is `{"host": "localhost", "port": 8080}`.
- debugging-01: The corrected code calls `print(get_url(config))`.
- debugging-03: The last window has a sum of 7.
- debugging-03: With the fix, the function returns `[3, 5, 7]`.
- debugging-03: `[3, 5, 7]` is the expected output.
- debugging-04: Curly quotes are an example of characters that cause this error.
- debugging-04: The byte 0xc3 is often the first byte of a two-byte UTF-8 character.
- debugging-04: UTF-8 supports ASCII characters.
- debugging-04: UTF-8 supports a much wider set of characters than ASCII.
- explanation-02: In the wiki page example, a page at version 5 is saved with a check that the version is still 5, and on success the new version becomes 6.
- explanation-02: In the wiki example, if someone else saved in between, the version is already 6 and the update fails, showing a message such as 'this page changed, please reload.'
- explanation-03: Dropped packets lead to delays and wasted bandwidth.
- explanation-04: Whether a thread crash brings down the whole program depends on the language and the type of crash.
- explanation-04: Web servers often run each request handler as its own process.
- explanation-04: Updating a shared cache is an example of a task suited to threads.
- explanation-05: Increasing memory use from a leak can slow a program down.
- explanation-05: Increasing memory use from a leak can crash a program.
- summarization-01: Each button's tooltip shows its keyboard shortcut.
- summarization-02: Detection and recovery of the incident were fast.
- summarization-02: The team paged on-call within 7 minutes of the first errors.
- summarization-02: The team rolled back within 34 minutes of the first errors.
- summarization-02: The incident response time worked well and is worth keeping as the standard.
- summarization-04: The failure was confirmed on two different machines.
- summarization-05: The text lists action items from a meeting.
- summarization-05: Ben is to prepare the runbook for migration night.
- summarization-05: Ada and the team are to run the payments database migration dry run before Thursday.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 33 | 25 | 0.758 | 16 | 2 |
| code-review-02 | 23 | 13 | 0.565 | 19 | 2 |
| code-review-03 | 20 | 14 | 0.7 | 19 | 2 |
| code-review-04 | 19 | 16 | 0.842 | 19 | 1 |
| code-review-05 | 28 | 20 | 0.714 | 23 | 1 |
| debugging-01 | 8 | 8 | 1.0 | 8 | 0 |
| debugging-02 | 12 | 6 | 0.5 | 13 | 2 |
| debugging-03 | 8 | 8 | 1.0 | 11 | 2 |
| debugging-04 | 11 | 7 | 0.636 | 12 | 6 |
| debugging-05 | 18 | 18 | 1.0 | 15 | 1 |
| explanation-01 | 34 | 23 | 0.676 | 23 | 1 |
| explanation-02 | 32 | 26 | 0.812 | 22 | 7 |
| explanation-03 | 28 | 14 | 0.5 | 15 | 0 |
| explanation-04 | 31 | 19 | 0.613 | 30 | 3 |
| explanation-05 | 17 | 15 | 0.882 | 12 | 0 |
| summarization-01 | 6 | 5 | 0.833 | 5 | 0 |
| summarization-02 | 13 | 9 | 0.692 | 12 | 4 |
| summarization-03 | 12 | 11 | 0.917 | 12 | 0 |
| summarization-04 | 12 | 9 | 0.75 | 11 | 0 |
| summarization-05 | 10 | 9 | 0.9 | 6 | 0 |

Median fraction: 0.754 over 20 scored pairs.

Median additions: 1.0 over 20 scored pairs.

Lost facts:

- code-review-01: `db` should probably be a required parameter rather than defaulted to `None`.
- code-review-01: There is no duplicate check on `"member"`.
- code-review-01: If `roles` already contains `"member"`, it gets duplicated.
- code-review-01: `roles` is not checked to be a list, so it could be any iterable or an entirely wrong type.
- code-review-01: Returning success/failure as `True`/`False` discards the actual error and useful information such as the inserted record's ID.
- code-review-01: The listed problems are presented roughly in order of severity.
- code-review-01: In the corrected version, a `ValueError` is raised with the message "db is required" when `db` is `None`.
- code-review-01: In the corrected version, `"member"` is appended only if it is not already in `roles`.
- code-review-02: The `async` keyword makes a function return a Promise.
- code-review-02: Callers that await the function get the wrong result and wrong timing.
- code-review-02: A network failure, non-OK HTTP status, or JSON parse error will produce an unhandled rejection in the `.then` chain because nothing observes it.
- code-review-02: `fetch` rejects only on network failure.
- code-review-02: Calling `res.json()` on an error response, such as a 404 returning an HTML error page, will likely throw a JSON parse error.
- code-review-02: Calling `res.json()` on an error response may silently succeed with unexpected data such as `{error: "not found"}`.
- code-review-02: Unexpected response data leads to `profile.name` being `undefined`.
- code-review-02: The function does not validate that `data` has a `name` field.
- code-review-02: If the API response shape differs, for example `{user: {...}}` instead of the user object directly, `profile.name` is `undefined` and `.toUpperCase()` throws.
- code-review-02: The corrected version checks `res.ok` and throws an Error containing the user ID and status when the response is not OK.
- code-review-03: Stacked queries could allow worse attacks, depending on the database driver.
- code-review-03: The query has no `LIMIT` clause.
- code-review-03: Without a `LIMIT`, a broad match could return an unexpectedly large row set.
- code-review-03: `%s` is the placeholder syntax used by psycopg2 and MySQLdb.
- code-review-03: `?` is the placeholder syntax used by sqlite3.
- code-review-03: The database driver handles escaping and type binding correctly.
- code-review-04: The class documents no memory barrier or visibility guarantee.
- code-review-04: A bare attribute read is safe in CPython.
- code-review-04: Locking the read of `value` keeps the thread-safety contract explicit and portable.
- code-review-05: If no `.tmp` files exist and globbing is unhandled, `*.tmp` is passed to `rm` literally.
- code-review-05: The `rm -rf *.tmp` command has no `-i` or confirmation flag and no scoping safeguard.
- code-review-05: Unquoted variable expansion breaks on paths containing spaces or glob characters.
- code-review-05: Parsing `ls` breaks on filenames containing spaces or newlines.
- code-review-05: If no `.log` files exist, `$(ls *.log)` expands to nothing and the loop body never runs.
- code-review-05: `nullglob` is not part of POSIX sh.
- code-review-05: The script does not validate that exactly one argument was passed.
- code-review-05: The script does not validate that the argument is an existing directory.
- debugging-02: A callback passed to `setInterval` is invoked as a plain function.
- debugging-02: When a function is called as a plain function in strict mode or inside a class, `this` is `undefined`.
- debugging-02: When a function is called as a plain function outside strict mode, `this` is the global object.
- debugging-02: If `this` is undefined or the global object, `this.seconds` evaluates to `undefined`.
- debugging-02: Class bodies execute in strict mode.
- debugging-02: Capturing `const self = this;` before the callback and using `self.seconds` is an alternative fix.
- debugging-04: errors="replace" substitutes the replacement character '�' for malformed bytes.
- debugging-04: errors="replace" can produce an inaccurate line count if bad bytes corrupt line boundaries.
- debugging-04: errors="replace" is usually acceptable for a line-counting use case.
- debugging-04: Opening the file in binary mode ("rb") and counting line separators gives an exact count regardless of the file's encoding.
- explanation-01: A hash map's array has a finite number of slots while the set of possible keys is effectively unlimited.
- explanation-01: Collisions are inevitable in a hash map.
- explanation-01: The collection in a separate chaining slot is usually a linked list and sometimes a tree.
- explanation-01: Quadratic probing tries index+1, index+4, index+9, and so on.
- explanation-01: Open addressing lookups follow the same probe sequence until they find the key or an empty slot.
- explanation-01: An empty slot encountered during an open addressing lookup signals that the key is not present.
- explanation-01: Chaining's worst case degrades to a linked list traversal in one bucket.
- explanation-01: Open addressing's worst case can degrade to scanning large clusters of the array.
- explanation-01: Open addressing is popular in performance-critical systems.
- explanation-01: Many general-purpose language implementations default to chaining.
- explanation-01: Java's HashMap defaults to chaining.
- explanation-02: Inventory decrement on a hot-selling item is an example of high contention suited to pessimistic locking.
- explanation-02: A user editing their own profile is an example of low contention suited to optimistic locking.
- explanation-02: Pessimistic locking carries a risk of deadlocks.
- explanation-02: Optimistic locking causes wasted work if conflicts are common.
- explanation-02: Typical pessimistic locking use cases are short transactions on hot rows and banking transfers.
- explanation-02: A typical optimistic locking use case is web apps with long think time between read and write, such as editing a form.
- explanation-03: Slow start is also used after some loss events.
- explanation-03: TCP tracks a congestion window, abbreviated cwnd.
- explanation-03: The congestion window is the amount of unacknowledged data a sender is allowed to have in flight at once.
- explanation-03: The congestion window is separate from the receiver's advertised window.
- explanation-03: The receiver's advertised window reflects the receiver's buffer space.
- explanation-03: The congestion window reflects the sender's estimate of what the network can handle.
- explanation-03: Historically the initial congestion window was 1 segment.
- explanation-03: Under current RFCs the initial congestion window is typically 2 to 10 segments.
- explanation-03: Each time the sender receives an ACK confirming successful delivery, it increases cwnd by roughly one segment.
- explanation-03: A larger congestion window means more segments in flight and thus more ACKs coming back.
- explanation-03: Congestion avoidance grows the congestion window more conservatively than slow start, typically linearly instead of exponentially.
- explanation-03: The slow start threshold is called ssthresh.
- explanation-03: ssthresh is a remembered estimate from a previous congestion event.
- explanation-03: When ssthresh is reached, TCP switches to the slower, linear growth phase to avoid repeating the same overshoot.
- explanation-04: Communication between processes requires explicit IPC such as pipes, sockets, or shared memory.
- explanation-04: Threads in the same process share the same memory address space, heap, and file descriptors.
- explanation-04: Each thread has its own stack and register state, including its own program counter.
- explanation-04: Chrome runs each tab as a separate process so that one crashing tab does not crash the whole browser.
- explanation-04: Processes get separate memory and can be sandboxed with different OS-level permissions.
- explanation-04: In CPython, threads only help with I/O-bound waiting rather than CPU-bound work.
- explanation-04: Processes can be started, stopped, restarted, or scaled independently, including across machines via a process manager or orchestrator.
- explanation-04: Independent process lifecycles fit worker pools, microservices, and supervisor patterns such as restarting a crashed worker.
- explanation-04: Restarting an individual unit of work is much harder with threads without restarting the whole program.
- explanation-04: Inter-process communication is explicit via message-passing.
- explanation-04: Using processes trades some IPC overhead for a simpler correctness model in highly concurrent or distributed workloads.
- explanation-04: Threads are appropriate when you need lightweight concurrency and can trust the code to share memory safely, such as I/O-bound work in a memory-safe language.
- explanation-05: Examples of such callbacks include UI event handlers, observers, and pub/sub subscribers.
- explanation-05: An unremoved listener often keeps a whole closure's captured scope alive.
- summarization-01: Cold start time was reduced by roughly 40%.
- summarization-02: The time from page to rollback was 34 minutes.
- summarization-02: The gap between deploy and detection was approximately 9 or more hours.
- summarization-02: The deploy-to-detection gap spanned overnight.
- summarization-02: The issue caused user impact.
- summarization-03: The proposal frees up web workers.
- summarization-04: The Reports page has an "Export" button that offers PDF and CSV options.
- summarization-04: Clicking the PDF export option produces no visible result; the export fails silently.
- summarization-04: The bug was reproduced on the latest version of Firefox.
- summarization-05: Ada is to confirm that the mobile team was informed about the API deprecation.

Added facts (styled only):

- code-review-01: Python creates a default argument value once, at function definition time.
- code-review-01: Explicit checks for `name` and `db` catch bad calls early.
- code-review-02: The async keyword has no effect on the function.
- code-review-02: The corrected version returns data.name.toUpperCase().
- code-review-03: Possible placeholder syntaxes include %s, ?, and :name.
- code-review-03: The driver's documentation should be checked for the correct placeholder syntax.
- code-review-04: The interleaving order of the two threads is not predictable.
- code-review-05: When no `.log` file exists, the loop body runs once with the literal text `*.log`.
- debugging-02: Each tick of the timer prints NaN.
- debugging-02: The arrow function is the simpler fix compared to using .bind(this).
- debugging-03: The fixed function produces the output `[3, 5, 7]`.
- debugging-03: `[3, 5, 7]` is the correct result for the example input.
- debugging-04: The byte 0xc3 occurs at position 512 in the file.
- debugging-04: The byte 0xc3 at position 512 is part of a UTF-8 character.
- debugging-04: The ASCII encoding only allows bytes from 0 to 127.
- debugging-04: The error can be fixed by using an encoding that supports the full byte range.
- debugging-04: If the file's encoding is unknown, there are two options: detect the encoding, or open with an error handler.
- debugging-04: `chardet` is a library that can detect a file's encoding before the file is opened.
- debugging-05: Results of earlier calls to make_post change as the list grows.
- explanation-01: Open addressing uses memory better than chaining.
- explanation-02: An example table `orders` has a column named `version`.
- explanation-02: In the example, a process reads a row with `version = 3`.
- explanation-02: In the example, the process writes the update with the SQL statement `UPDATE orders SET status = 'shipped', version = 4 WHERE id = 42 AND version = 3;`.
- explanation-02: Optimistic locking fits when conflicts are rare and reads are frequent.
- explanation-02: An example pessimistic locking query run inside a transaction is `SELECT * FROM accounts WHERE id = 42 FOR UPDATE;`.
- explanation-02: A bank transfer is an example of a case where the cost of a failed write is high.
- explanation-02: Batch jobs and financial systems often use pessimistic locking.
- explanation-04: Processes are preferable to threads when tasks do not need to share much data.
- explanation-04: Processes take more time to start than threads.
- explanation-04: Threads cost less to create than processes.
- summarization-02: The page went out at 09:21.
- summarization-02: The page went out seven minutes after the errors started.
- summarization-02: The rollback finished at 09:48.
- summarization-02: Error rates returned to normal after the rollback.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 0 | 2 | n/a |
| code-review-02 | 1 | 0 | 0 | 1 | n/a |
| code-review-03 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 1 | 0 | 2 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 4 | 0 | 3 | 1 | 0.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 6 | 3 | 2 | 1 | 0.6 |
| explanation-04 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-03 | 2 | 2 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.6 over 7 scored pairs.

Claims that became certain:

- code-review-03: With no LIMIT, a broad match could return an unexpectedly large row set.
- explanation-01: Each array slot holds a small collection — usually a linked list, sometimes a tree.
- explanation-01: Chaining's performance is predictable-ish even at a high load factor.
- explanation-01: Deletion under open addressing usually needs "tombstone" markers.
- explanation-03: Congestion avoidance grows the window much more conservatively — typically linearly instead of exponentially.
- explanation-03: Slow start lets a new connection find a good sending rate quickly without assuming — and potentially wrecking — the network's actual capacity.
- summarization-02: Settings other than connection pool size — likely other capacity-sensitive settings — should also be added to the config review checklist.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 2 | 0 | 0 | 2 | n/a |
| code-review-02 | 1 | 0 | 0 | 1 | n/a |
| code-review-03 | 2 | 0 | 0 | 2 | n/a |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 0 | 0 | 0 | 0 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 0 | 1 | 2 | 0.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 4 | 0 | 2 | 2 | 0.0 |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 6 | 2 | 3 | 1 | 0.4 |
| explanation-04 | 1 | 0 | 1 | 0 | 0.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 1 | 0 | 0 | 1 | n/a |
| summarization-03 | 2 | 2 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 5 scored pairs.

Claims that became certain:

- debugging-04: The non-ASCII byte `0xc3` in the file is likely part of a UTF-8 multi-byte sequence, such as `é` or `ñ`.
- explanation-01: Each array slot holds a small collection — usually a linked list, sometimes a tree.
- explanation-01: Deletion under open addressing usually needs "tombstone" markers.
- explanation-03: The window roughly doubles every round-trip time.
- explanation-03: Congestion avoidance grows the window much more conservatively — typically linearly instead of exponentially.
- explanation-03: Slow start lets a new connection find a good sending rate quickly without assuming — and potentially wrecking — the network's actual capacity.
- explanation-04: A memory-safety bug anywhere in a process can potentially read or write any other thread's data, since threads offer no isolation boundary.

## Warnings

- none
