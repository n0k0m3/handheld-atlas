#!/usr/bin/env python3
"""Build a spec-box outline SVG from a device JSON (no image needed).

Usage:
    uv run box_outline.py <device.json> --view top|side|bottom --out <svg>

Views:
    top     rounded rect W x H. Corner radius 14 mm for classic, 8 mm for the
            other form factors, capped at 0.2 x min(W, H). Adds a centered
            <rect class="screen"> from screen.size_in and res_w:res_h (16:9
            fallback). No screen rect when size_in is null.
    side    rounded rect H x D (H across, D down). Radius 0.3 x min(H, D).
    bottom  the top rect mirrored (a symmetric rect, so the same shape), no screen.

Dimensions come from dims_mm.handheld. Corners are polylines, so the path
uses M / L / Z only, like a traced outline.
"""
import argparse
import json
import math
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent))

from outline_svg import ROOT, VIEWS, path_from_points, svg_text, write_atomic  # noqa: E402

TOP_RADIUS = {"classic": 14.0}
TOP_RADIUS_DEFAULT = 8.0     # clamshell, 3-in-1, slider, other
TOP_RADIUS_CAP = 0.2         # x min(W, H)
SIDE_RADIUS = 0.3            # x min(H, D)
CORNER_SEGMENTS = 8          # line segments per 90-degree corner
MM_PER_INCH = 25.4


def rounded_rect_points(w, h, r):
    """Clockwise points of a w x h rect with corner radius r, origin top-left."""
    r = max(0.0, min(r, w / 2, h / 2))
    if r == 0:
        return [(0, 0), (w, 0), (w, h), (0, h)]
    # (corner center, start angle in degrees). y grows down, so angles run clockwise.
    corners = [((w - r, r), -90), ((w - r, h - r), 0), ((r, h - r), 90), ((r, r), 180)]
    pts = []
    for (cx, cy), a0 in corners:
        for i in range(CORNER_SEGMENTS + 1):
            a = math.radians(a0 + 90 * i / CORNER_SEGMENTS)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def screen_rect(device, w, h):
    """Return the centered screen (x, y, w, h) in mm, or None when size_in is null."""
    scr = device.get("screen") or {}
    size_in = scr.get("size_in")
    if not size_in:
        return None
    rw, rh = scr.get("res_w"), scr.get("res_h")
    if not (rw and rh):
        rw, rh = 16, 9
    diag = size_in * MM_PER_INCH
    k = diag / math.hypot(rw, rh)
    sw, sh = rw * k, rh * k
    return ((w - sw) / 2, (h - sh) / 2, sw, sh)


def box(device, view):
    """Return (w, h, path, screen) in mm for one view of a device dict."""
    dims = device["dims_mm"]["handheld"]
    W, H, D = float(dims["w"]), float(dims["h"]), float(dims["d"])
    if view in ("top", "bottom"):
        r = TOP_RADIUS.get(device.get("form_factor"), TOP_RADIUS_DEFAULT)
        r = min(r, TOP_RADIUS_CAP * min(W, H))
        pts = rounded_rect_points(W, H, r)
        if view == "bottom":
            # Mirror across the vertical axis. The shape is symmetric, so this
            # only reverses the point order.
            pts = [(W - x, y) for x, y in reversed(pts)]
        screen = screen_rect(device, W, H) if view == "top" else None
        return W, H, path_from_points(pts), screen
    if view == "side":
        r = SIDE_RADIUS * min(H, D)
        return H, D, path_from_points(rounded_rect_points(H, D, r)), None
    raise ValueError(f"unknown view {view!r}")


def box_svg(device, view, source=None):
    """Return (svg text, w, h) for one view."""
    w, h, d, screen = box(device, view)
    return svg_text(device["id"], view, "box", w, h, d, source=source, screen=screen), w, h


def device_source(path):
    """Relative device JSON path for data-source."""
    p = pathlib.Path(path).resolve()
    return str(p.relative_to(ROOT)) if ROOT in p.parents else p.name


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a spec-box outline SVG from a device JSON.")
    ap.add_argument("device", type=pathlib.Path, help="data/devices/<brand>/<slug>.json")
    ap.add_argument("--view", required=True, choices=VIEWS)
    ap.add_argument("--out", type=pathlib.Path, required=True, help="output SVG path")
    args = ap.parse_args(argv)

    try:
        with open(args.device) as f:
            device = json.load(f)
        svg, w, h = box_svg(device, args.view, device_source(args.device))
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"FAIL {args.device}: {e}", file=sys.stderr)
        return 1
    write_atomic(args.out, svg)
    print(f"OK   {device['id']} {args.view}: box {w:g} x {h:g} mm -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
