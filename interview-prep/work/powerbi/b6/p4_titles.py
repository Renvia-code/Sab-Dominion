"""List the on-screen text of the Power BI template, page by page, with the fields behind each
visual, and flag text that may break the deck's rules.

Usage: python -I p4_titles.py <template.pbit> <out.md>

Lists page names, titles, subtitles, text boxes, card labels, reference-line labels, axis titles,
and the text that text-returning measures put on cards. Flags (for review, not auto-fixes):
  causal       wording that reads as cause (because, caused, due to, drives, explains, ...)
  eaglei       a visual on EAGLE-I tables whose title and subtitle do not say "all utilities"
  storms       pre-D22 storm counts (465, 796, 723, 851, ...) or counts other than 464/791 for 2024/2025
  reconcile    a reconciliation count other than "12 of 12"
  winter       winter-peak years other than 2019, 2022 and 2025
  hours        "night"/"afternoon" growth wording instead of single hours or hours ending 1-5 a.m.
  uk           UK spelling or day-month date
"""
import json
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

EAGLEI = {"COUNTY_OUTAGE_MAP", "OUTAGE_EVENTS_TOP10", "RESTORATION_CURVE"}
CAUSAL = re.compile(r"\b(because|caus\w*|due to|drive[sn]?|driving|driven by|led to|leads? to|"
                    r"result(s|ed)? (in|from)|as a result|explain\w*|impact\w*|effect of|thanks to|"
                    r"is data cent\w*|attribut\w*)\b", re.I)
PRE_D22 = re.compile(r"(?<![\d,.])(465|796|723|851|526|597|420|687|431|676|391)(?![\d,])")
UK = re.compile(r"\b(programmes?|colour\w*|centres?|analys(e|ed|es|ing)|labell(ed|ing)|modell(ed|ing)|"
                r"organis\w*|behaviour\w*|normalis\w*|optimis\w*|summaris\w*|grey|"
                r"\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*( \d{4})?)\b")


def lit(v):
    """Literal value of a PBIR expression, quotes stripped."""
    try:
        s = v["expr"]["Literal"]["Value"]
    except (KeyError, TypeError):
        return None
    return s[1:-1].replace("''", "'") if s.startswith("'") and s.endswith("'") else s


def prop(objs, key, name):
    out = []
    for o in (objs or {}).get(key, []) or []:
        t = lit((o.get("properties") or {}).get(name))
        if t:
            out.append(t)
    return out


def field_name(f):
    for kind in ("Measure", "Column"):
        if kind in f:
            return f"{f[kind]['Expression']['SourceRef'].get('Entity')}[{f[kind]['Property']}]", kind
    if "Aggregation" in f:
        inner, _ = field_name(f["Aggregation"]["Expression"])
        return f"agg({inner})", "Aggregation"
    if "HierarchyLevel" in f:
        h = f["HierarchyLevel"]["Expression"]["Hierarchy"]
        return f"{h['Expression']['SourceRef'].get('Entity')}[{h['Hierarchy']}]", "Hierarchy"
    return json.dumps(f)[:60], "?"


def flags(text, tables, title_sub):
    fl = []
    if CAUSAL.search(text):
        fl.append("causal?")
    if tables & EAGLEI and "all utilities" not in title_sub.lower():
        fl.append("eaglei: no 'all utilities'")
    if PRE_D22.search(text) and re.search(r"storm", text, re.I):
        fl.append("storms: pre-D22 count?")
    m = re.search(r"(\d+) of (\d+)", text)
    if m and re.search(r"reconcil|match|published", text, re.I) and m.group(0) != "12 of 12":
        fl.append("reconcile: not 12 of 12")
    if re.search(r"winter", text, re.I) and re.search(r"20\d\d", text):
        yrs = re.findall(r"20\d\d", text)
        if "2019" not in yrs or "2022" not in yrs or "2025" not in yrs:
            fl.append("winter years?")
    if re.search(r"\bnight\b|\bafternoon\b", text, re.I) and "%" in text:
        fl.append("hours wording?")
    if UK.search(text):
        fl.append("uk")
    return fl


def main(pbit, out):
    z = zipfile.ZipFile(pbit)
    raw = z.read("DataModelSchema")
    model = json.loads(raw.decode("utf-16-le" if raw[:2] == b"\xff\xfe" or raw[1:2] == b"\x00" else "utf-8").lstrip("\ufeff"))
    measures = {}
    for t in model["model"]["tables"]:
        for m in t.get("measures", []) or []:
            e = m["expression"]
            measures[f"{t['name']}[{m['name']}]"] = "\n".join(e) if isinstance(e, list) else e
    order = json.loads(z.read("Report/definition/pages/pages.json").decode("utf-8"))["pageOrder"]
    lines, nflag = [], 0
    for n, pid in enumerate(order, 1):
        page = json.loads(z.read(f"Report/definition/pages/{pid}/page.json").decode("utf-8"))
        pname = page.get("displayName", pid)
        pf = flags(pname, set(), "")
        lines.append(f"\n### Page {n}: {pname}" + (f"  **[{'; '.join(pf)}]**" if pf else ""))
        lines.append("")
        lines.append("| Visual | Text on screen | Behind it | Flags |")
        lines.append("|---|---|---|---|")
        vis = []
        for name in z.namelist():
            if name.startswith(f"Report/definition/pages/{pid}/visuals/") and name.endswith("/visual.json"):
                v = json.loads(z.read(name).decode("utf-8"))
                vis.append(v)
        vis.sort(key=lambda v: (round(v["position"]["y"] / 40), v["position"]["x"]))
        for v in vis:
            vv = v.get("visual", {})
            vt = vv.get("visualType", "?")
            vco, obj = vv.get("visualContainerObjects", {}), vv.get("objects", {})
            texts = []
            for t in prop(vco, "title", "text"):
                texts.append(("title", t))
            for t in prop(vco, "subTitle", "text"):
                texts.append(("subtitle", t))
            for g in (obj or {}).get("general", []) or []:
                for para in (g.get("properties") or {}).get("paragraphs", []) or []:
                    s = "".join(r.get("value", "") for r in para.get("textRuns", []))
                    if s.strip():
                        texts.append(("text box", s))
            for key in ("y1AxisReferenceLine", "xAxisReferenceLine", "referenceLine"):
                for o in (obj or {}).get(key, []) or []:
                    p = o.get("properties") or {}
                    if lit(p.get("show")) == "false":
                        continue
                    d = lit(p.get("displayName"))
                    if d:
                        texts.append(("reference line", d))
            for key in ("categoryAxis", "valueAxis"):
                for t in prop(obj, key, "titleText"):
                    texts.append((f"{key} title", t))
            fields, tables = [], set()
            for role, st in ((vv.get("query") or {}).get("queryState") or {}).items():
                for p in st.get("projections", []) or []:
                    fn, kind = field_name(p["field"])
                    tables.add(fn.split("[")[0].replace("agg(", ""))
                    label = p.get("displayName")
                    fields.append((role, fn, kind, label))
                    if vt in ("card", "cardVisual", "multiRowCard", "kpi") and (label or p.get("nativeQueryRef")):
                        texts.append(("card label", label or p.get("nativeQueryRef")))
                    if kind == "Measure" and vt in ("card", "cardVisual", "multiRowCard"):
                        strs = re.findall(r'"([^"]*[A-Za-z][^"]*)"', measures.get(fn, ""))
                        strs = [s for s in strs if len(s) > 3 and not re.fullmatch(r"[#0,.%]+", s)
                                and s not in ("Dominion Energy Virginia",)]
                        if strs:
                            texts.append(("card text (DAX)", " / ".join(dict.fromkeys(strs))))
            title_sub = " ".join(t for k, t in texts if k in ("title", "subtitle", "text box"))
            behind = "; ".join(dict.fromkeys(f"{fn}" for role, fn, kind, label in fields)) or "static text"
            if not texts:
                continue
            for i, (k, t) in enumerate(texts):
                fl = flags(t, tables if k in ("title", "subtitle") else set(), title_sub)
                if k == "subtitle":
                    fl = [f for f in fl if not f.startswith("eaglei")]
                nflag += bool(fl)
                cell = t.replace("|", "\\|").replace("\n", " ")
                lines.append(f"| {vt} `{v['name'][:6]}` {k} | {cell} | {behind if i == 0 else '″'} | "
                             f"{'**' + '; '.join(fl) + '**' if fl else ''} |")
    head = [f"Template: `{Path(pbit).name}` ({len(order)} pages). Flags to review: {nflag}."]
    Path(out).write_text("\n".join(head + lines) + "\n", encoding="utf-8")
    print("\n".join(head))
    for ln in lines:
        if "**" in ln.split("|")[-2] if ln.startswith("|") and ln.count("|") > 4 else False:
            print(ln)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
