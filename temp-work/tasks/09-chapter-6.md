# Task 09: Chapter 6 — Summary & Next Steps (7 slides)

> **Purpose:** Review the full presentation and provide actionable next steps for tomorrow.
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 348–361
> **JP reference:** `slides/spec-kit-presentation.md` lines 2455–2565

---

## Slide 6-1: Chapter 6 Section Divider

**Plan ref:** Line 354

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 6: Summary & Next Steps
```

---

## Slide 6-2: The Transformation — What SDD Changes

**Plan ref:** Line 355 | **JP ref:** Lines 2462–2478

```markdown
---

## Chapter 6

# The Transformation — What SDD Changes

**SDD doesn't replace developers — it automates mechanical translation and amplifies human capability.**

| Axis | Traditional | SDD |
|---|---|---|
| **Central asset** | Code (specs serve code) | Spec (code serves specs) |
| **Maintenance** | Fix code, docs get outdated | Evolve specs, regenerate code |
| **Pivoting** | Full rewrite (high cost) | Spec update → regenerate (low cost) |
| **Developer role** | Mechanical translation | Creativity, experimentation, critical thinking |

> **The lingua franca of development moves from code to natural-language specifications.**
> Debugging means fixing specifications. Refactoring means restructuring for clarity.
```

**Notes:**
- Source: `spec-driven.md`
- 4-row comparison table
- Blockquote includes "debugging = fixing specs" (R10 enhancement)
- This is the philosophical closing slide

---

## Slide 6-3: 4 Core SDD Principles

**Plan ref:** Line 356 | **JP ref:** Lines 2480–2497

```markdown
---

## Chapter 6

# 4 Core SDD Principles

### 1. Specs catch bugs before they exist
> Bugs found in Clarify **never reach production**

### 2. AI works dramatically better with structure
> Structured specifications = predictable AI output

### 3. Pivoting becomes low-cost
> Update the spec → regenerate. No full rewrite needed.

### 4. The spec is the Single Source of Truth
> 3 months later: "Why this design?" → read the spec
```

**Notes:**
- 4 h3 sub-sections, each with a blockquote elaboration
- Large, visually impactful slide — principles displayed prominently

---

## Slide 6-4: Recommended Learning Paths

**Plan ref:** Line 357 | **JP ref:** Lines 2499–2515

```markdown
---

## Chapter 6

# Recommended Learning Paths

| Available Time | Recommended Path |
|---|---|
| **90 minutes** | Scenario A (QuickRetro) — full SDD workflow |
| **Half day** | A → M (ShortLink) — add API contracts |
| **Full day** | A → J → K → M → N → pick one ⭐⭐⭐ |
| **Advanced track** | M → D → P → R — shortest to distributed SDD |
| **Team training** | Everyone starts with A → self-select by level |
| **Conference (60 min)** | A or J, MVP tier only |

### Tips
- **Never skip Clarify** — it's the ROI source
- Check answer keys **after** (not during) — think first
- Watch **constitution density grow** with project risk
```

**Notes:**
- R7 enhancement — dedicated Learning Paths slide (split from combined slide)
- 6-row × 2-column table (at the row limit)
- 3 tips as bullet points under h3

---

## Slide 6-5: SDD Practice Guide — Start Today Checklist

**Plan ref:** Line 358 | **JP ref:** Lines 2517–2534

```markdown
---

## Chapter 6

# SDD Practice Guide — Start Today Checklist

| # | Action | Key Point |
|---|---|---|
| 1 | **`specify init` your project** | Constitution + templates auto-generated |
| 2 | **Write constitution first** | Principles before specs — not after |
| 3 | **Never skip Clarify** | `[NEEDS CLARIFICATION]` is SDD's ROI source |
| 4 | **Manage specs in branches** | `specs/[branch]/` for team review & merge |
| 5 | **Start with one feature** | Experience specify → plan → tasks on one feature |
| 6 | **Verify AI output vs spec** | Always cross-check generated code |

> **Mindset shift: Before writing code, ask "Is the spec sufficient?"**
```

**Notes:**
- R7 enhancement — dedicated Practice Checklist slide (split from combined slide)
- 6-row × 3-column table (at the limit)
- Blockquote for mindset shift message

---

## Slide 6-6: Resources

**Plan ref:** Line 359 | **JP ref:** Lines 2536–2558

```markdown
---

## Chapter 6

# Resources

### Spec Kit
- **Repository:** `github.com/github/spec-kit`
- **📽️ Video Overview:** `youtube.com/watch?v=a9eR1xsfvHg`
- **📖 Documentation:** `github.github.io/spec-kit/`
- **Workshop Guide:** `WORKSHOP.md` · **Scenarios:** `SCENARIOS.md`

### SDD Methodology
- **Complete guide:** `spec-driven.md`
- **Phase details:** each `/speckit.*` prompt file

### Get Started Now

```bash
specify init my-first-sdd-project --ai copilot
cd my-first-sdd-project && code .
# Open Copilot Chat → type /speckit.constitution
```
```

**Notes:**
- R8 enhancement — dedicated Resources slide (split from combined slide)
- 3 h3 categories: Spec Kit, SDD Methodology, Get Started
- Code block for quick start (3 lines)
- URLs in backtick code format

---

## Slide 6-7: Thank You

**Plan ref:** Line 360 | **JP ref:** Lines 2559–2565

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "Stop vibe coding. Start writing specs. — @shinyay" -->

# Stop vibe coding. Start specifying.
```

**Notes:**
- Section divider style — h1 only (centered, large)
- `_paginate: false` — no page number
- `_header: ""` — no header
- `_footer` overridden with the tagline + handle
- This is the FINAL slide — no additional content, clean ending
- QR code could optionally be added: `![QR](../QR.png)` (check with presenter)

---

## ✅ Chapter 6 Quality Checks

- [ ] Section divider for Chapter 6 present (slide 6-1)
- [ ] 7 numbered slides (6-1 through 6-7)
- [ ] Transformation slide has comparison table + "debugging = fixing specs" (slide 6-2)
- [ ] 4 Core Principles displayed prominently (slide 6-3)
- [ ] Learning Paths is a **separate** slide from Practice Checklist (slides 6-4 and 6-5)
- [ ] Resources is a **separate** slide from Thank You (slides 6-6 and 6-7)
- [ ] Learning paths table has 6 rows including conference talk
- [ ] Practice checklist has 6 actionable items
- [ ] Resources categorized: Spec Kit / SDD Methodology / Get Started
- [ ] Thank You slide has custom footer override
- [ ] Thank You slide uses `_paginate: false`, `_header: ""`
- [ ] Quick-start code block present in Resources
- [ ] No Japanese text
- [ ] Final tagline: "Stop vibe coding. Start specifying."

---

## 🏁 Final Assembly Checklist

After ALL chapter tasks (01–09) are complete, verify:

- [ ] Front-matter at top of file matches 00-overview.md specification
- [ ] Total slide count = 131 (count `---` separators = 131 + front-matter separator)
- [ ] Chapter section dividers: 7 total (Chapters 0–6, though Ch0 uses title slide instead)
  - Actually: Ch1, Ch2, Ch3, Ch4, Ch5, Ch6 = 6 section dividers + 1 title slide
- [ ] Every content slide has `## Section` h2 label
- [ ] No duplicate slide content
- [ ] Consistent formatting throughout (bold, italic, code, blockquote)
- [ ] All 18 scenarios (A–R) referenced at least once
- [ ] Theme file referenced correctly: `theme: github-dark`
- [ ] No Japanese text anywhere in the file
- [ ] File renders correctly with: `npx @marp-team/marp-cli --theme slides/themes/github-dark.css slides/spec-kit-presentation-en.md`
