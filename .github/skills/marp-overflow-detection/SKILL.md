---
name: marp-overflow-detection
description: >
  Detect overflow in Marp slides — content that does not fit within a single slide, causing layout breakage.
  Parse Marp presentation files, estimate per-slide content height based on CSS theme settings,
  and identify and report slides whose content exceeds the available area.
  Use this skill when asked to check Marp slides for overflow, detect layout issues, find slides that are too long,
  or validate Marp presentation content fits within slide boundaries.
---

# Marp Slide Overflow Detection

## Overview

Parses a Marp presentation Markdown file and heuristically detects whether each slide's content fits within the slide area. Using CSS theme values such as font size, line height, and padding, it estimates the height of each element (headings, tables, code blocks, bullet lists, blockquotes, etc.) and reports any slides that exceed the available slide height.

## Usage

### 1. Running the detection script

Use the `check-overflow.py` script located in this skill's directory.

```bash
python3 .github/skills/marp-overflow-detection/check-overflow.py <marp-file-path>
```

Example:

```bash
python3 .github/skills/marp-overflow-detection/check-overflow.py slides/2026-02-20-weekly-digest-feb-13-19.md
```

### 2. Reading the output

The script outputs the following information:

- **Total slide count** and **number of overflows detected**
- Details for each overflowing slide:
  - **Slide number** and **source line number**
  - **Severity**: `WARNING` (less than 5% over), `OVERFLOW` (5–20% over), `CRITICAL` (20%+ over)
  - **Estimated height** vs **available height** (in pixels)
  - **Breakdown**: how much height each element contributes

### 3. Severity levels

| Severity | Icon | Excess | Action |
|----------|------|--------|--------|
| WARNING | ⚠️ | < 5% | Borderline. May fit after adjusting fonts or margins |
| OVERFLOW | 🔴 | 5–20% | Overflowing. Reduce content or split the slide |
| CRITICAL | 🚨 | 20%+ | Significantly overflowing. Splitting the slide is required |

## Remediation strategies

Recommended approaches when overflow is detected:

1. **Split the slide**: If there is too much content, divide it across multiple slides
2. **Reduce table rows**: Split large tables across slides or select only the most important rows
3. **Shorten code blocks**: Keep only the essential lines in long code blocks
4. **Condense blockquotes**: Summarize lengthy quotations
5. **Adjust CSS theme**: Reduce `font-size`, adjust `padding`, or change `line-height`

## Detection parameters

The script uses the following CSS theme constants (based on the `github-dark` theme):

- Slide height: 720px (16:9)
- Padding: 40px top and bottom
- Header / footer: 22px
- **Available height: 618px**
- Base font size: 22px
- Line height: 1.5

If you use a different theme, adjust the constants at the top of the script.

## Caveats

- This script is heuristic-based (estimation) and is not 100% accurate
- Image heights are not accounted for (because Marp's automatic image resizing behavior is complex)
- Per-slide style overrides via CSS `scoped` directives (`<!-- _class: ... -->`) are not considered
- Always verify the final rendering result using Marp Preview
