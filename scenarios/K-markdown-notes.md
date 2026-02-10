# Scenario K: Markdown Note-Taking App

| | |
|---|---|
| **Level** | ⭐ Beginner |
| **Duration** | ~90 min |
| **Key SDD themes** | Content rendering correctness, feature scoping (whitelist), security |
| **Why it tests SDD** | "Render markdown" hides massive ambiguity — which subset, what security rules, what output stability guarantees — that only specs can resolve |
| **Best for** | Developers learning that output correctness needs explicit specification |

---

## The Concept

You are building a markdown note-taking app with a live preview. Every developer knows markdown, so they think they don't need to specify what "render markdown" means. That assumption is the trap.

Markdown is ambiguous:
- Which features are supported? (Tables? Footnotes? Math?)
- What happens with unsupported syntax? (Rendered? Stripped? Error?)
- Is `[Click me](javascript:alert('xss'))` a valid link?
- What does the preview show when the user types `<script>alert('hi')</script>`?

This scenario teaches that **output correctness requires an explicit whitelist**: what you DON'T render is as important as what you DO. And it introduces security (XSS prevention) as part of correctness, not as a separate concern.

This is the same skill that appears at higher difficulty in:
- Scenario H (⭐⭐): CLI output fields are a public contract — changing them breaks scripts
- Scenario I (⭐⭐⭐): API v2 response shapes must be precisely defined and stable

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a personal note-taking application with markdown rendering. Prioritize content safety (sanitize all rendered HTML; prevent XSS), rendering whitelist (explicitly list supported markdown features; anything not listed is not rendered), no data loss (auto-save; confirm before delete), keyboard-first UX (all actions via keyboard; mouse is convenience), accessibility (semantic HTML in rendered output), and minimal dependencies (no build tools; at most two external libraries: a markdown parser and an HTML sanitizer).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Content safety / XSS prevention
- [ ] Whitelist-based feature scoping (not blacklist)
- [ ] Data persistence / no data loss
- [ ] Accessibility requirements
- [ ] Dependency constraints

---

### Specification

```
/speckit.specify Build MarkdownPad — a personal markdown note-taking app with live preview.

Editor layout:
- Split-pane: left = markdown textarea, right = live HTML preview.
- Panes resizable via drag handle.
- Responsive: viewport < 768px stacks vertically with Edit/Preview toggle button.

Supported markdown (whitelist — this IS the rendering contract):
- Headings: # (h1), ## (h2), ### (h3)
- Inline: **bold**, *italic*, `inline code`, ~~strikethrough~~
- Links: [text](url) → opens in new tab with rel="noopener noreferrer"
- Images: ![alt](url) → displays inline with alt text
- Code blocks: triple backtick with optional language hint (no syntax highlighting in v1)
- Lists: unordered (- item, single level only) and ordered (1. item, single level only)
- Blockquotes: > text (single level only)
- Horizontal rules: ---
- Paragraphs: blank-line separated

NOT supported (v1): tables, footnotes, math/LaTeX, nested lists beyond 1 level, nested blockquotes, raw HTML pass-through (stripped entirely), task list checkboxes.

Unsupported markdown behavior: when the user types unsupported syntax (e.g., a markdown table), the preview renders it as plain escaped text.

URL security:
- Allowed link schemes: http, https, mailto. All others (javascript:, data:, vbscript:) are stripped — render the link text only, no <a> tag.
- Allowed image schemes: http, https only.
- All <a> tags include target="_blank" rel="noopener noreferrer".

Broken image handling: if an image URL fails to load, replace the <img> in the preview with styled text: "[Image: {alt text}]". Attach error handlers in JS after sanitization (since onerror HTML attributes are stripped by the sanitizer).

Rendering pipeline:
- markdown source → parser (CommonMark-compatible mode) → raw HTML → HTML sanitizer → safe HTML → preview pane.
- Parser must be configured to treat raw HTML tokens as plain text (escaped), not as HTML.
- Parser configuration must disable features matching the NOT-supported list (tables, task lists, etc.).

Preview performance: updates after 300ms of typing inactivity (debounced), or immediately on Ctrl+S.

Note management:
- Sidebar with folder tree (left of editor).
- Create new note (default name "Untitled Note"), rename (inline edit in sidebar), delete (confirmation dialog: "Permanently delete '{name}'?"). No trash/recycle bin in v1 — deletion is permanent.
- Organize into folders: create folder, drag note into folder. Folder nesting capped at 2 levels (folder / subfolder / note).

Search: search bar filters sidebar by title AND content match. Case-insensitive substring. Instant client-side filter.

Export:
- Single note: download as standalone .html file with inline CSS.
- All notes: download as .json backup file containing all notes and folders. (Not zip — avoids a third dependency.)
- Import: load a previously exported .json backup to restore notes.

Auto-save: save current note to localStorage after 3 seconds of typing inactivity (debounced).

Two-tab conflict: use the browser storage event to detect when another tab writes to the same note key. Show non-blocking banner: "This note was modified in another tab. Reload to see changes." Resolution: last-save-wins.

Paste behavior: pasting from external sources (Google Docs, web pages) must insert plain text only. Intercept paste event and extract text/plain.

Keyboard shortcuts: Ctrl+B (bold selection), Ctrl+I (italic selection), Ctrl+K (insert link template at cursor), Ctrl+S (force save), Ctrl+N (new note), Ctrl+Shift+F (focus search bar).

Sample data: 3 pre-loaded notes:
- "Welcome to MarkdownPad" — demonstrates ALL supported markdown features
- "Meeting Notes — Sprint 42" — practical everyday example
- "Shopping List" — simple list example

Scope tiers:
- MVP (required): Single note + markdown whitelist rendering + DOMPurify sanitizer + auto-save
- Core (recommended): + Multi-note + folders + sidebar + search + single-note HTML export
- Stretch (optional): + JSON backup export/import + resizable panes + keyboard formatting + responsive layout
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: What markdown dialect defines behavior when the parser is ambiguous — CommonMark strict, GFM, or "whatever the parser does by default"?
2. Decision needed: Should raw HTML in markdown source be stripped entirely (invisible), or escaped and shown as visible text?
3. Decision needed: If a link has a disallowed URL scheme, do we drop the link but keep the text, or render the entire markdown syntax as plain text?
4. Decision needed: What is the maximum note size before the app is allowed to degrade? (1K lines? 10K? Best-effort?)
5. Decision needed: Can users paste images into notes, or only reference images by URL?
6. Decision needed: What should folder nesting depth be — unlimited, or capped at a specific level?
7. Decision needed: When two tabs edit the same note, should we warn + last-write-wins, or lock editing to one tab?
8. Decision needed: Is deleted note recovery possible (trash bin with retention), or is deletion permanent?
9. Decision needed: What happens when localStorage quota is exceeded — silent failure, error banner, or auto-prune oldest notes?
10. Decision needed: When unsupported markdown is typed (e.g., a table), should the preview show escaped text, show nothing, or show a "not supported" indicator?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/K-markdown-notes-answers.md`](_answers/K-markdown-notes-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Supported markdown features whitelist with rendered HTML tag mapping
- [ ] NOT-supported list with reasons for each exclusion
- [ ] Security rules (URL schemes, sanitization, raw HTML handling)
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement** — add details the AI missed:

```
For the sample data: the "Welcome to MarkdownPad" note should demonstrate every supported markdown feature — headings (h1–h3), bold, italic, inline code, strikethrough, a link, an image, a code block, unordered list, ordered list, blockquote, and horizontal rule. The preview of this note serves as a visual reference for what the renderer supports.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] All 10 deliberate ambiguities have documented resolutions
- [ ] URL scheme rules are explicit and complete
- [ ] Rendering whitelist is unambiguous

---

### Plan

```
/speckit.plan Use vanilla HTML, CSS, and JavaScript. Two allowed external dependencies: a CommonMark-compatible markdown parser (e.g., marked.js configured for CommonMark) and an HTML sanitizer (e.g., DOMPurify). Store all data in localStorage. The rendering pipeline is: markdown source → parser → raw HTML → sanitizer → safe HTML → preview pane. Parser must be configured to disable features not in the supported list (tables, task lists, raw HTML). Sanitizer must run with an allowlist matching only the HTML tags the supported markdown can produce.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture with rendering pipeline design |
| `data-model.md` | Note, folder, and settings models |
| `research.md` | Markdown parser config options, DOMPurify allowlist, storage event API |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Is the parser configured to disable unsupported features (tables, task lists, raw HTML tokens)? (2) Does the sanitizer use an allowlist, not a denylist? (3) Is the rendering pipeline clearly defined as source → parse → sanitize → display? (4) Are broken image error handlers attached after sanitization?
```

**Checkpoint:**
- [ ] Rendering pipeline is explicit and ordered
- [ ] Parser config disables unsupported features
- [ ] Sanitizer uses tag/attribute allowlist
- [ ] Only 2 external dependencies

---

### Tasks

```
/speckit.tasks
```

**What to observe in `tasks.md`:**
- Rendering pipeline tasks come early (parser config → sanitizer config → integration)
- Security rules (URL scheme filtering, raw HTML handling) are NOT deferred to the end
- Note management tasks follow rendering tasks
- MVP / Core / Stretch ordering is respected
- Export tasks come after note management (they depend on the data model)

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run after tasks to verify every rendering rule and security constraint in the spec has a corresponding implementation task.

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- Parser is configured to disable tables, task lists, and other unsupported features
- DOMPurify runs with an explicit tag/attribute allowlist, not default settings
- `javascript:` / `data:` / `vbscript:` links are stripped; link text is preserved
- Broken image `onerror` handlers are attached after DOMPurify sanitization (not as HTML attributes)
- Paste event is intercepted; only `text/plain` is inserted
- Preview debounce is 300ms, not instant
- No features outside the specified scope tier

---

## Extension Activities

### Add a Feature: Tags

Add tags to notes using the full SDD workflow:

```
/speckit.specify Add a "Tags" feature to MarkdownPad. Users can add tags to any note via a comma-separated input below the title. Tags appear as styled pills/badges. The sidebar can filter notes by tag — clicking a tag shows only notes with that tag. Tag autocomplete suggests existing tags as the user types. Tags are stored alongside each note in localStorage.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Add Table Support

Move "Tables" from the NOT-supported list to the supported list. See how a "small" feature cascades through the entire SDD lifecycle:

```
/speckit.specify Update MarkdownPad to support markdown tables. Tables should render as HTML <table> with proper <thead>/<tbody>. Column alignment (left/center/right via colons) should be supported. The sanitizer allowlist must be updated to include table-related tags. Update the "Welcome to MarkdownPad" sample note to include a table example.
```

Then re-run `/speckit.clarify` to discover new ambiguities: nested tables? Empty cells? Very wide tables overflowing the preview pane? This demonstrates how a "small" spec change cascades — the whitelist changes, the sanitizer config changes, the sample data changes, and new edge cases appear.
