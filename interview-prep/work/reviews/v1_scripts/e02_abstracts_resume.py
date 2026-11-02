"""Effect sizes from OpenAlex / Crossref abstracts (untrusted data), and the resume text (local only, never sent anywhere)."""
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')
import fitz
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
BASE = REPO + r"\interview-prep\work\reviews\v1_sources"
for d in sorted(os.listdir(BASE)):
    if d.startswith("openalex_"):
        j = json.load(open(os.path.join(BASE, d, "work.json"), encoding="utf-8"))
        inv = j.get("abstract_inverted_index") or {}
        words = sorted(((p, w) for w, ps in inv.items() for p in ps))
        ab = " ".join(w for _, w in words)
        hits = re.findall(r"[^.]*?\b(?:r|rs)\s*=\s*[-−–]?\.?\d[^.]*\.", ab) or re.findall(r"[^.]*[-−–]?\.\d\d[^.]*\.", ab)
        print(d, "|", j.get("publication_year"), "|", (j.get("title") or "")[:80]); print("   ", " || ".join(h.strip() for h in hits)[:700])
j = json.load(open(os.path.join(BASE, "crossref_10_1038_s41598-024-58408-w", "meta.json"), encoding="utf-8"))["message"]
ab = re.sub(r"<[^>]+>", " ", j.get("abstract", "")); ab = re.sub(r"\s+", " ", ab)
print("Bosshard & Gomez 2024 effect sizes:", re.findall(r"[^.]*\b[dg]\s*=\s*[^.]*\.", ab)[:4])
print("\n===== RESUME (local) =====")
doc = fitz.open(REPO + r"\Saketh_Bollina_Resume.pdf")
for p in doc:
    print(p.get_text("text"))
