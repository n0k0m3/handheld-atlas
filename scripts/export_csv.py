#!/usr/bin/env python3
"""Export the device and SoC JSON rows to flat CSV files.

Usage:
    uv run export_csv.py

Writes:
    data/export/devices.csv  one row per device, flattened (see DEVICE_COLUMNS)
    data/export/socs.csv     one row per SoC, every schema field flattened
    data/export/ports.csv    one row per device port entry

Rules:
- null becomes an empty cell. Booleans are "true" / "false".
- Lists join with "; ".
- official_url is the first source with field "*".
Files that do not parse are skipped with a warning.
"""
import argparse
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEV_DIR = ROOT / "data" / "devices"
SOC_DIR = ROOT / "data" / "socs"
SCHEMA_DIR = ROOT / "schema"
EXPORT_DIR = ROOT / "data" / "export"

DEVICE_COLUMNS = [
    "id", "brand", "model", "variant", "status", "release_date", "msrp_usd", "form_factor",
    "w", "h", "d", "weight_stated", "weight_measured",
    "soc_id", "soc_name", "ram_sizes", "ram_type", "ram_speed",
    "ssd_slots", "expansion", "ports_summary",
    "has_tb4", "has_tb5", "has_usb4", "has_oculink",
    "screen_size", "panel", "res", "refresh", "vrr",
    "battery_wh", "external_battery", "stick_type", "trigger_type", "trackpads", "keyboard",
    "wifi", "os", "official_url",
]
PORT_COLUMNS = ["device_id", "kind", "count", "speed_gbps", "dp_alt", "pd_in_w", "location", "note"]

# Short port names for ports_summary. Kinds not listed print as is.
PORT_SHORT = {
    "USB-C 3.2 Gen2": "USB-C 3.2G2",
    "USB-C 3.2 Gen1": "USB-C 3.2G1",
    "USB-A 3.2 Gen2": "USB-A 3.2G2",
    "USB-A 3.2 Gen1": "USB-A 3.2G1",
    "USB-C unspecified": "USB-C",
    "USB-A unspecified": "USB-A",
}
# These kinds always show a count, even 1x. Other kinds show a count above 1.
COUNTED = ("USB", "TB")
# Kinds that print their link speed (example: "2x USB4 40G").
SPEED_KINDS = {"USB4", "USB4v2", "TB4", "TB5"}
# Card slots go in the expansion column, not in ports_summary.
NOT_IN_SUMMARY = {"microSD", "SD", "mini-ssd-1517"}
# Video kinds take a version from the note (example: note "HDMI 2.1").
VERSIONED = {"HDMI": "HDMI", "DP": "DP"}


def cell(v):
    """Format one value for CSV."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, list):
        return "; ".join(cell(x) for x in v)
    return str(v)


def g(obj, dotted):
    """Get a dot path from nested dicts, or None."""
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def load_rows(paths):
    rows = []
    for p in paths:
        try:
            rows.append((p, json.loads(p.read_text())))
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARN  {p.relative_to(ROOT)}: skipped, cannot parse: {e}")
    return rows


def ssd_slots(storage):
    """Example: '2280 PCIe4x4; 2230 PCIe4'."""
    out = []
    for s in (storage or {}).get("slots") or []:
        txt = s.get("form_factor") or "?"
        gen, lanes = s.get("pcie_gen"), s.get("lanes")
        if gen is not None:
            txt += f" PCIe{gen}" + (f"x{lanes}" if lanes else "")
        elif lanes:
            txt += f" x{lanes}"
        out.append(txt)
    return "; ".join(out)


def port_label(p):
    kind = p.get("kind") or "?"
    name = PORT_SHORT.get(kind, kind)
    if kind in VERSIONED:
        note = p.get("note") or ""
        word = VERSIONED[kind]
        if note.startswith(word + " "):
            name = note.split(",")[0].strip()
    if kind in SPEED_KINDS and p.get("speed_gbps"):
        name += f" {cell(p['speed_gbps'])}G"
    count = p.get("count") or 1
    if kind.startswith(COUNTED) or count > 1:
        name = f"{count}x {name}"
    return name


def ports_summary(ports):
    """Example: '2x USB4 40G; 2x USB-A 3.2G2; HDMI 2.1; OCuLink; 3.5mm'."""
    return "; ".join(port_label(p) for p in ports or [] if p.get("kind") not in NOT_IN_SUMMARY)


def official_url(sources):
    for s in sources or []:
        if s.get("field") == "*":
            return s.get("url")
    return None


def device_row(d, soc_names):
    kinds = {p.get("kind") for p in d.get("ports") or []}
    scr = d.get("screen") or {}
    rw, rh = scr.get("res_w"), scr.get("res_h")
    row = {
        "id": d.get("id"),
        "brand": d.get("brand"),
        "model": d.get("model"),
        "variant": d.get("variant"),
        "status": d.get("status"),
        "release_date": d.get("release_date"),
        "msrp_usd": d.get("msrp_usd"),
        "form_factor": d.get("form_factor"),
        "w": g(d, "dims_mm.handheld.w"),
        "h": g(d, "dims_mm.handheld.h"),
        "d": g(d, "dims_mm.handheld.d"),
        "weight_stated": g(d, "weight_g.handheld.stated"),
        "weight_measured": g(d, "weight_g.handheld.measured"),
        "soc_id": d.get("soc_id"),
        "soc_name": soc_names.get(d.get("soc_id")),
        "ram_sizes": g(d, "ram.sizes_gb"),
        "ram_type": g(d, "ram.type"),
        "ram_speed": g(d, "ram.speed_mts"),
        "ssd_slots": ssd_slots(d.get("storage")),
        "expansion": g(d, "storage.expansion"),
        "ports_summary": ports_summary(d.get("ports")),
        "has_tb4": "TB4" in kinds,
        "has_tb5": "TB5" in kinds,
        "has_usb4": bool(kinds & {"USB4", "USB4v2"}),
        "has_oculink": "OCuLink" in kinds,
        "screen_size": scr.get("size_in"),
        "panel": scr.get("panel"),
        "res": f"{rw}x{rh}" if rw and rh else None,
        "refresh": scr.get("refresh_hz"),
        "vrr": scr.get("vrr"),
        "battery_wh": g(d, "battery.wh"),
        "external_battery": g(d, "battery.external"),
        "stick_type": g(d, "controls.stick_type"),
        "trigger_type": g(d, "controls.trigger_type"),
        "trackpads": g(d, "controls.trackpads"),
        "keyboard": g(d, "controls.keyboard"),
        "wifi": g(d, "wireless.wifi"),
        "os": d.get("os"),
        "official_url": official_url(d.get("sources")),
    }
    return {k: cell(row[k]) for k in DEVICE_COLUMNS}


def soc_columns():
    """Flatten soc.schema.json properties in schema order. Example: tdp_w.max -> tdp_w_max."""
    schema = json.loads((SCHEMA_DIR / "soc.schema.json").read_text())
    cols = []

    def walk(props, prefix):
        for name, spec in props.items():
            if name in ("unresolved", "sources"):
                continue
            if spec.get("type") == "object" and "properties" in spec:
                walk(spec["properties"], f"{prefix}{name}.")
            else:
                cols.append(f"{prefix}{name}")

    walk(schema["properties"], "")
    return cols + ["source_url"]


def soc_row(s, cols):
    sources = s.get("sources") or []
    # Prefer the "*" source. Else take the first source.
    src = official_url(sources) or (sources[0].get("url") if sources else None)
    row = {c: cell(src if c == "source_url" else g(s, c)) for c in cols}
    return {c.replace(".", "_"): v for c, v in row.items()}


def write_csv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{path.relative_to(ROOT)}: {len(rows)} row(s)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args(argv)

    socs = load_rows(sorted(SOC_DIR.glob("*.json")))
    devices = load_rows(sorted(DEV_DIR.glob("*/*.json")))
    soc_names = {s.get("id"): s.get("name") for _, s in socs}

    dev_rows, port_rows = [], []
    for _, d in sorted(devices, key=lambda r: (str(r[1].get("brand")).lower(), str(r[1].get("id")))):
        dev_rows.append(device_row(d, soc_names))
        for p in d.get("ports") or []:
            port_rows.append({c: cell(d.get("id") if c == "device_id" else p.get(c)) for c in PORT_COLUMNS})

    cols = soc_columns()
    soc_rows = [soc_row(s, cols) for _, s in sorted(socs, key=lambda r: str(r[1].get("id")))]

    write_csv(EXPORT_DIR / "devices.csv", DEVICE_COLUMNS, dev_rows)
    write_csv(EXPORT_DIR / "socs.csv", [c.replace(".", "_") for c in cols], soc_rows)
    write_csv(EXPORT_DIR / "ports.csv", PORT_COLUMNS, port_rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
