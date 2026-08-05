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

Judge: opus. Judged on 2026-08-05T06:28:26+00:00.

## Completeness (fact survival)

The judge lists the facts of the unstyled answer, then checks each fact against the styled answer. The fraction is the share of the facts that survive. The judge also lists the facts of the styled answer and checks each fact against the unstyled answer: a styled fact that the unstyled answer does not state is an addition. The lost facts and the added facts appear verbatim below the table.

### plain-language

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 29 | 18 | 0.621 | 23 | 2 |
| code-review-02 | 24 | 14 | 0.583 | 21 | 0 |
| code-review-03 | 26 | 18 | 0.692 | 26 | 5 |
| code-review-04 | 29 | 17 | 0.586 | 23 | 4 |
| code-review-05 | 34 | 28 | 0.824 | 39 | 5 |
| debugging-01 | 8 | 8 | 1.0 | 9 | 0 |
| debugging-02 | 17 | 14 | 0.824 | 16 | 1 |
| debugging-03 | 15 | 15 | 1.0 | 12 | 0 |
| debugging-04 | 19 | 11 | 0.579 | 14 | 1 |
| debugging-05 | 16 | 11 | 0.688 | 18 | 0 |
| explanation-01 | 42 | 35 | 0.833 | 27 | 1 |
| explanation-02 | 28 | 25 | 0.893 | 26 | 4 |
| explanation-03 | 36 | 22 | 0.611 | 20 | 1 |
| explanation-04 | 41 | 28 | 0.683 | 29 | 2 |
| explanation-05 | 17 | 14 | 0.824 | 17 | 0 |
| summarization-01 | 6 | 6 | 1.0 | 5 | 0 |
| summarization-02 | 12 | 5 | 0.417 | 13 | 4 |
| summarization-03 | 16 | 16 | 1.0 | 11 | 0 |
| summarization-04 | 14 | 10 | 0.714 | 11 | 0 |
| summarization-05 | 8 | 8 | 1.0 | 8 | 0 |

Median fraction: 0.769 over 20 scored pairs.

Median additions: 1.0 over 20 scored pairs.

Lost facts:

- code-review-01: If `db` is not provided, `db.insert(...)` raises `AttributeError`.
- code-review-01: Nothing checks that `name` is non-empty, is the correct type, or is not already present.
- code-review-01: Without validation, invalid input gets stored.
- code-review-01: The return value carries no information about failure.
- code-review-01: When `roles` is explicitly passed in, `.append` mutates the caller's list in place.
- code-review-01: Mutating the caller's list is a surprising side effect if the caller reuses that list elsewhere.
- code-review-01: The code has no duplicate-role guard.
- code-review-01: Calling the function with `roles=["member"]` produces `["member", "member"]`.
- code-review-01: The fixed version copies `roles` with `list(roles) if roles else []`.
- code-review-01: The fixed version appends `"member"` only if `"member"` is not already in `roles`.
- code-review-01: The fixed version calls `db.insert({"name": name, "roles": roles})` and returns `True`.
- code-review-02: Marking the function `async` gives no benefit here and masks the fact that the body is really synchronous.
- code-review-02: There is no guard on `data.name`.
- code-review-02: If the API returns a payload without a `name` field, or with `name` set to `null`, `.toUpperCase()` throws.
- code-review-02: The outer `profile` variable is unnecessary.
- code-review-02: Using a shared `profile` variable and mutating it in a closure is more indirect than working with the resolved value directly.
- code-review-02: The shared outer variable is what let the async bug hide in plain sight.
- code-review-02: `userId` is not encoded.
- code-review-02: If `userId` can contain special characters, it should be passed through `encodeURIComponent` before being interpolated into the URL path.
- code-review-02: The corrected version awaits `fetch` with the URL `/api/users/${encodeURIComponent(userId)}`.
- code-review-02: The corrected version throws an `Error` with the message 'Profile response missing name' when `data?.name` is falsy.
- code-review-03: A stacked or UNION payload can exploit the SQL injection, depending on the driver.
- code-review-03: `status` presumably comes from a small fixed set of values, such as an enum.
- code-review-03: Unexpected `status` values silently produce empty results instead of failing fast.
- code-review-03: `fetchall()` is used on potentially large result sets.
- code-review-03: The query has no LIMIT or pagination.
- code-review-03: A broad `customer_name` match could pull an unbounded number of rows into memory.
- code-review-03: The function has no type hints.
- code-review-03: Missing type hints make the expected argument and return types unclear at the call site.
- code-review-04: This failure mode is known as the lost-update bug.
- code-review-04: `+=` compiles to separate LOAD, ADD, and STORE steps at the bytecode level.
- code-review-04: `reset` writes `self.value = 0` with no coordination.
- code-review-04: Such an interleaving silently discards either the reset or the increment, depending on timing.
- code-review-04: Any external read of `self.value` is exposed to a TOCTOU race.
- code-review-04: The class has no `__slots__`.
- code-review-04: Relying on CPython's GIL to hand-wave these issues is not portable.
- code-review-04: The code is unsafe on any implementation without a GIL guaranteeing bytecode-level atomicity of the whole `current = ...; self.value = ...` sequence.
- code-review-04: In the fixed version, `__init__` creates `self._lock = threading.Lock()` and sets `self.value = 0`.
- code-review-04: In the fixed version, `increment` executes `self.value += 1` inside a `with self._lock:` block.
- code-review-04: In the fixed version, `reset` executes `self.value = 0` inside a `with self._lock:` block.
- code-review-04: The fixed version imports the `threading` module.
- code-review-05: The script assigns `BACKUP_DIR=$1` without quoting.
- code-review-05: If `$1` is empty, `cd` is called with no arguments and changes to `$HOME` instead of failing.
- code-review-05: With an unexpanded `*.tmp` glob, `rm -rf` fails harmlessly.
- code-review-05: If no `.log` files match, the glob `*.log` is passed literally to `ls`.
- code-review-05: `ls` errors to stderr with a message like `ls: cannot access '*.log'` when the glob does not match.
- code-review-05: The suggested fix checks `[ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]` and exits 1 with a usage message on stderr.
- debugging-02: The resulting `NaN` is assigned back to the property and logged.
- debugging-02: An alternative fix is to bind the regular function with `.bind(this)`.
- debugging-02: Another alternative fix is to capture `this` beforehand in a variable such as `const self = this;` and use `self.seconds` inside the callback.
- debugging-04: The errors="ignore" option is an alternative fallback to errors="replace".
- debugging-04: Detecting the encoding first is an alternative to assuming ASCII.
- debugging-04: chardet and charset-normalizer are libraries that detect encodings.
- debugging-04: The actual encoding might not be UTF-8 at all, for example Latin-1 or Windows-1252.
- debugging-04: The command `file <path>` inspects a specific file to determine its encoding.
- debugging-04: Checking the source of a file is a way to confirm its encoding.
- debugging-04: The encoding should be confirmed before picking it.
- debugging-04: errors="replace" silently corrupts characters when the encoding is wrong.
- debugging-05: When the test runs alone, it is the only call to make_post.
- debugging-05: In the full suite, DEFAULT_TAGS is already ["draft", "post"] by the time this test runs.
- debugging-05: In the full suite, the result becomes ["draft", "post", "post"], failing the assertion.
- debugging-05: The fixed code is: tags = list(tags) if tags is not None else list(DEFAULT_TAGS).
- debugging-05: Copying the caller's tags list protects callers from having their own list mutated in place.
- explanation-01: The array of a hash map is finite, but the space of possible keys usually is not.
- explanation-01: Collisions in a hash map are inevitable.
- explanation-01: The collection in a chaining bucket is sometimes a tree.
- explanation-01: Linear probing checks index+1, index+2, and so on.
- explanation-01: Quadratic probing is a probe sequence.
- explanation-01: Double hashing is a probe sequence.
- explanation-01: Rust's HashMap uses an open addressing variant for speed.
- explanation-02: Optimistic locking fits when transactions are short but the think time between read and write can be long.
- explanation-02: A user editing a form in a browser is an example of long think time between read and write.
- explanation-02: Pessimistic locking fits when the critical section is short so lock hold time stays small.
- explanation-03: The sender keeps a variable called the congestion window, abbreviated cwnd.
- explanation-03: The receiver's advertised window caps data based on the receiver's buffer space, not on the network.
- explanation-03: The initial congestion window was historically 1 segment.
- explanation-03: The initial congestion window is now commonly 10 segments.
- explanation-03: RFC 6928 specifies the initial congestion window of 10 segments.
- explanation-03: The name 'slow start' is somewhat misleading, because growth is slow only in the first round trip and then accelerates rapidly.
- explanation-03: Congestion avoidance is more cautious than slow start and grows the window linearly instead of exponentially.
- explanation-03: If a sender transmitted at a fixed conservative rate and never grew it, well-provisioned paths would be badly underused.
- explanation-03: With a fixed conservative rate, every connection would be slow regardless of the available capacity.
- explanation-03: Exponential growth is a deliberate compromise.
- explanation-03: Additive growth from the start would take too long to reach a good rate on high-capacity paths.
- explanation-03: Growth must stop being exponential, via ssthresh or a loss event, before it overshoots the network's actual capacity.
- explanation-03: Routers on the Internet do not tell endpoints that they are sending too fast.
- explanation-03: Newer algorithms use delay or ECN signals as feedback.
- explanation-04: A process has its own set of OS resources, such as file descriptors and signal handlers.
- explanation-04: Processes are isolated from each other by the OS and MMU.
- explanation-04: All threads in a process share the same open file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state, including the program counter.
- explanation-04: Browser tabs and sandboxed plugins are examples of running untrusted code.
- explanation-04: Independent lifecycle and restart is a reason to use more processes instead of more threads.
- explanation-04: A process provides restart granularity through the OS via kill, exit codes, and resource limits.
- explanation-04: A thread cannot be forcibly terminated as cleanly as a process.
- explanation-04: Resource limiting is a reason to use more processes instead of more threads.
- explanation-04: OS tools like ulimit, cgroups, and nice apply per-process.
- explanation-04: Capping CPU or memory for one piece of work independently requires that work to have its own process.
- explanation-04: Many workers reading and writing a shared in-memory cache is an example of work suited to threads.
- explanation-05: GC roots include globals, stacks, and active closures.
- explanation-05: Using a regular strong-referencing collection as a cache instead of a weak or bounded one causes a memory leak.
- explanation-05: A listener closure that captures its enclosing scope keeps a whole chain of otherwise-unrelated objects alive.
- summarization-02: The pool size was changed from 50 to 5.
- summarization-02: Connection pool sizing, and likely other resource limits, should be added to the review checklist.
- summarization-02: Detection to mitigation took about 34 minutes.
- summarization-02: The errors started at 09:14.
- summarization-02: The rollback happened at 09:48.
- summarization-02: The page fired quickly, within 7 minutes.
- summarization-02: Alerting on pool exhaustion specifically, rather than only on error rate, could shorten the diagnosis step.
- summarization-04: The reproduction clicks the "Export" button and then selects the PDF option.
- summarization-04: After selecting the PDF option, nothing happens.
- summarization-04: Four identical "export failed" error banners appear simultaneously.
- summarization-04: The bug was reproduced on Chrome on a colleague's machine.

Added facts (styled only):

- code-review-01: The function does not validate that `roles` is a list.
- code-review-01: Bad input can cause errors that the `except` then swallows.
- code-review-03: The psycopg2 driver uses `%s` as its parameter placeholder.
- code-review-03: Code that unpacks rows by position may misalign when a column is added to the table.
- code-review-03: One option for error handling is to catch the exception and re-raise it with more detail.
- code-review-03: Another option for error handling is to let the caller handle the exception deliberately.
- code-review-03: The appropriate error-handling choice depends on the needs of the surrounding code.
- code-review-04: The class is not thread-safe despite the code claiming it is.
- code-review-04: Another fix is to use `itertools.count()` or another atomic counter instead of a plain attribute.
- code-review-04: Another fix is to use `multiprocessing.Value` or an atomic integer type if the counter must work across processes.
- code-review-04: If calling code reads `counter.value` directly, that read can happen mid-write in another language's runtime.
- code-review-05: `cd` should be followed by `|| exit 1`, for example `cd "$BACKUP_DIR" || exit 1`.
- code-review-05: Running `rm -rf` on an unexpanded glob hides a wrong-directory mistake because it does not error out.
- code-review-05: Using a plain glob instead of `$(ls ...)` avoids a needless subprocess.
- code-review-05: Disk full or a permission problem can cause `gzip` to fail.
- code-review-05: `${1:?...}` fails immediately with a clear message when no argument is given.
- debugging-02: In strict mode, `this` inside such a plain function callback is `undefined`.
- debugging-04: The problematic byte is at position 512.
- explanation-01: Separate chaining's performance stays steady as the map fills up.
- explanation-02: Financial transfers, seat reservations, and inventory deductions are common cases for pessimistic locking.
- explanation-02: Two transactions that both act on stale data could cause real harm, such as double-booking a seat.
- explanation-02: Content editing systems and shopping-cart updates fit optimistic locking well.
- explanation-02: Most users edit different rows at the same time, so the check-and-retry cost of optimistic locking stays low.
- explanation-03: Slow start continues until the sender detects a loss, or the window reaches a threshold, or the window reaches the receiver's stated capacity.
- explanation-04: Web servers often run one process per worker for fault isolation.
- explanation-04: With one process per worker, a bug in handling one request won't take down the whole server.
- summarization-02: Small pool size values are set on purpose in staging.
- summarization-02: The connection pool exhaustion led to errors for about 12% of checkout requests.
- summarization-02: The staging and production templates sit in the same directory.
- summarization-02: The staging and production templates have similar names.

### technical-simplified

| Pair | Facts | Survived | Fraction | Styled facts | Additions |
|---|---|---|---|---|---|
| code-review-01 | 29 | 29 | 1.0 | 26 | 4 |
| code-review-02 | 24 | 19 | 0.792 | 20 | 0 |
| code-review-03 | 26 | 11 | 0.423 | 22 | 7 |
| code-review-04 | 29 | 24 | 0.828 | 22 | 5 |
| code-review-05 | 34 | 31 | 0.912 | 36 | 4 |
| debugging-01 | 8 | 7 | 0.875 | 6 | 0 |
| debugging-02 | 17 | 13 | 0.765 | 13 | 1 |
| debugging-03 | 15 | 13 | 0.867 | 12 | 2 |
| debugging-05 | 16 | 14 | 0.875 | 17 | 0 |
| explanation-02 | 28 | 24 | 0.857 | 20 | 1 |
| explanation-04 | 41 | 27 | 0.659 | 31 | 3 |
| summarization-01 | 6 | 6 | 1.0 | 5 | 0 |
| summarization-02 | 12 | 7 | 0.583 | 12 | 5 |
| summarization-03 | 16 | 16 | 1.0 | 13 | 0 |
| summarization-04 | 14 | 12 | 0.857 | 14 | 0 |
| summarization-05 | 8 | 7 | 0.875 | 6 | 0 |

Median fraction: 0.862 over 16 scored pairs.

Median additions: 1.0 over 16 scored pairs.

Lost facts:

- code-review-02: Marking the function `async` gives no benefit here and masks the fact that the body is really synchronous.
- code-review-02: The outer `profile` variable is unnecessary.
- code-review-02: Using a shared `profile` variable and mutating it in a closure is more indirect than working with the resolved value directly.
- code-review-02: The shared outer variable is what let the async bug hide in plain sight.
- code-review-02: The corrected version throws an `Error` with the message 'Profile response missing name' when `data?.name` is falsy.
- code-review-03: SQL injection is the biggest issue in the code.
- code-review-03: A stacked or UNION payload can exploit the SQL injection, depending on the driver.
- code-review-03: The SQL injection lets an attacker manipulate arbitrary rows.
- code-review-03: sqlite3 uses `?` placeholders instead of `%s`.
- code-review-03: `status` presumably comes from a small fixed set of values, such as an enum.
- code-review-03: Nothing in the code checks that `status` is one of the allowed values.
- code-review-03: Unexpected `status` values silently produce empty results instead of failing fast.
- code-review-03: The code has no error handling.
- code-review-03: A database error such as a bad connection or lock timeout propagates as a raw exception.
- code-review-03: The propagated exception gives the caller no context.
- code-review-03: `fetchall()` is used on potentially large result sets.
- code-review-03: The query has no LIMIT or pagination.
- code-review-03: A broad `customer_name` match could pull an unbounded number of rows into memory.
- code-review-03: The function has no type hints.
- code-review-03: Missing type hints make the expected argument and return types unclear at the call site.
- code-review-04: This failure mode is known as the lost-update bug.
- code-review-04: `+=` compiles to separate LOAD, ADD, and STORE steps at the bytecode level.
- code-review-04: The value read may already be stale by the time it is used.
- code-review-04: Any external read of `self.value` is exposed to a TOCTOU race.
- code-review-04: The class has no `__slots__`.
- code-review-05: `ls` errors to stderr with a message like `ls: cannot access '*.log'` when the glob does not match.
- code-review-05: The suggested fix checks `[ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]` and exits 1 with a usage message on stderr.
- code-review-05: Using `--` stops `rm` and `gzip` from treating filenames as options.
- debugging-01: The mismatch between `"port"` and `'Port'` raises a `KeyError`.
- debugging-02: The global object is `window` or `globalThis`.
- debugging-02: The resulting `NaN` is assigned back to the property and logged.
- debugging-02: An alternative fix is to bind the regular function with `.bind(this)`.
- debugging-02: Another alternative fix is to capture `this` beforehand in a variable such as `const self = this;` and use `self.seconds` inside the callback.
- debugging-03: The corrected code gives `[3, 5, 7]`.
- debugging-03: `[3, 5, 7]` is the expected result.
- debugging-05: The fixed code is: tags = list(tags) if tags is not None else list(DEFAULT_TAGS).
- debugging-05: Copying the caller's tags list protects callers from having their own list mutated in place.
- explanation-02: Optimistic locking fits when transactions are short but the think time between read and write can be long.
- explanation-02: A user editing a form in a browser is an example of long think time between read and write.
- explanation-02: Financial transactions and inventory decrements are cases where the cost of a conflict is severe.
- explanation-02: Pessimistic locking fits when the critical section is short so lock hold time stays small.
- explanation-04: A process has its own memory, including heap, stack, and data segment.
- explanation-04: A process has its own set of OS resources, such as file descriptors and signal handlers.
- explanation-04: All threads in a process share the same open file descriptors.
- explanation-04: Each thread has its own stack.
- explanation-04: Each thread has its own register state, including the program counter.
- explanation-04: Threads are cheaper to switch between than processes.
- explanation-04: Separate processes allow OS-level restrictions such as seccomp, capabilities, and separate users.
- explanation-04: Threads cannot get OS-level restrictions like seccomp, capabilities, or separate users.
- explanation-04: Threads share the parent's privileges and address space.
- explanation-04: A process provides restart granularity through the OS via kill, exit codes, and resource limits.
- explanation-04: A thread cannot be forcibly terminated as cleanly as a process.
- explanation-04: Resource limiting is a reason to use more processes instead of more threads.
- explanation-04: OS tools like ulimit, cgroups, and nice apply per-process.
- explanation-04: Capping CPU or memory for one piece of work independently requires that work to have its own process.
- summarization-02: The pool size was changed from 50 to 5.
- summarization-02: Detection to mitigation took about 34 minutes.
- summarization-02: The errors started at 09:14.
- summarization-02: The rollback happened at 09:48.
- summarization-02: The page fired quickly, within 7 minutes.
- summarization-04: The reproduction clicks the "Export" button and then selects the PDF option.
- summarization-04: The bug was reproduced on Chrome on a colleague's machine.
- summarization-05: Ada will run the payments database migration dry run

Added facts (styled only):

- code-review-01: The suggested fix raises `ValueError("name is required")` when `name` is falsy.
- code-review-01: The suggested fix catches `Exception` instead of using a bare `except`.
- code-review-01: The suggested fix logs the error with `logger.error` including the name and the exception.
- code-review-01: The suggested fix returns `True` on success and `False` on failure.
- code-review-03: The function has four problems.
- code-review-03: Most database drivers support parameterized queries.
- code-review-03: A later change to the table structure can break the caller in a silent way.
- code-review-03: A caller can pass `None` or another type to the function.
- code-review-03: The string concatenation raises an error when a caller passes a non-string value.
- code-review-03: Placeholder syntaxes include `%s`, `?`, and `:name`.
- code-review-03: The driver documentation states the correct placeholder syntax.
- code-review-04: Free-threaded CPython builds (3.13+) do not guarantee the atomicity of a single attribute read.
- code-review-04: The error grows with more threads and more calls.
- code-review-04: In the fix, the counter state is a private attribute `self._value` initialized to 0.
- code-review-04: In the fix, a `get` method returns `self._value` while holding the lock.
- code-review-04: The `get` method gives callers a safe way to read the count.
- code-review-05: `set -f` avoidance is not needed for the zero-match problem.
- code-review-05: When a `.gz` file with the same name already exists, `gzip` refuses by default.
- code-review-05: `gzip` prints an error to stderr when it refuses to overwrite an existing `.gz` file.
- code-review-05: A safer version loops over `*.tmp` and uses `[ -e "$f" ] && rm -f -- "$f"`.
- debugging-02: In strict mode, `this` inside the `setInterval` callback is `undefined`.
- debugging-03: The last valid start index is `len(values) - window`.
- debugging-03: Because `range()` excludes its end value, the code needs `+ 1` to include the last valid start index.
- explanation-02: Web applications with many read-heavy views often use optimistic locking.
- explanation-04: Shared memory is a mechanism that lets one process access another process's memory.
- explanation-04: A pipe is a mechanism that lets one process access another process's memory.
- explanation-04: A thread crash can bring down the whole process because the threads share memory.
- summarization-02: The staging and production templates live in the same directory.
- summarization-02: The staging and production templates have similar names.
- summarization-02: The shared directory and similar names make it easy to copy the wrong value.
- summarization-02: The team found the cause fast.
- summarization-02: The gap between the deployment and the page was long.

## Hedging survival

The judge lists the claims that the unstyled answer presents with uncertainty, then judges each claim in the styled answer: hedged (the uncertainty survives in some form), certain (the claim survives but reads as a fact — the failure this check targets), or absent (the claim is gone, a completeness loss). Survival is hedged / (hedged + certain). The claims that became certain appear verbatim below the table.

### plain-language

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 3 | 1 | 1 | 1 | 0.5 |
| code-review-03 | 4 | 0 | 1 | 3 | 0.0 |
| code-review-04 | 2 | 2 | 0 | 0 | 1.0 |
| code-review-05 | 2 | 1 | 1 | 0 | 0.5 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-04 | 2 | 2 | 0 | 0 | 1.0 |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-01 | 5 | 1 | 3 | 1 | 0.25 |
| explanation-02 | 4 | 0 | 3 | 1 | 0.0 |
| explanation-03 | 3 | 2 | 0 | 1 | 1.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| explanation-05 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 2 | 0 | 0 | 2 | n/a |
| summarization-03 | 2 | 2 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.75 over 10 scored pairs.

Claims that became certain:

- code-review-02: A corrected version would look like the code shown (one possible correction, not necessarily the only one)
- code-review-03: A value like `' OR '1'='1` — or possibly a worse stacked/UNION payload, depending on the driver — lets an attacker read or manipulate arbitrary rows.
- code-review-05: If no `.log` files match, the loop body may run once with the literal string `*.log` as `f`, causing `gzip` to fail noisily.
- explanation-01: Each bucket in separate chaining holds a small collection, usually a linked list and sometimes a tree.
- explanation-01: Implementations of open addressing typically use a "tombstone" marker instead of a true empty slot when deleting.
- explanation-01: Some high-performance implementations, like Python's dict or Rust's HashMap, use open addressing variants for speed.
- explanation-02: Holding a pessimistic lock until the transaction commits blocks other writers, and sometimes blocks readers as well.
- explanation-02: Pessimistic locking suits cases where you assume conflicts are likely enough that you would rather prevent them upfront.
- explanation-02: As a rule of thumb, optimistic locking trades a small chance of retry for better throughput under low contention, while pessimistic locking trades throughput and concurrency for guaranteed correctness under high contention or high-stakes writes.

### technical-simplified

| Pair | Claims | Hedged | Certain | Absent | Survival |
|---|---|---|---|---|---|
| code-review-01 | 0 | 0 | 0 | 0 | n/a |
| code-review-02 | 3 | 2 | 1 | 0 | 0.667 |
| code-review-03 | 4 | 0 | 1 | 3 | 0.0 |
| code-review-04 | 2 | 1 | 0 | 1 | 1.0 |
| code-review-05 | 2 | 0 | 2 | 0 | 0.0 |
| debugging-01 | 0 | 0 | 0 | 0 | n/a |
| debugging-02 | 0 | 0 | 0 | 0 | n/a |
| debugging-03 | 0 | 0 | 0 | 0 | n/a |
| debugging-05 | 1 | 1 | 0 | 0 | 1.0 |
| explanation-02 | 4 | 0 | 3 | 1 | 0.0 |
| explanation-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-01 | 0 | 0 | 0 | 0 | n/a |
| summarization-02 | 2 | 1 | 0 | 1 | 1.0 |
| summarization-03 | 2 | 2 | 0 | 0 | 1.0 |
| summarization-04 | 0 | 0 | 0 | 0 | n/a |
| summarization-05 | 0 | 0 | 0 | 0 | n/a |

Median survival: 0.834 over 8 scored pairs.

Claims that became certain:

- code-review-02: res.json() will probably attempt to parse an error body on a 4xx/5xx response, or may fail confusingly, instead of surfacing "user not found" cleanly
- code-review-03: A value like `' OR '1'='1` — or possibly a worse stacked/UNION payload, depending on the driver — lets an attacker read or manipulate arbitrary rows.
- code-review-05: If no `.tmp` files exist, most shells leave the literal glob `*.tmp` unexpanded, so `rm -rf` fails harmlessly here.
- code-review-05: If no `.log` files match, the loop body may run once with the literal string `*.log` as `f`, causing `gzip` to fail noisily.
- explanation-02: Holding a pessimistic lock until the transaction commits blocks other writers, and sometimes blocks readers as well.
- explanation-02: Pessimistic locking suits cases where you assume conflicts are likely enough that you would rather prevent them upfront.
- explanation-02: As a rule of thumb, optimistic locking trades a small chance of retry for better throughput under low contention, while pessimistic locking trades throughput and concurrency for guaranteed correctness under high contention or high-stakes writes.

## Warnings

- technical-simplified/explanation-01: the pair failed the gate, excluded
- technical-simplified/explanation-03: the pair failed the gate, excluded
- technical-simplified/explanation-05: the pair failed the gate, excluded
- technical-simplified/debugging-04: the pair failed the gate, excluded
