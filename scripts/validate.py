#!/usr/bin/env python3
"""Validate device and SoC JSON files against the schemas.

Usage:
    uv run validate.py                 # every file under data/devices and data/socs
    uv run validate.py path/to/a.json  # one or more files
    uv run validate.py --outlines      # also require outlines/<id>.top.svg per device

Errors exit 1. Range checks and undocumented nulls are warnings only.
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
DEV_DIR = ROOT / "data" / "devices"
SOC_DIR = ROOT / "data" / "socs"
OUT_DIR = ROOT / "outlines"

# (low, high) inclusive. Outside the range is a warning, not an error.
RANGES = {
    "weight_g.handheld.stated": (350, 1500),
    "weight_g.handheld.measured": (350, 1500),
    "dims_mm.handheld.w": (180, 400),
    "dims_mm.handheld.h": (80, 200),
    "dims_mm.handheld.d": (12, 55),
    "screen.size_in": (5, 12),
    "screen.refresh_hz": (60, 240),
    "battery.wh": (30, 130),
}

# Every device needs a source entry for each of these groups,
# or one "*" source (the official spec page) that covers all of them.
SOURCE_GROUPS = ["dims_mm", "weight_g", "soc_id", "storage", "ports", "screen", "battery", "controls"]


def load_schema(name):
    with open(SCHEMA_DIR / name) as f:
        return Draft202012Validator(json.load(f))


def get_path(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def null_leaves(obj, prefix=""):
    """Yield dot paths of every null leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from null_leaves(v, f"{prefix}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from null_leaves(v, f"{prefix}{i}.")
    elif obj is None:
        yield prefix.rstrip(".")


def check_device(path, data, soc_ids, want_outlines, errors, warns):
    if data.get("id") != path.stem:
        errors.append(f"{path}: id '{data.get('id')}' does not match file name '{path.stem}'")
    if data.get("soc_id") not in soc_ids:
        errors.append(f"{path}: soc_id '{data.get('soc_id')}' has no file in data/socs/")

    fields = {s.get("field") for s in data.get("sources", [])}
    if "*" not in fields:
        for g in SOURCE_GROUPS:
            if not any(f == g or f.startswith(g + ".") for f in fields):
                errors.append(f"{path}: no source for '{g}' (add a '*' source or one per group)")

    for dotted, (lo, hi) in RANGES.items():
        v = get_path(data, dotted)
        if isinstance(v, (int, float)) and not (lo <= v <= hi):
            warns.append(f"{path}: {dotted}={v} outside {lo}-{hi}")

    unresolved = {u["field"] for u in data.get("unresolved", [])}
    undocumented = [
        p for p in null_leaves(data)
        if not any(p == u or p.startswith(u + ".") or u.startswith(p) for u in unresolved)
        and not p.split(".")[-1] in {"note", "notes", "variant", "stick_note", "measured_source", "mapping_note", "process_note"}
    ]
    if undocumented:
        warns.append(f"{path}: {len(undocumented)} null field(s) without an unresolved entry: {', '.join(undocumented[:6])}{' ...' if len(undocumented) > 6 else ''}")

    if want_outlines:
        top = OUT_DIR / f"{data.get('id')}.top.svg"
        if not top.exists():
            errors.append(f"{path}: missing {top.relative_to(ROOT)}")


def check_soc(path, data, errors, warns):
    if data.get("id") != path.stem:
        errors.append(f"{path}: id '{data.get('id')}' does not match file name '{path.stem}'")
    pm = data.get("passmark", {})
    if pm.get("cpu_mark") is None:
        warns.append(f"{path}: passmark.cpu_mark is null")
    if pm.get("g3d_mark") is None:
        warns.append(f"{path}: passmark.g3d_mark is null")


def main(argv):
    want_outlines = "--outlines" in argv
    files = [pathlib.Path(a) for a in argv if not a.startswith("--")]
    if not files:
        files = sorted(DEV_DIR.rglob("*.json")) + sorted(SOC_DIR.glob("*.json"))

    dev_schema = load_schema("device.schema.json")
    soc_schema = load_schema("soc.schema.json")
    soc_ids = {p.stem for p in SOC_DIR.glob("*.json")}

    errors, warns = [], []
    n_dev = n_soc = 0
    for path in files:
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{path}: cannot parse JSON: {e}")
            continue
        is_soc = SOC_DIR in path.resolve().parents
        schema = soc_schema if is_soc else dev_schema
        for err in sorted(schema.iter_errors(data), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{path}: schema: {loc}: {err.message[:160]}")
        if is_soc:
            n_soc += 1
            check_soc(path, data, errors, warns)
        else:
            n_dev += 1
            check_device(path, data, soc_ids, want_outlines, errors, warns)

    for w in warns:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{n_dev} device file(s), {n_soc} SoC file(s): {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
