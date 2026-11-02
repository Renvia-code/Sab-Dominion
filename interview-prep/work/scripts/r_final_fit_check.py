"""Fit check for R_company_glossary.md: print-text size of sections 1 and 2, word count of the section 3 answer.

Strips [source tags], markdown emphasis and list markers, then counts characters and estimates printed lines at
a given characters-per-line width (default 100, roughly 10.5 pt on a 7.3-inch measure).
Usage: python -I r_final_fit_check.py <md> [chars_per_line]
"""
import math
import re
import sys


def section(text: str, start: str, end: str) -> str:
    a = text.index(start)
    b = text.index(end, a + len(start))
    return text[a:b]


def clean_lines(block: str) -> list[str]:
    """Join wrapped source lines into printed items, then strip tags and markup."""
    items: list[str] = []
    for raw in block.splitlines()[1:]:
        if not raw.strip():
            continue
        starts_item = bool(re.match(r"^\s*(?:[-*]\s|\d+\.\s|\*\*)", raw))
        if starts_item or not items:
            items.append(raw.strip())
        else:
            items[-1] += " " + raw.strip()
    out = []
    for item in items:
        item = re.sub(r"\[(?:R-|C-|docs|brief|README|peer set|co-ops|you:)[^\]]*\]", "", item)
        item = re.sub(r"\*\*|\*|`", "", item)
        item = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", item)
        item = re.sub(r"\s+", " ", item).strip()
        if item:
            out.append(item)
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    cpl = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    text = open(path, encoding="utf-8").read()
    for name, start, end in [("box", "## 1.", "## 2."), ("glossary", "## 2.", "## 3.")]:
        lines = clean_lines(section(text, start, end))
        # join wrapped source lines back into logical items (an item starts with a bold term in the source)
        chars = sum(len(x) for x in lines)
        est = sum(math.ceil(len(x) / cpl) for x in lines)
        print(f"{name}: {chars} characters of print text; about {est} printed lines at {cpl} chars/line")
    answer = section(text, "## 3.", "Sources:")
    quote = " ".join(l.lstrip("> ").strip() for l in answer.splitlines() if l.startswith(">"))
    quote = re.sub(r"\[you:[^\]]*\]", "", quote)
    words = re.findall(r"[A-Za-z0-9.,'’-]+", quote)
    print(f"45-second answer: {len(words)} words before the [you: …] line; at 150 wpm = {len(words) / 2.5:.0f} s")


if __name__ == "__main__":
    main()
