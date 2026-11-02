"""Final-pack audit, step 0: freeze copies of the inputs (read-only on the originals), hash them, and print
the ten C-F rows with every register row they cite. Writes only under work/reviews/snapshot_final_audit and v1_work."""
import sys, os, re, csv, shutil, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
IP = REPO + r"\interview-prep"
SNAP = IP + r"\work\reviews\snapshot_final_audit"
os.makedirs(SNAP, exist_ok=True)
SRC = [r"claims.csv", r"research\claims_register.csv", r"work\v6_inputs\R_company_glossary.md", r"work\v6_inputs\D_facts.md",
       r"deliverables\03_interview_brief\Dominion_interview_brief.pdf", r"deliverables\03_interview_brief\Dominion_interview_brief.html",
       r"deliverables\02_question_sheet\Dominion_question_sheet.pdf", r"deliverables\02_question_sheet\Dominion_question_sheet.html",
       r"deliverables\01_deck\Dominion_reliability_deck_adopted_print_letter.pdf", r"deliverables\01_deck\Dominion_reliability_deck_public_print_letter.pdf",
       r"deliverables\01_deck\Dominion_reliability_deck_adopted.pptx", r"deliverables\01_deck\Dominion_reliability_deck_public.pptx"]
lines = []
for s in SRC:
    p = os.path.join(IP, s)
    dst = os.path.join(SNAP, os.path.basename(s))
    shutil.copy2(p, dst)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    lines.append(f"{h} *{s}")
lines.append(datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
open(os.path.join(SNAP, "_sha256.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
IDS = "C-F-01 C-F-02 C-F-03 C-F-04 C-F-06 C-F-07 C-F-08 C-F-09 C-F-10 C-F-12".split()
claims = list(csv.DictReader(open(os.path.join(SNAP, "claims.csv"), encoding="utf-8")))
reg = {r["id"]: r for r in csv.DictReader(open(os.path.join(SNAP, "claims_register.csv"), encoding="utf-8"))}
print("\nclaims rows:", len(claims), "| register rows:", len(reg), "| C-F rows present:", [c["id"] for c in claims if c["id"].startswith("C-F")])
cited = []
for c in claims:
    if c["id"] in IDS:
        print("=" * 110)
        for k, v in c.items(): print(f"{k}: {v}")
        for r in re.findall(r"R-\d{3}", " ".join(c.values())):
            if r not in cited: cited.append(r)
print("\n\nREGISTER ROWS CITED:", cited)
for r in cited:
    print("=" * 110)
    for k, v in reg.get(r, {"id": r + " NOT FOUND"}).items(): print(f"{k}: {v}")
new = [i for i in reg if re.fullmatch(r"R-\d{3}", i) and 107 <= int(i[2:]) <= 131]
print("\nR-107..R-131 present:", len(new), "| not cited by the ten rows:", [i for i in new if i not in cited])
