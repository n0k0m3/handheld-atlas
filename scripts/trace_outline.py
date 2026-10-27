#!/usr/bin/env python3
"""Trace a device outline from a product render and write an outline SVG.

Usage:
    uv run python -I trace_outline.py <image> --w <mm> --h <mm> --out <svg> \\
        --slug <slug> --view top [--source <url>] [--eps 0.0008]

Steps:
1. Load the image with PIL.
2. Build the object mask. If the image has real alpha (a pixel with alpha < 250),
   the mask is alpha > 16. Else flood-fill the background from the four corners
   (tolerance 28/255 against each corner color). The object is not background,
   so a white screen inside the body stays part of the object.
3. Close the mask (5 px). Take the largest external contour.
4. Simplify with approxPolyDP, epsilon = 0.0008 x perimeter. Raise epsilon
   until the path string is under 4 KB.
5. Scale so the bounding box width equals --w mm. Origin = bounding box top-left.
6. Check the aspect: abs((bbox_h / bbox_w) / (h / w) - 1) <= 0.12. If that fails,
   try the image rotated 90 degrees clockwise.

Exit codes:
    0  SVG written
    1  no usable object (unreadable image, no background, no contour)
    2  bad arguments
    3  aspect check failed, as is and rotated

No SVG is written on a failure. The input image is untrusted: run with python -I.
"""
import argparse
import pathlib
import sys

# python -I drops the script directory from sys.path. Add it back at the end
# so the shared format module loads. scripts/ is trusted; images/raw/ is never added.
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402

from outline_svg import MAX_PATH_BYTES, ROOT, VIEWS, path_from_points, svg_text, write_atomic  # noqa: E402

MAX_SIDE = 2000        # Downscale larger images to this many px on the long side.
ALPHA_REAL = 250       # Any pixel below this means the alpha channel is real.
ALPHA_ON = 16          # Alpha above this is object.
BG_TOL = 28            # Flood-fill tolerance per channel, against the corner color.
CLOSE_PX = 5           # Morphological close kernel size.
EPS_START = 0.0008     # approxPolyDP epsilon as a fraction of the perimeter.
EPS_STEP = 1.25        # Multiply epsilon by this until the path fits.
ASPECT_TOL = 0.12      # Allowed relative aspect error before the fit to spec w x h.
MIN_OBJECT = 0.01      # The object must cover at least 1 % of the image.
MIN_BACKGROUND = 0.01  # Flood fill must find at least 1 % background.


class TraceError(Exception):
    def __init__(self, msg, code=1):
        super().__init__(msg)
        self.code = code


def load_rgba(path):
    """Load the first frame as an RGBA uint8 array, upright, at most MAX_SIDE px."""
    try:
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode in ("I", "I;16", "I;16B", "I;16L", "F"):
                # 16-bit and float grey: scale to 8 bit before the RGBA convert.
                arr = np.asarray(im, dtype=np.float64)
                hi = arr.max() or 1.0
                im = Image.fromarray((arr / hi * 255).astype(np.uint8), "L")
            im = im.convert("RGBA")
            if max(im.size) > MAX_SIDE:
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
            return np.array(im)
    except (OSError, ValueError, Image.DecompressionBombError) as e:
        raise TraceError(f"cannot read image: {e}") from e


def object_mask(rgba):
    """Return (mask uint8 0/255, mode). mode is 'alpha' or 'flood'."""
    alpha = rgba[..., 3]
    if (alpha < ALPHA_REAL).any():
        return np.where(alpha > ALPHA_ON, 255, 0).astype(np.uint8), "alpha"

    rgb = np.ascontiguousarray(rgba[..., :3])
    h, w = rgb.shape[:2]
    ff = np.zeros((h + 2, w + 2), np.uint8)
    # FIXED_RANGE compares each pixel with the seed (corner) color, not with its neighbour.
    flags = 4 | cv2.FLOODFILL_FIXED_RANGE | cv2.FLOODFILL_MASK_ONLY | (255 << 8)
    tol = (BG_TOL, BG_TOL, BG_TOL)
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if ff[y + 1, x + 1]:
            continue
        cv2.floodFill(rgb, ff, (x, y), (0, 0, 0), tol, tol, flags)
    bg = ff[1:-1, 1:-1] > 0
    if bg.mean() < MIN_BACKGROUND:
        raise TraceError("flood fill found no background; the object fills the frame")
    return np.where(bg, 0, 255).astype(np.uint8), "flood"


def largest_contour(mask):
    """Close the mask, return the largest external contour as an (N, 2) int array."""
    pad = CLOSE_PX * 2
    m = cv2.copyMakeBorder(mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CLOSE_PX, CLOSE_PX))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise TraceError("no contour found")
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < MIN_OBJECT * mask.size:
        raise TraceError(f"largest contour covers under {MIN_OBJECT:.0%} of the image")
    return c


def orient(pts, ref, rotated):
    """Rotate pts 90 degrees clockwise (image coordinates, y down) when rotated is set.

    ref is the full contour. It fixes the rotation frame, so the simplified
    points land in the same place as the full contour.
    """
    if not rotated:
        return pts
    return np.stack([ref[:, 1].max() - pts[:, 1], pts[:, 0] - ref[:, 0].min()], axis=1)


def aspect_err(pts, want):
    """Return abs((bbox_h / bbox_w) / want - 1) for points. want = h / w."""
    bw, bh = (float(v) for v in pts.max(axis=0) - pts.min(axis=0))
    if bw <= 0 or bh <= 0:
        return float("inf")
    return abs((bh / bw) / want - 1)


def simplify(contour, rotated, w_mm, h_mm, eps_frac=EPS_START):
    """Return (path string, point count, out height mm) under MAX_PATH_BYTES.

    The bounding box is fitted to the spec w x h (x and y scaled separately).
    The aspect check in trace() bounds that distortion to ASPECT_TOL.
    """
    ref = contour.reshape(-1, 2).astype(np.float64)
    full = orient(ref, ref, rotated)
    lo = full.min(axis=0)
    span = full.max(axis=0) - lo
    scale = np.array([w_mm / span[0], h_mm / span[1]])
    eps = eps_frac * cv2.arcLength(contour, True)
    while True:
        approx = cv2.approxPolyDP(contour, eps, True).reshape(-1, 2).astype(np.float64)
        mm = (orient(approx, ref, rotated) - lo) * scale
        if len(approx) < 3:
            raise TraceError("the contour collapses to under 3 points")
        d = path_from_points(mm)
        if len(d.encode()) < MAX_PATH_BYTES:
            return d, len(approx), h_mm
        eps *= EPS_STEP


def trace(image, w_mm, h_mm, eps_frac=EPS_START):
    """Trace one image. Return a dict with path data and stats, or raise TraceError."""
    rgba = load_rgba(image)
    mask, mode = object_mask(rgba)
    c = largest_contour(mask)
    pts = c.reshape(-1, 2).astype(np.float64)
    want = h_mm / w_mm
    err0 = aspect_err(pts, want)
    err90 = aspect_err(orient(pts, pts, True), want)
    if err0 <= ASPECT_TOL:
        rotated, err = False, err0
    elif err90 <= ASPECT_TOL:
        rotated, err = True, err90
    else:
        raise TraceError(
            f"aspect check failed: err {err0:.3f} as is, {err90:.3f} rotated 90 "
            f"(limit {ASPECT_TOL}, want h/w {want:.3f}, mask {mode})",
            code=3,
        )
    d, n, h_out = simplify(c, rotated, w_mm, h_mm, eps_frac)
    return {"path": d, "points": n, "h": h_out, "aspect_err": err, "rotated": rotated, "mode": mode}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Trace a device outline from a render into an outline SVG (1 unit = 1 mm).",
        epilog="Exit 3 when the aspect check fails both as is and rotated 90 degrees. Run with python -I.",
    )
    ap.add_argument("image", type=pathlib.Path, help="render file (png, jpg, webp, ...)")
    ap.add_argument("--w", type=float, required=True, help="device width in mm (bounding box width)")
    ap.add_argument("--h", type=float, required=True, help="device height in mm, for the aspect check")
    ap.add_argument("--out", type=pathlib.Path, required=True, help="output SVG path")
    ap.add_argument("--slug", required=True, help="device id for data-device")
    ap.add_argument("--view", required=True, choices=VIEWS, help="view name for data-view")
    ap.add_argument("--source", default=None, help="image URL for data-source (default: the image file path)")
    ap.add_argument("--eps", type=float, default=EPS_START,
                    help=f"start epsilon as a fraction of the perimeter (default {EPS_START})")
    args = ap.parse_args(argv)

    if args.w <= 0 or args.h <= 0:
        ap.error("--w and --h must be positive")
    if args.eps <= 0:
        ap.error("--eps must be positive")

    try:
        r = trace(args.image, args.w, args.h, args.eps)
    except TraceError as e:
        print(f"FAIL {args.slug} {args.view}: {e}", file=sys.stderr)
        return e.code

    source = args.source
    if not source:
        img = args.image.resolve()
        source = str(img.relative_to(ROOT)) if ROOT in img.parents else img.name
    svg = svg_text(args.slug, args.view, "traced", args.w, r["h"], r["path"], source, r["aspect_err"])
    write_atomic(args.out, svg)
    print(
        f"OK   {args.slug} {args.view}: aspect_err={r['aspect_err']:.3f} "
        f"rotated={'90' if r['rotated'] else '0'} mask={r['mode']} points={r['points']} "
        f"path={len(r['path'].encode())} B -> {args.out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
