"""Contact sheet for proofing: tile PNGs into one image (each tile scaled to the same width).

Usage: python -I montage.py OUT.png COLS TILE_WIDTH_PX img1.png img2.png ...
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    out, cols, tw = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ims = []
    for p in sys.argv[4:]:
        im = Image.open(p).convert("RGB")
        h = round(im.height * tw / im.width)
        ims.append((Path(p).stem, im.resize((tw, h), Image.LANCZOS)))
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    gap, lab = 12, 18
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
    print(out, sheet.size)


if __name__ == "__main__":
    main()
