"""Build research/question_bank.csv and research/top40.md from work/scripts/r5_questions.json (R5).

Usage: python -I r5_build_bank.py <questions.json> <out_dir> <stamp>
  out_dir: interview-prep/research ; stamp: e.g. "2026-11-01 08:50"

Scoring (stated in top40.md):
  frequency = distinct external sources that ask the question or a close variant;
              sources read only as search snippets (opened = false) count 0.5
  fit       = 1-3 fit to the Grid Resiliency BI Analyst role and this deck
  score     = frequency x fit
Ranking ties: a Dominion-specific source first, then the posting (S12), then fit, then id.
Top 40 = every brief-required item + the best question in each technical subtopic + the
highest-ranked others until 40. The P2 sheet picks follow fixed group quotas (see QUOTA).
Reads the JSON only; writes the two outputs.
"""
import csv
import json
import math
import sys
from pathlib import Path

GROUPS = ["Opening", "Behavioural", "Technical BI", "Utility domain", "Role and Dominion",
          "Logistics", "Closing"]
TECH_SUBS = ["Data modelling", "DAX and filter context", "Performance and refresh",
             "SQL", "Snowflake"]
QUOTA = {"Behavioural": 5, "Role and Dominion": 1}  # beyond the brief-required items
TECH_OTHER = 1  # plus the best technical question outside the five named subtopics


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out_dir = Path(sys.argv[2])
    stamp = sys.argv[3]
    src = data["sources"]
    qs = data["questions"]

    ids = [q["id"] for q in qs] + [a["id"] for a in data["asks"]] + [h["id"] for h in data["hard"]]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for q in qs:
        assert q["group"] in GROUPS, q["id"]
        assert q["fit"] in (1, 2, 3), q["id"]
        assert len(set(q["src"])) == len(q["src"]), q["id"]
        for s in q["src"]:
            assert s in src, (q["id"], s)
        q["n_open"] = sum(1 for s in q["src"] if src[s]["opened"])
        q["n_snip"] = sum(1 for s in q["src"] if not src[s]["opened"])
        q["freq"] = q["n_open"] + 0.5 * q["n_snip"]
        q["score"] = q["freq"] * q["fit"]
        q["dom"] = any(src[s]["dominion"] for s in q["src"])
        q["posting"] = "S12" in q["src"]

    order = sorted(qs, key=lambda q: (-q["score"], not q["dom"], not q["posting"],
                                      "BRIEF" not in q["int"], -q["fit"], q["id"]))
    for i, q in enumerate(order, start=1):
        q["rank"] = i

    # Top 40
    top = {q["id"] for q in qs if q["req"]}
    sub_best = {}
    for sub in TECH_SUBS:
        best = next(q for q in order if q["group"] == "Technical BI" and q["sub"] == sub)
        sub_best[sub] = best["id"]
        top.add(best["id"])
    for q in order:
        if len(top) >= 40:
            break
        top.add(q["id"])
    assert len(top) == 40, len(top)
    for q in qs:
        q["top40"] = q["id"] in top

    # Sheet picks
    sheet = {q["id"] for q in qs if q["req"] and q["id"] != "C2"}
    sheet |= set(sub_best.values())
    for grp, n in QUOTA.items():
        extra = [q for q in order if q["group"] == grp and q["id"] not in sheet][:n]
        sheet |= {q["id"] for q in extra}
    other = [q for q in order if q["group"] == "Technical BI" and q["sub"] not in TECH_SUBS][:TECH_OTHER]
    sheet |= {q["id"] for q in other}
    for q in qs:
        q["sheet"] = q["id"] in sheet
    n_sheet = len(sheet)
    assert 20 <= n_sheet <= 24, n_sheet

    # Check of D's H01 statistics from the unrounded r (D: r = 0.6973, t = 2.752, p = 0.025, CI 0.121-0.922)
    r, n = 0.6973, 10
    t = r * math.sqrt(n - 2) / math.sqrt(1 - r * r)
    z, se = math.atanh(r), 1 / math.sqrt(n - 3)
    lo, hi = math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)

    write_csv(out_dir / "question_bank.csv", order, data, src)
    write_md(out_dir / "top40.md", order, data, src, sub_best, n_sheet, stamp, (t, lo, hi))

    print(f"questions {len(qs)}, asks {len(data['asks'])}, hard {len(data['hard'])}, sheet {n_sheet}")
    print(f"H01 check: t = {t:.3f} (df 8; two-sided p between 0.02 and 0.05), 95% CI r = {lo:.2f} to {hi:.2f}")
    for q in order:
        flag = ("*" if q["sheet"] else " ") + ("T" if q["top40"] else " ")
        print(f"{q['rank']:>3} {flag} {q['id']:<4} {q['score']:>5.1f} {q['group'][:12]:<12} {q['q'][:70]}")


def src_list(ids, src):
    return "; ".join(s + ("" if src[s]["opened"] else " (snippet)") for s in ids)


def write_csv(path, order, data, src):
    cols = ["id", "rank", "group", "subtopic", "question", "sources", "internal_refs", "n_opened",
            "n_snippet", "frequency", "fit", "score", "dominion_source", "top40", "on_sheet",
            "proof_locator", "dominion_tie", "notes"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for q in order:
            w.writerow([q["id"], q["rank"], q["group"], q["sub"], q["q"], src_list(q["src"], src),
                        "; ".join(q["int"]), q["n_open"], q["n_snip"], f"{q['freq']:g}", q["fit"],
                        f"{q['score']:g}", "yes" if q["dom"] else "no", "yes" if q["top40"] else "no",
                        "yes" if q["sheet"] else "no", q["proof"], q["tie"], q["notes"]])
        for a in data["asks"]:
            w.writerow([a["id"], "", "Ask the panel", "", a["q"], src_list(a["src"], src), "", "", "",
                        "", "", "", "", "", "yes" if a["pick"] else "no", "", "", a["notes"]])
        for h in data["hard"]:
            w.writerow([h["id"], "", "Hard (this project)", h["slide"], h["q"], "",
                        "BRIEF (required)" if h["brief"] else "", "", "", "", 3, "", "", "", "",
                        "", h["ids"], h["frame"]])


def write_md(path, order, data, src, sub_best, n_sheet, stamp, h01):
    qs = {q["id"]: q for q in order}
    t, lo, hi = h01
    L = []
    a = L.append
    a("# Top 40 questions for the Dominion panel (R5, for B)")
    a("")
    a(f"*Agent R · {stamp} · generated by `work/scripts/r5_build_bank.py` from `work/scripts/r5_questions.json`.*")
    a(f"*Full bank: `research/question_bank.csv` ({len(order)} panel questions, {len(data['asks'])} questions to ask,")
    a(f"{len(data['hard'])} hard project questions). Not for publication: candidate-only material.*")
    a("")
    a("## How B uses this")
    a("")
    a(f"- **★ = on the P2 sheet** ({n_sheet} answered questions, plus five questions to ask and the closing line).")
    a("  The picks follow the rule below, not taste (brief P2).")
    a("- **Answers come only from the resume.** Proof points are locators (role and bullet, as in `role_brief.md`");
    a("  §5); take the wording and figures from the resume itself. `[you: …]` where the resume has nothing.")
    a("- **Dominion ties** carry claim ids (`research/claims_register.csv`) for the brief's appendix. No citations")
    a("  on the sheet.")
    a("- Numbers from the deck: use D's current values (`work/data/findings.md`, `claims.csv`); the figures quoted")
    a("  here follow `work/storyline_LOCK_G1.md` as of 08:25.")
    a("- The role-brief gaps (G1–G10) appear as O5 and H28–H32. R1 (30/60/90 days) is outside the 40 because the")
    a("  deck's S6 answers it.")
    a("")
    a("## What Dominion interviews look like (reported)")
    a("")
    a("- **Opened (R-068, CLIMB, dated 15 Jul 2025):** most interviews use \"behavioral questions to assess your fit")
    a("  for the role\"; \"many interviews will be conducted with a panel of multiple interviewers\"; hiring takes")
    a("  \"typically around six weeks\". A third-party aggregator with no byline: medium confidence.")
    a("- **Not opened (R-069, Glassdoor search snippets; the site returns 403):** a group panel is the most commonly")
    a("  reported stage, with about three panelists and about six behavioural questions. Unverified; it matches")
    a("  the owner's note of a panel of three.")
    a("- **So:** STAR micro-scripts for the five behavioural ★ items carry the most weight; expect each panelist to")
    a("  ask in turn.")
    a("")
    a("## Method")
    a("")
    a("- **Sources** (all accessed 2026-11-01):")
    for sid, s in src.items():
        tag = "opened" if s["opened"] else "**not opened**: snippet only, counts 0.5"
        a(f"  - {sid}: {s['name']}. {s['url']} ({tag})")
    a("- **Frequency** = the number of distinct sources that ask the question or a close variant. Snippet-only")
    a("  sources count half. Internal references (brief, role brief, dossier) never add frequency.")
    a("- **Fit** (1–3) = 3 if it tests a posting requirement, a resume claim the panel can probe, or this deck;")
    a("  2 if it is generic but plausible for an analyst panel.")
    a("- **Score** = frequency × fit. Ties: a Dominion-specific source (S01, S02, S12) first, then the posting,")
    a("  then a topic the brief names, then fit.")
    a("- **Top 40** = every brief-required item (opening three, the three utility basics, the merger, the four")
    a("  logistics placeholders, the closing) + the best-scoring question in each technical subtopic the brief")
    a("  names + the highest-ranked others until 40.")
    a(f"- **Sheet (★)** = opening three; top {QUOTA['Behavioural']} behavioural; one per technical subtopic "
      f"({', '.join(TECH_SUBS)}) plus the best other technical question; the three utility basics; the merger")
    a("  and the top-ranked other role question; the four logistics placeholders; the closing line. If the page")
    a("  is short of room, drop ★ items from the bottom of the ranked table first, never a brief-required one.")
    a("- **Gaps.** Glassdoor, Indeed and Teal return 403; Interview Query returns 429; the OMS page returns 403. None")
    a("  were worked around. Dominion-specific reports come from CLIMB (opened) and Glassdoor search snippets")
    a("  (not opened), so the Dominion signal is thin. Only one or two technical banks per tool were opened, so")
    a("  technical scores are compressed; that is why the sheet takes one question per technical subtopic.")
    a("")
    a("## The 40, ranked")
    a("")
    a("| Rank | Id | Question | Group | Freq | Fit | Score | Sheet |")
    a("|---:|---|---|---|---:|---:|---:|:---:|")
    for q in order:
        if q["top40"]:
            a(f"| {q['rank']} | {q['id']} | {q['q']} | {q['group']} | {q['freq']:g} | {q['fit']} | "
              f"{q['score']:g} | {'★' if q['sheet'] else ''} |")
    a("")
    a("Ranks run over the whole bank, so gaps in the rank column are questions outside the 40.")
    a("")
    a("## Research backing, by sheet group")
    a("")
    for grp in GROUPS:
        items = [q for q in order if q["group"] == grp and q["top40"]]
        if not items:
            continue
        a(f"### {grp}")
        a("")
        if grp == "Technical BI":
            winners = ", ".join(f"{sub}: {sid}" for sub, sid in sub_best.items())
            a(f"*Subtopic winners:* {winners}.")
            a("")
        for q in items:
            star = " ★" if q["sheet"] else ""
            sub = f" · {q['sub']}" if q["sub"] else ""
            a(f"**{q['id']}. {q['q']}**{star}  ")
            a(f"rank {q['rank']} · score {q['score']:g} ({q['freq']:g} × {q['fit']}) · {src_list(q['src'], src) or 'brief only'}{sub}")
            if q["proof"]:
                a(f"- Proof: {q['proof']}")
            if q["tie"]:
                a(f"- Dominion tie: {q['tie']}")
            if q["notes"]:
                a(f"- Note: {q['notes']}")
            a("")
    a("## Five questions to ask the panel")
    a("")
    a("Ranked by fit and by what R's research makes specific; frequency means little for questions the candidate")
    a("asks. Ask two or three; A8 always last.")
    a("")
    for x in data["asks"]:
        mark = "**Pick**" if x["pick"] else "Alternate"
        a(f"- {mark} · {x['id']}. {x['q']} *({x['notes']})*")
    a("")
    a("## The hardest questions this project invites")
    a("")
    a("**Superseded for the brief (09:41) by `research/hard25_answers.md`**, which merges V3's 25 with the brief's")
    a("seven and follows the G2 storyline and the V2 rulings. Frames below predate them: use hard25 Q18 for H06,")
    a("Q5 for H11, Q13 for H14 and Q11 for H15. H02 is corrected (Dominion reports under 'Other', not IEEE 1366).")
    a("")
    a("Seed for V3's mock panel and the P3 appendix (25 hardest). The seven the brief requires are marked ●.")
    a("Frames are claim → evidence → limit; B writes the final answers. H01's statistics are D's, from the")
    a(f"unrounded r = 0.6973 (t = 2.752 on 8 df, p = 0.025, Fisher 95% interval for r 0.121 to 0.922); R's check")
    a(f"gives t = {t:.3f} and {lo:.3f} to {hi:.3f}. Storm county-days are 464 → 791 after D's Bedford-city fix (D22).")
    a("")
    a("| Id | Question | Where it bites | Answer frame | Numbers and ids |")
    a("|---|---|---|---|---|")
    for h in data["hard"]:
        dot = "● " if h["brief"] else ""
        a(f"| {h['id']} | {dot}{h['q']} | {h['slide']} | {h['frame']} | {h['ids']} |")
    a("")
    a("## Outside the 40 (the rest of the bank, for practice)")
    a("")
    a("| Rank | Id | Question | Group | Score |")
    a("|---:|---|---|---|---:|")
    for q in order:
        if not q["top40"]:
            a(f"| {q['rank']} | {q['id']} | {q['q']} | {q['group']} | {q['score']:g} |")
    a("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
