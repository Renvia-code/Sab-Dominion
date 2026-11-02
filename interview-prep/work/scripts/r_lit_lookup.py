"""Verify literature metadata: OpenAlex title search -> DOI, then Crossref record for that DOI.

Usage: python -I r_lit_lookup.py <queries.json> <raw_out_dir> <report_out.txt>
  queries.json: [{"key": "brooks2014", "title": "Get excited: ...", "year": 2014}, ...]
For each query prints: OpenAlex best match (title, year, venue, DOI, first authors, cited_by_count),
the Crossref record for that DOI (title, container, year, volume, issue, page), a title-match flag,
and the OpenAlex abstract (rebuilt from the inverted index) when present.
Raw API responses are saved under raw_out_dir (data only; never executed).
No e-mail address is sent to either API.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (research-verification script; no contact)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def abstract(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    queries = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    raw = Path(sys.argv[2])
    raw.mkdir(parents=True, exist_ok=True)
    out = []
    for q in queries:
        key, title = q["key"], q.get("title", "")
        line = [f"=== {key}: {title or q.get('doi')}"]
        try:
            if q.get("doi"):
                oa = {"results": [get("https://api.openalex.org/works/doi:" + q["doi"])]}
                title = title or oa["results"][0].get("title") or ""
            else:
                url = "https://api.openalex.org/works?per-page=3&search=" + urllib.parse.quote(title)
                oa = get(url)
            (raw / f"{key}_openalex.json").write_text(json.dumps(oa), encoding="utf-8")
            res = oa.get("results", [])
            best = None
            for r in res:
                if norm(r.get("title"))[:60] == norm(title)[:60]:
                    best = r
                    break
            if best is None and res:
                best = res[0]
            if best is None:
                line.append("OpenAlex: no result")
            else:
                doi = (best.get("doi") or "").replace("https://doi.org/", "")
                venue = ((best.get("primary_location") or {}).get("source") or {}).get("display_name")
                auths = [a["author"]["display_name"] for a in best.get("authorships", [])[:5]]
                match = norm(best.get("title"))[:60] == norm(title)[:60]
                line.append(f"OpenAlex: {best.get('title')} | {best.get('publication_year')} | {venue} | "
                            f"doi {doi} | {', '.join(auths)} | cited_by {best.get('cited_by_count')} | "
                            f"title_match {match}")
                if doi:
                    time.sleep(0.4)
                    cr = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
                    (raw / f"{key}_crossref.json").write_text(json.dumps(cr), encoding="utf-8")
                    m = cr.get("message", {})
                    ct = (m.get("container-title") or [""])[0]
                    yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
                    line.append(f"Crossref: {(m.get('title') or [''])[0]} | {ct} | {yr} | vol {m.get('volume')} "
                                f"| issue {m.get('issue')} | pages {m.get('page')} | type {m.get('type')}")
                ab = abstract(best.get("abstract_inverted_index"))
                src_ab = "OpenAlex"
                if not ab and doi:
                    try:
                        time.sleep(1.0)
                        ss = get("https://api.semanticscholar.org/graph/v1/paper/DOI:" + doi
                                 + "?fields=title,abstract,year,venue,tldr")
                        (raw / f"{key}_s2.json").write_text(json.dumps(ss), encoding="utf-8")
                        ab = ss.get("abstract") or ""
                        src_ab = "Semantic Scholar"
                        if not ab and ss.get("tldr"):
                            ab = "[TLDR only] " + (ss["tldr"].get("text") or "")
                    except Exception as e:  # noqa: BLE001
                        line.append(f"Semantic Scholar: {type(e).__name__}: {e}")
                line.append(f"Abstract ({src_ab}): " + (ab[:1500] if ab else "(none found)"))
        except Exception as e:  # noqa: BLE001 - report and continue
            line.append(f"ERROR: {type(e).__name__}: {e}")
        print("\n".join(line))
        out.append("\n".join(line))
        time.sleep(0.4)
    Path(sys.argv[3]).write_text("\n\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
