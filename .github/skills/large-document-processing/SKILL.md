---
name: large-document-processing
description: >
  A 4-phase chunked processing strategy for analyzing, translating, summarizing, and explaining
  large documents (e.g., Markdown files spanning hundreds to thousands of lines) while avoiding
  context window saturation and producing high-quality output.
  Use this skill when processing documents over 200 lines, translating large Markdown files,
  generating detailed technical explanations, or producing AI analysis sidecars for long source content.
---

# Skill: Large Document Processing

A strategy for analyzing, translating, summarizing, and explaining large documents (e.g., Markdown files spanning hundreds to thousands of lines) while avoiding context window saturation and producing high-quality output.

## When to apply

Apply this skill when any of the following conditions are met:

- The input source is a Markdown or text file exceeding 200 lines
- The output is a long-form document spanning multiple sections
- The task requires covering the entire input, such as translation, detailed explanation, or AI analysis sidecar generation

## Strategy: 4-phase chunked processing

### Phase 1 — Structural Analysis

Grasp the structure of the source file **without reading it in full**.

1. Use `wc -l` to check the total number of lines in the file
2. Use `grep -n '^## \|^### '` to extract headings and line numbers, mapping section boundaries
3. Determine the number of sections and the line ranges for each, then plan the processing chunks

**Purpose**: Obtain an overview without consuming context, and optimize subsequent chunk splitting.

### Phase 2 — Chunked Reading

Following the section boundaries identified in Phase 1, read in units of 100–200 lines using the `offset` / `limit` parameters of `read_file`.

- Set chunk boundaries so as not to break the semantic coherence of sections
- After reading each chunk, **understand and interpret its content before** proceeding to the next chunk
- Never read the entire file at once

**Purpose**: Reliably comprehend the content in units that fit within the context window.

### Phase 3 — Incremental Output

Once comprehension of each chunk is complete, write it to the output file **immediately**.

1. First chunk → use `create_file` to create the file and output the opening portion (front matter, overview, first section)
2. Subsequent chunks → append to the end using `replace_string_in_file`
3. Writing out each chunk as it is processed persists intermediate results to the file

**Purpose**: Free processed content from context, securing room for subsequent chunk processing.

### Phase 4 — Mashup & Finalization

After all chunks have been processed, integrate and finalize the document as a whole.

- Add cross-cutting aggregation sections (configuration item summary tables, Breaking Changes, wrap-up, etc.)
- Check the document structure for consistency
- Report statistics (line count, section count, number of configuration items, etc.)

**Purpose**: Elevate the individual chunk outputs into a single, completed document.

## Guidelines

### Principles during chunk processing

- Follow the cycle of **1 chunk = 1 read + 1 comprehend + 1 write**
- Do not rely on memory for the detailed content of previous chunks. Trust that it has already been written to the output file
- Track per-section progress using `manage_todo_list`

### Techniques for context efficiency

- Collect metadata in advance using lightweight commands such as `grep` and `wc` to minimize the number of `read_file` calls
- Execute mutually independent information gathering (line count checks, heading extraction, etc.) in parallel
- Do not re-read the details of chunks that have already been written to the output file

### Quality assurance

- Cross-check the list of sections identified during Phase 1 structural analysis against the sections in the final output to ensure nothing is missing
- In Phase 4, use `wc -l` and `grep` to collect and report statistics on the final output
