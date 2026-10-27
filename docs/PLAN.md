# Handheld Atlas — x86 handheld gaming PC comparison

## Context

The user wants one database of x86 handheld gaming PCs (2022 to today). It must compare the fields they care about, in this priority order:

1. Weight, port spec (USB4 / TB4 / TB5 / USB 3.2), SSD form factor (2230 / 2242 / 2280).
2. True-scale size overlay in three views: top-down (required), bottom, side.
3. Joystick type (potentiometer / Hall / TMR) and trigger type.
4. CPU, iGPU, and PassMark scores per SoC.
5. Screen, battery, RAM, and other specs.

Decisions the user already made:

| Question | Answer |
|---|---|
| Scope | Broad: all x86 handhelds 2022+, about 35–45 rows |
| Unshipped devices | Include, flagged with a `status` column |
| Deliverable | Published dashboard artifact **and** a local static website |
| Overlay | Hybrid: spec-derived box for all 3 views, traced silhouette for top-down where a clean render exists |
| Who does what | Fable plans and QA's. Opus subagents crawl, trace, and build. |

Verified facts from the first search pass (2026-10-27):

- GPD Win Max 3 shipped 2026-09-02 (Strix Halo, 9.06" 165 Hz AMOLED, 97 Wh external battery, 815 g / 1220 g).
- GPD Win 5 shipped late 2025 (Strix Halo, 7" 120 Hz, 80 Wh external, 565 g / 915 g).
- OneXPlayer X2 Mini Pro shipped June 2026 (Ryzen AI Max+ 388, 8.8" 144 Hz OLED, $2499).
- Post-cutoff devices to include: Acer Predator Atlas 8 (Intel Arc G3 Extreme), ROG Xbox Ally X20 (launch 2026-10-15), MSI Claw 8 EX AI+, OneXFly Apex, AYANEO Next II.
- Python 3.14 resolves `opencv-python-headless`, `numpy`, `pillow`. `rembg` needs `onnxruntime`; use a 3.12 venv only if a device needs it.
- The Artifact "Dashboard" type exists, but it cannot host a custom SVG overlay tool and cannot be the local site. Build a plain HTML page and use the same build for both targets.

## Project layout

Path: `~/Programming/handheld-atlas/` (new, no git commits unless asked).

```
handheld-atlas/
  README.md                      how to re-run each step
  schema/device.schema.json      one row per hardware variant
  schema/soc.schema.json         one row per SoC
  data/devices/<brand>/<slug>.json
  data/socs/<slug>.json
  data/export/devices.csv, socs.csv, ports.csv
  images/manifest/<brand>.json   render URLs per device (one file per crawler, no shared writes)
  images/raw/<slug>/{top,bottom,side}.{png,jpg}   downloaded renders, untrusted, never published
  outlines/<slug>.{top,bottom,side}.svg           traced or box outlines, 1 unit = 1 mm
  outlines/index.json            which outlines are traced vs box
  site/CONTRACT.md               the Artifact page contract text, saved for the site agent
  scripts/                       uv project (pyproject.toml)
    discover/<brand>.md          agent notes: variant list per brand (one file per crawler)
    fetch_images.py              download renders listed in images/manifest/*.json
    trace_outline.py             image -> silhouette -> simplified SVG path scaled to mm
    box_outline.py               W x H x D -> rounded box + screen rect
    build_outlines.py            runs trace or box per device, writes outlines/index.json
    validate.py                  schema + range + source-URL checks
    export_csv.py                flattens JSON to CSV
    build_site.py                inlines data + outlines into one HTML file
  site/src/index.html            page template (vanilla JS + SVG, no CDN libs)
  site/dist/index.html           local website (full document)
  site/dist/artifact.html        same page as a fragment for the Artifact tool
```

## Data model

`device.schema.json` fields (every top-level fact carries a source URL in `sources[]`):

| Group | Fields |
|---|---|
| Identity | `id`, `brand`, `model`, `variant`, `status` (shipped / pre-order / announced), `announce_date`, `release_date`, `msrp_usd` |
| Size | `dims_mm {handheld: {w, h, d}, tablet_only?, closed?, with_keyboard?}` and `weight_g {handheld: {stated, measured, measured_source}, tablet_only?, without_battery?, closed?}`. `handheld` is required: controllers attached, battery attached, lid open for clamshells. The overlay and the default table column use `handheld`. Alternates are optional and shown as a tooltip. |
| Compute | `soc_id` (FK to socs), `ram {sizes_gb[], type, speed_mts, channels}` |
| Storage | `storage {slots[{form_factor: 2230|2242|2280, pcie_gen, lanes}], expansion[] (microSD, SD, mini SSD 1517)}` |
| Ports | `ports[] {kind: USB4|TB4|TB5|USB-C 3.2 Gen2|USB-C 3.2 Gen1|USB-A|OCuLink|HDMI|DP|3.5mm|RJ45, count, speed_gbps, dp_alt, pd_in_w, note}` |
| Screen | `screen {size_in, panel: IPS|LTPS|OLED|AMOLED|VA, res_w, res_h, refresh_hz, vrr, touch, nits_sdr, nits_peak}` |
| Battery | `battery {wh, removable, external, charge_w}` |
| Controls | `controls {stick_type: potentiometer|hall|tmr, trigger_type: potentiometer|hall|digital, trackpads, gyro, rear_buttons, keyboard, haptics}` |
| Other | `wireless {wifi, bt}`, `os[]`, `cooling`, `fingerprint`, `form_factor` (classic / clamshell / 3-in-1 / slider), `notes` |
| Provenance | `sources[] {field, url, accessed}` |

`soc.schema.json`: `id`, `vendor`, `name`, `codename`, `cores`, `threads`, `cpu_arch`, `base_ghz`, `boost_ghz`, `tdp_w {min, max}`, `process_nm`, `npu_tops`, `igpu {name, cu, arch, clock_mhz}`, `passmark {cpu_mark, single_thread, g3d_mark, cpu_url, gpu_url, samples, fetched}`, `notes` (state that PassMark samples mix TDPs and devices).

## Device list (starting set, agents confirm and extend)

| Group | Devices (one row per hardware variant) |
|---|---|
| Valve | Steam Deck LCD, Steam Deck OLED |
| ASUS | ROG Ally Z1, Ally Z1 Extreme, Ally X, ROG Xbox Ally (Z2 A), Xbox Ally X (Z2 Extreme), Xbox Ally X20 |
| Lenovo | Legion Go (Z1E), Legion Go S (Z2 Go, Z1E; Windows and SteamOS if hardware differs), Legion Go 2 |
| MSI | Claw A1M (135H, 155H), Claw 7 AI+, Claw 8 AI+, Claw A8, Claw 8 EX AI+ |
| GPD | Win 4 (2023 7840U, 2024 8840U, 2025 HX 370), Win Mini (2023, 2024, 2025), Win Max 2 (2023, 2024, 2025), Win 5, Win Max 3 |
| OneXPlayer | OneXPlayer 2, 2 Pro, OneXFly (7840U), X1 (155H, 8840U, HX 370), X1 Mini, X1 Mini Pro, X1 Pro, X2 Mini Pro, OneXFly F1 Pro, OneXFly Apex, G1 |
| AOKZOE | A1, A1 Pro, A1X, A2 |
| AYANEO | AYANEO 2, 2S, Geek, Geek 1S, Air Plus, Air 1S, Kun, Flip DS, Flip KB, Slide, AYANEO 3, Next II |
| Others | Zotac Zone, Acer Nitro Blaze 7, Blaze 8, Blaze 11, Predator Atlas 8 |

Exclude: ARM devices (AYANEO Pocket, Konkr, Odin), Android cloud handhelds, pre-2022 x86 (Win 3, original AYANEO), sub-$300 x86 (Anbernic Win600).

## Execution steps

### Step 1 — Scaffold (Fable, main thread)

1. Create the layout above. Write both JSON schemas and `README.md`.
2. `uv init` in `scripts/`, pin `opencv-python-headless`, `numpy`, `pillow`, `jsonschema`.
3. Write a minimal `validate.py` (schema check, range **warnings**, source-URL check) so every crawler can self-check from the start.
4. Seed `data/socs/` with stub files for the known SoC ids so agents use the same keys:
   `steam-deck-apu-lcd`, `steam-deck-apu-oled`, `z1`, `z1-extreme`, `z2-a`, `z2-go`, `z2-extreme`, `r7-6800u`, `r7-7840u`, `r7-8840u`, `r7-8840hs`, `ai9-hx370`, `ai9-365`, `ai-max-385`, `ai-max-388`, `ai-max-395`, `cu7-155h`, `cu5-135h`, `cu7-258v`, `arc-g3-extreme`.
5. Save the Artifact quickstart contract text to `site/CONTRACT.md`.
6. Hand-seed two device rows for toolchain tests: Steam Deck OLED (classic) and GPD Win Max 2 2025 (clamshell).

### Step 1b — Toolchain (1 Opus agent, runs with Steps 2–3)

Writes and tests every script except `validate.py` against the two seeded rows:

1. `fetch_images.py`: reads `images/manifest/*.json`, downloads to `images/raw/<slug>/`, never executes anything from there.
2. `trace_outline.py`: threshold on light background → largest external contour → `approxPolyDP` → SVG path scaled so the bounding width equals `dims_mm.handheld.w`. Sanity check: traced aspect vs `dims_mm` within 8 %.
3. `box_outline.py`: rounded box from `dims_mm.handheld` plus a screen rect from `screen.size_in` and the resolution aspect. Side view = h × d. Bottom view = mirrored top box.
4. `build_outlines.py`: trace or box per device and view, writes `outlines/index.json`.
5. `export_csv.py`: flattens devices, socs, and ports.
6. `build_site.py`: inlines data and outlines into `site/src/index.html`, writes `site/dist/index.html` and `site/dist/artifact.html`.
7. Extends `validate.py`: every `soc_id` resolves, every device has a top outline.
8. Returns: test output for the two seeds and the command to run each script.

### Step 2 — Crawl (6 Opus `general-purpose` agents in parallel)

One agent per brand group: (1) Valve + ASUS, (2) Lenovo + MSI, (3) GPD, (4) OneXPlayer + AOKZOE, (5) AYANEO, (6) Zotac + Acer.

Each agent brief:

1. Confirm the variant list for its brands. Add variants it finds (2022+). Record the list in `scripts/discover/<brand>.md`.
2. Source order per fact: official spec page → NotebookCheck review (measured weight, dims) → Liliputing / The Verge / Tom's Hardware (joystick and trigger tech) → manufacturer press kit.
3. Use Firecrawl scrape (markdown) for pages. If a page blocks, use the Playwright MCP on the shared agent Chrome (new tab, close only that tab).
4. Write `data/devices/<brand>/<slug>.json` per variant. Run `uv run validate.py`. Fix failures.
5. Record a candidate top-down render URL (and side / bottom if present) per device in `images/manifest/<brand>.json` (white background, straight-on, no hands).
6. Never write to `data/socs/`. Return any SoC id that is missing from the seed list; Fable forwards it to the SoC agent with SendMessage.
7. Return: file paths written, fields left `null` with the reason, and any conflicting values seen.

### Step 3 — SoC + PassMark (1 Opus agent, runs with Step 2)

1. Fill `data/socs/*.json` from AMD / Intel ARK and TechPowerUp.
2. Fetch PassMark CPU Mark, Single Thread, and sample count from cpubenchmark.net per SoC. Fetch G3D Mark from videocardbenchmark.net per iGPU (780M, 890M, 8050S, 8060S, Arc 140V, Arc B390, Steam Deck "Custom GPU 0405", etc.).
3. PassMark pages often sit behind Cloudflare. If Firecrawl scrape fails, use the Playwright MCP on the shared agent Chrome (new tab, close only that tab).
4. Map custom chips: Z1 Extreme has its own PassMark entry; Z2 A ≈ Steam Deck OLED APU; Z2 Go ≈ 6-core Zen 3+. Record the mapping and the caveat in `notes`.
5. Accept new SoC ids forwarded from the crawlers and add them.
6. Return: table of SoC → scores, and any SoC with no PassMark entry.

### Step 4 — Images and outlines (2 Opus agents, after Step 2)

Split devices in half by brand. Each agent uses the Step 1b scripts:

1. Run `fetch_images.py` for its manifests. Downloads go to `images/raw/<slug>/` only. Run Python on them with `-I`.
2. Run `build_outlines.py` for its devices. It traces the top view where a clean render exists and falls back to the box where the trace fails the 8 % aspect check.
3. Where the render is poor (hands, angle, shadow), look for a better one and update the manifest. Try at most two renders per device.
4. Side and bottom views: trace only when a straight-on render exists; otherwise box.
5. Each agent writes its own `outlines/index.<half>.json`; Fable merges them into `outlines/index.json`.
6. Return: counts of traced vs box per view, and devices with no usable image.

### Step 5 — Site build (1 Opus agent)

`site/src/index.html`, vanilla JS and inline SVG, no external scripts. The agent reads `site/CONTRACT.md` first (tokens on `:root`, dark-mode blocks, 16 px gutters, phone width) and loads the `dataviz` skill before it writes the SoC score bars. Sections:

1. **Header** with device count, last-crawl date, and a search box.
2. **Compare table**: sortable and filterable (brand, SoC, stick type, SSD form factor, status, screen panel). Columns default to the user's priority order: weight, ports, SSD, sticks, SoC, screen, battery. Column picker for the rest. Each cell shows its source link on hover/tap.
3. **Size overlay tool**: pick up to 6 devices, view toggle (top / bottom / side), align mode (center / bottom edge / left edge), mm grid and ruler, Steam Deck OLED as the default reference, per-device color with 35 % fill, legend with W × H × D and weight, badge showing traced vs box outline.
4. **SoC view**: table of SoC, iGPU, CPU Mark, Single Thread, G3D Mark, TDP range, with the devices that use it. Simple scaled bar per score column.
5. **Notes**: PassMark caveat, weight stated vs measured, data date, source list.

The Step 1b `build_site.py` inlines `data/**.json` and `outlines/*.svg` into the template and writes two files: `site/dist/index.html` (full document, opens from `file://` and `python -m http.server`) and `site/dist/artifact.html` (fragment: `<title>` and `<style>` first, no doctype / html / head / body). The site agent may extend the build script if the template needs it.

### Step 6 — QA and publish (Fable, main thread)

1. Run `validate.py` and `export_csv.py`.
2. Spot-check 6 rows against the official page: Win Max 3, Win 5, X2 Mini Pro, Legion Go 2, Xbox Ally X, Steam Deck OLED.
3. Screenshot `site/dist/index.html` with Playwright at desktop and 400 px width. Fix overflow.
4. Publish `site/dist/artifact.html` with the Artifact tool (icon `chart`, title "Handheld Atlas").
5. Write a memory note: project path, decisions, re-run steps.
6. Report: row count, traced vs box counts, null fields, artifact link, local path.

## Guardrails

- Downloaded renders stay in `images/raw/`. Scripts live in `scripts/`. Run Python on downloads with `-I`. Published outputs hold only derived SVG paths, never the renders.
- Every fact needs a source URL. A missing value stays `null` with a reason; never guess.
- One row per hardware variant. Same hardware with a different OS is one row with `os[]`.
- Weight: keep `stated` and `measured` separate. `handheld` config is required; record `without_battery` for GPD Win 5 / Max 3 / OneXFly Apex and `tablet_only` for 3-in-1s.
- Parallel agents never share an output file. Crawlers own `data/devices/<brand>/`, `images/manifest/<brand>.json`, `scripts/discover/<brand>.md`. The SoC agent owns `data/socs/`. The toolchain agent owns `scripts/`.
- Agents return paths and gaps, not data dumps.

## Verification

1. `uv run validate.py` passes with zero errors. Range checks are warnings only (weight 350–1500 g, W 180–400 mm, H 80–200 mm, D 12–55 mm; Steam Deck is 49 mm deep and 11" 3-in-1s with controllers are wide). Errors: schema, unresolved `soc_id`, missing top outline, missing source URL.
2. `site/dist/index.html` renders from `file://` with no console errors (Playwright check).
3. Overlay sanity: pick any two devices; the on-screen width ratio equals the `dims_mm.handheld.w` ratio within 1 %.
4. Artifact preview shows no overflow at phone width and no theme-ignoring colors.
5. Six spot-checked rows match their official pages.
