#!/usr/bin/env python3
"""Build the site from site/src/index.html and the JSON data.

Usage:
    uv run build_site.py

Steps:
1. Load every device and SoC JSON and every outlines/<slug>.<view>.svg.
2. Build one data object:
   {generated, devices[], socs[],
    outlines: {slug: {view: {kind, w, h, path, screen: {x,y,w,h}|null, source, aspect_err}}}}
   Outlines carry path data parsed from the SVG files, not raw SVG.
3. Replace the <!--ATLAS_DATA--> marker in the template with
   <script id="atlas-data" type="application/json">...</script>.
   "</" is escaped as "<\\/" and "<!--" as "\\u003c!--".

Writes:
    site/dist/artifact.html  the fragment for the claude.ai Artifact (no doctype/html/head/body)
    site/dist/index.html     the same fragment wrapped in a full document

The template must start with its head elements (title, meta, link, style).
The wrapper moves that leading run into <head> and the rest into <body>.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent))

from outline_svg import DEV_DIR, OUT_DIR, ROOT, SOC_DIR, VIEWS, parse_svg, write_atomic  # noqa: E402

TEMPLATE = ROOT / "site" / "src" / "index.html"
DIST = ROOT / "site" / "dist"
MARKER = "<!--ATLAS_DATA-->"
MAX_BYTES = 16 * 1024 * 1024
TITLE_SCAN = 8 * 1024

# Leading head elements of the fragment. Comments are allowed between them.
HEAD_PART = re.compile(
    r"\s*(?:<title\b[^>]*>.*?</title\s*>|<meta\b[^>]*>|<link\b[^>]*>"
    r"|<style\b[^>]*>.*?</style\s*>|<!--.*?-->)",
    re.S | re.I,
)
FORBIDDEN = re.compile(r"<!doctype|<html[\s>]|<head[\s>]|<body[\s>]", re.I)
DOC_HEAD = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
)


def load_json_dir(paths):
    rows = []
    for p in paths:
        try:
            rows.append(json.loads(p.read_text()))
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARN  {p.relative_to(ROOT)}: skipped, cannot parse: {e}")
    return rows


def load_outlines(device_ids):
    out = {}
    for slug in device_ids:
        for view in VIEWS:
            path = OUT_DIR / f"{slug}.{view}.svg"
            if not path.exists():
                continue
            try:
                o = parse_svg(path)
            except ValueError as e:
                print(f"WARN  {e}")
                continue
            if o["slug"] != slug or o["view"] != view:
                print(f"WARN  {path.name}: data-device/data-view do not match the file name, skipped")
                continue
            src = o["source"] if (o["source"] or "").startswith(("http://", "https://")) else None
            out.setdefault(slug, {})[view] = {
                "kind": o["kind"],
                "w": o["w"],
                "h": o["h"],
                "path": o["path"],
                "screen": o["screen"],
                "source": src,
                "aspect_err": o["aspect_err"],
            }
    return out


def data_script(data):
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    text = text.replace("</", "<\\/").replace("<!--", "\\u003c!--")
    return f'<script id="atlas-data" type="application/json">{text}</script>'


def split_head(fragment):
    """Return (leading head elements, rest)."""
    pos = 0
    while True:
        m = HEAD_PART.match(fragment, pos)
        if not m:
            break
        pos = m.end()
    return fragment[:pos].strip(), fragment[pos:].strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args(argv)

    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count(MARKER) != 1:
        print(f"ERROR {TEMPLATE.relative_to(ROOT)}: needs exactly one {MARKER} marker")
        return 1
    if FORBIDDEN.search(template):
        print(f"ERROR {TEMPLATE.relative_to(ROOT)}: a fragment must not contain doctype/html/head/body tags")
        return 1

    devices = load_json_dir(sorted(DEV_DIR.glob("*/*.json")))
    devices.sort(key=lambda d: (str(d.get("brand")).lower(), str(d.get("id"))))
    socs = load_json_dir(sorted(SOC_DIR.glob("*.json")))
    socs.sort(key=lambda s: str(s.get("id")))
    outlines = load_outlines([d.get("id") for d in devices if d.get("id")])

    data = {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "devices": devices,
        "socs": socs,
        "outlines": outlines,
    }
    fragment = template.replace(MARKER, data_script(data))
    head, body = split_head(fragment)
    if "<title" not in head.lower():
        print("WARN  the fragment does not start with a <title>")
    if "<title" not in fragment[:TITLE_SCAN].lower():
        print(f"WARN  <title> is not in the first {TITLE_SCAN // 1024} KB")
    document = f"{DOC_HEAD}{head}</head><body>{body}</body></html>\n"

    DIST.mkdir(parents=True, exist_ok=True)
    artifact, index = DIST / "artifact.html", DIST / "index.html"
    write_atomic(artifact, fragment)
    write_atomic(index, document)

    n_views = sum(len(v) for v in outlines.values())
    print(f"{len(devices)} device(s), {len(socs)} SoC(s), {n_views} outline view(s)")
    for p in (artifact, index):
        size = p.stat().st_size
        flag = "  OVER 16 MB" if size > MAX_BYTES else ""
        print(f"{p.relative_to(ROOT)}: {size:,} bytes ({size / 1024:.1f} KB){flag}")
    return 1 if artifact.stat().st_size > MAX_BYTES else 0


if __name__ == "__main__":
    sys.exit(main())
