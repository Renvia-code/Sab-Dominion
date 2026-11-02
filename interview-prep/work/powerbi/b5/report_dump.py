"""Dump the PBIR report in a .pbit extraction: pages, visuals, titles, fields, filters.
Usage: python -I report_dump.py <extracted_dir>"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "Report" / "definition"


def fields(obj, out, path=""):
    """Collect every field reference (Measure / Column / Aggregation) in a JSON tree."""
    if isinstance(obj, dict):
        for kind in ("Measure", "Column"):
            if kind in obj and isinstance(obj[kind], dict) and "Property" in obj[kind]:
                ent = obj[kind].get("Expression", {}).get("SourceRef", {}).get("Entity")
                out.append(f"{kind}:{ent}.{obj[kind]['Property']}")
        if "Aggregation" in obj and isinstance(obj["Aggregation"], dict):
            inner = obj["Aggregation"].get("Expression", {})
            col = inner.get("Column", {})
            ent = col.get("Expression", {}).get("SourceRef", {}).get("Entity")
            out.append(f"Agg{obj['Aggregation'].get('Function')}:{ent}.{col.get('Property')}")
            return
        for k, v in obj.items():
            fields(v, out, path + "/" + k)
    elif isinstance(obj, list):
        for v in obj:
            fields(v, out, path)


def literal_texts(obj, out):
    if isinstance(obj, dict):
        if "Literal" in obj and isinstance(obj["Literal"], dict):
            out.append(obj["Literal"].get("Value"))
        for v in obj.values():
            literal_texts(v, out)
    elif isinstance(obj, list):
        for v in obj:
            literal_texts(v, out)


print("report.json:", json.dumps(json.loads((root / "report.json").read_text(encoding="utf-8")))[:900])
print("pages.json:", (root / "pages" / "pages.json").read_text(encoding="utf-8"))
for pdir in sorted((root / "pages").iterdir()):
    if not pdir.is_dir():
        continue
    page = json.loads((pdir / "page.json").read_text(encoding="utf-8"))
    pf = []
    fields(page.get("filterConfig", {}), pf)
    print(f"\n=== PAGE {pdir.name} '{page.get('displayName')}' {page.get('width')}x{page.get('height')} filters={pf}")
    lits = []
    literal_texts(page.get("filterConfig", {}), lits)
    if lits:
        print("    page filter literals:", lits)
    for vdir in sorted((pdir / "visuals").iterdir()):
        v = json.loads((vdir / "visual.json").read_text(encoding="utf-8"))
        vis = v.get("visual", {})
        pos = v.get("position", {})
        vtype = vis.get("visualType")
        f = []
        fields(vis.get("query", {}), f)
        lit = []
        literal_texts(vis.get("visualContainerObjects", {}), lit)
        objs = []
        literal_texts(vis.get("objects", {}), objs)
        ff = []
        fields(v.get("filterConfig", {}), ff)
        print(f"  [{vdir.name}] {vtype} pos=({pos.get('x'):.0f},{pos.get('y'):.0f},{pos.get('width'):.0f},{pos.get('height'):.0f}) z={pos.get('z')}")
        if f:
            print("      fields:", f)
        if lit:
            print("      container literals:", [str(x)[:160] for x in lit])
        if objs:
            print("      object literals:", [str(x)[:120] for x in objs][:30])
        if ff:
            print("      visual filters:", ff)
        if vtype == "textbox":
            paras = vis.get("objects", {}).get("general", [{}])[0].get("properties", {}).get("paragraphs", [])
            txt = " / ".join("".join(r.get("value", "") for r in p.get("textRuns", [])) for p in paras)
            print("      text:", txt[:300])
