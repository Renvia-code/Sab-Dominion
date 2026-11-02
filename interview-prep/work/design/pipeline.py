"""Print pipelines for the interview pack (Windows, this PC).

    PPTX  -> LibreOffice (headless)  -> PDF at slide size -> PyMuPDF imposition on US Letter landscape
    HTML  -> Microsoft Edge (headless) -> PDF (page size from CSS @page)
    PDF   -> PyMuPDF -> PNG, colour and greyscale, for proofing by eye

Every function returns the path it wrote and raises on failure, so a caller never
proceeds on a missing file.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

SOFFICE = Path(r"C:\Program Files\LibreOffice\program\soffice.com")
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

LETTER_W, LETTER_H = 612.0, 792.0  # points


def pptx_to_pdf(pptx: Path, outdir: Path, timeout: int = 240) -> Path:
    """Convert with LibreOffice in a throwaway profile (no first-run dialogs, no clash
    with any LibreOffice the owner has open)."""
    pptx, outdir = Path(pptx).resolve(), Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="lo_profile_"))
    target = outdir / (pptx.stem + ".pdf")
    if target.exists():
        target.unlink()
    cmd = [str(SOFFICE), f"-env:UserInstallation={profile.as_uri()}", "--headless", "--norestore",
           "--nologo", "--convert-to", "pdf:impress_pdf_Export", "--outdir", str(outdir), str(pptx)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not target.exists():
        raise RuntimeError(f"LibreOffice did not write {target}\nstdout={res.stdout}\nstderr={res.stderr}")
    return target


def docx_to_pdf(docx: Path, outdir: Path, timeout: int = 240) -> Path:
    docx, outdir = Path(docx).resolve(), Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="lo_profile_"))
    target = outdir / (docx.stem + ".pdf")
    if target.exists():
        target.unlink()
    cmd = [str(SOFFICE), f"-env:UserInstallation={profile.as_uri()}", "--headless", "--norestore",
           "--nologo", "--convert-to", "pdf:writer_pdf_Export", "--outdir", str(outdir), str(docx)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not target.exists():
        raise RuntimeError(f"LibreOffice did not write {target}\nstdout={res.stdout}\nstderr={res.stderr}")
    return target


def impose_letter_landscape(pdf_in: Path, pdf_out: Path, scale: float = 0.75) -> Path:
    """Place each slide page, as vectors, centred on a US Letter landscape page."""
    import pymupdf

    src = pymupdf.open(str(pdf_in))
    out = pymupdf.open()
    pw, ph = LETTER_H, LETTER_W  # landscape: 792 x 612
    for i, page in enumerate(src):
        r = page.rect
        w, h = r.width * scale, r.height * scale
        x0, y0 = (pw - w) / 2, (ph - h) / 2
        new = out.new_page(width=pw, height=ph)
        new.show_pdf_page(pymupdf.Rect(x0, y0, x0 + w, y0 + h), src, i)
    out.set_metadata(src.metadata or {})
    out.save(str(pdf_out), garbage=3, deflate=True)
    return Path(pdf_out)


def html_to_pdf(html: Path, pdf_out: Path, timeout: int = 180) -> Path:
    """Print an HTML file with headless Edge. Page size and margins come from CSS @page."""
    html, pdf_out = Path(html).resolve(), Path(pdf_out).resolve()
    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    if pdf_out.exists():
        pdf_out.unlink()
    profile = Path(tempfile.mkdtemp(prefix="edge_profile_"))
    cmd = [str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--disable-extensions", f"--user-data-dir={profile}", "--no-pdf-header-footer",
           "--generate-pdf-document-outline", "--virtual-time-budget=5000",
           f"--print-to-pdf={pdf_out}", html.as_uri()]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    finally:
        # Edge may hold the profile for a moment after exit
        for _ in range(10):
            try:
                shutil.rmtree(profile)
                break
            except OSError:
                time.sleep(0.5)
    if not pdf_out.exists():
        raise RuntimeError(f"Edge did not write {pdf_out}\nstdout={res.stdout}\nstderr={res.stderr}")
    return pdf_out


def pdf_to_pngs(pdf: Path, outdir: Path, dpi: int = 110, grey: bool = False, prefix: str | None = None,
                pages: list[int] | None = None) -> list[Path]:
    """Render pages to PNG. grey=True renders a true greyscale copy (what a mono printer sees)."""
    import pymupdf

    pdf, outdir = Path(pdf), Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(pdf))
    paths = []
    prefix = prefix or pdf.stem
    for i, page in enumerate(doc):
        if pages and (i + 1) not in pages:
            continue
        cs = pymupdf.csGRAY if grey else pymupdf.csRGB
        pix = page.get_pixmap(dpi=dpi, colorspace=cs, alpha=False)
        p = outdir / f"{prefix}_p{i + 1:02d}{'_grey' if grey else ''}.png"
        pix.save(str(p))
        paths.append(p)
    return paths


def pdf_fonts(pdf: Path) -> list[str]:
    """List embedded font names, to confirm the one family made it through."""
    import pymupdf

    doc = pymupdf.open(str(pdf))
    names = set()
    for page in doc:
        for f in page.get_fonts(full=True):
            names.add(f[3])
    return sorted(names)


def pdf_min_font_size(pdf: Path, scale: float = 1.0) -> list[tuple[int, float, str]]:
    """Smallest text size per page (in printed points, after an optional scale) and a sample."""
    import pymupdf

    doc = pymupdf.open(str(pdf))
    out = []
    for i, page in enumerate(doc):
        smallest = (999.0, "")
        d = page.get_text("dict")
        for b in d.get("blocks", []):
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    if s["text"].strip() and s["size"] * scale < smallest[0]:
                        smallest = (s["size"] * scale, s["text"].strip()[:40])
        out.append((i + 1, round(smallest[0], 2), smallest[1]))
    return out
