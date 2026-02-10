# Scenario H: Cross-platform Log Analysis CLI Tool

| | |
|---|---|
| **Level** | ⭐⭐ Intermediate |
| **Duration** | ~100 min |
| **Key SDD themes** | CLI UX conventions, deterministic output, streaming performance, cross-platform packaging, backward compatibility |
| **Why it tests SDD** | CLI tools live in a contract with scripts, pipes, and humans simultaneously — vague exit codes, unstable output, or silent failures break entire automation chains |
| **Best for** | Developers building developer tools, CLIs, or data processing utilities |

---

## The Concept

You are building a CLI tool that analyzes application log files and produces actionable summaries — top errors, timelines, service breakdowns. It must handle multi-gigabyte files via streaming, produce machine-parseable JSON for scripting and human-readable text for terminals, and work identically on macOS, Linux, and Windows.

This scenario stress-tests SDD because:
- **CLI output IS the contract** — scripts depend on exact field names, column order, and exit codes; an unspecified output change breaks downstream automation silently
- **Backward compatibility is immediate** — once a flag or output field is released, changing it is a breaking change for every script that uses it
- **Performance must be specified** — "handles large files" without defining memory bounds and time budgets lets the AI load 2GB into RAM
- **Cross-platform behavior diverges in subtle ways** — line endings, path separators, terminal encoding, ANSI color support all need explicit handling
- **Error UX is the difference between a good and bad CLI** — clear error messages with actionable suggestions vs. stack traces dumped to stdout

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for building a cross-platform CLI tool.

Non-negotiables:
- Deterministic output: identical input must produce identical output across runs, platforms, and locales. No timestamps, random values, or locale-dependent formatting in output unless explicitly requested.
- Stable output contract: text output column order and JSON field names are part of the public API. Changes require a major version bump.
- Backward compatibility: commands, subcommands, and flags must not be removed or have their behavior changed once released. Deprecation with a warning for at least 2 minor versions before removal.
- Exit codes are semantic: 0 = success, 1 = user error (bad args, missing file), 2 = data error (parse failure, invalid log format), 3 = internal error (bug). Exit codes are part of the public API.
- Stderr for diagnostics, stdout for data: error messages, warnings, and progress indicators go to stderr. Command output goes to stdout. This ensures piping works correctly (e.g., tool summarize logs.json | jq).
- No silent failures: every error must produce a message to stderr and a non-zero exit code. If a file has unparseable lines, report them (count + sample) rather than silently skipping.
- Cross-platform: works identically on macOS, Linux, and Windows. Handle path separators, line endings, terminal encoding (UTF-8), and ANSI color detection. Colors are auto-detected (TTY) and controllable via --color=always|never|auto.
- Performance: streaming architecture — memory usage must be O(1) relative to file size (bounded by the number of unique error signatures, not the number of log lines). Define a concrete performance target.
- Testing: unit tests for parsing and grouping logic, golden tests for CLI output (text and JSON), performance benchmarks with large fixtures, and cross-platform CI (test on all three OSes).
- Documentation: README with install instructions (per platform), quickstart, command reference, examples with real output, piping/scripting recipes, and troubleshooting.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Deterministic output guarantee
- [ ] Stable output contract (field names/columns = public API)
- [ ] Backward compatibility with deprecation policy
- [ ] Semantic exit codes defined
- [ ] Stderr/stdout separation rule
- [ ] No-silent-failures guarantee
- [ ] Cross-platform requirements (paths, line endings, encoding, colors)
- [ ] Streaming / bounded memory constraint
- [ ] Golden test requirement

---

### Specification

```
/speckit.specify Build a CLI tool called "logsaw" that analyzes application log files and produces actionable summaries.

User goals:
- Quickly answer: "What are the top errors?", "When did they start?", "Which services are impacted?"
- Work locally on log files; also read from stdin for piping (e.g., cat logs.json | logsaw summarize).
- Integrate into scripts and automation via JSON output and reliable exit codes.

Commands:

1) logsaw summarize <path|->
   Prints a high-level summary of the log file:
   - Total lines, time range (first → last timestamp)
   - Breakdown by log level (ERROR, WARN, INFO, DEBUG) with counts and percentages
   - Top 3 error signatures with counts
   - If --service filter is active, show summary for that service only

2) logsaw top-errors <path|->
   Groups errors by signature (normalized message — strip variable parts like IDs, timestamps, file paths).
   Shows: rank, count, error signature, first seen, last seen, affected services.
   Default: top 10. Configurable with --limit N.
   Sorted by count descending.

3) logsaw timeline <path|->
   Shows error rate over time buckets.
   Default bucket size: auto (choose based on time range — minutes for <1h, hours for <24h, days for longer).
   Configurable with --bucket 5m|1h|1d.
   Output: time bucket, total events, error count, error rate (%).
   In text mode, include a simple ASCII bar chart for error rate.

Global options:
- <path> or - (stdin). If neither is provided and stdin is not a pipe, print usage and exit 1.
- --since <datetime> / --until <datetime> : filter by timestamp. Accept ISO 8601 and common relative formats ("1h ago", "yesterday").
- --format text|json : default "text" if stdout is a TTY, "json" if piped.
- --service <name> : filter to log lines from a specific service (if the log format includes a service field).
- --color always|never|auto : default "auto" (detect TTY).
- --verbose : show parse warnings (unparseable lines) on stderr.
- --version : print version and exit 0.
- --help : print help and exit 0.

Log format support:
- JSON Lines (one JSON object per line): auto-detected. Expected fields: timestamp (ISO 8601), level, message. Optional: service, error, stack_trace, request_id. Unknown fields are ignored.
- Plain text with timestamp prefix: auto-detected. Pattern: [YYYY-MM-DD HH:MM:SS] [LEVEL] message. Multi-line stack traces are grouped with the preceding error line.
- Auto-detection: try JSON parse on the first line. If it fails, fall back to plain text pattern. If neither matches, exit 2 with "Unsupported log format" error.

Error signature normalization:
- Replace UUIDs, numeric IDs, IP addresses, file paths, and timestamps in error messages with placeholders ({uuid}, {id}, {ip}, {path}, {timestamp}).
- Group errors with identical normalized signatures.

Performance:
- Streaming: process line-by-line. Never load the entire file into memory.
- Memory: O(unique_signatures + unique_services + time_buckets), not O(total_lines). For typical log files (<10,000 unique signatures), memory stays under 100MB.
- Speed: process a 2GB JSON Lines file in under 60 seconds on a modern laptop (single-threaded baseline).
- Large file progress: when processing files >100MB, show a progress indicator on stderr (bytes processed / total, if file size is known). Not shown when reading from stdin (size unknown).

Acceptance criteria:
- For a 2GB log file with 10M lines: completes in <60s, uses <100MB RAM, produces correct output.
- JSON output (--format json) is valid JSON, stable (same field names and structure across versions), and parseable by jq.
- Text output is human-readable with aligned columns, respects terminal width (truncate long signatures), and includes color when appropriate.
- Exit codes: 0 success, 1 user error (bad args, missing file, invalid date format), 2 data error (unsupported format, all lines unparseable), 3 internal error.
- Unparseable lines: by default, silently skip and count them. If --verbose, print first 5 unparseable lines to stderr with line numbers. If >50% of lines are unparseable, exit 2 with "Most lines could not be parsed" error.
- Piping works: logsaw summarize - < app.log | jq '.top_errors[0]' produces valid output.
- --help output includes usage, all commands, all options, and at least 2 examples.

Edge cases to explicitly cover:
- Empty file: print "No log entries found" to stderr, exit 0 (not an error — file exists but is empty).
- File with only unparseable lines: exit 2 with "Unsupported log format" error.
- Stdin is a TTY (user ran logsaw summarize without arguments or pipe): print usage to stderr, exit 1.
- Log file with mixed JSON and plain text lines: treat as JSON Lines (majority format wins based on first 100 lines).
- Timestamps in different time zones within the same file: normalize to UTC for grouping; display in original timezone in output.
- Very long error messages (>500 chars): truncate in text output with "…"; full message in JSON output.
- Windows path separators in error messages: normalize to forward slashes in signature placeholders.
- File path with spaces or special characters: handle correctly on all platforms.
- Compressed files (.gz): detect and decompress transparently if the gzip magic bytes are present.

Non-goals (explicitly out of scope):
- Real-time log tailing (tail -f equivalent) — future iteration.
- Remote log sources (S3, CloudWatch, etc.) — future iteration.
- Interactive/TUI mode — future iteration.
- Log format configuration file — auto-detection only for v1.
```

**Deliberate ambiguities to watch for:**
- What language/runtime is the CLI built in? (Affects distribution strategy significantly)
- Should `--since "1h ago"` be relative to now or to the last timestamp in the file?
- What is the exact JSON schema for each command's output?
- How are multi-line stack traces associated with their parent error in plain text format?
- Should the tool follow symlinks?

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguous areas
- [ ] All three commands defined with input/output behavior
- [ ] Exit codes defined with meanings
- [ ] Performance targets with concrete numbers
- [ ] A review and acceptance checklist

---

### Clarification

```
/speckit.clarify Review the logsaw CLI spec and ask me about every ambiguity, unstated assumption, and gap — especially around: implementation language, relative time semantics, JSON output schema, multi-line stack trace grouping, symlink handling, and any CLI UX conventions I may have missed.
```

Suggested answers for the workshop:

| Question Theme | Suggested Answer |
|---|---|
| Implementation language | Rust. Single static binary, no runtime dependencies, fast performance, cross-compiles to all three platforms. Use clap for argument parsing, serde for JSON, and indicatif for progress bars. |
| Relative time (--since "1h ago") | Relative to the current wall clock time (not to the file). This matches the mental model of "show me errors from the last hour." |
| JSON output schema | Each command has a documented JSON schema. `summarize` returns `{total_lines, time_range: {first, last}, levels: {error: N, warn: N, ...}, top_errors: [{signature, count, first_seen, last_seen}]}`. Schema is versioned and documented in the README. |
| Multi-line stack trace grouping | In plain text mode, any line that does not match the timestamp prefix pattern is treated as a continuation of the previous line. Stack traces are appended to the parent error's message. In JSON Lines, stack_trace is a separate field (no grouping needed). |
| Symlinks | Follow symlinks by default. If a symlink loop is detected, report error to stderr and exit 1. |
| Shell completions | Generate shell completions for bash, zsh, fish, and PowerShell via `logsaw completions <shell>`. Clap supports this natively. |
| Config file | No config file for v1. All options are CLI flags. A future version may support a .logsawrc for defaults. |
| Signal handling | Handle SIGINT (Ctrl+C) gracefully: stop processing, print partial results to stdout (with a "partial: true" field in JSON), exit 130 (128 + SIGINT). |

**Manual refinement:**

```
For test fixtures: create 3 sample log files — a small JSON Lines file (100 lines, 3 services, 5 error signatures), a large fixture generator script that creates a 2GB file for performance testing, and a plain text log file with multi-line stack traces. Include edge case fixtures: empty file, all-unparseable file, and mixed-format file.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] All three commands have defined input/output behavior and JSON schema
- [ ] Exit codes are semantic and documented
- [ ] Performance targets are concrete (60s for 2GB, <100MB RAM)
- [ ] Cross-platform behavior is specified (paths, line endings, colors, encoding)
- [ ] Edge cases all have defined behaviors (empty file, stdin TTY, mixed formats, compressed files)

---

### Plan

```
/speckit.plan Create a technical plan for implementing the logsaw CLI.

Tech stack:
- Language: Rust (2021 edition).
- Argument parsing: clap v4 with derive macros.
- JSON output: serde + serde_json.
- Progress bar: indicatif.
- Time parsing: chrono for timestamps, humantime for relative durations.
- Compression: flate2 for gzip decompression.
- Testing: built-in Rust test framework + insta for snapshot/golden tests.
- CI: GitHub Actions with matrix (ubuntu, macos, windows).
- Distribution: GitHub Releases with pre-built binaries for x86_64 and aarch64 on all three platforms. Homebrew formula for macOS. cargo install for Rust users.

The plan must include:
- Architecture: input layer (file/stdin/gzip detection) → parser layer (format detection, line parsing, multi-line grouping) → analysis layer (signature normalization, grouping, time bucketing) → output layer (text formatter, JSON serializer). Each layer is a separate module with clean interfaces.
- Parsing strategy: streaming line-by-line iterator. Format detection on first line. JSON Lines parser (serde_json::from_str per line). Plain text parser (regex for timestamp prefix, continuation line detection for stack traces). Error signature normalization via regex replacements (UUIDs, IDs, IPs, paths, timestamps → placeholders).
- Streaming architecture: single-pass processing. Accumulate in-memory only: HashMap<Signature, ErrorStats> + per-service counters + time bucket counters. Bounded by unique signatures, not total lines.
- Output formatting: text formatter with column alignment (terminal width detection via terminal_size crate, fallback to 80). JSON formatter via serde Serialize derive. --format auto-detection (isatty check on stdout).
- Cross-platform concerns: path handling via std::path (platform-agnostic). Line ending handling via BufReader (handles \r\n and \n). ANSI color via supports-color crate (or --color flag override). UTF-8 everywhere (reject non-UTF-8 input with error).
- Packaging and distribution: cargo build --release for each target. Cross-compilation via cross or cargo-zigbuild. Binary size optimization (LTO, strip). GitHub Actions release workflow triggered by git tag. Homebrew formula in a tap repository. SHA256 checksums for all binaries.
- Error handling: anyhow for internal errors, thiserror for typed errors in the library layer. All errors produce a human-readable message on stderr + appropriate exit code. No panics in release builds (catch_unwind at top level).
- Test strategy: unit tests for each parser (JSON Lines, plain text), unit tests for signature normalization (regex patterns), golden/snapshot tests for each command's text and JSON output (insta crate), performance benchmarks (criterion crate) with the 2GB fixture, cross-platform CI matrix (ubuntu-latest, macos-latest, windows-latest), integration tests that invoke the binary as a subprocess and verify stdout/stderr/exit code.
- Documentation plan: README with install (Homebrew, GitHub Releases, cargo install), quickstart (3 examples), full command reference (generated from clap help), piping recipes (jq, grep, awk integration), troubleshooting section (common errors + solutions).
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture, module breakdown, distribution strategy |
| `data-model.md` | Log entry structure, error signature format, JSON output schemas |
| `research.md` | Rust CLI ecosystem (clap, serde, indicatif), cross-compilation, Homebrew tap |
| `contracts/` | JSON output schema per command, exit code table, CLI help text |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Is the streaming architecture truly single-pass with bounded memory? (2) Does the cross-platform CI test on all three OSes? (3) Is the distribution strategy complete (binaries + Homebrew + cargo install)? (4) Are golden tests specified for both text and JSON output of every command?
```

**Checkpoint:**
- [ ] Architecture has clean layer separation (input → parse → analyze → output)
- [ ] Streaming is single-pass with bounded memory
- [ ] Cross-platform concerns are addressed (paths, line endings, colors, encoding)
- [ ] Distribution covers all three platforms with multiple install methods
- [ ] Error handling produces human-readable messages + correct exit codes
- [ ] Golden tests exist for every command × every format (text/JSON)
- [ ] Performance benchmarks exist with the 2GB fixture

---

### Tasks

```
/speckit.tasks Generate tasks for building the logsaw CLI.

Task preferences:
- Start with a minimal vertical slice: read a JSON Lines file line-by-line → parse → summarize command → text output. Validate end-to-end before adding more features.
- Add commands iteratively: summarize first (simplest), then top-errors (grouping logic), then timeline (time bucketing).
- Add each output format per command: text first, then JSON. Golden test for each.
- Add input sources iteratively: file path first, then stdin, then gzip.
- Include separate tasks for: error signature normalization (regex patterns with tests), plain text log parser (with multi-line stack trace grouping), --since/--until filtering, --service filtering, progress indicator, cross-platform testing, and packaging/release automation.
- Include a performance task: benchmark with the 2GB fixture, profile, and optimize if needed.
- Include documentation tasks: README, command reference, piping recipes, and shell completion generation.
- Each task must have a "done when" check.
```

**What to observe in `tasks.md`:**
- Vertical slice (parse → summarize → text output) is the first deliverable
- Commands are added iteratively (summarize → top-errors → timeline)
- Golden tests are created alongside each command + format combination
- Error signature normalization is a dedicated task with regex test cases
- Cross-platform CI setup appears early (not at the end)
- Packaging/release tasks include binary building + Homebrew + checksums
- Performance benchmark task exists with concrete targets

---

### Implement

```
/speckit.implement Execute all tasks in order. After completing the vertical slice (summarize command with JSON Lines input and text output), run the golden tests and verify the output is deterministic. After adding each new command, run all golden tests to ensure no regressions.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- Errors go to stderr, data goes to stdout (never mixed)
- Exit codes match the specification (0, 1, 2, 3)
- JSON output is valid and parseable by jq
- Memory usage is bounded (no Vec collecting all lines)
- File reading is streaming (BufReader line-by-line)
- Cross-platform path handling uses std::path, not string manipulation
- No panics in the codebase (proper error handling with anyhow/thiserror)

---

## Extension Activities

### Add a Feature: Real-time Log Tailing

Extend the CLI with a streaming mode:

```
/speckit.specify Add a "logsaw tail <path>" command that watches a log file for new lines (like tail -f) and continuously updates a live summary. Show a TUI dashboard with: current error rate (last 60 seconds), top 5 active error signatures, and a live ASCII timeline. Update every second. Handle log rotation (file is renamed and a new file appears at the same path). Exit cleanly on Ctrl+C with a final summary. Consider: how does this interact with piping (--format json should emit newline-delimited JSON events)?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Breaking Output Change

Force a backward-incompatible output change and trace the consequences:

```
A user request has come in: rename the JSON field "first_seen" to "earliest_occurrence" and "last_seen" to "latest_occurrence" across all commands. This is a breaking change for every script that parses the JSON output. Update the spec to define how this is handled. Consider: should this be gated behind --output-version 2? Should the old field names be preserved as aliases? What does the deprecation timeline look like per the constitution's backward compatibility rules? How do golden tests handle the transition?
```

This demonstrates how SDD handles backward compatibility in developer tools — the spec forces you to think through the impact on downstream consumers before making the change.
