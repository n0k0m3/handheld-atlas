#!/usr/bin/env python3
"""Download device renders listed in images/manifest/*.json.

Usage:
    uv run fetch_images.py                       # every manifest, every slug
    uv run fetch_images.py --brand valve         # only images/manifest/valve.json
    uv run fetch_images.py --slugs a b c         # only these slugs
    uv run fetch_images.py --force               # download views that exist again

Manifest format, one file per brand:
    { "<slug>": { "page": url, "top": [url, ...], "bottom": [...], "side": [...],
                  "closed_top": [...], "note": null } }

Files merge by slug. URL lists union in file order (sorted file names).
For each slug and view the URLs are tried in order. The first image that
decodes is saved as images/raw/<slug>/<view>.<ext>. WebP, AVIF and GIF files
that OpenCV cannot decode are saved as PNG. images/raw/<slug>/meta.json
records {view: {url, bytes, content_type, file}}.

Downloads are untrusted data. This script only writes them; it never runs
or imports anything from images/raw/.
"""
import argparse
import io
import json
import pathlib
import sys
import time
from urllib.parse import urlparse

import cv2
import numpy as np
import requests
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "images" / "manifest"
RAW_DIR = ROOT / "images" / "raw"

VIEWS = ("top", "bottom", "side", "closed_top")
SLUG_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789-")
TIMEOUT = 20
MAX_BYTES = 40 * 1024 * 1024
PAUSE_S = 0.4  # between requests, to be polite
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "image/avif,image/webp,image/apng,image/png,image/jpeg,image/*;q=0.8,*/*;q=0.5",
    "Accept-Language": "en-US,en;q=0.9",
}
CT_EXT = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/pjpeg": "jpg",
    "image/webp": "webp",
    "image/avif": "avif",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/tiff": "tif",
}
# Formats that may need a PNG copy when OpenCV cannot decode them.
CONVERT = {"webp", "avif", "gif"}


def valid_slug(s):
    return isinstance(s, str) and s and set(s) <= SLUG_CHARS and not s.startswith("-") and "--" not in s


def sniff_ext(data):
    """Guess the image type from magic bytes. Return an ext or None."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if data[4:8] == b"ftyp" and data[8:12] in (b"avif", b"avis"):
        return "avif"
    if data.startswith(b"BM"):
        return "bmp"
    return None


def load_manifests(brand):
    """Return {slug: {"page": str|None, view: [urls]}} merged across files."""
    files = sorted(MANIFEST_DIR.glob("*.json"))
    if brand:
        files = [p for p in files if p.stem == brand]
        if not files:
            raise SystemExit(f"no manifest images/manifest/{brand}.json")
    merged = {}
    for path in files:
        try:
            with open(path) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARN  {path.name}: cannot parse: {e}")
            continue
        if not isinstance(data, dict):
            print(f"WARN  {path.name}: top level is not an object")
            continue
        for slug, entry in data.items():
            if not valid_slug(slug):
                print(f"WARN  {path.name}: bad slug {slug!r}, skipped")
                continue
            if not isinstance(entry, dict):
                continue
            m = merged.setdefault(slug, {"page": None, **{v: [] for v in VIEWS}})
            if not m["page"] and isinstance(entry.get("page"), str):
                m["page"] = entry["page"]
            for view in VIEWS:
                for url in entry.get(view) or []:
                    if isinstance(url, str) and urlparse(url).scheme in ("http", "https") and url not in m[view]:
                        m[view].append(url)
    return merged


def existing(slug_dir, view):
    """Return saved files for a view (any extension)."""
    return [p for p in slug_dir.glob(f"{view}.*") if p.is_file()]


def download(session, url, referer):
    """GET url. Return (bytes, content_type) or raise ValueError."""
    headers = {"Referer": referer} if referer else {}
    with session.get(url, headers=headers, timeout=TIMEOUT, stream=True, allow_redirects=True) as r:
        if r.status_code != 200:
            raise ValueError(f"HTTP {r.status_code}")
        if urlparse(r.url).scheme not in ("http", "https"):
            raise ValueError(f"redirect to {r.url}")
        ct = (r.headers.get("content-type") or "").split(";")[0].strip().lower()
        buf = io.BytesIO()
        for chunk in r.iter_content(64 * 1024):
            buf.write(chunk)
            if buf.tell() > MAX_BYTES:
                raise ValueError(f"over {MAX_BYTES // (1024 * 1024)} MB")
    return buf.getvalue(), ct


def to_saved(data, ct):
    """Decide the saved bytes and extension. Raise ValueError when not an image."""
    ext = CT_EXT.get(ct) or sniff_ext(data)
    if ext is None:
        raise ValueError(f"not a raster image (content-type {ct or 'none'})")
    # PIL must open it; that rejects HTML error pages served as image/*.
    try:
        with Image.open(io.BytesIO(data)) as im:
            im.load()
            size = im.size
            pil_png = None
            arr = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)
            if arr is None and ext in CONVERT:
                out = io.BytesIO()
                im.seek(0)
                frame = im.convert("RGBA") if im.mode not in ("RGB", "RGBA", "L", "LA") else im
                frame.save(out, "PNG")
                pil_png = out.getvalue()
    except (OSError, ValueError, Image.DecompressionBombError) as e:
        raise ValueError(f"cannot decode image: {e}") from e
    if size[0] < 32 or size[1] < 32:
        raise ValueError(f"image too small {size[0]}x{size[1]}")
    if pil_png is not None:
        return pil_png, "png", True
    if arr is None:
        raise ValueError(f"OpenCV cannot decode {ext}")
    return data, ext, False


def fetch_view(session, slug, view, urls, referer, force):
    """Try each URL. Return (status, meta entry or None, message)."""
    slug_dir = RAW_DIR / slug
    old = existing(slug_dir, view)
    if old and not force:
        return "skip", None, f"exists ({old[0].name})"
    errors = []
    for url in urls:
        try:
            data, ct = download(session, url, referer)
            saved, ext, converted = to_saved(data, ct)
        except (requests.RequestException, ValueError) as e:
            errors.append(f"{url}: {e}")
            time.sleep(PAUSE_S)
            continue
        slug_dir.mkdir(parents=True, exist_ok=True)
        for p in existing(slug_dir, view):
            p.unlink()
        out = slug_dir / f"{view}.{ext}"
        out.write_bytes(saved)
        time.sleep(PAUSE_S)
        note = " (converted to png)" if converted else ""
        meta = {"url": url, "bytes": len(data), "content_type": ct or None, "file": out.name}
        return "ok", meta, f"{out.relative_to(ROOT)} {len(data)} B{note}"
    return "fail", None, "; ".join(errors) if errors else "no URLs"


def update_meta(slug, entries):
    slug_dir = RAW_DIR / slug
    meta_path = slug_dir / "meta.json"
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
        except (OSError, json.JSONDecodeError):
            meta = {}
    meta.update(entries)
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Download device renders listed in images/manifest/*.json.")
    ap.add_argument("--slugs", nargs="+", metavar="SLUG", help="only these device slugs")
    ap.add_argument("--brand", metavar="STEM", help="only images/manifest/<STEM>.json")
    ap.add_argument("--force", action="store_true", help="download views that already exist again")
    args = ap.parse_args(argv)

    manifest = load_manifests(args.brand)
    slugs = sorted(manifest)
    if args.slugs:
        missing = [s for s in args.slugs if s not in manifest]
        for s in missing:
            print(f"WARN  {s}: not in any manifest")
        slugs = [s for s in slugs if s in set(args.slugs)]

    session = requests.Session()
    session.headers.update(HEADERS)
    counts = {"ok": 0, "skip": 0, "fail": 0}
    for slug in slugs:
        entry = manifest[slug]
        new_meta = {}
        for view in VIEWS:
            urls = entry[view]
            if not urls:
                continue
            status, meta, msg = fetch_view(session, slug, view, urls, entry["page"], args.force)
            counts[status] += 1
            print(f"{status.upper():5} {slug} {view}: {msg}")
            if meta:
                new_meta[view] = meta
        if new_meta:
            update_meta(slug, new_meta)
    print(f"\n{len(slugs)} slug(s): {counts['ok']} downloaded, {counts['skip']} skipped, {counts['fail']} failed")
    return 1 if counts["fail"] and not counts["ok"] and not counts["skip"] else 0


if __name__ == "__main__":
    sys.exit(main())
