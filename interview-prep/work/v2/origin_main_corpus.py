"""What the candidate's public repo (origin/main) says, as searchable text: the public-variant number rule.

Rule (V2 rulings, 09:15): in the public variant every project number must be findable on origin/main.
Two tiers:
  A  README, docs/, sql/, scripts/, data/output/, powerbi/ (measures.dax and the workbook's cell values)
  B  data/input/ and data/reference/ (the raw public extracts: a reported value found only here is a
     source value, e.g. EIA-861 SAIFI for one year, not an analysis result)

Usage (from the repo root):
  .venv\\Scripts\\python.exe -I interview-prep\\work\\v2\\origin_main_corpus.py 136.0 1.199 "+39"
Writes interview-prep/work/v2/origin_main_tierA.txt and _tierB.txt (cached; delete them to refresh).
"""
from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
REF = "origin/main"
TIER_A = HERE / "origin_main_tierA.txt"
TIER_B = HERE / "origin_main_tierB.txt"


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True).stdout


def build() -> None:
    files = git("ls-tree", "-r", REF, "--name-only").decode().splitlines()
    a, b = [], []
    for f in files:
        raw = git("show", f"{REF}:{f}")
        if f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True, read_only=True)
            for ws in wb.worksheets:
                lines = []
                for row in ws.iter_rows(values_only=True):
                    vals = [str(v) for v in row if v is not None]
                    if vals:
                        lines.append(" | ".join(vals))
                block = "\n".join(f"{f}[{ws.title}]:{i + 1}: {ln}" for i, ln in enumerate(lines))
                # the all-utility rows sheet is raw EIA data, not an analysis result
                (b if ws.title == "ReliabilityRows" else a).append(block)
            continue
        elif f.endswith((".svg", ".png", ".pbix", ".zip")):
            text = raw.decode("utf-8", "replace") if f.endswith(".svg") else ""
        else:
            text = raw.decode("utf-8", "replace")
        block = "\n".join(f"{f}:{i + 1}: {ln}" for i, ln in enumerate(text.splitlines()))
        (b if f.startswith(("data/input/", "data/reference/")) else a).append(block)
    TIER_A.write_text("\n".join(a), encoding="utf-8")
    TIER_B.write_text("\n".join(b), encoding="utf-8")


def load() -> tuple[str, str]:
    if not (TIER_A.exists() and TIER_B.exists()):
        build()
    return TIER_A.read_text(encoding="utf-8"), TIER_B.read_text(encoding="utf-8")


def find(needle: str, text: str, limit: int = 3) -> list[str]:
    """Lines whose content (after the 'path:line: ' prefix) holds the needle as a whole number."""
    import re
    pat = re.compile(r"(?<![\d.])" + re.escape(needle) + r"(?![\d])")
    out = []
    for ln in text.splitlines():
        content = ln.split(": ", 1)[1] if ": " in ln else ln
        if pat.search(content):
            out.append(ln[:220])
            if len(out) >= limit:
                break
    return out


def findable(token: str) -> str:
    """'A', 'B' or '' for a printed number such as '+10%', '1,320', '133.0'."""
    ta, tb = load()
    t = token.replace("−", "-").replace("+", "").rstrip("%")
    forms = {t, t.replace(",", "")}
    if "." in t:
        forms.add(t.rstrip("0").rstrip("."))
    for f in forms:
        if f and find(f, ta, 1):
            return "A"
    for f in forms:
        if f and find(f, tb, 1):
            return "B"
    return ""


if __name__ == "__main__":
    ta, tb = load()
    for n in sys.argv[1:]:
        ha = find(n, ta)
        hb = [] if ha else find(n, tb, 1)
        tag = "A" if ha else ("B" if hb else "-")
        print(f"[{tag}] {n}")
        for h in (ha or hb):
            print("      ", h)
