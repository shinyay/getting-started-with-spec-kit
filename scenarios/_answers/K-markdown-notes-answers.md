# Scenario K: Markdown Notes — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Rendering Pipeline (Expected Output)

A well-run SDD process should produce a pipeline like this:

```
markdown source
  → marked.js (CommonMark mode, disable: tables, taskLists, html)
  → raw HTML
  → DOMPurify (allowlist: h1-h3, p, strong, em, del, code, pre, a, img, ul, ol, li, blockquote, hr)
  → safe HTML
  → preview pane
```

Key implementation details the plan should capture:
- **Parser config**: `{ gfm: false }` or equivalent CommonMark-strict mode; disable table/taskList/html extensions
- **Sanitizer allowlist**: matches ONLY tags the supported markdown can produce — no `<table>`, `<input>`, `<form>`, `<script>`, etc.
- **Link handling**: `<a>` tags forced to include `target="_blank" rel="noopener noreferrer"`; `href` values filtered against scheme allowlist
- **Scheme allowlist**: `javascript:` / `data:` / `vbscript:` stripped from both `href` and `src` attributes
- **Broken images**: `<img>` onerror handlers attached in JS AFTER DOMPurify runs (DOMPurify strips `onerror` HTML attributes)
- **Raw HTML**: parser configured to escape raw HTML tokens, not pass them through

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Markdown dialect | CommonMark strict — configure parser accordingly | Deterministic; avoids GFM-specific features leaking in |
| 2 | Raw HTML treatment | Stripped entirely (invisible) — parser config disables HTML input | Showing escaped `<div>` confuses non-developer users |
| 3 | Disallowed link scheme | Drop the `<a>` tag, keep link text as plain text | Preserves the content while removing the dangerous vector |
| 4 | Max note size | Best-effort up to 10K lines; 300ms debounce protects UX | Hard limits create surprising failures; debounce is sufficient |
| 5 | Image handling | URL-reference only; no paste/upload of image files in v1 | Storing image blobs in localStorage is impractical |
| 6 | Folder nesting | Capped at 2 levels (folder / subfolder / note) | Prevents recursive rendering complexity; simple CSS/HTML |
| 7 | Two-tab editing | Banner warning via `storage` event + last-write-wins | Tab locking is overkill for a single-user app |
| 8 | Delete recovery | Permanent delete with confirmation dialog; no trash bin in v1 | Trash adds significant implementation complexity |
| 9 | Storage full | Error banner: "Storage full — export your notes and remove old ones" | Never silent failure; never auto-prune (that's data loss) |
| 10 | Unsupported markdown | Rendered as plain escaped text; no warning badge in v1 | Clean and predictable; warning badge is a Stretch feature |

## Facilitator Notes

- **After Specify**: "Notice the NOT-supported list. It's as important as the supported list. Without it, the AI adds tables, footnotes, and math — complexity and attack surface you didn't ask for."
- **After Clarify**: "The `javascript:` link example surprises everyone. Most people don't think of markdown as a security concern until they see `[link](javascript:...)` is valid syntax."
- **After Plan**: "The rendering pipeline (source → parse → sanitize → display) decomposes 'just render markdown' into safety-critical processing steps. Ask: what happens if you skip the sanitizer?"
