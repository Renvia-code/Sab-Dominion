"""Power BI template: tables by partition source, DataFolder use, and report pages (PBIR layout)."""
import sys, os, json, zipfile, re
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
z = zipfile.ZipFile(os.path.join(REPO, "powerbi", "Dominion_reliability_review.pbit"))
sch = json.loads(z.read("DataModelSchema").decode("utf-16-le").lstrip("\ufeff"))
via_folder = []
for tb in sch["model"]["tables"]:
    parts = tb.get("partitions", [])
    src = parts[0]["source"] if parts else {}
    kind = src.get("type", "?")
    expr = src.get("expression", "")
    expr = "\n".join(expr) if isinstance(expr, list) else str(expr)
    uses = "DataFolder" in expr
    if uses: via_folder.append(tb["name"])
    print(f"{tb['name']:<28} source={kind:<11} DataFolder={uses} hidden={tb.get('isHidden', False)}")
print("tables:", len(sch["model"]["tables"]), "| via DataFolder:", len(via_folder))
pages = sorted({n.split("/")[3] for n in z.namelist() if n.startswith("Report/definition/pages/") and n.count("/") >= 4})
names = []
for p in pages:
    j = json.loads(z.read(f"Report/definition/pages/{p}/page.json").decode("utf-8-sig"))
    names.append(j.get("displayName"))
print("pages:", len(pages), names)
