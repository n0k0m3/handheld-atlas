# Handheld Atlas

A spec database of x86 handheld gaming PCs from 2022 onward, with a true-scale size overlay tool.

Reference site that inspired the project: https://retrocatalog.com. It lacks a layout / size comparison, does not separate TMR from Hall sticks, and misses some port and SSD details. This project fills those gaps.

## Layout

| Path | What |
|---|---|
| `schema/` | JSON Schemas for a device row and a SoC row |
| `data/devices/<brand>/<slug>.json` | One file per hardware variant |
| `data/socs/<slug>.json` | One file per SoC, with PassMark scores |
| `data/export/` | CSV exports built from the JSON |
| `images/manifest/<brand>.json` | Render URLs per device, written by the crawlers |
| `images/raw/<slug>/` | Downloaded renders. Untrusted. Never published. |
| `outlines/<slug>.{top,side,bottom}.svg` | Device outlines, 1 SVG unit = 1 mm |
| `outlines/index.json` | Which outlines are traced and which are spec boxes |
| `scripts/` | uv project with every script |
| `scripts/discover/<brand>.md` | Crawler notes: variant list and source URLs |
| `site/src/index.html` | Page template: Browse, Compare, Detail (v3 design) |
| `site/dist/index.html` | Local website (full document) |
| `site/dist/artifact.html` | Same page as a fragment for the claude.ai Artifact |
| `site/CONTRACT.md` | Page rules the artifact viewer enforces |

## Re-run

All commands run from `scripts/`.

1. `uv sync` — install the Python environment.
2. `uv run validate.py` — check every JSON file. Add `--outlines` to require a top outline per device.
3. `uv run fetch_images.py` — download renders listed in `images/manifest/*.json`.
4. `uv run build_outlines.py` — trace or box every device, write `outlines/`.
5. `uv run export_csv.py` — write `data/export/*.csv`.
6. `uv run build_site.py` — write `site/dist/index.html` and `site/dist/artifact.html`.
7. Open `site/dist/index.html` in a browser, or `python -m http.server -d ../site/dist`.
8. `uv run gen_socs.py ../data/socs` — rebuild every SoC file from the embedded table (edit the table in the script to refresh PassMark scores).
9. `uv run preview_outline.py --slugs <slug> ... --view top --out /tmp/sheet.png` — draw outlines on one sheet for a visual check.

Parallel outline workers: run `build_outlines.py --brand <x> --index-name <n>` per worker, then `build_outlines.py --merge`. A single run with no filter rebuilds everything and writes `outlines/index.json` directly.

## Rules

- Every fact carries a source URL in `sources[]`. A missing value stays `null` with an `unresolved[]` entry.
- One row per hardware variant. Same hardware with a different OS is one row.
- `dims_mm.handheld` and `weight_g.handheld` describe the device as held: controllers on, battery on, lid open.
- `stick_type` separates `potentiometer`, `hall`, and `tmr`.
- The site list and compare grid show the measured weight where a reviewer weighed a unit, else the stated weight. The device sheet shows both.
- PassMark scores mix TDPs and host devices. Treat them as a rough guide only.
