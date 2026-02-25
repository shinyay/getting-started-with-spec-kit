#!/usr/bin/env python3
"""
Marp slide overflow detection script

Estimates content height from CSS theme values and reports
slides whose content may not fit within a single slide.

Usage:
  python3 .github/skills/marp-overflow-detection/check-overflow.py slides/<deck>.md
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ── Marp / Theme Constants ──────────────────────────────────────────
SLIDE_HEIGHT = 720  # default 16:9
PADDING_TOP = 40
PADDING_BOTTOM = 40
HEADER_FOOTER_HEIGHT = 22  # header + footer area (font-size 0.55em ≒ 14px + padding)
USABLE_HEIGHT = SLIDE_HEIGHT - PADDING_TOP - PADDING_BOTTOM - HEADER_FOOTER_HEIGHT

FONT_SIZE = 22  # section { font-size: 22px }
LINE_HEIGHT = 1.5  # section { line-height: 1.5 }
BASE_LINE = FONT_SIZE * LINE_HEIGHT  # ≈ 41.6px


@dataclass
class SlideMetrics:
    """Estimated height metrics for a single slide"""

    slide_number: int
    start_line: int
    estimated_height: float
    available_height: float
    overflow: float  # positive = overflow
    title: str = ""
    breakdown: list = field(default_factory=list)

    @property
    def is_overflow(self) -> bool:
        return self.overflow > 0

    @property
    def severity(self) -> str:
        if self.overflow <= 0:
            return "OK"
        ratio = self.overflow / self.available_height
        if ratio < 0.05:
            return "WARNING"  # < 5%: marginal
        elif ratio < 0.20:
            return "OVERFLOW"  # 5-20%: overflows
        else:
            return "CRITICAL"  # >= 20%: significantly overflows


def _estimate_heading_height(level: int) -> float:
    """Estimate the height of a heading element"""
    sizes = {
        1: FONT_SIZE * 1.6,  # h1: 1.6em
        2: FONT_SIZE * 0.85,  # h2: 0.85em
        3: FONT_SIZE * 1.0,  # h3: 1.0em
    }
    fs = sizes.get(level, FONT_SIZE)
    h = fs * LINE_HEIGHT
    if level == 1:
        # border-bottom + padding-bottom
        h += 3 + FONT_SIZE * 0.2
    if level == 3:
        h += FONT_SIZE * 0.3 + FONT_SIZE * 0.15  # margin top/bottom
    return h


def _estimate_table_height(rows: list[str]) -> float:
    """Estimate the height of a table (header + divider + rows)"""
    data_rows = [
        r for r in rows if r.strip() and not re.match(r"^\s*\|[-:\s|]+\|\s*$", r)
    ]
    if not data_rows:
        return 0
    cell_font = FONT_SIZE * 0.88
    cell_padding = 0.4 * cell_font * 2  # top + bottom
    row_h = cell_font * LINE_HEIGHT + cell_padding

    header_rows = 1
    body_rows = max(0, len(data_rows) - 1)
    # table margin + border
    table_margin = FONT_SIZE * 0.4 * 2
    header_border = 2

    # Multi-line cells (long text) are not considered (estimation only)
    return (header_rows + body_rows) * row_h + table_margin + header_border


def _estimate_code_block_height(lines: list[str]) -> float:
    """Estimate the height of a code block"""
    code_font = FONT_SIZE * 0.80
    code_line_h = code_font * 1.4
    padding = FONT_SIZE * 0.7 * 2  # top + bottom 0.7em equivalent
    border = 2
    n_lines = len(lines)
    return n_lines * code_line_h + padding + border


def _estimate_blockquote_height(content_lines: int) -> float:
    """Estimate the height of a blockquote"""
    padding = FONT_SIZE * 0.4 * 2  # top + bottom
    margin = FONT_SIZE * 0.3 * 2
    return content_lines * BASE_LINE + padding + margin


def _count_text_lines(text: str, slide_width: float = 1140) -> int:
    """Estimate the number of lines considering text wrapping"""
    if not text.strip():
        return 0
    # Approx. font_size * 0.5-0.7 width per character (wider for CJK)
    # Detect CJK characters and adjust width estimation
    jp_chars = len(re.findall(r"[\u3000-\u9fff\uff00-\uffef]", text))
    en_chars = len(text) - jp_chars
    char_width = FONT_SIZE * 0.55  # average width of Latin characters
    jp_char_width = FONT_SIZE * 1.0  # width of CJK characters
    total_width = en_chars * char_width + jp_chars * jp_char_width
    lines = max(1, int((total_width / slide_width) + 0.99))
    return lines


def parse_slides(content: str) -> list[tuple[int, str]]:
    """Split Markdown into individual slides, excluding front matter."""
    # Remove front matter
    content = re.sub(r"^---\n.*?\n---\n", "", content, count=1, flags=re.DOTALL)

    slides = []
    current_lines = []
    current_start = 1
    line_num = 0

    for line in content.split("\n"):
        line_num += 1
        if line.strip() == "---":
            if current_lines:
                slides.append((current_start, "\n".join(current_lines)))
            current_lines = []
            current_start = line_num + 1
        else:
            if not current_lines and not line.strip():
                current_start = line_num + 1
                continue
            current_lines.append(line)

    if current_lines:
        slides.append((current_start, "\n".join(current_lines)))

    return slides


def estimate_slide_height(slide_content: str) -> tuple[float, list[str]]:
    """Estimate the content height of a slide"""
    height = 0.0
    breakdown = []
    lines = slide_content.split("\n")

    # Remove HTML comments (Marp directives)
    lines = [l for l in lines if not re.match(r"^\s*<!--.*?-->\s*$", l)]

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty line
        if not stripped:
            # Add a small amount of inter-paragraph spacing
            height += BASE_LINE * 0.3
            i += 1
            continue

        # Heading
        heading_match = re.match(r"^(#{1,3})\s+(.+)", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            h = _estimate_heading_height(level)
            height += h
            breakdown.append(f"h{level}: {heading_match.group(2)[:30]}... → {h:.0f}px")
            i += 1
            continue

        # Code block start
        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # closing ```
            h = _estimate_code_block_height(code_lines)
            height += h
            breakdown.append(f"code block ({len(code_lines)} lines) → {h:.0f}px")
            continue

        # Table
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            h = _estimate_table_height(table_lines)
            height += h
            n_data_rows = len(
                [
                    r
                    for r in table_lines
                    if r.strip() and not re.match(r"^\s*\|[-:\s|]+\|\s*$", r.strip())
                ]
            )
            breakdown.append(f"table ({n_data_rows} rows) → {h:.0f}px")
            continue

        # Blockquote
        if stripped.startswith(">"):
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq_lines.append(lines[i])
                i += 1
            # Number of text lines inside the blockquote
            text_in_bq = "\n".join(l.lstrip(">").strip() for l in bq_lines)
            content_lines = sum(
                _count_text_lines(l) for l in text_in_bq.split("\n") if l.strip()
            )
            h = _estimate_blockquote_height(max(1, content_lines))
            height += h
            breakdown.append(f"blockquote ({len(bq_lines)} lines) → {h:.0f}px")
            continue

        # Horizontal rule (slide-internal)
        if re.match(r"^---+$", stripped) or re.match(r"^\*\*\*+$", stripped):
            h = 3 + FONT_SIZE * 0.8 * 2
            height += h
            i += 1
            continue

        # List item
        if re.match(r"^[-*+]\s", stripped) or re.match(r"^\d+\.\s", stripped):
            # List item text content
            text = re.sub(r"^[-*+\d.]+\s*", "", stripped)
            n_lines = _count_text_lines(text)
            h = n_lines * BASE_LINE + FONT_SIZE * 0.35  # li margin-bottom
            height += h
            i += 1
            continue

        # Nested list item
        if re.match(r"^  +[-*+]\s", line) or re.match(r"^  +\d+\.\s", line):
            text = re.sub(r"^[-*+\d.]+\s*", "", stripped)
            nested_font = FONT_SIZE * 0.92
            n_lines = _count_text_lines(text)
            h = n_lines * (nested_font * LINE_HEIGHT) + nested_font * 0.15
            height += h
            i += 1
            continue

        # Regular text line
        n_lines = _count_text_lines(stripped)
        h = n_lines * BASE_LINE + FONT_SIZE * 0.4  # p margin
        height += h
        i += 1

    return height, breakdown


def extract_title(slide_content: str) -> str:
    """Extract the title from a slide"""
    for line in slide_content.split("\n"):
        m = re.match(r"^#{1,3}\s+(.+)", line.strip())
        if m:
            return m.group(1).strip()
    # If no title found, use first non-empty line
    for line in slide_content.split("\n"):
        if line.strip() and not line.strip().startswith("<!--"):
            return line.strip()[:50]
    return "(empty)"


def analyze(filepath: str) -> list[SlideMetrics]:
    """Analyze a slide file and return metrics for each slide"""
    content = Path(filepath).read_text(encoding="utf-8")
    slides = parse_slides(content)

    results = []
    for idx, (start_line, slide_content) in enumerate(slides, 1):
        # Detect slides with paginate: false via Marp directives
        is_divider = bool(
            re.search(r"section:has\(> h1:only-child\)", slide_content)
        ) or (
            slide_content.strip().count("\n") < 5
            and re.match(r"^(<!--.*?-->\s*\n)*#\s+", slide_content.strip())
        )

        estimated, breakdown = estimate_slide_height(slide_content)
        available = USABLE_HEIGHT

        # Section divider slides are vertically centered, so less likely to overflow
        # Height estimation is still the same

        metrics = SlideMetrics(
            slide_number=idx,
            start_line=start_line,
            estimated_height=estimated,
            available_height=available,
            overflow=estimated - available,
            title=extract_title(slide_content),
            breakdown=breakdown,
        )
        results.append(metrics)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check-overflow.py <marp-markdown-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    results = analyze(filepath)

    overflow_slides = [r for r in results if r.is_overflow]

    print(f"\n{'=' * 70}")
    print(f" Marp Slide Overflow Detection Report")
    print(f"{'=' * 70}")
    print(f" File: {filepath}")
    print(f" Total slides: {len(results)}")
    print(
        f" Usable height: {USABLE_HEIGHT:.0f}px (slide {SLIDE_HEIGHT}px - padding {PADDING_TOP + PADDING_BOTTOM}px - header/footer {HEADER_FOOTER_HEIGHT}px)"
    )
    print(f" Overflow detected: {len(overflow_slides)} slide(s)")
    print(f"{'=' * 70}\n")

    if not overflow_slides:
        print(" ✅ All slides fit within boundaries.\n")
        return

    for r in sorted(overflow_slides, key=lambda x: -x.overflow):
        icon = {"WARNING": "⚠️", "OVERFLOW": "🔴", "CRITICAL": "🚨"}.get(
            r.severity, "❓"
        )
        print(f" {icon} Slide #{r.slide_number} (line {r.start_line}) [{r.severity}]")
        print(f"    Title: {r.title}")
        print(
            f"    Est. height: {r.estimated_height:.0f}px / {r.available_height:.0f}px "
            f"(+{r.overflow:.0f}px, {r.overflow / r.available_height * 100:.0f}% over)"
        )
        if r.breakdown:
            print(f"    Breakdown:")
            for item in r.breakdown:
                print(f"      - {item}")
        print()

    # Summary table
    print(f"\n{'─' * 70}")
    print(f" Summary by severity")
    print(f"{'─' * 70}")
    for severity in ["CRITICAL", "OVERFLOW", "WARNING"]:
        count = sum(1 for r in overflow_slides if r.severity == severity)
        if count > 0:
            print(f"  {severity:10s}: {count} slide(s)")
    print()


if __name__ == "__main__":
    main()
