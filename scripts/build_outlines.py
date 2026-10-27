#!/usr/bin/env python3
"""Trace or box the top, side and bottom outline of every device.

Usage:
    uv run build_outlines.py                               # every device -> outlines/index.json
    uv run build_outlines.py --brand gpd                   # only data/devices/gpd/
    uv run build_outlines.py --slugs a b                   # only these device ids
    uv run build_outlines.py --brand gpd --index-name gpd  # index -> outlines/index.gpd.json
    uv run build_outlines.py --merge                       # merge outlines/index.*.json into index.json

For each device and view:
1. Look for images/raw/<slug>/<view>.<ext>. For a clamshell top view,
   use only closed_top.<ext>; a front render shows the lid open.
2. If an image exists, run trace_outline.py on it in a separate
   `python -I` process (the image is untrusted).
3. If there is no image, or the tracer fails, write a spec box (box_outline.py).

Trace dimensions:
    top, bottom   dims_mm.handheld w x h (closed_top uses dims_mm.closed when set)
    side          dims_mm.handheld h x d

Writes outlines/<slug>.<view>.svg and an index:
    {slug: {view: {kind: "traced"|"box", source: url|null, aspect_err: float|null}}}
A run with no --slugs/--brand replaces the index file. A filtered run updates
only its own slugs. Parallel runs should each use their own --index-name, then
one --merge run combines them. --merge only merges; it traces nothing.
"""
import argparse
import json
import pathlib
import subprocess
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent))

from box_outline import box_svg, device_source  # noqa: E402
from outline_svg import DEV_DIR, OUT_DIR, RAW_DIR, ROOT, SLUG_RE, VIEWS, parse_svg, write_atomic  # noqa: E402

TRACER = pathlib.Path(__file__).resolve().parent / "trace_outline.py"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".bmp", ".tif", ".tiff"}
TRACE_TIMEOUT_S = 120


def find_image(slug, view):
    """Return the saved image for a raw view name, or None."""
    d = RAW_DIR / slug
    if not d.is_dir():
        return None
    hits = sorted(p for p in d.glob(f"{view}.*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    return hits[0] if hits else None


def image_for(device, view):
    """Return (image path, raw view name) or (None, None)."""
    slug = device["id"]
    if view == "top" and device.get("form_factor") == "clamshell":
        # A front render of a clamshell shows the lid open, so it can never
        # give the closed footprint. Trace only from a lid-closed render.
        img = find_image(slug, "closed_top")
        return (img, "closed_top") if img else (None, None)
    img = find_image(slug, view)
    return (img, view) if img else (None, None)


def trace_dims(device, view, raw_view):
    """Return (w, h) in mm that the traced image must match."""
    dims = device["dims_mm"]
    hand = dims["handheld"]
    if view == "side":
        # A real profile shows the grips, so compare against d_max when the
        # vendor gives one. Box side views still use the thin body d.
        return hand["h"], hand.get("d_max") or hand["d"]
    if raw_view == "closed_top" and dims.get("closed"):
        return dims["closed"]["w"], dims["closed"]["h"]
    return hand["w"], hand["h"]


def image_url(slug, raw_view):
    """Return the download URL from images/raw/<slug>/meta.json, or None."""
    meta_path = RAW_DIR / slug / "meta.json"
    try:
        meta = json.loads(meta_path.read_text())
        url = meta.get(raw_view, {}).get("url")
    except (OSError, json.JSONDecodeError, AttributeError):
        return None
    return url if isinstance(url, str) and url.startswith(("http://", "https://")) else None


def run_tracer(img, w, h, out, slug, view, source):
    """Run the tracer in an isolated process. Return (ok, message)."""
    cmd = [
        sys.executable, "-I", str(TRACER), str(img),
        "--w", f"{w:g}", "--h", f"{h:g}", "--out", str(out),
        "--slug", slug, "--view", view,
    ]
    if source:
        cmd += ["--source", source]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TRACE_TIMEOUT_S, cwd=TRACER.parent)
    except subprocess.TimeoutExpired:
        return False, f"tracer timed out after {TRACE_TIMEOUT_S} s"
    msg = (r.stdout.strip() or r.stderr.strip()).splitlines()
    return r.returncode == 0, (msg[-1] if msg else f"tracer exit {r.returncode}")


def build_device(path, device):
    """Write the three views of one device. Return {view: index entry}."""
    slug = device["id"]
    entries = {}
    for view in VIEWS:
        out = OUT_DIR / f"{slug}.{view}.svg"
        img, raw_view = image_for(device, view)
        if img is not None:
            w, h = trace_dims(device, view, raw_view)
            url = image_url(slug, raw_view)
            ok, msg = run_tracer(img, float(w), float(h), out, slug, view, url)
            if ok:
                parsed = parse_svg(out)
                entries[view] = {"kind": "traced", "source": url, "aspect_err": parsed["aspect_err"]}
                print(f"  {view:6} traced from {raw_view}: aspect_err={parsed['aspect_err']:.3f}")
                continue
            print(f"  {view:6} trace failed ({img.name}): {msg}; using box")
        svg, _, _ = box_svg(device, view, device_source(path))
        write_atomic(out, svg)
        entries[view] = {"kind": "box", "source": None, "aspect_err": None}
        if img is None:
            print(f"  {view:6} box (no image)")
    return entries


def load_index(path):
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_index(path, idx):
    ordered = {s: {v: idx[s][v] for v in VIEWS if v in idx[s]} for s in sorted(idx)}
    write_atomic(path, json.dumps(ordered, indent=1) + "\n")


def merge():
    target = OUT_DIR / "index.json"
    idx = load_index(target)
    parts = sorted(OUT_DIR.glob("index.*.json"))
    for p in parts:
        for slug, views in load_index(p).items():
            if isinstance(views, dict):
                idx.setdefault(slug, {}).update(views)
        print(f"merged {p.name}")
    write_index(target, idx)
    print(f"{target.relative_to(ROOT)}: {len(idx)} device(s) from {len(parts)} part file(s)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Trace or box every device outline into outlines/.")
    ap.add_argument("--slugs", nargs="+", metavar="SLUG", help="only these device ids")
    ap.add_argument("--brand", metavar="DIR", help="only data/devices/<DIR>/")
    ap.add_argument("--index-name", metavar="NAME", help="write outlines/index.<NAME>.json instead of index.json")
    ap.add_argument("--merge", action="store_true", help="merge outlines/index.*.json into outlines/index.json and exit")
    args = ap.parse_args(argv)

    if args.merge:
        return merge()
    if args.index_name and not SLUG_RE.match(args.index_name):
        ap.error("--index-name must be lower-case letters, digits and dashes")

    paths = sorted(DEV_DIR.glob("*/*.json"))
    if args.brand:
        paths = [p for p in paths if p.parent.name == args.brand]
    if args.slugs:
        want = set(args.slugs)
        paths = [p for p in paths if p.stem in want]
    if not paths:
        print("no device files match")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    built, errors = {}, 0
    for path in paths:
        try:
            device = json.loads(path.read_text())
            slug = device["id"]
            if slug != path.stem or not SLUG_RE.match(slug):
                raise ValueError(f"id {slug!r} does not match the file name")
            print(f"{slug}")
            built[slug] = build_device(path, device)
        except (OSError, ValueError, KeyError, TypeError) as e:
            errors += 1
            print(f"ERROR {path.relative_to(ROOT)}: {e}")

    name = f"index.{args.index_name}.json" if args.index_name else "index.json"
    index_path = OUT_DIR / name
    full_run = not (args.slugs or args.brand)
    idx = {} if full_run else load_index(index_path)
    idx.update(built)
    write_index(index_path, idx)

    traced = sum(1 for v in built.values() for e in v.values() if e["kind"] == "traced")
    boxes = sum(1 for v in built.values() for e in v.values() if e["kind"] == "box")
    print(f"\n{len(built)} device(s): {traced} traced view(s), {boxes} box view(s), {errors} error(s)"
          f" -> {index_path.relative_to(ROOT)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
