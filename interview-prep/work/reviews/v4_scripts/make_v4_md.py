"""Write work/reviews/V4_print_proof.md from v4_numbers.json (v4_proof.py) and v4_notes.json (my page notes).

Usage: python -I make_v4_md.py <v4_numbers.json> <v4_notes.json> <head.md> <out.md>
v4_notes.json: {"<doc>": {"title": "...", "summary": "...", "pages": {"1": ["colour note", "grey note"], ...}}}
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
nums = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
notes = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
head = Path(sys.argv[3]).read_text(encoding="utf-8")
out = [head.rstrip(), ""]

out += ["## Summary", "", "| Document | File (modified) | Pages | Page size | Smallest text | Fonts embedded | Nearest text to an edge | Smallest image resolution |",
        "|---|---|---|---|---|---|---|---|"]
for key, d in nums.items():
    imgs = [p["min_image"][0] for p in d["page_detail"] if p["min_image"]]
    size = d["page_detail"][0]["size_in"]
    out.append(f"| {notes[key]['title']} | `{d['pdf']}` ({d['modified']}) | {d['pages']} | {size[0]} × {size[1]} in | "
               f"{d['min_pt_doc']} pt | {len(d['fonts'])} of {len(d['fonts'])}"
               f"{'' if not d['not_embedded'] else ' (NOT: ' + ', '.join(d['not_embedded']) + ')'} | "
               f"{d.get('edge_in', '')} in | {str(min(imgs)) + ' ppi' if imgs else 'no raster images'} |")
out.append("")

for key, d in nums.items():
    n = notes[key]
    out += [f"## {n['title']}", "", n["summary"], "",
            "| Page | Smallest text | Color | Grayscale |", "|---|---|---|---|"]
    for p in d["page_detail"]:
        c, g = n["pages"].get(str(p["page"]), ["", ""])
        out.append(f"| {p['page']} | {p['min_pt']} pt | {c} | {g} |")
    out.append("")

Path(sys.argv[4]).write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", sys.argv[4], len(out), "lines")
