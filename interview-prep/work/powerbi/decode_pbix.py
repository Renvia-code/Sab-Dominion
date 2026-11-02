"""Read-only inventory of the report layer of a .pbix in PBIR format.

Lists every page and visual: type, position, title and subtitle text, fields with their
aggregation (Sum of a raw column vs a measure), slicers, filters and alt text.
It never writes into the .pbix.

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\powerbi\\decode_pbix.py <file.pbix> <out.md>
"""
import json
import sys
import zipfile
from pathlib import Path

AGG = {0: "Sum", 1: "Avg", 2: "Count", 3: "Min", 4: "Max", 5: "CountNonNull", 6: "Median", 7: "StdDev", 8: "Var"}


def literal_text(expr):
    """Pull a text literal out of a PBIR expression (titles, subtitles, alt text)."""
    if not isinstance(expr, dict):
        return None
    e = expr.get("expr", expr)
    lit = e.get("Literal") if isinstance(e, dict) else None
    if lit and isinstance(lit.get("Value"), str):
        v = lit["Value"]
        return v[1:-1].replace("''", "'") if v.startswith("'") else v
    return None


def walk_props(obj, wanted):
    """Find properties named in `wanted` anywhere under objects/visualContainerObjects."""
    found = {}

    def rec(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in wanted and isinstance(v, dict):
                    t = literal_text(v)
                    if t is not None:
                        found.setdefault(path + "." + k, t)
                rec(v, path + "." + k if k not in ("properties",) else path)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                rec(v, path)
    rec(obj, "")
    return found


def field_desc(f):
    """Describe one projection field: Measure, Column, or Aggregation(Column)."""
    fld = f.get("field", {})
    if "Measure" in fld:
        m = fld["Measure"]
        return f"[{m['Property']}] (measure on {m['Expression']['SourceRef'].get('Entity')})", "measure"
    if "Column" in fld:
        c = fld["Column"]
        return f"{c['Expression']['SourceRef'].get('Entity')}[{c['Property']}] (column)", "column"
    if "Aggregation" in fld:
        a = fld["Aggregation"]
        inner = a["Expression"].get("Column", {})
        ent = inner.get("Expression", {}).get("SourceRef", {}).get("Entity")
        return f"{AGG.get(a.get('Function'), a.get('Function'))} of {ent}[{inner.get('Property')}]", "aggregation"
    if "HierarchyLevel" in fld:
        return "hierarchy level", "column"
    return json.dumps(fld)[:120], "other"


def main(pbix, out_md):
    z = zipfile.ZipFile(pbix)
    names = z.namelist()
    pages_meta = json.loads(z.read("Report/definition/pages/pages.json"))
    order = pages_meta.get("pageOrder", [])
    lines = [f"# Report inventory: `{Path(pbix).name}` (read-only decode)", ""]
    report = json.loads(z.read("Report/definition/report.json"))
    lines += ["## report.json", "", "```json", json.dumps(report, indent=1)[:1500], "```", ""]
    raw_aggs = []
    for pid in order:
        page = json.loads(z.read(f"Report/definition/pages/{pid}/page.json"))
        lines.append(f"## Page `{pid}`: \"{page.get('displayName')}\" ({page.get('width')}x{page.get('height')})")
        if page.get("filterConfig"):
            lines.append("")
            lines.append("Page filters: `" + json.dumps(page["filterConfig"])[:600] + "`")
        lines.append("")
        vis = sorted(n for n in names if n.startswith(f"Report/definition/pages/{pid}/visuals/") and n.endswith("visual.json"))
        rows = []
        for vn in vis:
            v = json.loads(z.read(vn))
            vid = vn.split("/")[-2]
            pos = v.get("position", {})
            visual = v.get("visual", {})
            vtype = visual.get("visualType", "?")
            vco = visual.get("visualContainerObjects", {})

            def first_prop(group, prop, src=vco):
                for entry in src.get(group, []) or []:
                    t = literal_text(entry.get("properties", {}).get(prop))
                    if t is not None:
                        return t
                return ""
            title = first_prop("title", "text")
            subtitle = first_prop("subTitle", "text")
            alt = first_prop("general", "altText")
            objs = visual.get("objects", {})
            axis_titles = [f"{g}: \"{first_prop(g, 'titleText', objs)}\"" for g in ("valueAxis", "categoryAxis")
                           if first_prop(g, "titleText", objs)]
            if axis_titles:
                subtitle = (subtitle + " | axis " if subtitle else "axis ") + "; ".join(axis_titles)
            # textbox paragraphs
            if vtype == "textbox":
                paras = []
                for p in visual.get("objects", {}).get("general", [{}])[0].get("properties", {}).get("paragraphs", []) if isinstance(visual.get("objects", {}).get("general"), list) else []:
                    for r in p.get("textRuns", []):
                        paras.append(r.get("value", ""))
                title = title or " ".join(paras)[:300]
            fields = []
            q = visual.get("query", {}).get("queryState", {})
            for role, proj in q.items():
                for f in proj.get("projections", []):
                    d, kind = field_desc(f)
                    fields.append(f"{role}: {d}")
                    if kind == "aggregation":
                        raw_aggs.append((page.get("displayName"), vid, vtype, role, d))
            filt = v.get("filterConfig")
            rows.append((vid, vtype, pos, title, subtitle, alt, fields, filt))
        for vid, vtype, pos, title, subtitle, alt, fields, filt in rows:
            lines.append(f"- **{vtype}** `{vid}` at x={pos.get('x', 0):.0f} y={pos.get('y', 0):.0f} "
                         f"w={pos.get('width', 0):.0f} h={pos.get('height', 0):.0f}")
            if title:
                lines.append(f"  - title/text: \"{title}\"")
            if subtitle:
                lines.append(f"  - subtitle: \"{subtitle}\"")
            lines.append(f"  - alt text: {('\"' + alt + '\"') if alt else 'none'}")
            for f in fields:
                lines.append(f"  - {f}")
            if filt:
                lines.append(f"  - visual filters: `{json.dumps(filt)[:300]}`")
        lines.append("")
    lines.append("## Visuals that aggregate a raw column (not a measure)")
    lines.append("")
    for r in raw_aggs:
        lines.append(f"- {r[0]} / `{r[1]}` ({r[2]}), {r[3]}: {r[4]}")
    lines.append("")
    lines.append(f"Count: {len(raw_aggs)} projections in {len(set((r[0], r[1]) for r in raw_aggs))} visuals")
    Path(out_md).write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}: {len(order)} pages, {len(raw_aggs)} raw aggregations")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
