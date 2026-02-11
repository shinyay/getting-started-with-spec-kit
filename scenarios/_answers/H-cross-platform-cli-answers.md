# Scenario H: Cross-platform Log Analysis CLI — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Exit Code Contract (Expected Output)

A well-run SDD process should produce a definitive exit code table:

| Code | Meaning | Example |
|---|---|---|
| 0 | Success | Command completed, output written to stdout |
| 1 | User error | Bad arguments, missing file, invalid date format, stdin is TTY without pipe |
| 2 | Data error | Unsupported log format, >50% unparseable lines, all lines unparseable |
| 3 | Internal error | Bug in logsaw (should never happen in release) |
| 130 | SIGINT | User pressed Ctrl+C; partial results emitted |

Key decisions embedded in this table:
- **Empty file = exit 0** (file exists, is readable, has no entries — not an error)
- **Partial parse = exit 0** with stderr warnings (some unparseable lines are normal in real logs)
- **Majority unparseable = exit 2** (>50% threshold means the format is wrong, not just noisy)
- **SIGINT = exit 130** (128 + signal number, Unix convention; partial results in stdout)

## Output Contract (Public API Fields)

These field names and their types are part of the stable public API. Changing them is a breaking change per the constitution.

### `summarize` JSON schema
```json
{
  "total_lines": 1234,
  "time_range": { "first": "2025-01-01T00:00:00Z", "last": "2025-01-01T23:59:59Z" },
  "levels": { "error": 45, "warn": 120, "info": 900, "debug": 169 },
  "top_errors": [
    { "signature": "Connection refused to {ip}:{id}", "count": 20, "first_seen": "...", "last_seen": "..." }
  ],
  "unparseable_lines": 5,
  "partial": false
}
```

### `top-errors` JSON schema
```json
{
  "errors": [
    { "rank": 1, "signature": "...", "count": 45, "first_seen": "...", "last_seen": "...", "services": ["api", "worker"] }
  ],
  "total_unique_signatures": 23,
  "partial": false
}
```

### `timeline` JSON schema
```json
{
  "bucket_size": "1h",
  "buckets": [
    { "time": "2025-01-01T00:00:00Z", "total": 500, "errors": 12, "error_rate": 2.4 }
  ],
  "partial": false
}
```

## Error Signature Normalization Examples

| Raw Error Message | Normalized Signature |
|---|---|
| `Connection refused to 10.0.1.42:5432` | `Connection refused to {ip}:{id}` |
| `User 550e8400-e29b-41d4-a716-446655440000 not found` | `User {uuid} not found` |
| `Failed to open /var/log/app/2025-01-01.log` | `Failed to open {path}` |
| `Timeout after 30000ms for request abc-123` | `Timeout after {id}ms for request {id}` |
| `OOM at 2025-01-01T12:00:00Z in worker-3` | `OOM at {timestamp} in worker-{id}` |

Normalization order matters: UUIDs first (most specific), then IPs, then paths, then timestamps, then generic numeric IDs.

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Implementation language | Rust — single static binary, no runtime deps, fast, cross-compiles | Go is also valid; Node.js fails the "no runtime" and streaming performance constraints |
| 2 | --since "1h ago" | Relative to current wall clock time | Matches the human mental model "show me errors from the last hour" |
| 3 | JSON schema stability | Yes — field names are public API, versioned, documented | Scripts break on field renames; the constitution mandates this |
| 4 | Stack trace grouping | Lines without timestamp prefix are continuations of previous line | Simple heuristic that works for Java, Python, Node.js stack traces |
| 5 | Symlinks | Follow by default; exit 1 on symlink loop | Refusing symlinks breaks common log directory setups (/var/log → mount) |
| 6 | Zero matching entries | Empty JSON array/object (not an error); exit 0 | No matches ≠ error; scripts should check result count, not exit code |
| 7 | --verbose warning output | Buffered to stderr after stdout is complete | Interleaving breaks piped JSON; buffering keeps stdout clean |
| 8 | Number formatting | Always C/POSIX locale (no thousands separator) | Deterministic output is a constitutional principle; locale breaks golden tests |
| 9 | Mixed timezone bucketing | Normalize all to UTC for bucketing; display original timezone | UTC is the only sane bucketing default; the original timezone is informational |
| 10 | Multiple files | v1: one file or stdin only; future: multiple files with per-file context | Multiple files add complexity (merged timeline? per-file summary?); defer to v2 |

## Golden Test Strategy

Golden tests are the primary correctness mechanism for CLI tools. The answer key should produce:

| Test | Input | Expected Output | Validates |
|---|---|---|---|
| `summarize-jsonl-text` | 100-line JSON Lines | Snapshot of text output | Text formatting, alignment, colors stripped |
| `summarize-jsonl-json` | Same file | Snapshot of JSON output | JSON schema, field names, types |
| `top-errors-text` | Same file | Snapshot of text output | Ranking, signature normalization |
| `top-errors-json` | Same file | Snapshot of JSON output | JSON schema stability |
| `timeline-text` | Same file | Snapshot with ASCII bars | Auto-bucketing, bar chart |
| `timeline-json` | Same file | Snapshot of JSON output | Bucket boundaries, rates |
| `empty-file` | 0 bytes | stderr: "No log entries found" | Exit 0, empty handling |
| `all-unparseable` | Garbage text | stderr: error message | Exit 2, format detection |
| `stdin-pipe` | Piped input | Same as file output | stdin/file equivalence |
| `since-filter` | 100 lines, --since | Subset of entries | Time filtering |

## Facilitator Notes

- **After Constitution**: "This constitution has 10 principles — more than the 5 for QuickRetro. CLI tools have a higher surface area because they're used by humans AND scripts simultaneously. More contract surfaces = more principles."
- **After Specify**: "Did the generated spec define the JSON schema for each command? If not, the AI will invent field names during implementation — and those names become the de facto API."
- **After Clarify**: "The locale question (#8) seems obscure. But imagine a CI pipeline that parses your text output with awk on a French server where 1,000 means 1.0. Deterministic output is non-negotiable for CLI tools."
- **After Plan**: "Ask: where do golden test snapshots live? Are they committed to the repo? How does the CI pipeline compare them? If the answer is vague, the test strategy won't work."
- **After Implement**: "Run the tool with `| jq '.'` after every command. If jq chokes, the JSON is invalid. This is the simplest contract test for CLI tools."
