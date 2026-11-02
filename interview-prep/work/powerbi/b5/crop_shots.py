"""Crop the report canvas out of full-window Power BI Desktop shots (pbi_pNN.png -> crop_pNN.png).
The box fits a 3864 x 2100 window with the panes as left by the tour. Usage: python -I crop_shots.py <dir>"""
import sys
from pathlib import Path

from PIL import Image

BOX = (85, 350, 2875, 1925)
d = Path(sys.argv[1])
for p in sorted(d.glob("pbi_p[0-9][0-9].png")):
    im = Image.open(p)
    if im.size != (3864, 2100):
        print(f"{p.name}: unexpected size {im.size}, not cropped")
        continue
    out = d / p.name.replace("pbi_", "crop_")
    im.crop(BOX).save(out)
    print(f"{out.name} {BOX[2] - BOX[0]} x {BOX[3] - BOX[1]}")
