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

Judge: opus. Judged on 2026-08-06T06:53:46+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 41 | 27 | 0.659 | 20 | 2 |
| code-review-02 | 20 | 18 | 0.9 | 16 | 0 |
| code-review-03 | 25 | 12 | 0.48 | 18 | 6 |
| code-review-04 | 28 | 16 | 0.571 | 17 | 3 |
| code-review-05 | 30 | 22 | 0.733 | 31 | 6 |
| debugging-01 | 5 | 3 | 0.6 | 10 | 2 |
| debugging-02 | 11 | 10 | 0.909 | 16 | 2 |
| debugging-03 | 10 | 10 | 1.0 | 12 | 0 |
| debugging-04 | 13 | 11 | 0.846 | 12 | 2 |
| debugging-05 | 14 | 14 | 1.0 | 18 | 0 |
| explanation-01 | 42 | 26 | 0.619 | 23 | 0 |
| explanation-02 | 29 | 27 | 0.931 | 24 | 2 |
| explanation-03 | 38 | 21 | 0.553 | 18 | 1 |
| explanation-04 | 30 | 19 | 0.633 | 34 | 0 |
| explanation-05 | 19 | 14 | 0.737 | 16 | 5 |
| summarization-01 | 5 | 4 | 0.8 | 6 | 1 |
| summarization-02 | 16 | 12 | 0.75 | 16 | 3 |
| summarization-03 | 14 | 14 | 1.0 | 15 | 0 |
| summarization-04 | 13 | 11 | 0.846 | 11 | 1 |
| summarization-05 | 10 | 9 | 0.9 | 8 | 1 |

Median fraction: 0.775 over 20 scored pairs.

Median additions: 1.5 over 20 scored pairs.

Lost facts:

- code-review-01: The mutable default argument is a classic Python footgun.
- code-review-01: The mutable default can be fixed by using `roles=None` and then `roles = roles or []` inside the function.
- code-review-01: Possible reasons for insertion failure include a bad connection, a duplicate name, a schema violation, and `db` being `None`.
- code-review-01: The except clause should at minimum catch `Exception`.
- code-review-01: The function has no duplicate-role protection.
- code-review-01: If the caller passes `roles=["member"]`, the result is `["member", "member"]`.
- code-review-01: Examples of specific failure modes are a duplicate user versus a connection error.
- code-review-01: `roles` is a list passed by reference.
- code-review-01: The `.append` call mutates the caller's original list in place as a side effect.
- code-review-01: Mutating the caller's list can surprise callers who didn't expect their list to change.
- code-review-01: The suggested rewrite raises `ValueError("name is required")` when `name` is falsy.
- code-review-01: The suggested rewrite copies roles with `roles = list(roles) if roles else []`.
- code-review-01: The suggested rewrite appends "member" only if "member" is not already in `roles`.
- code-review-01: The suggested rewrite calls `db.insert({"name": name, "roles": roles})` and returns `True`.
- code-review-02: The returned promise resolves or rejects based on the synchronous throw rather than on the fetch result.
- code-review-02: The corrected version throws an Error with the message `Failed to load profile: ${res.status}` when `res.ok` is false.
- code-review-03: A customer name containing an apostrophe, such as `"O'Brien"`, would produce malformed SQL and raise an error.
- code-review-03: The apostrophe failure occurs even with no malicious intent.
- code-review-03: The query has no `LIMIT` clause.
- code-review-03: Without a `LIMIT`, a broad match could return an unbounded number of rows.
- code-review-03: `status` presumably should be one of a fixed set of values such as 'pending', 'shipped', or 'cancelled'.
- code-review-03: Nothing in the code enforces that `status` is one of the allowed values.
- code-review-03: Without status validation, typos or garbage input silently produce empty results.
- code-review-03: The function has no type hints and no docstring.
- code-review-03: Type hints and a docstring would help callers know the expected types and return shape.
- code-review-03: The return shape is a list of tuples/rows, dependent on the cursor's row factory.
- code-review-03: The missing type hints and docstring are a minor issue.
- code-review-03: The issues other than the SQL injection are quality-of-life improvements.
- code-review-03: The other listed issues are independent of the security bug.
- code-review-04: Even with the GIL, the interpreter can switch threads between the read and the write.
- code-review-04: Under real concurrent load, the increment implementation reliably drops updates.
- code-review-04: `self.value = 0` is a single atomic bytecode operation.
- code-review-04: Without external locking, there is no way to reason about 'reset happens after all these increments'.
- code-review-04: In CPython, the plain attribute read itself is fine.
- code-review-04: The plain attribute read does not compose safely with check-then-act patterns such as reading and then deciding to reset.
- code-review-04: The code relies implicitly on CPython/GIL semantics.
- code-review-04: The code is not safe under free-threaded CPython (3.13+ no-GIL builds).
- code-review-04: The code is not safe under other Python implementations that lack a GIL.
- code-review-04: The code would be broken even more without the GIL's coarse-grained help masking some issues.
- code-review-04: The proposed fix imports `threading` and stores the count in `self._value` with a `threading.Lock` in `self._lock`.
- code-review-04: In the fix, `value` is a property that acquires the lock and returns `self._value`.
- code-review-05: `$1` and `$BACKUP_DIR` are unquoted in the script.
- code-review-05: `for f in $(ls *.log)` breaks on filenames containing spaces, newlines, or glob characters.
- code-review-05: If no `.log` files exist, `ls *.log` prints a "No such file or directory" error to stderr.
- code-review-05: The `ls *.log` error is cosmetic but noisy and misleading in a script meant to run unattended.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` is harmless only because `-f` suppresses the "no such file" error.
- code-review-05: Filenames beginning with `-` could be interpreted as options by `gzip` because there is no `--` separator.
- code-review-05: `gzip` will refuse or prompt, depending on version and TTY, if a `.gz` file already exists for a given file.
- code-review-05: `gzip -f` can be used to overwrite an existing `.gz` file.
- debugging-01: Line 4 is the line that needs to be fixed.
- debugging-01: The corrected line 4 is: return f"http://{cfg['host']}:{cfg['port']}/api".
- debugging-02: Calling `.bind(this)` on the callback function is an alternative fix.
- debugging-04: Accented names and currency symbols are examples of non-ASCII characters.
- debugging-04: utf-8 is almost always the appropriate Unicode-capable encoding to use.
- explanation-01: The internal array of a hash map is called the bucket array.
- explanation-01: Collisions are inevitable once there are enough keys, because the array has a limited number of slots.
- explanation-01: Collisions are expected behavior rather than a bug.
- explanation-01: The per-bucket collection in separate chaining is usually a linked list, and sometimes a tree or dynamic array.
- explanation-01: Quadratic probing is a probing sequence.
- explanation-01: Double hashing is a probing sequence.
- explanation-01: Open addressing can fail entirely if the array is full.
- explanation-01: Open addressing is more subtle to implement due to probe sequences, tombstones, and resizing.
- explanation-01: Open addressing's speed and memory advantages hold only if the load factor is kept low.
- explanation-01: The load factor is entries divided by array size.
- explanation-01: Most hash map implementations resize by rehashing into a bigger array once the load factor crosses a threshold such as 0.7.
- explanation-01: Resizing at a load factor threshold happens regardless of which collision strategy is used.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Java's HashMap switches to trees for long chains.
- explanation-01: Python's dict leans toward open addressing.
- explanation-01: Most C++ hash map implementations lean toward open addressing.
- explanation-02: Editing a user profile is an example use case for optimistic locking.
- explanation-02: Updating a document or CMS record is an example use case for optimistic locking.
- explanation-03: A network path may be a fast direct link or may cross several routers with limited buffer space and bandwidth.
- explanation-03: TCP tracks a value called the congestion window, abbreviated cwnd.
- explanation-03: The congestion window caps the send rate independently of the receiver's advertised window.
- explanation-03: Historically the initial cwnd was 1 segment.
- explanation-03: Modern defaults set the initial cwnd to approximately 10 segments.
- explanation-03: One round trip typically produces multiple ACKs, one per segment sent.
- explanation-03: In RTT 1, the sender sends 1 segment, receives 1 ACK, and cwnd becomes 2.
- explanation-03: In RTT 2, the sender sends 2 segments, receives 2 ACKs, and cwnd becomes 4.
- explanation-03: In RTT 3, the sender sends 4 segments and cwnd becomes 8.
- explanation-03: Doubling cwnd each RTT reaches useful throughput within a handful of round trips.
- explanation-03: On detecting loss, the sender backs off, typically cutting cwnd substantially.
- explanation-03: Congestion avoidance increases cwnd linearly rather than exponentially.
- explanation-03: ssthresh is a threshold value the connection remembers from a previous congestion event.
- explanation-03: ssthresh serves as an estimate of how much data was too much during the last congestion event.
- explanation-03: Other TCP congestion control mechanisms include congestion avoidance, fast retransmit, and fast recovery.
- explanation-03: CUBIC and BBR are more modern TCP congestion control variants.
- explanation-03: TCP congestion control lets millions of independent connections share network capacity without a central coordinator.
- explanation-04: A process is an independent execution unit with its own memory address space, file descriptors, and OS resources.
- explanation-04: Threads have their own stack and register state.
- explanation-04: Threads share heap, global variables, and file descriptors with sibling threads.
- explanation-04: Supervisors such as Gunicorn/uWSGI workers or pm2 restart a crashed worker process without affecting other workers.
- explanation-04: Different processes can run as different users, with different permissions and different sandboxing such as seccomp or containers.
- explanation-04: A thread cannot be given less privilege than its sibling threads because they share the same process security context.
- explanation-04: SSH privilege separation and browser sandboxes use processes rather than threads.
- explanation-04: Processes can be killed, restarted, or migrated to another host individually.
- explanation-04: A thread cannot be relocated independently of its process.
- explanation-04: Because processes do not share memory, using processes eliminates whole classes of race conditions.
- explanation-04: Using processes requires explicit, deliberate IPC for anything shared, which forces cleaner boundaries in some architectures such as microservices and worker pools communicating via queues.
- explanation-05: A program's root set includes globals, the stack, and active closures.
- explanation-05: A collection referenced by a long-lived object stays reachable.
- explanation-05: Callbacks often close over a large object graph.
- explanation-05: Both common causes share a pattern in which something long-lived accumulates references to something that should be short-lived.
- explanation-05: Examples of long-lived things that accumulate references include globals, caches, and singletons.
- summarization-01: The new keyboard shortcuts are shown in the tooltips on toolbar buttons.
- summarization-02: Detection and recovery for the incident were fast.
- summarization-02: It took 7 minutes from the incident to the page firing.
- summarization-02: Full rollback took approximately 34 minutes.
- summarization-02: The incident response process worked as intended.
- summarization-04: Clicking Export for PDF produces no immediate response.
- summarization-04: The bug was reproduced on two different machines.
- summarization-05: Ada is assigned to check with the mobile team lead about API deprecation notification.

Added facts (styled only):

- code-review-01: The function does not check that `roles` holds valid values before writing to the database.
- code-review-01: A `True`/`False` return value conveys neither what went wrong on failure nor what was inserted on success.
- code-review-03: The function assumes `customer_name` and `status` are valid, non-empty strings.
- code-review-03: If the caller passes `None` or an unexpected type, the error surfaces deep inside the database driver rather than where the bad input entered.
- code-review-03: The function has no error handling.
- code-review-03: If `cursor.execute` fails, for example because the database connection dropped, the exception propagates up with no context about what the function was trying to do.
- code-review-03: The function does not state whether an empty result list means no matching orders or that something went wrong.
- code-review-03: The empty-result behavior is worth documenting if the function is a shared API.
- code-review-04: If `value` is 5 and two threads both read 5, they both write 6 instead of the correct 7.
- code-review-04: The `reset` method has the same thread-safety issue as `increment`.
- code-review-04: If one thread calls `reset` while another is in the middle of `increment`, the increment can silently disappear or apply to the wrong value.
- code-review-05: If `$BACKUP_DIR` is empty or invalid, or `cd` fails for reasons such as permissions, a typo, or a missing argument, the script keeps running in the directory it started in.
- code-review-05: `gzip` fails on both `my` and `report.log` in that case.
- code-review-05: If no `.log` files exist, `ls *.log` prints an error message to standard output.
- code-review-05: That error text gets fed into the `for` loop as fake filenames, causing more errors when passed to `gzip`.
- code-review-05: The `-r` flag in `rm -rf` means it removes directories too, not just files.
- code-review-05: A directory named `archive.tmp` would be deleted entirely by `rm -rf *.tmp`.
- debugging-01: The function get_url takes a parameter named cfg.
- debugging-01: The corrected get_url returns the f-string "http://{cfg['host']}:{cfg['port']}/api".
- debugging-02: The value remains `NaN` on every tick of the interval.
- debugging-02: The arrow function is the more common fix.
- debugging-04: The byte 0xc3 appears at position 512 in the file.
- debugging-04: UTF-8 encoding can also read plain ASCII text.
- explanation-02: In an optimistic locking example, a record has a `version` number that starts at 1.
- explanation-02: Under pessimistic locking, no one else can read or change the locked record until you finish.
- explanation-03: Dropped packets force retransmissions and waste bandwidth.
- explanation-05: A leaking program uses more and more memory over time.
- explanation-05: Increasing memory use from a leak can slow a program down.
- explanation-05: Increasing memory use from a leak can crash a program.
- explanation-05: Leaks from forgotten listeners are common in user interfaces.
- explanation-05: In user interfaces, a component can be removed from the screen while its listener still holds a reference to it.
- summarization-01: Each button's tooltip shows that button's keyboard shortcut.
- summarization-02: The wrong pool size starved the checkout service's connection pool.
- summarization-02: The outage caused errors for about 12% of requests.
- summarization-02: The outage lasted from 09:14 to 09:48 UTC.
- summarization-04: The reporter concludes the issue is not browser-specific.
- summarization-05: Ada is assigned to run the dry run of the payments database migration.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 41 | 35 | 0.854 | 27 | 0 |
| code-review-02 | 20 | 15 | 0.75 | 18 | 2 |
| code-review-03 | 25 | 11 | 0.44 | 21 | 5 |
| code-review-04 | 28 | 13 | 0.464 | 18 | 5 |
| code-review-05 | 30 | 22 | 0.733 | 24 | 4 |
| debugging-01 | 5 | 5 | 1.0 | 8 | 3 |
| debugging-02 | 11 | 6 | 0.545 | 13 | 0 |
| debugging-03 | 10 | 10 | 1.0 | 9 | 0 |
| debugging-04 | 13 | 8 | 0.615 | 9 | 1 |
| debugging-05 | 14 | 12 | 0.857 | 15 | 0 |
| explanation-01 | 42 | 22 | 0.524 | 24 | 1 |
| explanation-02 | 29 | 25 | 0.862 | 32 | 8 |
| explanation-04 | 30 | 19 | 0.633 | 23 | 2 |
| explanation-05 | 19 | 13 | 0.684 | 14 | 2 |
| summarization-01 | 5 | 4 | 0.8 | 7 | 0 |
| summarization-02 | 16 | 10 | 0.625 | 8 | 2 |
| summarization-03 | 14 | 14 | 1.0 | 13 | 0 |
| summarization-04 | 13 | 13 | 1.0 | 11 | 2 |
| summarization-05 | 10 | 10 | 1.0 | 6 | 1 |

Median fraction: 0.75 over 19 scored pairs.

Median additions: 2 over 19 scored pairs.

Lost facts:

- code-review-01: The mutable default argument is a classic Python footgun.
- code-review-01: The mutable default can be fixed by using `roles=None` and then `roles = roles or []` inside the function.
- code-review-01: The mutable default can be fixed by using `roles=None` and then `if roles is None: roles = []` inside the function.
- code-review-01: Possible reasons for insertion failure include a bad connection, a duplicate name, a schema violation, and `db` being `None`.
- code-review-01: The except clause should at minimum catch `Exception`.
- code-review-01: Examples of specific failure modes are a duplicate user versus a connection error.
- code-review-02: The function throws `TypeError: Cannot read properties of undefined (reading 'name')` on every call.
- code-review-02: The `async` keyword makes the function return a Promise.
- code-review-02: The returned promise resolves or rejects based on the synchronous throw rather than on the fetch result.
- code-review-02: If the API returns an error object or unexpected shape, the function fails unpredictably.
- code-review-02: The corrected version awaits `res.json()` and returns `data.name.toUpperCase()`.
- code-review-03: Caller-controlled input such as `customer_name = "x' OR '1'='1"` lets an attacker read or modify arbitrary rows.
- code-review-03: The SQL injection allows an attacker to exfiltrate the whole table.
- code-review-03: A customer name containing an apostrophe, such as `"O'Brien"`, would produce malformed SQL and raise an error.
- code-review-03: The apostrophe failure occurs even with no malicious intent.
- code-review-03: `status` presumably should be one of a fixed set of values such as 'pending', 'shipped', or 'cancelled'.
- code-review-03: Nothing in the code enforces that `status` is one of the allowed values.
- code-review-03: Without status validation, typos or garbage input silently produce empty results.
- code-review-03: The function has no type hints and no docstring.
- code-review-03: Type hints and a docstring would help callers know the expected types and return shape.
- code-review-03: The return shape is a list of tuples/rows, dependent on the cursor's row factory.
- code-review-03: The missing type hints and docstring are a minor issue.
- code-review-03: The SQL injection must be fixed before the code ships.
- code-review-03: The issues other than the SQL injection are quality-of-life improvements.
- code-review-03: The other listed issues are independent of the security bug.
- code-review-04: Even with the GIL, the interpreter can switch threads between the read and the write.
- code-review-04: `self.value = 0` is a single atomic bytecode operation.
- code-review-04: Without external locking, there is no way to reason about 'reset happens after all these increments'.
- code-review-04: The class provides no `get()` or `value` accessor documented as thread-safe.
- code-review-04: Reading `counter.value` directly is a plain attribute read with no ordering guarantee relative to concurrent writers.
- code-review-04: In CPython, the plain attribute read itself is fine.
- code-review-04: The plain attribute read does not compose safely with check-then-act patterns such as reading and then deciding to reset.
- code-review-04: The code relies implicitly on CPython/GIL semantics.
- code-review-04: The code is not safe under free-threaded CPython (3.13+ no-GIL builds).
- code-review-04: The code is not safe under other Python implementations that lack a GIL.
- code-review-04: The code would be broken even more without the GIL's coarse-grained help masking some issues.
- code-review-04: The proposed fix imports `threading` and stores the count in `self._value` with a `threading.Lock` in `self._lock`.
- code-review-04: In the fix, `value` is a property that acquires the lock and returns `self._value`.
- code-review-04: The fix makes every mutation and read go through the same lock.
- code-review-04: The fix gives callers a well-defined `value` snapshot.
- code-review-05: `cd` can fail because the directory doesn't exist, because of permissions, or because of a typo.
- code-review-05: `cd $BACKUP_DIR` breaks on paths containing spaces or glob characters.
- code-review-05: The `ls *.log` error is cosmetic but noisy and misleading in a script meant to run unattended.
- code-review-05: Passing the literal `*.tmp` to `rm -rf` is harmless only because `-f` suppresses the "no such file" error.
- code-review-05: Filenames beginning with `-` could be interpreted as options by `gzip` because there is no `--` separator.
- code-review-05: `gzip` will refuse or prompt, depending on version and TTY, if a `.gz` file already exists for a given file.
- code-review-05: `gzip -f` can be used to overwrite an existing `.gz` file.
- code-review-05: The suggested rewrite fixes the empty-argument/home-directory problem, the silent `cd` failure, the `ls`-parsing bug, quoting throughout, and the "no matching files" glob edge case.
- debugging-02: A regular `function` passed to `setInterval` is called with `this` set to the global object.
- debugging-02: In strict mode, a regular function passed to `setInterval` is called with `this` set to `undefined`.
- debugging-02: Calling `.bind(this)` on the callback function is an alternative fix.
- debugging-02: Capturing `const self = this;` before `setInterval` and using `self.seconds` inside is an alternative fix.
- debugging-02: The arrow function is the cleanest modern solution among these fixes.
- debugging-04: Accented names and currency symbols are examples of non-ASCII characters.
- debugging-04: utf-8 is almost always the appropriate Unicode-capable encoding to use.
- debugging-04: errors="ignore" is an alternative to errors="replace".
- debugging-04: Using errors="replace" still counts lines correctly.
- debugging-04: Line counting does not depend on decoding every byte perfectly.
- debugging-05: When the test runs in isolation, "post" is appended so the list becomes ["draft", "post"], and the test passes.
- debugging-05: The fixed code is: def make_post(title, tags=None): if tags is None: tags = list(DEFAULT_TAGS); tags.append("post"); return {"title": title, "tags": tags}.
- explanation-01: The internal array of a hash map is called the bucket array.
- explanation-01: Collisions are inevitable once there are enough keys, because the array has a limited number of slots.
- explanation-01: Collisions are expected behavior rather than a bug.
- explanation-01: Every hash map implementation must handle collisions.
- explanation-01: The per-bucket collection in separate chaining is usually a linked list, and sometimes a tree or dynamic array.
- explanation-01: Linear probing is a probing sequence that tries index+1, index+2, and so on.
- explanation-01: Quadratic probing is a probing sequence.
- explanation-01: Double hashing is a probing sequence.
- explanation-01: Separate chaining has poor cache performance because linked list nodes are scattered in memory.
- explanation-01: Open addressing has good cache performance because its data is contiguous.
- explanation-01: Open addressing can fail entirely if the array is full.
- explanation-01: Chaining trades memory and cache locality for simplicity and graceful degradation.
- explanation-01: Open addressing trades simplicity for raw speed and memory efficiency.
- explanation-01: The load factor is entries divided by array size.
- explanation-01: Most hash map implementations resize by rehashing into a bigger array once the load factor crosses a threshold such as 0.7.
- explanation-01: Resizing at a load factor threshold happens regardless of which collision strategy is used.
- explanation-01: Java's HashMap uses chaining.
- explanation-01: Java's HashMap switches to trees for long chains.
- explanation-01: Python's dict leans toward open addressing.
- explanation-01: Most C++ hash map implementations lean toward open addressing.
- explanation-02: Seat booking is an example use case for pessimistic locking.
- explanation-02: An optimistic locking UPDATE increments the version column and includes the originally read version in its WHERE clause.
- explanation-02: If an optimistic locking UPDATE affects 0 rows, someone else updated the row first.
- explanation-02: Editing a user profile is an example use case for optimistic locking.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, or files.
- explanation-04: Threads have their own stack and register state.
- explanation-04: Processes must serialize or copy data across a boundary via IPC, which is slower than thread communication.
- explanation-04: Browsers sandbox each tab or renderer in a separate process.
- explanation-04: Supervisors such as Gunicorn/uWSGI workers or pm2 restart a crashed worker process without affecting other workers.
- explanation-04: Different processes can run as different users, with different permissions and different sandboxing such as seccomp or containers.
- explanation-04: A thread cannot be given less privilege than its sibling threads because they share the same process security context.
- explanation-04: SSH privilege separation and browser sandboxes use processes rather than threads.
- explanation-04: Processes can be killed, restarted, or migrated to another host individually.
- explanation-04: A thread cannot be relocated independently of its process.
- explanation-04: Using processes requires explicit, deliberate IPC for anything shared, which forces cleaner boundaries in some architectures such as microservices and worker pools communicating via queues.
- explanation-05: A program's root set includes globals, the stack, and active closures.
- explanation-05: A memory leak in a garbage-collected language is not a failure of the garbage collector.
- explanation-05: A memory leak in a garbage-collected language is a bug in reachability rather than in reclamation.
- explanation-05: Callbacks often close over a large object graph.
- explanation-05: A retained callback keeps its closed-over object graph alive long after the logical owner should have been discarded.
- explanation-05: Examples of long-lived things that accumulate references include globals, caches, and singletons.
- summarization-01: The new keyboard shortcuts are shown in the tooltips on toolbar buttons.
- summarization-02: Staging intentionally uses smaller configuration values than production.
- summarization-02: Detection and recovery for the incident were fast.
- summarization-02: It took 7 minutes from the incident to the page firing.
- summarization-02: Full rollback took approximately 34 minutes.
- summarization-02: The incident response process worked as intended.
- summarization-02: The remediation should focus on prevention rather than on incident response speed.

Added facts (styled only):

- code-review-02: If the request fails, the function throws an unhandled error.
- code-review-02: The corrected version throws an Error when the parsed profile has no name.
- code-review-03: The function does not check that `customer_name` and `status` are non-empty.
- code-review-03: The function does not check that `customer_name` and `status` are of the correct type.
- code-review-03: The function has no error handling.
- code-review-03: If `cursor.execute` fails, the exception propagates up without context about what the function was doing.
- code-review-03: Returning all matching orders can use a large amount of memory.
- code-review-04: Because the class uses no lock, none of its methods are thread-safe.
- code-review-04: If `reset` runs between the read and write in `increment`, the increment overwrites the reset with a stale value plus one.
- code-review-04: The fixed `Counter.__init__` sets `self.value = 0` and `self._lock = threading.Lock()`.
- code-review-04: The fixed `increment` uses `with self._lock:` and executes `self.value += 1`.
- code-review-04: The fixed `reset` uses `with self._lock:` and executes `self.value = 0`.
- code-review-05: `cd` can fail if `$BACKUP_DIR` is empty or wrong.
- code-review-05: `$1` is not quoted on the `cd` line.
- code-review-05: If no `.tmp` files exist, `rm -rf *.tmp` can receive the literal string `*.tmp` and print an error.
- code-review-05: If no `.log` files exist, `gzip` receives the literal string `*.log`.
- debugging-01: Looking up the missing key raises a KeyError.
- debugging-01: In the corrected code, config is {"host": "localhost", "port": 8080}.
- debugging-01: In the corrected code, get_url(cfg) returns the f-string "http://{cfg['host']}:{cfg['port']}/api".
- debugging-04: Passing errors="replace" to open() replaces each bad byte with a placeholder character.
- explanation-01: Chaining is the recommended choice for general-purpose maps.
- explanation-02: Under optimistic locking, a process must retry after a failed write.
- explanation-02: In the wiki example, the page has a `version` column.
- explanation-02: In the wiki example, two users open the page at version 5.
- explanation-02: In the wiki example, the database sets the version to 6 when the first user saves.
- explanation-02: In the wiki example, the database rejects the second user's write submitted with version 5.
- explanation-02: In the wiki example, the app shows a conflict message after the rejected write.
- explanation-02: In web apps, many users read data but few users write to the same row at the same time.
- explanation-02: In the bank transfer example, the process runs `SELECT ... FOR UPDATE` on both account rows.
- explanation-04: Switching between processes costs more than switching between threads.
- explanation-04: Process creation and switching cost more because the operating system must set up separate memory and resources.
- explanation-05: Memory held by a leak grows over time.
- explanation-05: A memory leak can exhaust the available memory.
- summarization-02: The incorrect pool size caused the connection pool to run out.
- summarization-02: The incorrect pool size caused checkout errors for 12% of requests.
- summarization-04: No error is shown after the first click of the PDF export button.
- summarization-04: Clicking the PDF export button several more times causes four identical "export failed" error banners to appear at once.
- summarization-05: Ada is to run the dry run for the payments database migration before Thursday.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 3 | 0 | 1 | 2 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 0 | 0 | 2 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 2 | 1 | 0 | 0.667 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-03 | 8 | 1 | 4 | 3 | 0.2 |
| explanation-04 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.2 over 5 scored pairs.

Claims that became certain:

- code-review-03: `SELECT *` also pulls columns the caller may not need.
- debugging-04: The Unicode-capable encoding to open the file with is almost always utf-8.
- explanation-03: If the sender started blasting data at full speed, it could easily overwhelm a router along the way.
- explanation-03: The congestion window is roughly the number of bytes of unacknowledged data the sender is allowed to have in flight at once.
- explanation-03: Packet loss usually means a router's queue overflowed.
- explanation-03: On loss, the sender backs off, typically cutting cwnd substantially.
- summarization-04: The PDF export failure is likely not browser-specific (reproduced on Firefox latest and Chrome, on two different machines).

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 1 | 0 | 0 | 1.0 |
| code-review-02 | 0 | 0 | 0 | 0 | n/a |
| code-review-03 | 3 | 0 | 2 | 1 | 0.0 |
| code-review-04 | 0 | 0 | 0 | 0 | n/a |
| code-review-05 | 2 | 0 | 0 | 2 | n/a |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 3 | 2 | 1 | 0 | 0.667 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 0 | 0 | 0 | 0 | n/a |
| explanation-04 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 0 | 0 | 0 | 0 | n/a |
| summarization-04 | 1 | 0 | 1 | 0 | 0.0 |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.667 over 5 scored pairs.

Claims that became certain:

- code-review-03: `SELECT *` also pulls columns the caller may not need.
- code-review-03: With no `LIMIT`, a broad match could return an unbounded number of rows.
- debugging-04: The Unicode-capable encoding to open the file with is almost always utf-8.
- summarization-04: The PDF export failure is likely not browser-specific (reproduced on Firefox latest and Chrome, on two different machines).

## Warnings

- technical-simplified/explanation-03: the pair failed the gate, excluded
