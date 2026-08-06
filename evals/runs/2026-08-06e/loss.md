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

Judge: opus. Judged on 2026-08-06T09:15:15+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 30 | 25 | 0.833 | 21 | 0 |
| code-review-02 | 24 | 20 | 0.833 | 26 | 2 |
| code-review-03 | 24 | 19 | 0.792 | 25 | 1 |
| code-review-04 | 24 | 18 | 0.75 | 18 | 3 |
| code-review-05 | 30 | 24 | 0.8 | 32 | 8 |
| debugging-01 | 7 | 7 | 1.0 | 9 | 1 |
| debugging-02 | 13 | 7 | 0.538 | 12 | 2 |
| debugging-03 | 11 | 10 | 0.909 | 9 | 0 |
| debugging-04 | 15 | 10 | 0.667 | 10 | 1 |
| debugging-05 | 18 | 15 | 0.833 | 14 | 1 |
| explanation-01 | 42 | 29 | 0.69 | 25 | 1 |
| explanation-02 | 29 | 24 | 0.828 | 33 | 9 |
| explanation-03 | 31 | 22 | 0.71 | 24 | 6 |
| explanation-04 | 32 | 22 | 0.688 | 32 | 3 |
| explanation-05 | 16 | 10 | 0.625 | 17 | 4 |
| summarization-01 | 5 | 5 | 1.0 | 5 | 1 |
| summarization-02 | 12 | 6 | 0.5 | 17 | 6 |
| summarization-03 | 16 | 15 | 0.938 | 15 | 0 |
| summarization-04 | 13 | 12 | 0.923 | 16 | 0 |
| summarization-05 | 10 | 10 | 1.0 | 11 | 2 |

Median fraction: 0.814 over 20 scored pairs.

Median additions: 1.5 over 20 scored pairs.

Lost facts:

- code-review-01: A caller-supplied `roles` list is mutated in place by `roles.append("member")`.
- code-review-01: Mutating a caller's list as a side effect can surprise the caller if they reuse that list elsewhere.
- code-review-01: The function has no duplicate check for `"member"`.
- code-review-01: If `"member"` is already in `roles`, it gets appended again, creating duplicates.
- code-review-01: A corrected version appends `"member"` only if it is not already in `roles`.
- code-review-02: The `async` keyword means the function always returns a Promise.
- code-review-02: The Promise returned by the function will reject due to the unawaited-fetch bug.
- code-review-02: There is no try/catch around the fetch chain.
- code-review-02: The fixed version validates the response shape by checking `data?.name` and throws if the name is missing.
- code-review-03: The `%s` placeholder style is appropriate for the driver shown.
- code-review-03: The code has a correctness bug that is independent of security.
- code-review-03: A benign customer name such as `O'Brien` would break the query because its quote is unescaped.
- code-review-03: The `O'Brien` breakage is caused by the use of plain string concatenation.
- code-review-03: Omitting error handling at this layer is probably acceptable if the caller handles exceptions.
- code-review-04: CPython has a GIL.
- code-review-04: The GIL only guarantees that individual bytecode operations are atomic.
- code-review-04: The GIL can still switch threads between the LOAD, ADD, and STORE steps of an increment.
- code-review-04: The counter code is not safe in CPython despite the GIL.
- code-review-04: It is a common misconception that GIL-protected code like this is safe in CPython.
- code-review-04: Integer assignment in Python is atomic, so the value cannot be corrupted.
- code-review-05: If no `.log` files exist, `ls *.log` prints an error to stderr.
- code-review-05: Using `#!/bin/sh` together with `$(...)` is fine because `$(...)` is POSIX.
- code-review-05: The script assumes GNU-ish behavior in places without being defensive.
- code-review-05: The suggested fix uses `set -eu`.
- code-review-05: The suggested fix uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` to validate the argument.
- code-review-05: The suggested fix loops over `*.tmp` and uses `[ -e "$f" ] && rm -f -- "$f"`.
- debugging-02: `this` inside a regular `function () {...}` is determined by how the function is called, not where it is defined.
- debugging-02: `setInterval` invokes its callback as a plain function call.
- debugging-02: Capturing `this` in a variable (e.g. `const self = this`) and referencing that variable inside the callback is a valid fix.
- debugging-02: Assigning `this` to a variable such as `self` is the pre-ES6 style of solving this problem.
- debugging-02: Calling `.bind(this)` on the callback function is a valid fix.
- debugging-02: The arrow function is the cleanest and most idiomatic of the three fixes.
- debugging-03: At i = 2 the window is `[3, 4]`.
- debugging-04: The byte 0xc3 is the start of a 2-byte UTF-8 sequence.
- debugging-04: Characters such as é and ñ are encoded as 2-byte UTF-8 sequences beginning with such a byte.
- debugging-04: Using errors="replace" or errors="ignore" can corrupt or mangle some characters.
- debugging-04: chardet and charset-normalizer are libraries that detect a file's real encoding.
- debugging-04: Detecting the real encoding is preferable to silently mangling data.
- debugging-05: The same test running twice can also cause the extra append.
- debugging-05: `pytest-randomly` can cause tests to run in an order that triggers the extra append.
- debugging-05: The fix creates a new list inside the function via `tags = list(DEFAULT_TAGS)` when `tags is None`.
- explanation-01: A hash map's backing array has a fixed number of slots.
- explanation-01: There are potentially infinite possible keys for a hash map.
- explanation-01: The per-slot collection in separate chaining is usually a linked list, sometimes a tree or dynamic array.
- explanation-01: Insert in separate chaining hashes the key, goes to the slot, and appends or updates an existing key.
- explanation-01: The fixed rule used to find another slot in open addressing is called a probe sequence.
- explanation-01: Linear probing tries the next slot, then the next (i+1, i+2, i+3...).
- explanation-01: Quadratic probing jumps by increasing squares (i+1, i+4, i+9...).
- explanation-01: Double hashing uses a second hash function to decide the step size.
- explanation-01: Separate chaining stays O(1) on average even with many collisions, until lists get long.
- explanation-01: The load factor is entries divided by slots.
- explanation-01: Both collision strategies rely on keeping the load factor low.
- explanation-01: Hash maps typically resize by rehashing into a bigger array once the load factor crosses a threshold like 0.7.
- explanation-01: Keeping the load factor low keeps collisions rare and operations close to O(1).
- explanation-02: A version marker can be a version number, a timestamp, or a hash.
- explanation-02: Editing a user profile is an example use case for optimistic locking.
- explanation-02: Editing a CMS document is an example use case for optimistic locking.
- explanation-02: A shopping cart is an example use case for optimistic locking.
- explanation-02: A dropped connection can leave stale locks.
- explanation-03: If a sender sent data at whatever rate the receiver's window allowed, it could put more data into the network than routers along the path can buffer.
- explanation-03: Slow start historically started with a congestion window of 1 segment.
- explanation-03: Modern TCP implementations often start with a congestion window of around 10 segments.
- explanation-03: Congestion avoidance is more cautious than slow start and grows the window linearly.
- explanation-03: When packet loss is detected, cwnd is cut back.
- explanation-03: When packet loss is detected, ssthresh is set near the point where the loss occurred.
- explanation-03: Setting ssthresh near the loss point prevents future slow starts from overshooting as far.
- explanation-03: Congestion avoidance and fast retransmit/recovery are later phases of congestion control.
- explanation-03: Congestion avoidance and fast retransmit/recovery handle steady-state and recovery from loss.
- explanation-04: A process is an independent execution unit with its own memory address space, file descriptors, and OS resources.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, or message queues.
- explanation-04: A thread shares its process's memory space, file descriptors, and resources with all other threads in the same process.
- explanation-04: Each thread has its own stack and register state.
- explanation-04: Multiple processes each get their own interpreter and GIL, so they run genuinely in parallel across cores.
- explanation-04: Processes can be killed, restarted, or resource-capped with memory or CPU quotas via OS tools independently of each other.
- explanation-04: Independent process lifecycles are useful for supervisor patterns, such as a master process restarting crashed workers.
- explanation-04: Independent process resource limits allow capping runaway memory use without affecting sibling processes.
- explanation-04: Using processes to avoid shared-state bugs trades performance and complexity for correctness guarantees.
- explanation-04: Threads are the right choice when tasks need to share large amounts of state cheaply and synchronization via locks and atomics can be managed correctly.
- explanation-05: Program roots include globals, the stack, and active closures.
- explanation-05: Examples of such callbacks include DOM event listeners, observers, and subscriptions to an event bus.
- explanation-05: A listener holds a reference to the object, and often the object holds a reference back to the listener, keeping it reachable indefinitely.
- explanation-05: A closely related cause is closures capturing more than intended.
- explanation-05: A closure kept alive, such as by being stored in a long-lived variable, can hold references to entire enclosing scopes.
- explanation-05: Closures capturing enclosing scopes can keep large objects alive that the closure does not actually need.
- summarization-02: Staging and production config templates currently live in the same directory.
- summarization-02: The staging and production config templates have similar names.
- summarization-02: The shared directory and similar names make it easy to copy a staging value into production by mistake.
- summarization-02: Detection-to-resolution took approximately 34 minutes.
- summarization-02: Error onset occurred at 09:14.
- summarization-02: Rollback was complete at 09:48.
- summarization-03: The worker pool will update the record when thumbnail generation is done.
- summarization-04: The bug was reproduced on the latest version of Firefox.

Added facts (styled only):

- code-review-02: The function throws `TypeError: Cannot read properties of undefined (reading 'name')` every time.
- code-review-02: The `async` keyword hides the real bug.
- code-review-03: Selecting every column wastes bandwidth.
- code-review-04: The bug where one update is lost is called a "lost update" bug.
- code-review-04: If one thread calls `reset()` while another is in the middle of `increment()`, the reset can wipe out an unfinished increment.
- code-review-04: In the fixed version, `increment()`, `reset()`, and `get()` each acquire `self._lock` using a `with` statement.
- code-review-05: If the target directory doesn't exist or is inaccessible, `cd` fails and prints an error.
- code-review-05: `rm -rf *.tmp` is dangerous if nothing matches the glob.
- code-review-05: The literal-glob risk is minor on its own but becomes much more damaging when combined with a wrong or missing directory.
- code-review-05: The suggested fix exits with status 1 and prints a usage message to stderr when $1 is empty.
- code-review-05: The suggested fix uses `cd "$BACKUP_DIR" || exit 1`.
- code-review-05: The suggested fix uses `rm -f -- *.tmp`.
- code-review-05: The suggested fix loops over `*.log` and uses `[ -e "$f" ] || continue` to skip when no files match.
- code-review-05: Using `--` before filenames prevents a name starting with `-` from being read as an option.
- debugging-01: The corrected function get_url returns f"http://{cfg['host']}:{cfg['port']}/api".
- debugging-02: With the arrow function fix, the code logs 1, 2, 3, and so on.
- debugging-02: The Timer constructor initializes this.seconds to 0.
- debugging-04: The byte 0xc3 appears at position 512 in the file.
- debugging-05: Each call to make_post adds another "post" entry to the same shared list.
- explanation-01: Rust's HashMap uses open addressing.
- explanation-02: In the example, two support agents open the same customer ticket with version = 3.
- explanation-02: In the example, Agent A changes the status and saves, the database confirms the version is still 3, saves the change, and sets version = 4.
- explanation-02: In the example, Agent B's save fails because Agent B's copy still has version = 3, and Agent B must reload the ticket and redo the edit.
- explanation-02: Most web applications have uncommon conflicts because users rarely edit the same record at the same time.
- explanation-02: Optimistic locking scales well because no one is blocked while they read or think.
- explanation-02: In the example, a bank transfer debits one account and credits another.
- explanation-02: In the example, the transaction locks both account rows with SELECT ... FOR UPDATE before making changes.
- explanation-02: Pessimistic locking prevents an account from going negative from two withdrawals that both saw the same starting balance.
- explanation-02: Pessimistic locking is simpler to reason about.
- explanation-03: The doubling continues until the sender hits a threshold, runs into a limit set by the receiver, or detects a lost packet.
- explanation-03: Once the sender hits a threshold, hits a receiver-set limit, or detects a lost packet, TCP switches to congestion avoidance.
- explanation-03: Retransmissions add more traffic to an already congested path.
- explanation-03: Retransmissions on a congested path can trigger a downward spiral called congestion collapse.
- explanation-03: In congestion collapse, the network becomes so overloaded that little useful data gets through.
- explanation-03: Slow start avoids congestion collapse by probing the network carefully.
- explanation-04: A single thread cannot be killed without special support.
- explanation-04: Killing a single thread is far riskier than killing a single process.
- explanation-04: Switching between processes takes more time and memory than switching between threads.
- explanation-05: A program with a memory leak uses more and more memory over time.
- explanation-05: Increasing memory use from a leak can slow a program down.
- explanation-05: Increasing memory use from a leak can crash a program.
- explanation-05: Keeping a reference to an object that is no longer needed is sometimes called a logical leak.
- summarization-01: Each button's tooltip shows its keyboard shortcut.
- summarization-02: A deploy used a staging template.
- summarization-02: The pool size mismatch exhausted the connection pool.
- summarization-02: The exhausted pool broke checkout for about 12% of requests.
- summarization-02: The recommended fix is to add pool size and other capacity settings to the review checklist.
- summarization-02: The team paged on-call within 7 minutes.
- summarization-02: The team rolled back within 34 minutes of the page.
- summarization-05: The listed items are action items from a meeting.
- summarization-05: Ada is assigned to run the dry run of the payments database migration.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 30 | 23 | 0.767 | 27 | 2 |
| code-review-02 | 24 | 15 | 0.625 | 15 | 1 |
| code-review-03 | 24 | 18 | 0.75 | 25 | 9 |
| code-review-04 | 24 | 18 | 0.75 | 21 | 3 |
| code-review-05 | 30 | 23 | 0.767 | 26 | 3 |
| debugging-01 | 7 | 6 | 0.857 | 6 | 1 |
| debugging-02 | 13 | 8 | 0.615 | 14 | 1 |
| debugging-03 | 11 | 11 | 1.0 | 11 | 1 |
| debugging-05 | 18 | 15 | 0.833 | 14 | 0 |
| explanation-01 | 42 | 24 | 0.571 | 22 | 1 |
| explanation-02 | 29 | 19 | 0.655 | 24 | 3 |
| explanation-04 | 32 | 12 | 0.375 | 23 | 5 |
| summarization-01 | 5 | 5 | 1.0 | 6 | 0 |
| summarization-02 | 12 | 8 | 0.667 | 15 | 2 |
| summarization-03 | 16 | 16 | 1.0 | 13 | 0 |
| summarization-04 | 13 | 12 | 0.923 | 10 | 0 |
| summarization-05 | 10 | 9 | 0.9 | 8 | 1 |

Median fraction: 0.767 over 17 scored pairs.

Median additions: 1 over 17 scored pairs.

Lost facts:

- code-review-01: Mutating a caller's list as a side effect can surprise the caller if they reuse that list elsewhere.
- code-review-01: The return value does not distinguish between a duplicate user, a db error, and invalid input.
- code-review-01: No exception or error message is logged.
- code-review-01: The function has no logging.
- code-review-01: Lack of logging makes failures vanish silently and makes production issues hard to diagnose.
- code-review-01: A corrected version catches `Exception` rather than using a bare except.
- code-review-01: A corrected version calls `logger.exception("Failed to insert user %s", name)` on failure and returns `False`.
- code-review-02: The `async` keyword means the function always returns a Promise.
- code-review-02: The Promise returned by the function will reject due to the unawaited-fetch bug.
- code-review-02: `fetch` does not reject on 4xx/5xx responses.
- code-review-02: Calling `res.json()` on an error body likely produces malformed or unexpected `data` instead of a clear error.
- code-review-02: The code does not validate the shape of the response.
- code-review-02: If the API returns an error object such as `{ error: "not found" }`, `data.name` is `undefined`.
- code-review-02: Calling `.toUpperCase()` on `undefined` throws.
- code-review-02: The fixed version validates the response shape by checking `data?.name` and throws if the name is missing.
- code-review-02: The fixed version lets callers handle errors via try/catch because the function is `async`.
- code-review-03: The SQL injection is a critical issue.
- code-review-03: The `%s` placeholder style is appropriate for the driver shown.
- code-review-03: The code has a correctness bug that is independent of security.
- code-review-03: A benign customer name such as `O'Brien` would break the query because its quote is unescaped.
- code-review-03: The `O'Brien` breakage is caused by the use of plain string concatenation.
- code-review-03: Omitting error handling at this layer is probably acceptable if the caller handles exceptions.
- code-review-04: CPython has a GIL.
- code-review-04: The GIL only guarantees that individual bytecode operations are atomic.
- code-review-04: The GIL can still switch threads between the LOAD, ADD, and STORE steps of an increment.
- code-review-04: The counter code is not safe in CPython despite the GIL.
- code-review-04: It is a common misconception that GIL-protected code like this is safe in CPython.
- code-review-04: Integer assignment in Python is atomic, so the value cannot be corrupted.
- code-review-05: `cd` with no arguments changes to the user's `$HOME` directory.
- code-review-05: Combined with `rm -rf *.tmp`, an empty `$BACKUP_DIR` could delete `.tmp` files from the user's home directory.
- code-review-05: If no `.log` files exist, `ls *.log` prints an error to stderr.
- code-review-05: Using `#!/bin/sh` together with `$(...)` is fine because `$(...)` is POSIX.
- code-review-05: The script assumes GNU-ish behavior in places without being defensive.
- code-review-05: The suggested fix uses `BACKUP_DIR=${1:?Usage: $0 <backup_dir>}` to validate the argument.
- code-review-05: The suggested fix loops over `*.tmp` and uses `[ -e "$f" ] && rm -f -- "$f"`.
- debugging-01: The mismatch between `'port'` and `'Port'` raises a `KeyError`.
- debugging-02: In strict mode, `this` in a plain function call is `undefined`.
- debugging-02: Capturing `this` in a variable (e.g. `const self = this`) and referencing that variable inside the callback is a valid fix.
- debugging-02: Assigning `this` to a variable such as `self` is the pre-ES6 style of solving this problem.
- debugging-02: Calling `.bind(this)` on the callback function is a valid fix.
- debugging-02: The arrow function is the cleanest and most idiomatic of the three fixes.
- debugging-05: The same test running twice can also cause the extra append.
- debugging-05: `pytest-randomly` can cause tests to run in an order that triggers the extra append.
- debugging-05: The repeated appends leave `DEFAULT_TAGS` as `["draft", "post", "post"]` by the time the test runs.
- explanation-01: A hash map's backing array has a fixed number of slots.
- explanation-01: There are potentially infinite possible keys for a hash map.
- explanation-01: The per-slot collection in separate chaining is usually a linked list, sometimes a tree or dynamic array.
- explanation-01: Insert in separate chaining hashes the key, goes to the slot, and appends or updates an existing key.
- explanation-01: The fixed rule used to find another slot in open addressing is called a probe sequence.
- explanation-01: Linear probing tries the next slot, then the next (i+1, i+2, i+3...).
- explanation-01: Quadratic probing jumps by increasing squares (i+1, i+4, i+9...).
- explanation-01: Double hashing uses a second hash function to decide the step size.
- explanation-01: Open addressing breaks down when full and needs resizing before the array fills up, since there is nowhere left to probe.
- explanation-01: Deletion in open addressing requires marking slots as 'deleted' rather than empty, or probing breaks.
- explanation-01: Separate chaining stays O(1) on average even with many collisions, until lists get long.
- explanation-01: Separate chaining is the more common default collision strategy.
- explanation-01: Java's HashMap uses separate chaining.
- explanation-01: Python's dict uses open addressing.
- explanation-01: The load factor is entries divided by slots.
- explanation-01: Both collision strategies rely on keeping the load factor low.
- explanation-01: Hash maps typically resize by rehashing into a bigger array once the load factor crosses a threshold like 0.7.
- explanation-01: Keeping the load factor low keeps collisions rare and operations close to O(1).
- explanation-02: Seat or ticket reservation systems are an example use case for pessimistic locking.
- explanation-02: Inventory decrement on checkout is an example use case for pessimistic locking.
- explanation-02: A version marker can be a version number, a timestamp, or a hash.
- explanation-02: An optimistic-locking update includes the read version in its WHERE clause and increments the version column.
- explanation-02: Editing a user profile is an example use case for optimistic locking.
- explanation-02: Editing a CMS document is an example use case for optimistic locking.
- explanation-02: A shopping cart is an example use case for optimistic locking.
- explanation-02: Optimistic locking is preferred in distributed or web systems where holding a database lock across a network round-trip or user think time is impractical or risky.
- explanation-02: Holding a database lock across user think time risks the lock being held far too long.
- explanation-02: A dropped connection can leave stale locks.
- explanation-04: A process is an independent execution unit with its own memory address space, file descriptors, and OS resources.
- explanation-04: Communication between processes requires explicit mechanisms such as pipes, sockets, shared memory, or message queues.
- explanation-04: A thread shares its process's memory space, file descriptors, and resources with all other threads in the same process.
- explanation-04: Each thread has its own stack and register state.
- explanation-04: Fault isolation matters for systems like web servers or worker pools where a bad request should fail in isolation rather than killing everything.
- explanation-04: In CPython, the Global Interpreter Lock means only one thread executes Python bytecode at a time.
- explanation-04: Because of the GIL, threads don't provide true CPU parallelism for compute-bound work in CPython.
- explanation-04: Multiple processes each get their own interpreter and GIL, so they run genuinely in parallel across cores.
- explanation-04: Browsers run tabs and renderers as separate processes.
- explanation-04: Running renderers as separate processes contains a renderer exploit rather than exposing the whole browser.
- explanation-04: Processes can be killed, restarted, or resource-capped with memory or CPU quotas via OS tools independently of each other.
- explanation-04: Independent process lifecycles are useful for supervisor patterns, such as a master process restarting crashed workers.
- explanation-04: Independent process resource limits allow capping runaway memory use without affecting sibling processes.
- explanation-04: Using processes to avoid shared-state bugs trades performance and complexity for correctness guarantees.
- explanation-04: Processes are heavier to create than threads because of the full memory space and OS bookkeeping.
- explanation-04: Inter-process communication is slower than thread communication because IPC has serialization and syscall overhead, whereas threads just touch shared memory.
- explanation-04: Processes use more total memory than threads.
- explanation-04: Examples of workloads suited to threads include a multithreaded server sharing a cache and parallel work on a shared in-memory dataset.
- explanation-04: For tightly sharing workloads, the coordination cost of processes, such as copying data and IPC, would dominate.
- explanation-04: Processes are the right choice when you need isolation, fault containment, or true parallelism despite a language runtime limitation.
- summarization-02: Detection-to-resolution took approximately 34 minutes.
- summarization-02: Error onset occurred at 09:14.
- summarization-02: Rollback was complete at 09:48.
- summarization-02: The paging and rollback process worked well.
- summarization-04: The bug was reproduced on the latest version of Firefox.
- summarization-05: Ada is assigned to check with the mobile team lead about whether the mobile team was informed of the API deprecation.

Added facts (styled only):

- code-review-01: The function has five problems.
- code-review-01: The corrected version lets errors propagate instead of hiding them.
- code-review-02: The corrected version returns `profile.name.toUpperCase()`.
- code-review-03: Memory was checked.
- code-review-03: There are no saved preferences for this project yet.
- code-review-03: `%s` is the parameter placeholder for MySQL.
- code-review-03: `%s` is the parameter placeholder for psycopg2.
- code-review-03: Returning all columns wastes bandwidth.
- code-review-03: The function has no docstring.
- code-review-03: The function has no type hints.
- code-review-03: Type hints for `customer_name: str` and `status: str` help readers and tools find errors early.
- code-review-03: Example allowed status values are "open", "shipped", and "canceled".
- code-review-04: The `reset` method can overwrite a concurrent `increment`.
- code-review-04: If a thread calls `reset` while another thread is inside `increment`, the increment can complete after the reset, so the increment is lost.
- code-review-04: The fixed class adds a `get` method that returns `self.value` while holding `self._lock`.
- code-review-05: If `$1` is empty or unset, `cd $BACKUP_DIR` does nothing and the shell stays in the current directory.
- code-review-05: The suggested rewrite exits with status 1 and an error message on stderr if `$BACKUP_DIR` is empty or is not a directory.
- code-review-05: `-r` is not needed for files matching `*.tmp` in a flat directory.
- debugging-01: The corrected function `get_url(cfg)` returns the f-string `f"http://{cfg['host']}:{cfg['port']}/api"`.
- debugging-02: The Timer constructor initializes `this.seconds` to 0.
- debugging-03: The corrected code, `moving_sum([1, 2, 3, 4], 2)`, prints `[3, 5, 7]`.
- explanation-01: Chaining is recommended when a high load factor or unknown data size is expected.
- explanation-02: In the optimistic locking example, reading a row returns `version = 3`.
- explanation-02: In the optimistic locking example, the update query includes `WHERE version = 3`.
- explanation-02: Optimistic locking avoids the cost of locks and keeps throughput high.
- explanation-04: A thread crash can bring down the whole program because all threads share the same memory.
- explanation-04: Locks can cause slowdowns.
- explanation-04: A process can run with different permissions than other processes.
- explanation-04: Threads cannot run with different permissions from one another.
- explanation-04: Threads share the same permissions and memory as the parent process.
- summarization-02: The database connection pool ran out.
- summarization-02: 12% of requests failed.
- summarization-05: Ada is assigned to run the dry run for the payments database migration.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 2 | 1 | 1 | 0 | 0.5 |
| code-review-03 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-04 | 1 | 1 | 0 | 0 | 1.0 |
| code-review-05 | 2 | 0 | 2 | 0 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 1 | 0 | 0 | 1 | n/a |
| explanation-03 | 5 | 2 | 2 | 1 | 0.5 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.5 over 7 scored pairs.

Claims that became certain:

- code-review-02: The unawaited fetch will throw `Cannot read properties of undefined (reading 'name')` almost every time.
- code-review-03: No error handling for `cursor.execute`, which can raise (bad connection, syntax error, etc.), is probably fine if the caller handles it, but it's worth confirming that's intentional.
- code-review-05: If `$1` is empty, `cd $BACKUP_DIR` goes to `$HOME`, and combined with `rm -rf *.tmp` this could wipe `.tmp` files from the user's home directory instead of failing safely.
- code-review-05: If the directory doesn't exist, `cd` fails but the script keeps going and runs `rm -rf *.tmp` in the current working directory, potentially deleting the wrong files entirely.
- explanation-03: The effect of increasing cwnd by one segment per ACK is that cwnd roughly doubles every round-trip time.
- explanation-03: Slow start ramps up quickly once it looks safe / grows fast while it seems safe.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 1 | 0 | 0 | 1 | n/a |
| code-review-02 | 2 | 0 | 1 | 1 | 0.0 |
| code-review-03 | 1 | 0 | 1 | 0 | 0.0 |
| code-review-04 | 1 | 1 | 0 | 0 | 1.0 |
| code-review-05 | 2 | 0 | 1 | 1 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-05 | 0 | 0 | 0 | 0 | n/a |
| explanation-01 | 0 | 0 | 0 | 0 | n/a |
| explanation-02 | 1 | 0 | 0 | 1 | n/a |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 0 | 0 | 0 | 0 | n/a |
| summarization-03 | 1 | 1 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.0 over 5 scored pairs.

Claims that became certain:

- code-review-02: The unawaited fetch will throw `Cannot read properties of undefined (reading 'name')` almost every time.
- code-review-03: No error handling for `cursor.execute`, which can raise (bad connection, syntax error, etc.), is probably fine if the caller handles it, but it's worth confirming that's intentional.
- code-review-05: If the directory doesn't exist, `cd` fails but the script keeps going and runs `rm -rf *.tmp` in the current working directory, potentially deleting the wrong files entirely.

## Call timing

A stored call row holds two times: duration_ms is the model
time that the CLI reports, and wall_ms is the wall clock of
the subprocess. The difference is the startup cost of one CLI
call.

Calls: 167, measured: 167.
Mean duration: 11085 ms. Mean wall: 32618 ms. Mean startup: 21533 ms.

## Warnings

- technical-simplified/explanation-05: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
- completeness:facts:85911da31d4f308ab275041e6a4e864825d5ab55a6b7e67c55ebd5fc38d48bad: the first call failed and the retry succeeded: claude exited with code 1: {"type":"system","subtype":"init","cwd":"/private/var/folders/tt/jh9lk8gs6_sfn5fhz4rp7pch0000gn/T/style-judge-loss-zd24zlb6","session_id":"8bed58b5-0b0d-4268-a71d-1204ea2a78e0","tools":[],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"auto","slash_commands":["deep-research","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","run","run-skill-generator","agents","autocompact","clea
