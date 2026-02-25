# Task 01: Chapter 0 — Title & Introduction (5 slides)

> **Purpose:** Hook the audience and present the presentation's overall structure.
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 42–53
> **JP reference:** `slides/spec-kit-presentation.md` lines 1–91

---

## Slide 0-1: Title Slide

**Plan ref:** Line 48 | **JP ref:** Lines 1–18

```markdown
---
(front-matter block from 00-overview.md)
---

<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Introduction to Spec-Driven Development (SDD)

## Building Better Software in the AI Era with GitHub Spec Kit

Shinya Yanagihara, Developer Global BlackBelt, Microsoft Corporation — 2026
```

**Notes:**
- This is the ONLY slide using `section:first-of-type` CSS (centered, 2.4em h1)
- The front-matter block goes at the very top of the file BEFORE this slide
- h2 appears below h1 on the title slide (CSS `order: 0` for first-of-type)
- Footer is hidden on this slide only

---

## Slide 0-2: Today's Agenda

**Plan ref:** Line 49 | **JP ref:** Lines 19–33

```markdown
---

## Chapter 0

# Today's Agenda

| Chapter | Theme | Level | Time |
|---|---|---|---|
| **Chapter 1** | General — SDD Overview & Spec Kit | All | 37 min |
| **Chapter 2** | Beginner — SDD Workflow Fundamentals | ⭐ | 15 min |
| **Chapter 3** | Intermediate — Server-Side & API Contracts | ⭐⭐ | 12 min |
| **Chapter 4** | Intermediate–Advanced — Real-World Complexity | ⭐⭐⭐ | 12 min |
| **Chapter 5** | Advanced — Distributed Systems & Failure Models | ⭐⭐⭐⭐ | 15 min |
| **Chapter 6** | Summary & Next Steps | All | 5 min |
```

**Notes:**
- h2 = `## Chapter 0` (green section label)
- h1 = `# Today's Agenda` (white main title)
- Table: 6 rows × 4 columns (within limits)
- Times match SLIDE-PLAN-EN.md statistics table

---

## Slide 0-3: Who Is This Presentation For?

**Plan ref:** Line 50 | **JP ref:** Lines 34–51

```markdown
---

## Chapter 0

# Who Is This Presentation For?

- **Beginners** 🟢
  "I let AI write code, but things keep breaking…"
  → Chapters 1–2: Learn SDD fundamentals and the workflow

- **Intermediate** 🟡
  "How should I design API contracts? What about external services?"
  → Chapters 3–4: Server-side and real-world complexity

- **Advanced** 🔴
  "How do I write specs for distributed systems? What about failure models?"
  → Chapter 5: Sagas, consistency, and failure path specification
```

**Notes:**
- 3 persona blocks with emoji color indicators
- Each persona: bold label + quoted pain point + arrow to relevant chapters
- Quoted text in regular quotes (not blockquote `>`) — these are character speech

---

## Slide 0-4: Prerequisites by Chapter

**Plan ref:** Line 51 | **JP ref:** Lines 52–67

```markdown
---

## Chapter 0

# Prerequisites by Chapter

| Chapter | Prerequisites | Tech Stack |
|---|---|---|
| Chapter 1 | None | — |
| Chapter 2 | HTML/CSS/JS basics | Vanilla JS + localStorage |
| Chapter 3 | Node.js fundamentals | Express + SQLite |
| Chapter 4 | External API experience | Stripe / OIDC / Terraform |
| Chapter 5 | Distributed systems fundamentals | WebSocket / Saga / CRDT |

> Start from any level. Recommended: everyone begins with Chapter 1.
```

**Notes:**
- Table: 5 rows × 3 columns
- Blockquote at bottom for the recommendation
- JP line 66 has the same recommendation message

---

## Slide 0-5: Hands-On Environment

**Plan ref:** Line 52 | **JP ref:** Lines 68–91

```markdown
---

## Chapter 0

# Hands-On Environment

### Option 1: GitHub Codespaces (Recommended)

Repository **Code** → **Codespaces** → **New codespace** — start instantly

### Option 2: Local Setup

```bash
# Install the Spec Kit CLI
uv tool install specify-cli \
  --from git+https://github.com/github/spec-kit.git

# Initialize your project
specify init my-project --ai copilot
cd my-project && code .
```

> Dev Container users: `specify` CLI is pre-installed
```

**Notes:**
- Two options as h3 sub-sections
- Code block for local setup (5 lines — within limits)
- Blockquote for Dev Container note
- QR code image could be added here if desired: `![QR](../QR.png)` (optional — check with presenter)

---

## ✅ Chapter 0 Quality Checks

- [ ] Front-matter block appears at very top of the file
- [ ] Title slide has `_paginate: false`, `_header: ""`, `_footer: ""`
- [ ] Agenda table has correct chapter times matching statistics
- [ ] 3 personas match plan (Beginner/Intermediate/Advanced)
- [ ] Prerequisites table has 5 rows
- [ ] Code block is ≤10 lines
- [ ] All 5 slides separated by `---`
- [ ] No Japanese text
