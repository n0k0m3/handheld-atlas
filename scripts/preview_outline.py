#!/usr/bin/env python3
"""Draw outline SVGs onto one PNG sheet so a person (or the Read tool) can judge them.

Usage:
    uv run preview_outline.py outlines/<slug>.top.svg [more .svg ...] --out /path/sheet.png
    uv run preview_outline.py --slugs steam-deck-oled legion-go-2 --view top --out /path/sheet.png

Each outline is drawn at the same scale (default 2 px per mm) with its slug,
kind (traced / box) and size under it. Nothing is read from images/raw.
"""
import argparse
import pathlib
import re
import sys

from PIL import Image, ImageDraw

from outline_svg import OUT_DIR, parse_svg

NUM = re.compile(r"[-+]?\d*\.?\d+")


def path_points(d):
    """Return the M/L points of an absolute M L Z path as (x, y) floats."""
    nums = [float(n) for n in NUM.findall(d)]
    return list(zip(nums[0::2], nums[1::2]))


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svgs", nargs="*", help="outline SVG files")
    ap.add_argument("--slugs", nargs="*", default=[], help="device slugs; combined with --view")
    ap.add_argument("--view", default="top", choices=["top", "side", "bottom"])
    ap.add_argument("--scale", type=float, default=2.0, help="pixels per mm (default 2)")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    files = [pathlib.Path(s) for s in args.svgs]
    files += [OUT_DIR / f"{s}.{args.view}.svg" for s in args.slugs]
    if not files:
        ap.error("give SVG files or --slugs")

    items = []
    for f in files:
        try:
            items.append((f, parse_svg(f)))
        except (ValueError, OSError) as e:
            print(f"skip {f}: {e}", file=sys.stderr)
    if not items:
        return 1

    s = args.scale
    pad, label_h = 16, 36
    cell_w = int(max(o["w"] for _, o in items) * s) + 2 * pad
    cell_h = int(max(o["h"] for _, o in items) * s) + 2 * pad + label_h
    cols = min(args.cols, len(items))
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), "white")
    draw = ImageDraw.Draw(sheet)

    for i, (f, o) in enumerate(items):
        ox = (i % cols) * cell_w + pad
        oy = (i // cols) * cell_h + pad
        pts = [(ox + x * s, oy + y * s) for x, y in path_points(o["path"])]
        if len(pts) >= 3:
            draw.polygon(pts, fill=(205, 220, 240), outline=(30, 60, 120))
        if o.get("screen"):
            sc = o["screen"]
            draw.rectangle([ox + sc["x"] * s, oy + sc["y"] * s, ox + (sc["x"] + sc["w"]) * s, oy + (sc["y"] + sc["h"]) * s], outline=(120, 120, 120))
        draw.rectangle([ox, oy, ox + o["w"] * s, oy + o["h"] * s], outline=(200, 200, 200))
        label = f"{o['slug']} [{o['kind']}] {o['w']:.0f}x{o['h']:.0f} mm"
        if o.get("aspect_err") is not None:
            label += f" err={o['aspect_err']:.3f}"
        draw.text((ox, oy + o["h"] * s + 4), label, fill=(0, 0, 0))

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"{len(items)} outline(s) -> {out} ({sheet.width}x{sheet.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
