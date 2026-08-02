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

Judge: opus. Judged on 2026-08-01T21:55:23+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The lost facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction |
|---|---|---|---|
| code-review-01 | 29 | 22 | 0.759 |
| code-review-02 | 20 | 14 | 0.7 |
| code-review-03 | 20 | 11 | 0.55 |
| code-review-04 | 22 | 17 | 0.773 |
| code-review-05 | 34 | 24 | 0.706 |
| debugging-01 | 8 | 8 | 1.0 |
| debugging-02 | 14 | 11 | 0.786 |
| debugging-03 | 7 | 6 | 0.857 |
| debugging-04 | 17 | 11 | 0.647 |
| debugging-05 | 10 | 9 | 0.9 |
| explanation-01 | 36 | 24 | 0.667 |
| explanation-02 | 24 | 19 | 0.792 |
| explanation-03 | 38 | 26 | 0.684 |
| explanation-04 | 46 | 31 | 0.674 |
| explanation-05 | 14 | 13 | 0.929 |
| summarization-01 | 8 | 8 | 1.0 |
| summarization-02 | 14 | 11 | 0.786 |
| summarization-03 | 13 | 13 | 1.0 |
| summarization-04 | 13 | 13 | 1.0 |
| summarization-05 | 9 | 9 | 1.0 |

Median fraction: 0.786 over 20 scored pairs.

Lost facts:

- code-review-01: `roles` is often the caller's own list object rather than a copy.
- code-review-01: `roles.append("member")` mutates the caller's list in place.
- code-review-01: The in-place mutation surprises the caller when their list changes after calling `add_user`.
- code-review-01: The function has no docstring and no type hints.
- code-review-01: The expected interface of `db` (that it must have `.insert`) is undocumented.
- code-review-01: The suggested fix copies `roles` with `list(roles)` and appends `"member"` only if not already present.
- code-review-01: The suggested fix drops the silent failure mode and lets real errors propagate to the caller.
- code-review-02: Without a `.catch()`, a failed network request or a throwing `res.json()` results in a silently unhandled promise rejection.
- code-review-02: An unhandled promise rejection crashes the process in strict environments.
- code-review-02: The `async` keyword is pointless as the function is written.
- code-review-02: The function always returns a resolved promise wrapping the error thrown by `undefined.name.toUpperCase()`.
- code-review-02: API error responses or an empty body are cases where `data` may lack a `name` property.
- code-review-02: The fixed version throws an `Error` with message `Failed to load profile: ${res.status}` when `res.ok` is false.
- code-review-03: The function has no error handling.
- code-review-03: `cursor.execute` can raise exceptions, for example on a bad connection or a malformed query.
- code-review-03: Exceptions from `cursor.execute` propagate raw to the call site with no handling.
- code-review-03: The lack of error handling is not necessarily wrong.
- code-review-03: `status` presumably comes from a small fixed set of values such as `"pending"` and `"shipped"`.
- code-review-03: Nothing in the function enforces that `status` belongs to the expected set of values.
- code-review-03: Typos or unexpected `status` values fail silently by returning zero rows rather than raising a clear error.
- code-review-03: `?` placeholders should be used instead of `%s` if the driver is sqlite3.
- code-review-03: `%s` placeholders are used by DB-API drivers such as psycopg2 and mysql-connector.
- code-review-04: CPython has a GIL.
- code-review-04: The GIL only guarantees that each individual bytecode operation is atomic.
- code-review-04: The GIL does not make the whole read-then-write sequence atomic.
- code-review-04: Writing the increment as `current + 1` is needlessly roundabout.
- code-review-04: The stylistic point about `current + 1` is cosmetic compared to the threading bug.
- code-review-05: `$1` and `$BACKUP_DIR` are unquoted in the script.
- code-review-05: On most shells, `cd ""` goes to `$HOME` or fails silently.
- code-review-05: Passing an unmatched glob literally to a command is a classic footgun pattern in general.
- code-review-05: Unmatched globs could match unintended files if `nullglob` or `nocaseglob` behavior differs.
- code-review-05: If no `.log` files exist, `ls *.log` prints an error to stderr.
- code-review-05: The script uses `sh` but relies on GNU-isms.
- code-review-05: Nothing stops the script from running under a shell where `$(ls ...)` behaves more surprisingly.
- code-review-05: The script performs destructive operations with no dry-run or confirmation.
- code-review-05: Compressing `.log` files with gzip overwrites the originals and is irreversible.
- code-review-05: The suggested fix prints a usage message to stderr and exits with status 1 when the argument is missing or not a directory.
- debugging-02: In a class, where `this` is `undefined`, the code would actually throw `TypeError: Cannot read properties of undefined`.
- debugging-02: Calling `.bind(this)` on the callback function is an alternative fix.
- debugging-02: Capturing `const self = this;` outside the callback and using `self.seconds` inside it is an alternative fix.
- debugging-03: With `len(values)=4` and `window=2`, the windows are `[1,2]`, `[2,3]`, and `[3,4]`.
- debugging-04: A file might be Latin-1 or use mixed encodings rather than UTF-8.
- debugging-04: When the encoding cannot be guaranteed, one option is to detect the encoding first.
- debugging-04: chardet and charset-normalizer are libraries that can detect a file's encoding.
- debugging-04: errors="replace" silently alters bad bytes.
- debugging-04: errors="replace" should only be used if exact byte fidelity does not matter.
- debugging-04: Exact byte fidelity does not matter for a line-count use case.
- debugging-05: The fixed make_post sets tags to a copy of DEFAULT_TAGS, via list(DEFAULT_TAGS), when tags is None.
- explanation-01: A hash map stores entries by computing hash(key) % capacity to pick a bucket index.
- explanation-01: The collection in a chaining bucket is usually a linked list, sometimes a tree.
- explanation-01: Chaining insert hashes the key, goes to the bucket, and appends the entry, or updates it if the key already exists.
- explanation-01: Chaining delete hashes the key, finds the entry in the list, and removes it.
- explanation-01: Quadratic hashing and double hashing are probing sequences that give better distribution than linear probing.
- explanation-01: Chaining has poor cache behavior because list nodes are scattered in memory.
- explanation-01: Open addressing has good cache behavior because data is contiguous in the array.
- explanation-01: Open addressing is more memory-efficient and cache-friendly than chaining.
- explanation-01: Open addressing is favored in performance-critical or memory-constrained contexts.
- explanation-01: Python's dict uses open addressing.
- explanation-01: Many C++ hash table implementations use open addressing.
- explanation-01: Open addressing implementations typically resize at around 70% full.
- explanation-02: An example optimistic locking schema is a `products` table with a `version` integer column.
- explanation-02: An example optimistic update is `UPDATE products SET stock = 5, version = version + 1 WHERE id = 42 AND version = 3;`.
- explanation-02: If another transaction already bumped `version` to 4, the example update affects 0 rows.
- explanation-02: An example pessimistic locking sequence is `BEGIN; SELECT balance FROM accounts WHERE id = 42 FOR UPDATE;` followed by `UPDATE accounts SET balance = balance - 100 WHERE id = 42; COMMIT;`.
- explanation-02: Pessimistic locking fits when transactions are short-lived.
- explanation-03: Congestion can cascade because dropped packets trigger retransmissions.
- explanation-03: Retransmissions add more traffic to an already-overloaded network, making congestion worse.
- explanation-03: During congestion collapse, throughput crashed because senders kept retransmitting into a saturated network.
- explanation-03: The initial cwnd was historically 1 segment.
- explanation-03: Current RFC guidance sets a typical initial cwnd of 4-10 segments.
- explanation-03: In slow start, cwnd is increased by one segment's worth for each ACK received.
- explanation-03: Because each ACK'd segment adds a full segment to the window, the congestion window roughly doubles every round-trip time.
- explanation-03: Slow start's initial window is small in contrast to sending as much as the receiver's advertised window would allow.
- explanation-03: In congestion avoidance, cwnd grows linearly rather than exponentially.
- explanation-03: Linear growth in congestion avoidance is more cautious than exponential growth.
- explanation-03: When loss is detected, cwnd is cut back.
- explanation-03: When loss is detected, ssthresh is set based on where the loss occurred, so subsequent slow start or recovery is less aggressive.
- explanation-04: A process has its own file descriptors.
- explanation-04: A process has its own OS resources.
- explanation-04: The shared address space of threads includes the heap, globals, and open file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state.
- explanation-04: Processing untrusted input is an example of work where a worker might crash or hang.
- explanation-04: Calling a flaky library is an example of work where a worker might crash or hang.
- explanation-04: Separate processes can run under different namespaces.
- explanation-04: Containers are an example of processes running under different namespaces.
- explanation-04: sudo subprocesses are an example of processes running under different users or permissions.
- explanation-04: Threads cannot run under different users, permissions, or namespaces because they share the parent's security context.
- explanation-04: No shared memory means no data races on that memory.
- explanation-04: IPC has its own complexity.
- explanation-04: Threads are preferable when memory footprint matters.
- explanation-04: N threads are far cheaper than N processes in memory footprint.
- explanation-05: A registry reference also keeps alive anything the registered object closes over.
- summarization-02: A copy-paste from staging silently dropped the production pool size from 50 to 5 connections.
- summarization-02: The reduction in production pool size was a 10x reduction.
- summarization-02: A recommended prevention is to add pool size and other critical infrastructure parameters to the review checklist.

### technical-simplified

| Pair | Facts | Survived | Fraction |
|---|---|---|---|
| code-review-01 | 29 | 24 | 0.828 |
| code-review-02 | 20 | 13 | 0.65 |
| code-review-03 | 20 | 9 | 0.45 |
| code-review-04 | 22 | 20 | 0.909 |
| code-review-05 | 34 | 25 | 0.735 |
| debugging-01 | 8 | 8 | 1.0 |
| debugging-02 | 14 | 9 | 0.643 |
| debugging-03 | 7 | 7 | 1.0 |
| debugging-04 | 17 | 12 | 0.706 |
| debugging-05 | 10 | 9 | 0.9 |
| explanation-01 | 36 | 24 | 0.667 |
| explanation-02 | 24 | 15 | 0.625 |
| explanation-04 | 46 | 27 | 0.587 |
| explanation-05 | 14 | 13 | 0.929 |
| summarization-01 | 8 | 8 | 1.0 |
| summarization-03 | 13 | 13 | 1.0 |
| summarization-04 | 13 | 12 | 0.923 |
| summarization-05 | 9 | 8 | 0.889 |

Median fraction: 0.859 over 18 scored pairs.

Lost facts:

- code-review-01: Duplicate roles aren't checked.
- code-review-01: The function has no docstring and no type hints.
- code-review-01: The expected interface of `db` (that it must have `.insert`) is undocumented.
- code-review-01: The suggested fix copies `roles` with `list(roles)` and appends `"member"` only if not already present.
- code-review-01: The suggested fix avoids duplicate roles.
- code-review-02: Without a `.catch()`, a failed network request or a throwing `res.json()` results in a silently unhandled promise rejection.
- code-review-02: An unhandled promise rejection crashes the process in strict environments.
- code-review-02: The `async` keyword is pointless as the function is written.
- code-review-02: The function always returns a resolved promise wrapping the error thrown by `undefined.name.toUpperCase()`.
- code-review-02: There is no null or shape check on `data`.
- code-review-02: Even once awaited, there is no guarantee that `data` has a `name` property.
- code-review-02: API error responses or an empty body are cases where `data` may lack a `name` property.
- code-review-03: SQL injection is the most critical issue in the function.
- code-review-03: The impact of the SQL injection can be worse than reading or manipulating rows, depending on the database permissions.
- code-review-03: The function has no error handling.
- code-review-03: `cursor.execute` can raise exceptions, for example on a bad connection or a malformed query.
- code-review-03: Exceptions from `cursor.execute` propagate raw to the call site with no handling.
- code-review-03: The lack of error handling is not necessarily wrong.
- code-review-03: `status` presumably comes from a small fixed set of values such as `"pending"` and `"shipped"`.
- code-review-03: Typos or unexpected `status` values fail silently by returning zero rows rather than raising a clear error.
- code-review-03: The fixed version uses the query `"SELECT * FROM orders WHERE customer = %s AND status = %s"` and passes `(customer_name, status)` as parameters to `cursor.execute`.
- code-review-03: `?` placeholders should be used instead of `%s` if the driver is sqlite3.
- code-review-03: `%s` placeholders are used by DB-API drivers such as psycopg2 and mysql-connector.
- code-review-04: Writing the increment as `current + 1` is needlessly roundabout.
- code-review-04: The stylistic point about `current + 1` is cosmetic compared to the threading bug.
- code-review-05: `rm -rf *.tmp` is dangerous and silent.
- code-review-05: If `cd` failed or `$BACKUP_DIR` was wrong, `rm -rf *.tmp` deletes `.tmp` files from an arbitrary directory with no confirmation or logging of what was removed.
- code-review-05: Passing an unmatched glob literally to a command is a classic footgun pattern in general.
- code-review-05: Unmatched globs could match unintended files if `nullglob` or `nocaseglob` behavior differs.
- code-review-05: The script uses `sh` but relies on GNU-isms.
- code-review-05: Nothing stops the script from running under a shell where `$(ls ...)` behaves more surprisingly.
- code-review-05: The script performs destructive operations with no dry-run or confirmation.
- code-review-05: Compressing `.log` files with gzip overwrites the originals and is irreversible.
- code-review-05: The suggested fix prints a usage message to stderr and exits with status 1 when the argument is missing or not a directory.
- debugging-02: In strict mode or class bodies, `this` inside such a plain-function callback is `undefined`.
- debugging-02: Neither `undefined` nor the global object has a `seconds` property.
- debugging-02: In a class, where `this` is `undefined`, the code would actually throw `TypeError: Cannot read properties of undefined`.
- debugging-02: Calling `.bind(this)` on the callback function is an alternative fix.
- debugging-02: Capturing `const self = this;` outside the callback and using `self.seconds` inside it is an alternative fix.
- debugging-04: A file might be Latin-1 or use mixed encodings rather than UTF-8.
- debugging-04: chardet and charset-normalizer are libraries that can detect a file's encoding.
- debugging-04: errors="replace" silently alters bad bytes.
- debugging-04: errors="replace" should only be used if exact byte fidelity does not matter.
- debugging-04: Exact byte fidelity does not matter for a line-count use case.
- debugging-05: The fixed make_post sets tags to a copy of DEFAULT_TAGS, via list(DEFAULT_TAGS), when tags is None.
- explanation-01: The collection in a chaining bucket is usually a linked list, sometimes a tree.
- explanation-01: Chaining insert hashes the key, goes to the bucket, and appends the entry, or updates it if the key already exists.
- explanation-01: Chaining delete hashes the key, finds the entry in the list, and removes it.
- explanation-01: Quadratic hashing and double hashing are probing sequences that give better distribution than linear probing.
- explanation-01: In open addressing, deletion cannot simply clear the slot because that would break probing for later entries.
- explanation-01: Open addressing deletion usually leaves a tombstone marker instead of clearing the slot.
- explanation-01: Deletion is simple in chaining.
- explanation-01: Deletion in open addressing needs tombstones or rehashing.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Python's dict uses open addressing.
- explanation-01: Many C++ hash table implementations use open addressing.
- explanation-01: Open addressing implementations typically resize at around 70% full.
- explanation-02: An example optimistic locking schema is a `products` table with a `version` integer column.
- explanation-02: An example optimistic update is `UPDATE products SET stock = 5, version = version + 1 WHERE id = 42 AND version = 3;`.
- explanation-02: If another transaction already bumped `version` to 4, the example update affects 0 rows.
- explanation-02: The application detects the 0-row update result and retries.
- explanation-02: Optimistic locking fits when throughput matters more than avoiding retries.
- explanation-02: Optimistic locking fits when the resource is held for a long time, such as a user editing a document over minutes.
- explanation-02: Holding a real database lock for the entire duration of a long-held resource would be wasteful.
- explanation-02: Pessimistic locking fits when retry logic would be expensive or unsafe to get right.
- explanation-02: Inventory decrements with hard limits are an example where retry logic would be expensive or unsafe to get right.
- explanation-04: A process has its own file descriptors.
- explanation-04: A process has its own OS resources.
- explanation-04: Pipes are a form of IPC.
- explanation-04: Sockets are a form of IPC.
- explanation-04: Shared memory segments are a form of IPC.
- explanation-04: The shared address space of threads includes the heap, globals, and open file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state.
- explanation-04: Processing untrusted input is an example of work where a worker might crash or hang.
- explanation-04: Calling a flaky library is an example of work where a worker might crash or hang.
- explanation-04: Separate processes can run under different namespaces.
- explanation-04: Containers are an example of processes running under different namespaces.
- explanation-04: Browser tabs are an example of processes running under different permissions or namespaces.
- explanation-04: sudo subprocesses are an example of processes running under different users or permissions.
- explanation-04: Separate processes map naturally onto components that need to be restarted, deployed, or scaled independently.
- explanation-04: A supervisor restarting a crashed worker is an example of independent lifecycle management.
- explanation-04: Killing or restarting a single thread cleanly is much harder than doing so for a process.
- explanation-04: IPC has its own complexity.
- explanation-04: Isolation includes crash containment, security, and independent scaling.
- explanation-05: A registry reference also keeps alive anything the registered object closes over.
- summarization-04: Clicking "Export as PDF" produces repeated "export failed" error banners.
- summarization-05: Ada is assigned to run the payments DB migration dry run.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 3 | 1 | 2 | 0 | 0.333 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.333 over 3 scored pairs.

Claims that became certain:

- code-review-03: `SELECT *` pulls columns the caller may not need.
- code-review-05: If `cd $BACKUP_DIR` fails, the script keeps going and runs `rm -rf *.tmp` in whatever directory it happens to be in — potentially the wrong place entirely.
- code-review-05: If run with no argument, `BACKUP_DIR` is empty and `cd ""` (on most shells) goes to `$HOME` or fails silently, then `rm -rf *.tmp` runs somewhere unintended.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 3 | 0 | 3 | 0 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 1 | 1 | 0 | 0.5 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 4 scored pairs.

Claims that became certain:

- code-review-01: Since `roles` is often the caller's own list object rather than a copy, `roles.append("member")` mutates it in place, surprising the caller when their list changes after calling `add_user`.
- code-review-03: `SELECT *` pulls columns the caller may not need.
- code-review-05: If `cd $BACKUP_DIR` fails, the script keeps going and runs `rm -rf *.tmp` in whatever directory it happens to be in — potentially the wrong place entirely.
- code-review-05: If run with no argument, `BACKUP_DIR` is empty and `cd ""` (on most shells) goes to `$HOME` or fails silently, then `rm -rf *.tmp` runs somewhere unintended.
- code-review-05: If no `*.tmp` files exist, most shells will pass the literal string `*.tmp` to `rm`, which fails harmlessly here but is a classic footgun pattern that could match unintended files if `nullglob`/`nocaseglob` behavior differs.
- debugging-04: The non-ASCII byte 0xc3 in the file is likely part of a UTF-8 encoded character, such as an accented letter.

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/summarization-02: the pair failed the gate, excluded
