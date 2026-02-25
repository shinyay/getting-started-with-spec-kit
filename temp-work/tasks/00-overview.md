# Task 00: Master Overview — Conventions, Theme, and Cross-Cutting Rules

> This file establishes **all** conventions for creating `slides/spec-kit-presentation-en.md`.
> Every chapter task file (01–09) references this document.
> Any convention not documented here should follow the JP presentation (`spec-kit-presentation.md`) as precedent.

---

## 🎯 Output File

- **Path:** `slides/spec-kit-presentation-en.md`
- **Format:** Marp Markdown (slide separator: `---`)
- **Total slides:** 131 content slides + 6 section dividers = **137 `---`-separated blocks** (+ 1 front-matter block)
- **Target line count:** ~2,600 lines (based on JP presentation's 2,565 lines for 132 slides ≈ 19 lines/slide)
- **Language:** English (natural phrasing — not mechanical translation from Japanese)
- **Reference plan:** `slides/SLIDE-PLAN-EN.md` (486 lines, slide specifications)
- **Reference implementation:** `slides/spec-kit-presentation.md` (Japanese, 2,565 lines, ~132 slides)
- **Theme CSS:** `slides/themes/github-dark.css` (313 lines)

---

## 🔧 Build & Preview

```bash
# Preview in browser (live reload)
npx @marp-team/marp-cli --theme slides/themes/github-dark.css \
  slides/spec-kit-presentation-en.md --preview

# Export to HTML
npx @marp-team/marp-cli --theme slides/themes/github-dark.css \
  slides/spec-kit-presentation-en.md -o slides/spec-kit-presentation-en.html

# Export to PDF
npx @marp-team/marp-cli --theme slides/themes/github-dark.css \
  slides/spec-kit-presentation-en.md --pdf -o slides/spec-kit-presentation-en.pdf
```

---

## 📋 Marp Front-Matter (EXACT — copy verbatim)

```yaml
---
marp: true
theme: github-dark
paginate: true
header: "Introduction to SDD — GitHub Spec Kit"
footer: "Shinya Yanagihara, Developer Global BlackBelt, Microsoft Corporation"
---
```

---

## 📐 File Assembly Order

The presentation file is assembled in this exact order:

```
1. Front-matter YAML block (lines 1–7)
2. Chapter 0: Title slide (0-1) + content slides (0-2 through 0-5)     [5 slides]
3. Chapter 1: Section divider + content slides (1-1 through 1-51)      [1 + 51 = 52 blocks]
4. Chapter 2: Section divider + content slides (2-1 through 2-18)      [1 + 18 = 19 blocks]
5. Chapter 3: Section divider + content slides (3-1 through 3-16)      [1 + 16 = 17 blocks]
6. Chapter 4: Section divider + content slides (4-1 through 4-16)      [1 + 16 = 17 blocks]
7. Chapter 5: Section divider + content slides (5-1 through 5-18)      [1 + 18 = 19 blocks]
8. Chapter 6: Section divider + content slides (6-1 through 6-7)       [1 + 7 = 8 blocks]
─────────────────────────────────────────────────────────────────────────
Total: 1 (front-matter) + 5 + 52 + 19 + 17 + 17 + 19 + 8 = 138 blocks
Total `---` separators: 138
```

**Note:** Chapter 0 does NOT have a separate section divider — slide 0-1 (the title slide) serves as both the title and the chapter opener via `section:first-of-type` CSS. Chapters 1–6 each have an explicit section divider slide before their numbered content slides.

---

## 🏗️ Slide Structure Patterns

### Pattern 1: Title Slide (Chapter 0, slide 0-1 only)

```markdown
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Main Title

## Subtitle

Presenter info — Year
```

- CSS: `section:first-of-type` → centered, large h1 (2.4em), subtitle below
- ONLY used for the very first slide

### Pattern 2: Section Divider (first slide of each chapter)

```markdown
<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter N: Chapter Title
```

- CSS: `section:has(> h1:only-child)` → centered, large h1 (2.2em), green underline
- **MUST have h1 as the ONLY child element** (no bullets, no paragraphs, no h2)
- No `## Section` subtitle — just the bare `# Title`

### Pattern 3: Standard Content Slide

```markdown
## Section X.Y: Section Name

# Slide Title

Body content: bullets, tables, code blocks, blockquotes
```

- CSS: h2 (green, 0.85em, order: -1 renders above h1) + h1 (white, 1.6em)
- h2 acts as a "section label" — always `## Section X.Y: Topic Name`
- h1 is the main slide title
- Body follows h1

### Pattern 4: Subsection / Multi-heading Content Slide

```markdown
## Section X.Y: Section Name

# Slide Title

### Sub-point 1
Text or bullets

### Sub-point 2
Text or bullets
```

- h3 (white, 1.0em, bold 600) for sub-sections within a slide

### ⚠️ IMPORTANT: h2 Section Label Convention Differs by Chapter

| Chapter | h2 Format | Example |
|---|---|---|
| **Chapter 0** | `## Chapter 0` | `## Chapter 0` (all slides) |
| **Chapter 1** | `## Section X.Y: Short Name` | `## Section 1.2: SDD Principles & the 6 Phases` |
| **Chapters 2–5** | `## Section X.Y: Short Name` | `## Section 3.2: ShortLink Walkthrough` |
| **Chapter 6** | `## Chapter 6` | `## Chapter 6` (all slides) |

- **Chapters 0 and 6** use simple `## Chapter N` — no section subdivision
- **Chapters 1–5** use `## Section X.Y: Name` — with section numbers
- Within a section, the h2 label can be **shortened** to a more specific name (e.g., `## Section 1.2: Phase 1` instead of the full section title). This is OK and matches JP precedent.
- The JP presentation uses this variation within Section 1.2 where individual phase slides have `## Section 1.2: Phase N` labels

---

## 🎨 Content Density Rules (STRICT)

| Rule | Limit |
|---|---|
| **1 slide = 1 message** | Never cram 2+ concepts into 1 slide |
| **Bullet points** | Max **5 items** per slide |
| **Tables** | Max **6 rows × 4 columns** |
| **Code blocks** | Max **10 lines** |
| **Font size** | Keep CSS default (22px) — never use `<!-- style -->` to shrink |
| **Nested bullets** | Max 1 level of nesting |

### Slide Length Target

- **Target:** 15–25 lines per slide (including blank lines)
- **Average:** ~19 lines per slide (based on JP presentation: 2,565 lines / 132 slides)
- **Minimum:** 6 lines (section dividers)
- **Maximum:** 30 lines (dense table/code slides — rare)

### Blockquote Usage

- **~72% of slides should have at least one blockquote** (JP precedent: 95/132 slides)
- Use blockquotes for **key messages, takeaways, and "aha moments"**
- Place blockquotes **at the bottom** of the slide as the closing punch
- Format: `> **Bold key message.**` (bold within blockquote for emphasis)
- Maximum 2 blockquotes per slide (e.g., opening definition + closing insight)

---

## 🖋️ Typography & Formatting

### Heading Rules
- **h1** (`#`): Main slide title — white, bold, green underline
- **h2** (`##`): Section label — green, light weight, rendered ABOVE h1 via CSS `order: -1`
- **h3** (`###`): Sub-section within a slide — white, semi-bold

### Text Formatting
- **Bold** (`**text**`): White color, weight 600 — use for key terms
- *Italic* (`*text*`): Muted gray — use sparingly
- `Code` (`` `text` ``): Code background, monospace — use for commands, file names, variables
- **Blockquotes** (`>`): Green left-border, green-tinted background — use for key messages

### Emoji Usage
- Use sparingly — only where the JP presentation uses them
- Section labels and slide titles: avoid emoji in h1/h2
- Bullet items: emoji as prefix icon is OK (e.g., 🔓, 🐛, 🏗️, 🔍)

---

## 📐 Marp Directives Reference

| Directive | Usage |
|---|---|
| `<!-- _paginate: false -->` | Hide page number (section dividers, title, thank-you) |
| `<!-- _header: "" -->` | Hide header (section dividers, title, thank-you) |
| `<!-- _footer: "" -->` | Hide footer (title slide only) |
| `<!-- _footer: "custom" -->` | Override footer (thank-you slide: "Stop vibe coding...") |

- Place directives **before** the slide content (after `---`)
- Multiple directives on separate lines

---

## 🔗 Cross-Reference Convention

When creating slides, reference these source materials:
- **EN Plan:** `slides/SLIDE-PLAN-EN.md` — line numbers for each slide's specification
- **JP Presentation:** `slides/spec-kit-presentation.md` — line numbers for implementation reference
- **Scenarios:** `scenarios/[A-R]-*.md` — for scenario-specific content
- **CSS Theme:** `slides/themes/github-dark.css` — for styling reference

---

## ✅ Per-Slide Quality Checklist

For EVERY slide, verify:
1. [ ] h2 section label is correct (`## Section X.Y: Name`)
2. [ ] h1 title matches the plan
3. [ ] Content does not exceed density limits (5 bullets, 6×4 table, 10-line code)
4. [ ] Marp directives are correct (paginate, header, footer)
5. [ ] Slide separator `---` appears before each slide
6. [ ] No Japanese text remains
7. [ ] Natural English phrasing (not translated Japanese)
8. [ ] Bold/italic/code formatting follows conventions
9. [ ] Slide delivers exactly 1 message

---

## 📊 Chapter Slide Counts (for verification)

| Chapter | Slides | Slide Numbers |
|---|---|---|
| Chapter 0 | 5 | 0-1 through 0-5 |
| Chapter 1 | 51 | 1-1 through 1-51 |
| Chapter 2 | 18 | 2-1 through 2-18 |
| Chapter 3 | 16 | 3-1 through 3-16 |
| Chapter 4 | 16 | 4-1 through 4-16 |
| Chapter 5 | 18 | 5-1 through 5-18 |
| Chapter 6 | 7 | 6-1 through 6-7 |
| **Total** | **131** | |

---

## 🚫 Anti-Patterns (DO NOT DO)

1. **No `<style>` tags** — all styling is in the CSS theme
2. **No font-size overrides** — keep 22px base
3. **No HTML tags** — pure Markdown only (exception: Marp directives `<!-- -->`)
4. **No image references** unless explicitly in the plan (only QR.png for 0-5 and 6-7)
5. **No links rendered as clickable** — use backtick code formatting for URLs
6. **No `#` heading on section divider slides** with additional content — h1 must be the ONLY element
7. **No combining two plan slides into one** — each slide number = one `---` block
8. **No empty slides** — every `---` block must have content
9. **No `## Section` label on section divider slides** — section dividers are bare `# Title` only

---

## 🌐 Theme Adaptation for English

### Font Stack Change

The CSS theme (`github-dark.css`) currently has:
```css
--font-body: "Mona Sans", "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
```

For the English version, consider creating a modified theme OR documenting that:
- **Keep:** `"Mona Sans"` as primary font
- **Remove:** `"Noto Sans JP"`, `"Hiragino Kaku Gothic ProN"`, `"Meiryo"` (Japanese-only fonts)
- **Fallback:** system `sans-serif`
- **Decision:** Either modify the CSS file or accept the Japanese font fallbacks (they'll be ignored on systems without them — no visual impact)

**Recommendation:** Leave the CSS as-is for now. Japanese fonts are fallbacks that won't be loaded on English-only systems. If needed, create a `github-dark-en.css` variant later.

### Text Considerations

- English text is typically **more compact** than Japanese — slides may have more whitespace
- Adjust content to fill slides naturally (add an extra example or elaboration if needed)
- Avoid overly terse bullet points — use natural English sentence fragments
- Article usage: include "the", "a", "an" naturally (don't omit for brevity like Japanese does)

---

## 📝 Slide Comment Convention (Optional)

For maintainability, add HTML comments with slide numbers at the start of each slide:

```markdown
---

<!-- Slide 1-7 -->
## Section 1.2: SDD Principles & the 6 Phases

# What Is Spec-Driven Development?
...
```

This helps with:
- Quickly finding slides by number
- Verifying slide count
- Cross-referencing with SLIDE-PLAN-EN.md

**Convention:** `<!-- Slide {chapter}-{number} -->` immediately after `---`
