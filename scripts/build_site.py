#!/usr/bin/env python3
"""Build the site from site/src/index.html and the JSON data.

Usage:
    uv run build_site.py
    uv run build_site.py --pages DIR --site-url https://handheld-atlas.surge.sh

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

The full document carries <html data-routing="path">, so the deployed site
uses real paths (/browse, /compare?d=..., /<device-id>). The fragment has no
<html> tag and keeps hash tokens, which the Artifact viewer needs.

The template must start with its head elements (title, meta, link, style).
The wrapper moves that leading run into <head> and the rest into <body>.

--pages DIR also writes the surge.sh site to DIR (the Deploy workflow uses
it; nothing in DIR is committed). Link preview bots do not run JavaScript, so
every screen gets its own small page with its own title, description and
Open Graph tags: index.html, browse.html, compare.html, one
<device-id>.html per device, and 200.html, the surge fallback for any other
path. surge serves <name>.html at /<name>. DIR should be a new folder: the
build adds files and removes none. The pages share atlas.css,
atlas.js and atlas-data.js (window.ATLAS_DATA), so each page stays small.
og.png, the preview image, comes from site/static/og.png.
"""
import argparse
import datetime
import hashlib
import html
import json
import math
import pathlib
import re
import shutil
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
    '<!doctype html><html lang="en" data-routing="path"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
)

# --pages: the surge.sh site.
OG_IMAGE = ROOT / "site" / "static" / "og.png"
OG_W, OG_H = 1200, 630
SITE = "Handheld Atlas"
# Every msrp_type except "msrp" names its kind, as the page's * mark does.
PRICE_KIND = {"crowdfunding": "crowdfunding price", "preorder": "pre-order price", "sale": "launch discount price", "store": "store price"}
INLINE_SCRIPT = re.compile(r"<script>(.*?)</script>", re.S)
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.S | re.I)
TITLE = re.compile(r"<title\b[^>]*>.*?</title\s*>", re.S | re.I)
DESC = re.compile(r'<meta name="description" content="([^"]*)">', re.I)


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


def num_text(x):
    """341.69 -> '341.7', 26.0 -> '26'. Rounds like the page's mm(): Math.round(v * 10) / 10, so 26.15 -> '26.2'."""
    return f"{math.floor(float(x) * 10 + 0.5) / 10:g}"


def device_name(d):
    """Brand, model and variant: the same name the page's script puts in the tab title."""
    return " ".join(str(x) for x in (d.get("brand"), d.get("model"), d.get("variant")) if x)


def device_summary(d, soc_names):
    """One short line for the link preview: size, weight, screen, chip, price."""
    out = []
    dm = (d.get("dims_mm") or {}).get("handheld") or {}
    wt = (d.get("weight_g") or {}).get("handheld") or {}
    grams = wt.get("measured") if wt.get("measured") is not None else wt.get("stated")
    size = " × ".join(num_text(dm[k]) for k in ("w", "h", "d")) + " mm" if all(dm.get(k) is not None for k in ("w", "h", "d")) else None
    pack = " with battery pack" if (d.get("battery") or {}).get("external") else ""
    first = ", ".join(x for x in (size, f"{math.floor(grams + 0.5):,} g{pack}" if grams is not None else None) if x)
    if first:
        out.append(first)
    s = d.get("screen") or {}
    scr = " ".join(x for x in (
        f"{s['size_in']:g}″" if s.get("size_in") is not None else None,
        f"{s['res_w']}×{s['res_h']}" if s.get("res_w") and s.get("res_h") else None,
        f"{s['refresh_hz']} Hz" if s.get("refresh_hz") else None,
    ) if x)
    if scr:
        out.append(scr + " screen")
    if soc_names.get(d.get("soc_id")):
        out.append(soc_names[d["soc_id"]])
    if d.get("msrp_usd") is not None:
        kind = PRICE_KIND.get(d.get("msrp_type"))
        out.append(f"${math.floor(d['msrp_usd'] + 0.5):,}" + (f" {kind}" if kind else ""))
    return ". ".join(out) + "." if out else "An x86 handheld gaming PC."


def write_pages(out_dir, site_url, head, body, data_js, devices, soc_names):
    """Write the surge.sh site: shared assets plus one small page per screen."""
    if not OG_IMAGE.is_file():
        raise SystemExit(f"ERROR {OG_IMAGE.relative_to(ROOT)} is missing")
    scripts = INLINE_SCRIPT.findall(body)
    if len(scripts) != 1 or not STYLE.search(head):
        raise SystemExit("ERROR --pages needs exactly one inline <script> and one <style> in the template")
    assets = {"atlas.css": STYLE.search(head).group(1), "atlas.js": scripts[0], "atlas-data.js": data_js}
    out_dir.mkdir(parents=True, exist_ok=True)
    ver = {}
    for name, text in assets.items():
        write_atomic(out_dir / name, text)
        ver[name] = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    shutil.copyfile(OG_IMAGE, out_dir / "og.png")

    site_desc = (DESC.search(head) or [None, ""])[1]
    # The template's title and description give way to each page's own; the style becomes a link to the shared file.
    rest = DESC.sub("", TITLE.sub("", head))
    rest = STYLE.sub(f'<link rel="stylesheet" href="/atlas.css?v={ver["atlas.css"]}">', rest)
    page_body = INLINE_SCRIPT.sub(lambda m: f'<script src="/atlas.js?v={ver["atlas.js"]}"></script>', body)
    page_body = page_body.replace(MARKER, f'<script src="/atlas-data.js?v={ver["atlas-data.js"]}"></script>')
    e = lambda s: html.escape(s, quote=True)  # noqa: E731

    def page(name, title, og_title, desc, path):
        tags = [
            f"<title>{html.escape(title)}</title>",
            f'<meta name="description" content="{e(desc)}">',
            '<meta property="og:type" content="website">',
            f'<meta property="og:site_name" content="{SITE}">',
            f'<meta property="og:title" content="{e(og_title)}">',
            f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:image" content="{e(site_url + "/og.png")}">',
            f'<meta property="og:image:width" content="{OG_W}">',
            f'<meta property="og:image:height" content="{OG_H}">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
        # 200.html answers any unknown path, and browse.html and compare.html carry their content in
        # the query, so they claim no address of their own: a static og:url or canonical link would drop
        # the query when Facebook or Chrome for Android shares the page.
        if path is not None:
            tags += [f'<meta property="og:url" content="{e(site_url + path)}">', f'<link rel="canonical" href="{e(site_url + path)}">']
        write_atomic(out_dir / name, f"{DOC_HEAD}{''.join(tags)}{rest}</head><body>{page_body}</body></html>\n")

    # Titles match titleFor() in the page script, so the tab title does not change on load.
    page("index.html", SITE, SITE, site_desc, "/")
    page("200.html", SITE, SITE, site_desc, None)
    page("browse.html", f"Browse handhelds · {SITE}", "Browse handhelds",
         "Filter x86 handheld gaming PCs by price, size, weight, chip, screen, battery, controls and ports.", None)
    page("compare.html", f"Compare handhelds · {SITE}", "Compare handhelds",
         "Compare up to eight x86 handhelds: outlines at true scale, weight, and every spec side by side.", None)
    for d in devices:
        name = device_name(d)
        page(f"{d['id']}.html", f"{name} · {SITE}", name, device_summary(d, soc_names), f"/{d['id']}")
    return 4 + len(devices)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages", type=pathlib.Path, help="also write the surge.sh site (one page per screen) to this folder")
    ap.add_argument("--site-url", help="the site's address without a trailing slash, for canonical and Open Graph URLs")
    args = ap.parse_args(argv)
    if args.pages and not args.site_url:
        ap.error("--pages needs --site-url")

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
    if args.pages:
        t_head, t_body = split_head(template)
        data_js = "window.ATLAS_DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
        n = write_pages(args.pages, args.site_url.rstrip("/"), t_head, t_body, data_js,
                        [d for d in devices if d.get("id")], {s.get("id"): s.get("name") for s in socs})
        total = sum(p.stat().st_size for p in args.pages.iterdir() if p.is_file())
        print(f"{args.pages}: {n} page(s), {total / 1024:.0f} KB in all")
    return 1 if artifact.stat().st_size > MAX_BYTES else 0


if __name__ == "__main__":
    sys.exit(main())
