"""Shared helpers for the outline SVG format.

The tracer, the box builder, the outline builder and the site builder
import this module. It holds the one writer and the one parser for
outlines/<slug>.<view>.svg, so the format cannot drift between scripts.

Format rules (see outlines/FORMAT.md):
- 1 SVG unit = 1 mm. Origin = top-left of the outline bounding box.
- One <path> with absolute M / L / Z commands only, coordinates to 0.1 mm.
- An optional <rect class="screen"> for box outlines of the top view.

This module imports only the standard library. It reads no image files.
"""
import html
import os
import pathlib
import re
import tempfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEV_DIR = ROOT / "data" / "devices"
SOC_DIR = ROOT / "data" / "socs"
OUT_DIR = ROOT / "outlines"
RAW_DIR = ROOT / "images" / "raw"

SVG_NS = "http://www.w3.org/2000/svg"
VIEWS = ("top", "side", "bottom")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_PATH_BYTES = 4096


def fmt(v):
    """Round to 0.1 and drop a trailing '.0'. -0 becomes 0."""
    s = f"{round(float(v), 1):.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    return "0" if s == "-0" else s


def path_from_points(points):
    """Return 'M x y L x y ... Z' for a closed polygon in mm."""
    parts = []
    last = None
    for x, y in points:
        cur = (fmt(x), fmt(y))
        if cur == last:
            continue
        parts.append(f"{cur[0]} {cur[1]}")
        last = cur
    if len(parts) > 1 and parts[0] == parts[-1]:
        parts.pop()
    return "M" + "L".join(parts) + "Z"


def svg_text(slug, view, kind, w, h, d, source=None, aspect_err=None, screen=None):
    """Build the SVG string. screen is (x, y, w, h) in mm or None."""
    attrs = [
        f'xmlns="{SVG_NS}"',
        f'viewBox="0 0 {fmt(w)} {fmt(h)}"',
        f'width="{fmt(w)}mm"',
        f'height="{fmt(h)}mm"',
        f'data-device="{html.escape(slug)}"',
        f'data-view="{html.escape(view)}"',
        f'data-kind="{html.escape(kind)}"',
        f'data-w="{fmt(w)}"',
        f'data-h="{fmt(h)}"',
    ]
    if aspect_err is not None:
        attrs.append(f'data-aspect-err="{aspect_err:.3f}"')
    if source:
        attrs.append(f'data-source="{html.escape(str(source), quote=True)}"')
    body = [f'<path d="{d}" fill="currentColor"/>']
    if screen is not None:
        sx, sy, sw, sh = screen
        # White stroke so the screen shows in a plain SVG viewer.
        # The site draws the screen from parsed numbers, not from this style.
        body.append(
            f'<rect class="screen" x="{fmt(sx)}" y="{fmt(sy)}" width="{fmt(sw)}" height="{fmt(sh)}"'
            ' fill="none" stroke="#fff" stroke-width="0.8"/>'
        )
    return f"<svg {' '.join(attrs)}>{''.join(body)}</svg>\n"


def write_atomic(path, text):
    """Write text to path through a temp file in the same directory."""
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        # mkstemp makes the file 0600. Give it the normal mode for new files.
        umask = os.umask(0)
        os.umask(umask)
        os.chmod(tmp, 0o666 & ~umask)
        os.replace(tmp, path)
    except BaseException:
        pathlib.Path(tmp).unlink(missing_ok=True)
        raise


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def parse_svg(path):
    """Read one outline SVG. Return a dict or raise ValueError."""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        raise ValueError(f"{path}: cannot parse SVG: {e}") from e
    if root.tag != f"{{{SVG_NS}}}svg":
        raise ValueError(f"{path}: root element is not <svg>")
    p = root.find(f"{{{SVG_NS}}}path")
    if p is None or not p.get("d"):
        raise ValueError(f"{path}: no <path d>")
    screen = None
    for r in root.iter(f"{{{SVG_NS}}}rect"):
        if "screen" in (r.get("class") or "").split():
            vals = [_num(r.get(k)) for k in ("x", "y", "width", "height")]
            if None not in vals:
                screen = dict(zip(("x", "y", "w", "h"), vals))
            break
    w, h = _num(root.get("data-w")), _num(root.get("data-h"))
    if w is None or h is None:
        raise ValueError(f"{path}: data-w / data-h missing")
    return {
        "slug": root.get("data-device"),
        "view": root.get("data-view"),
        "kind": root.get("data-kind"),
        "w": w,
        "h": h,
        "path": p.get("d"),
        "screen": screen,
        "source": root.get("data-source"),
        "aspect_err": _num(root.get("data-aspect-err")),
    }
