---
name: marp-slide-fix
description: >
  Systematically fix Marp slide overflow (content exceeding slide boundaries).
  Uses a two-phase approach — CSS theme optimization followed by per-slide content fixes —
  to fit all slides within the specified height.
  Use this skill when asked to fix Marp slide overflow, adjust slide layout,
  compress slide content, or resolve layout issues detected by marp-overflow-detection.
---

# Marp Slide Overflow Fix

## Overview

A methodology for systematically fixing overflows detected by the `marp-overflow-detection` skill.
Uses a two-phase approach (CSS theme optimization → per-slide content fixes) to resolve overflows efficiently with minimal changes.

## Prerequisites

- Overflow detection by the `marp-overflow-detection` skill must be complete.
- The detection report must provide each slide's overflow amount (px) and element breakdown.

## Fix workflow

```
① Overflow detection (marp-overflow-detection)
    ↓
② Phase 1: CSS theme optimization (affects all slides)
    ↓
③ Re-detect → confirm remaining overflows
    ↓
④ Phase 2: Per-slide content fixes (remaining slides only)
    ↓
⑤ Final detection → confirm zero overflows
```

## Phase 1: CSS theme optimization

### Purpose

CSS property adjustments **affect all slides in a single change**, so they are applied first.
When many slides overflow, the majority can be resolved in this phase.

### Adjustable properties and priority

| Priority | Property | Impact | Visual effect |
|----------|----------|--------|---------------|
| 1 | `padding` | ◎ Large (doubled effect for top + bottom) | Small |
| 2 | `font-size` | ◎ Large (cascades to all elements) | Moderate |
| 3 | `line-height` | ○ Moderate | Small |
| 4 | `h1` / `h3` size & margin | ○ Moderate | Small |
| 5 | Table cell padding | ○ Proportional to row count | Small |
| 6 | Code block padding & font-size | △ Small | Small |
| 7 | blockquote padding & margin | △ Small | Small |

### CSS adjustment guidelines

- **font-size**: 26px → 22px is the readability limit. Avoid going below 20px.
- **padding**: top/bottom 60px → 40px is reasonable. Below 30px looks cramped.
- **line-height**: 1.6 → 1.5 is the limit. Below 1.4 becomes hard to read.
- **h1**: 1.9em → 1.6em range. Preserve the title's visual prominence.
- **Table**: reduce cell padding from 0.55em → 0.4em. Going smaller hurts readability.

### Important: Sync with detection script

After changing CSS, update the constants at the top of `.github/skills/marp-overflow-detection/check-overflow.py` to match.

```python
# .github/skills/marp-overflow-detection/check-overflow.py constants (must match CSS)
PADDING_TOP = 40      # CSS: padding-top
PADDING_BOTTOM = 40   # CSS: padding-bottom
FONT_SIZE = 22        # CSS: font-size (section)
LINE_HEIGHT = 1.5     # CSS: line-height (section)
```

## Phase 2: Per-slide content fixes

### Fix techniques

Apply techniques proportional to the overflow amount for slides that remain after Phase 1.

#### Technique 1: Compress blockquotes (saves ~33px/line)

Merge a two-line blockquote into a single line.

**Before:**
```markdown
> First line of text.
> Second line of text.
```

**After:**
```markdown
> First line of text. Second line of text.
```

#### Technique 2: Remove blockquotes (saves ~64px)

Remove blockquotes that serve as conclusions or supplementary notes.
Effective when the information can be inferred from headings or tables.

#### Technique 3: Reduce table rows (saves ~46px/row)

- Remove low-priority rows
- Merge multiple rows into one (`ColA / ColB / ColC` format)
- Consolidate rows with empty cells into a single summary row

**Before:**
```markdown
| | Webhook signature verification |
| | PCI compliance |
| | Audit logging |
```

**After:**
```markdown
| — | +Webhook verification, PCI, Audit log |
```

#### Technique 4: Shorten code blocks (saves ~25px/line)

- Remove unnecessary blank lines
- Reduce similar examples (e.g., from 3 to 2)
- Compress ASCII art lines
- Merge multiple lines into one

#### Technique 5: Merge headings (saves ~43px/h3)

Merge an h3 and the blockquote immediately following it.

**Before:**
```markdown
### Back-pressure

> Returns 429 when processing capacity is exceeded.
```

**After:**
```markdown
> **Back-pressure**: Returns 429 when processing capacity is exceeded.
```

#### Technique 6: Combine list items (saves ~33px/item)

Consolidate 3 items into 2.

**Before:**
```markdown
- Output is directly tied to security
- Blocklists are prone to gaps → use allowlists
- URL scheme restriction: https and http only
```

**After:**
```markdown
- **Output directly impacts security (XSS prevention)** — blocklists have gaps → use allowlists
- URL scheme restriction: https and http only
```

#### Technique 7: Merge consecutive blockquotes (saves ~64px/merge)

Convert multiple blockquotes separated by blank lines into consecutive `>` lines.

**Before:**
```markdown
> **P**: "Do not ship unpaid orders"

> **R**: "Do not assign to two exclusive experiments simultaneously"

> **E**: "Deleted objects must not be displayed"
```

**After:**
```markdown
> **P**: "Do not ship unpaid orders"
> **R**: "Do not assign to two exclusive experiments simultaneously"
> **E**: "Deleted objects must not be displayed"
```

#### Technique 8: Split slides (last resort)

For CRITICAL slides exceeding 20%+, split the content across two slides.
Place the split at a logical content boundary.

### Choosing fix priority

Based on the overflow amount and element breakdown, choose the minimum changes that achieve sufficient reduction.

| Overflow | Recommended technique |
|----------|----------------------|
| 1–10px | Technique 1 (blockquote merge) only |
| 10–40px | Technique 1 + Technique 4 (shorten code) |
| 40–70px | Technique 2 (remove blockquote) or Technique 5 (merge h3) |
| 70–100px | Technique 3 (reduce table rows) + Technique 2 |
| 100px+ | Technique 8 (split slide) or combine multiple techniques |

## Track record (past project results)

| Phase | Overflows | Changes |
|-------|-----------|---------|
| After detection | 103 / 114 slides | — |
| Phase 1 (CSS optimization) | 30 / 114 slides | Adjusted 9 properties: font-size, padding, line-height, etc. |
| Phase 2 (content fixes) | 0 / 114 slides | Individual fixes on 30 slides (Techniques 1–7 applied) |

## Caveats

- When fixing content, **preserving the essence of the information** takes priority. Deletions and compressions should be limited to supplementary material.
- Always sync detection script constants after CSS changes.
- Perform a final visual check in Marp Preview as well (due to heuristic limitations).
- Decide whether to remove a blockquote based on whether it is the slide's core message.
