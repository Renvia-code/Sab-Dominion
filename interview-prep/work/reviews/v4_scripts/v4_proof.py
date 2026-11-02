"""V4 print proof: for each print PDF, page count and size, smallest printed text per page, embedded
fonts, smallest effective image resolution per page, text within 0.25 in of the page edge, then colour
and greyscale PNGs per page plus contact sheets for viewing.

Usage: python -I v4_proof.py <out_dir> <version, e.g. v3> [--no-png]
Writes <out_dir>/<doc>/<stem>_pNN[_grey].png, <out_dir>/<doc>/sheet_*.png and <out_dir>/v4_numbers.json.
"""
import hashlib
import json
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
IP = Path(__file__).resolve().parents[3]          # interview-prep/
DEL = IP / "deliverables"
VER = sys.argv[2]
PNG = "--no-png" not in sys.argv
if VER == "final":                                  # O-34: the final files carry no version suffix
    DOCS = [
        ("deck_adopted", DEL / "01_deck" / "Dominion_reliability_deck_adopted_print_letter.pdf", "landscape"),
        ("deck_public", DEL / "01_deck" / "Dominion_reliability_deck_public_print_letter.pdf", "landscape"),
        ("sheet", DEL / "02_question_sheet" / "Dominion_question_sheet.pdf", "portrait"),
        ("brief", DEL / "03_interview_brief" / "Dominion_interview_brief.pdf", "portrait"),
    ]
else:
    DOCS = [
        ("deck_adopted", DEL / "01_deck" / f"Dominion_reliability_deck_{VER}_print_letter.pdf", "landscape"),
        ("deck_public", DEL / "01_deck" / f"Dominion_reliability_deck_{VER}_public_print_letter.pdf", "landscape"),
        ("sheet", DEL / "02_question_sheet" / f"Dominion_question_sheet_{VER}.pdf", "portrait"),
        ("brief", DEL / "03_interview_brief" / f"Dominion_interview_brief_{VER}.pdf", "portrait"),
    ]
EDGE_IN = 0.25


def min_font(page):
    best = (999.0, "")
    for b in page.get_text("dict").get("blocks", []):
        for ln in b.get("lines", []):
            for s in ln.get("spans", []):
                if s["text"].strip() and s["size"] < best[0]:
                    best = (s["size"], s["text"].strip()[:40])
    return round(best[0], 2), best[1]


def edge_text(page):
    r = page.rect
    m = EDGE_IN * 72
    hits = []
    for x0, y0, x1, y1, w, *_ in page.get_text("words"):
        if x0 < m or y0 < m or x1 > r.width - m or y1 > r.height - m:
            hits.append(w)
    return hits


def edge_min_in(page):
    r = page.rect
    ds = [min(x0, y0, r.width - x1, r.height - y1) for x0, y0, x1, y1, *_ in page.get_text("words")]
    return round(min(ds) / 72, 3) if ds else None


def image_dpi(page):
    """Smallest effective resolution (pixels per printed inch) of the images placed on the page."""
    worst = None
    for info in page.get_image_info(xrefs=True):
        bw = info["bbox"][2] - info["bbox"][0]
        bh = info["bbox"][3] - info["bbox"][1]
        if bw < 20 or bh < 20:
            continue
        dpi = min(info["width"] / (bw / 72), info["height"] / (bh / 72))
        if worst is None or dpi < worst[0]:
            worst = (round(dpi), info["width"], info["height"], round(bw / 72, 2), round(bh / 72, 2))
    return worst


def contact(paths, out, cols, tw):
    ims = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        ims.append((p.stem, im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS)))
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    gap, lab = 10, 16
    W = cols * tw + (cols + 1) * gap
    H = sum(max(im.height for _, im in r) + lab + gap for r in rows) + gap
    sheet = Image.new("RGB", (W, H), "#9CA3AF")
    d = ImageDraw.Draw(sheet)
    y = gap
    for r in rows:
        x = gap
        for name, im in r:
            d.text((x, y), name, fill="#111111")
            sheet.paste(im, (x, y + lab))
            x += tw + gap
        y += max(im.height for _, im in r) + lab + gap
    sheet.save(out)
    return out


def main():
    out_root = Path(sys.argv[1])
    report = {}
    for key, pdf, orient in DOCS:
        doc = pymupdf.open(str(pdf))
        od = out_root / key
        od.mkdir(parents=True, exist_ok=True)
        for old in od.glob("*.png"):
            old.unlink()
        pages = []
        fonts = {}
        for i, page in enumerate(doc):
            for f in page.get_fonts(full=True):
                fonts[f[3]] = f[1]          # name -> ext ("n/a" = not embedded)
            mf = min_font(page)
            pages.append({"page": i + 1, "size_in": [round(page.rect.width / 72, 2), round(page.rect.height / 72, 2)],
                          "min_pt": mf[0], "min_sample": mf[1], "edge_words": edge_text(page)[:8],
                          "edge_in": edge_min_in(page),
                          "min_image": image_dpi(page)})
        col, grey = [], []
        for i, page in enumerate(doc if PNG else []):
            for g, lst in ((False, col), (True, grey)):
                pix = page.get_pixmap(dpi=100, colorspace=pymupdf.csGRAY if g else pymupdf.csRGB, alpha=False)
                p = od / f"{key}_p{i + 1:02d}{'_grey' if g else ''}.png"
                pix.save(str(p))
                lst.append(p)
        sheets = []
        if orient == "landscape":
            spec = ((col, 4, 2, 775), (grey, 6, 3, 515))
        elif key == "sheet":
            spec = ((col, 2, 2, 775), (grey, 2, 2, 775))
        else:
            spec = ((col, 3, 3, 515), (grey, 6, 3, 515))
        for lst, per, cols, tw in (spec if PNG else ()):
            for j in range(0, len(lst), per):
                tag = "grey" if "_grey" in lst[0].name else "colour"
                sheets.append(str(contact(lst[j:j + per], od / f"sheet_{tag}_{j // per + 1}.png", cols, tw)))
        report[key] = {"pdf": pdf.relative_to(IP).as_posix(), "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()[:16],
                       "modified": __import__("datetime").datetime.fromtimestamp(pdf.stat().st_mtime).strftime("%d %b %H:%M:%S"),
                       "bytes": pdf.stat().st_size, "pages": doc.page_count,
                       "min_pt_doc": min(p["min_pt"] for p in pages),
                       "edge_in": min(p["edge_in"] for p in pages if p["edge_in"] is not None),
                       "fonts": {k: v for k, v in sorted(fonts.items())},
                       "not_embedded": sorted(k for k, v in fonts.items() if v == "n/a"),
                       "page_detail": pages, "contact_sheets": sheets}
        print(f"{key}: {doc.page_count} pages, {pages[0]['size_in']} in, min {report[key]['min_pt_doc']} pt, "
              f"fonts {len(fonts)} (not embedded: {report[key]['not_embedded']}), sha {report[key]['sha256']}")
        for p in pages:
            print(f"  p{p['page']:02d} min {p['min_pt']:>5} pt '{p['min_sample']}'  img {p['min_image']}  edge {p['edge_words']}")
    (out_root / "v4_numbers.json").write_text(json.dumps(report, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
