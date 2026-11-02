"""Colour maths for the interview-pack design system.

Computes, for each palette colour: OKLCH, WCAG contrast against white, and the
grey level it prints at in a greyscale copy (CIE L* and Rec.601 luma). Also
builds the one-hue sequential ramp from the subject blue (#0A66C2) in OKLCH and
snaps the third-category gold into the dataviz lightness band for print marks.

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\design\\palette_tools.py
Writes: interview-prep/work/design/palette_computed.json
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in rgb)


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def rgb_to_oklab(rgb):
    r, g, b = (srgb_to_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, bb


def oklab_to_rgb_linear(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, bb


def oklch(hexv):
    L, a, b = rgb_to_oklab(hex_to_rgb(hexv))
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H


def oklch_to_hex(L, C, H):
    """Convert OKLCH to hex, reducing chroma until the colour is in sRGB gamut."""
    c = C
    while c >= 0:
        a = c * math.cos(math.radians(H))
        b = c * math.sin(math.radians(H))
        lin = oklab_to_rgb_linear(L, a, b)
        if all(-1e-6 <= v <= 1 + 1e-6 for v in lin):
            return rgb_to_hex([linear_to_srgb(min(1, max(0, v))) for v in lin])
        c -= 0.002
    return rgb_to_hex([linear_to_srgb(min(1, max(0, v))) for v in oklab_to_rgb_linear(L, 0, 0)])


def rel_lum(hexv):
    r, g, b = (srgb_to_linear(c) for c in hex_to_rgb(hexv))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(h1, h2):
    a, b = rel_lum(h1), rel_lum(h2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def cie_lstar(hexv):
    y = rel_lum(hexv)
    return 116 * (y ** (1 / 3)) - 16 if y > 216 / 24389 else y * 24389 / 27


def luma601(hexv):
    r, g, b = (c * 255 for c in hex_to_rgb(hexv))
    return 0.299 * r + 0.587 * g + 0.114 * b


def describe(name, hexv):
    L, C, H = oklch(hexv)
    return {
        "name": name,
        "hex": hexv,
        "oklch": [round(L, 3), round(C, 3), round(H, 1)],
        "contrast_on_white": round(contrast(hexv, "#FFFFFF"), 2),
        "grey_Lstar": round(cie_lstar(hexv), 1),
        "grey_luma601": round(luma601(hexv), 1),
    }


CONVENTIONS = {
    "subject": "#0A66C2",
    "context": "#B8BCC2",
    "context_2": "#6B7280",
    "third": "#E8B117",
    "dark_accent": "#1F2A44",
}


def main():
    out = {"conventions": [describe(k, v) for k, v in CONVENTIONS.items()]}

    # Third-category gold snapped into the dataviz light band (L <= 0.77) for print marks,
    # same hue and chroma as #E8B117.
    L, C, H = oklch(CONVENTIONS["third"])
    snapped = oklch_to_hex(0.74, C, H)
    out["third_print_mark"] = describe("third_print_mark", snapped)

    # One-hue sequential ramp from the subject blue's hue. Light end recedes toward white;
    # dark end deeper than the subject. Chroma follows a gentle arch so the light steps
    # are not grey and the dark steps stay in gamut.
    Ls, Cs, Hs = oklch(CONVENTIONS["subject"])
    steps = [0.96, 0.90, 0.83, 0.75, 0.67, 0.59, Ls, 0.44, 0.36]
    ramp = []
    for i, l in enumerate(steps):
        # chroma: low at the light end, the subject's chroma in the middle, slightly less at the dark end
        if l >= Ls:
            t = (l - Ls) / (0.96 - Ls)
            c = Cs * (1 - 0.82 * t)
        else:
            t = (Ls - l) / (Ls - 0.36)
            c = Cs * (1 - 0.25 * t)
        hexv = CONVENTIONS["subject"] if abs(l - Ls) < 1e-9 else oklch_to_hex(l, c, Hs)
        ramp.append(describe(f"seq_{i + 1}", hexv))
    out["sequential_blue"] = ramp

    # Chrome (not data): text and rules
    chrome = {
        "ink": "#1F2A44",
        "ink_2": "#374151",
        "muted": "#6B7280",
        "rule": "#D1D5DB",
        "grid": "#E5E7EB",
        "tint": "#F3F6FA",
        "subject_tint": "#E8F0FB",
    }
    out["chrome"] = [describe(k, v) for k, v in chrome.items()]

    (HERE / "palette_computed.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for section, rows in out.items():
        print(f"== {section}")
        rows = rows if isinstance(rows, list) else [rows]
        for r in rows:
            print(f"  {r['name']:<18} {r['hex']}  OKLCH {r['oklch']}  contrast/white {r['contrast_on_white']:>5}  "
                  f"grey L* {r['grey_Lstar']:>5}  luma {r['grey_luma601']:>5}")


if __name__ == "__main__":
    main()
