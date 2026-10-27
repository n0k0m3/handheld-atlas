# GPD crawler notes

Crawl date: 2026-10-27. Brand dir: `data/devices/gpd/`.

## Method

1. Find the product and tech-spec pages on gpd.hk. The site renders by script. Firecrawl renders it. WebFetch and curl get an empty shell.
2. Older model years are gone from gpd.hk. Use Wayback Machine copies of the official tech-spec pages. Download the raw copy (`id_` URL), unzip it, and read the text.
3. Use Liliputing, NotebookCheck and other press only for launch price, release month, and stick sensor type.
4. Write all rows with one generator script (kept in the session scratchpad, not in the repo).
5. Validate with `uv run validate.py ../data/devices/gpd/*.json`. The only warnings are Win Mini widths (168 / 172 mm) below the 180 mm range check. These widths are sourced. The `r5-8640u` and `i7-1260p` rows give a soc_id error until the SoC agent adds those files.

## Rows written (26)

| id | Model | SoC (soc_id) | Official spec source |
|---|---|---|---|
| gpd-win-4-2022 | Win 4 | Ryzen 7 6800U (r7-6800u) | Wayback gpdwin4techspecs 2023-05 (post-launch) and 2022-09 (pre-launch) |
| gpd-win-4-2023 | Win 4 | Ryzen 7 7840U (r7-7840u) | Wayback gpdwin4techspecs 2023-12 |
| gpd-win-4-2023-7640u | Win 4 | Ryzen 5 7640U (r5-7640u) | Wayback gpdwin4techspecs 2023-12 |
| gpd-win-4-2024 | Win 4 | Ryzen 7 8840U (r7-8840u) | Wayback gpdwin4techspecs 2024-04, plus gpdwin42025techspecs |
| gpd-win-4-2024-8640u | Win 4 | Ryzen 5 8640U (r5-8640u) | Wayback gpdwin4techspecs 2024-04 |
| gpd-win-4-2025 | Win 4 | Ryzen AI 9 HX 370 (ai9-hx370) | gpdwin42025techspecs |
| gpd-win-mini-2023 | Win Mini | Ryzen 7 7840U (r7-7840u) | Wayback gpdwinminitechspecssdfwerwer 2024-01 |
| gpd-win-mini-2023-7640u | Win Mini | Ryzen 5 7640U (r5-7640u) | same |
| gpd-win-mini-2024 | Win Mini | Ryzen 7 8840U (r7-8840u) | gpdwinminitechspecssdfwerwer (live) |
| gpd-win-mini-2024-8640u | Win Mini | Ryzen 5 8640U (r5-8640u) | gpdwinminitechspecssdfwerwer (live) |
| gpd-win-mini-2025 | Win Mini | Ryzen AI 9 HX 370 (ai9-hx370) | gpdwinmini2025techspecs |
| gpd-win-mini-2025-365 | Win Mini | Ryzen AI 9 365 (ai9-365) | gpdwinmini2025techspecs |
| gpd-win-mini-2025-8840u | Win Mini | Ryzen 7 8840U (r7-8840u) | gpdwinmini2025techspecs |
| gpd-win-max-2-2022 | Win Max 2 | Ryzen 7 6800U (r7-6800u) | Wayback gpdwinmax2techspecs 2022-12 |
| gpd-win-max-2-2022-1260p | Win Max 2 | Intel Core i7-1260P (i7-1260p) | Wayback gpdwinmax2techspecs 2022-12 |
| gpd-win-max-2-2023 | Win Max 2 | Ryzen 7 7840U (r7-7840u) | Wayback gpdwinmax2techspecs 2024-01 |
| gpd-win-max-2-2023-7640u | Win Max 2 | Ryzen 5 7640U (r5-7640u) | same |
| gpd-win-max-2-2024 | Win Max 2 | Ryzen 7 8840U (r7-8840u) | gpdwinmax2techspecs (live) |
| gpd-win-max-2-2024-8640u | Win Max 2 | Ryzen 5 8640U (r5-8640u) | gpdwinmax2techspecs (live) |
| gpd-win-max-2-2025 | Win Max 2 | Ryzen AI 9 HX 370 (ai9-hx370) | gpdwinmax22025techspecs (seed row replaced) |
| gpd-win-max-2-2025-8840u | Win Max 2 | Ryzen 7 8840U (r7-8840u) | gpdwinmax22025techspecs |
| gpd-win-5-385 | Win 5 | Ryzen AI Max 385 (ai-max-385) | Wayback gpdwin5techspecs 2025-09 |
| gpd-win-5-388 | Win 5 | Ryzen AI Max+ 388 (ai-max-388) | gpdwin5techspecs (live) |
| gpd-win-5-395 | Win 5 | Ryzen AI Max+ 395 (ai-max-395) | gpdwin5techspecs (live) |
| gpd-win-max-3-388 | Win Max 3 | Ryzen AI Max+ 388 (ai-max-388) | gpdwinmax3techspecs |
| gpd-win-max-3-395 | Win Max 3 | Ryzen AI Max+ 395 (ai-max-395) | gpdwinmax3techspecs |

Slug rule for extra SoC options: the main SoC keeps the brief slug. Other SoCs of the same model year get a chip suffix (`-7640u`, `-8640u`, `-365`, `-8840u`, `-1260p`). Win 5 slugs use the chip number (`-385`, `-388`, `-395`).

## Rows merged

- Win 4 (2025) with Ryzen 7 8840U is merged into `gpd-win-4-2024`. Size, weight, ports, screen and battery match the 2024 page. The 2025 page adds a 32 GB / 1 TB config and lists Wi-Fi 6E and BT 5.3. The row keeps the 2024 values and records the Wi-Fi difference in `conflicts[]`.

## Rows not merged (hardware differs)

- Win 4 (2022, 6800U) vs 2023: the 2022 model has a USB-A port and no OCuLink. Separate row.
- Win Mini (2025, 8840U) vs Win Mini (2024, 8840U): different shell (172 x 109 x 27 vs 168 x 109 x 26 mm), 2280 vs 2230 SSD, LPDDR5X-7500 vs LPDDR5-6400. Separate row.
- Win Max 2 (2025, 8840U) vs Win Max 2 (2024, 8840U): the 2025 page lists 2x USB4 and no USB-C 3.2 port, Wi-Fi 6E, LPDDR5X-7500. Separate row.
- Win Max 2 (2022, 6800U) vs 2023: the 2022 model has 3x USB-A 3.2 Gen1 and no OCuLink. Separate row.

## Variants skipped

| Variant | Reason |
|---|---|
| GPD Pocket 3 / Pocket 4 / MicroPC 2 / Duo | laptops without built-in game controls |
| GPD G1 / G2 | eGPU docks, not handhelds |
| GPD Win 3 | 2021, before the 2022 cut-off |

## Differences from the crawler brief

- Win Mini is a clamshell (hinged lid, 168 degree opening). The rows use `form_factor: clamshell`, not `classic`. `dims_mm.handheld` = `dims_mm.closed` = the closed footprint.
- Win 5 has one M.2 2280 slot, not two (official spec: "1 x M.2 NVMe 2280"). The mini SSD 1517 slot is the second storage slot.
- Win 5 now lists the 395 and 388. The 385 was the launch SKU (2025-09 Wayback page). A 388 SKU was added in 2026-09. Three rows.
- Win Max 3 lists 2280 (PCIe 4.0 x4) + 2230 (PCIe 4.0 x2) + microSD Express. The official pages list no mini SSD slot.
- Win 5 and Win Max 3 sticks are "capacitive joysticks" per GPD. GPD contrasts them with Hall sticks. `stick_type` = `capacitive` (enum added later). The Liliputing Strix Halo comparison lists Win 5 as "Hall joysticks"; that is a `conflicts[]` entry and the official value wins.
- Win 5 `dims_mm.handheld.d_max` = 42.3 mm, derived: 24.21 mm body + 18.1 mm pack. GPD gives no combined figure. Win Max 3 `d_max` stays null: GPD gives no pack thickness, and the module sits on the front edge (34 mm with and without modules).
- The 8640U rows have no USD price. Win 4 (2024) 8640U has no first-sale date. Win Max 2 (2024) 8640U rests on the official spec page only; no retail listing was found.
- Win Max 3 is not shipped at retail. China presale opened in 2026-09 (CNY 9,999 base). Indiegogo opened 2026-09-02. DroiX takes pre-orders and plans shipping from 2026-12-15. `status: pre-order`, `release_date: null`. This is the only model where the official "Release Date" month (August 2026) is treated as an announcement month and not as `release_date`.

## Field conventions used

- `release_date` = the "Launch Date" month on the official tech-spec page, unless a source shows later retail shipping. Other dates go in `conflicts[]`.
- `msrp_usd` = launch price of the base config for the row's SoC. For GPD this is almost always the Indiegogo price. Each row says which config the price is for.
- `ram.channels` = the value the row's main spec page states. GPD writes "quad 32-bit channels" on some pages and "dual channel" on others for the same 128-bit bus.
- `ram.soldered: true` for every row. All GPD rows use LPDDR5 or LPDDR5X, which is soldered by design. GPD does not state it.
- `ports` lists device ports only. Dock ports (Win 4, Win 5) are not counted.
- `controls.stick_type` for Win 4 = potentiometer. Source: China-Gadgets hands-on of the 6800U unit says the ALPS sticks are not Hall sticks. Later Win 4 spec pages list the same ALPS 3D joysticks.
- `controls.trigger_type` for Win Max 2 (2025) = potentiometer. Source: the WIN Max 3 comparison table calls the Win Max 2 (2025) trigger "linear trigger" and defines an ordinary linear trigger as potentiometer / carbon film. Other Win Max 2, Win 4 and Win Mini triggers stay `null` because GPD does not name the sensor.
- `weight_g.handheld.measured` is `null` on every row. No reviewer scale weight was fetched within the budget.

## URLs used

Official (gpd.hk, live):
- https://www.gpd.hk/gpdwin56773453f
- https://www.gpd.hk/gpdwin5techspecs34524234456
- https://www.gpd.hk/gpdwinmax3
- https://www.gpd.hk/gpdwinmax3techspecs
- https://www.gpd.hk/gpdwinmax3gellery
- https://www.gpd.hk/gpdwin42025
- https://www.gpd.hk/gpdwin42025techspecs
- https://www.gpd.hk/gpdwinmini2025
- https://www.gpd.hk/gpdwinmini2025techspecs
- https://www.gpd.hk/gpdwinminisdfewr (search excerpt)
- https://www.gpd.hk/gpdwinminitechspecssdfwerwer
- https://www.gpd.hk/gpdwinmax2 (search excerpt)
- https://www.gpd.hk/gpdwinmax2techspecs
- https://www.gpd.hk/gpdwinmax22025 (search excerpt)
- https://www.gpd.hk/gpdwinmax22025techspecs
- https://www.gpd.hk/ (Win Max 3 price table)
- https://www.gpd.hk/newsinfo/986178.html (Win 4 2025 price)

Official (Wayback copies):
- https://web.archive.org/web/20220930184835/https://gpd.hk/gpdwin4techspecs
- https://web.archive.org/web/20230516105947/https://gpd.hk/gpdwin4techspecs
- https://web.archive.org/web/20231204091925/https://gpd.hk/gpdwin4techspecs
- https://web.archive.org/web/20240425004609/https://gpd.hk/gpdwin4techspecs
- https://web.archive.org/web/20241105220542/https://gpd.hk/gpdwin4techspecs
- https://web.archive.org/web/20240105185847/https://gpd.hk/gpdwinminitechspecssdfwerwer
- https://web.archive.org/web/20221209000108/https://gpd.hk/gpdwinmax2techspecs
- https://web.archive.org/web/20230605173954/https://gpd.hk/gpdwinmax2techspecs
- https://web.archive.org/web/20240118103244/https://gpd.hk/gpdwinmax2techspecs
- https://web.archive.org/web/20250905070257/https://gpd.hk/gpdwin5techspecs34524234456
- https://web.archive.org/web/20251012081529/https://gpd.hk/gpdwin5techspecs34524234456

Press and reviews:
- https://www.china-gadgets.de/gpd-win-4-gaming-handheld-test/ (Win 4 ALPS sticks, not Hall)
- https://www.notebookcheck.net/GPD-Win-4-PSP-Vita-lookalike-launches-for-US-799-with-design-improvements-and-Radeon-680M-iGPU.675748.0.html
- https://www.notebookcheck.net/GPD-Win-4-2023-Launch-date-and-pricing-announced-for-refreshed-US-699-gaming-handheld.733696.0.html
- https://liliputing.com/the-gpd-win-4-2024-handheld-gaming-pc-is-now-available-with-a-ryzen-7-8840u-processor/
- https://liliputing.com/gpd-win-mini-to-sell-for-699-and-up-during-crowdfunding-handheld-gaming-pc-with-a-7-inch-screen-qwerty-keyboard-ryzen-7040-processor-and-clamshell-design/
- https://liliputing.com/gpd-win-mini-2024-is-a-mini-gaming-laptop-with-ryzen-7-8840u-and-7-inch-120-hz-vrr-display/
- https://www.notebookcheck.net/GPD-Win-Mini-2024-announced-with-updated-AMD-Ryzen-processors-and-ASUS-ROG-Ally-display.808867.0.html
- https://liliputing.com/gpd-win-mini-2025-handheld-gaming-pc-hits-indiegogo-for-769-and-up/
- https://www.notebookcheck.net/GPD-Win-Mini-2025-released-globally-in-fetching-new-colour-with-tweaked-design-improved-cooling-and-up-to-64-GB-of-RAM.946298.0.html
- https://liliputing.com/gpd-win-max-2-mini-gaming-laptop-with-ryzen-7-6800u-or-core-i7-1260p-hits-indiegogo-july-7-for-899-and-up-crowdfunding/
- https://www.notebookcheck.net/GPD-Win-Max-2-2023-launches-with-AMD-Phoenix-APU-and-other-upgrades.716634.0.html
- https://www.notebookcheck.net/2024-GPD-Win-Max-2-handheld-gaming-PC-with-AMD-Ryzen-7-8840U-goes-up-for-preorders-soon.822860.0.html
- https://liliputing.com/?p=174116 (Win Max 2 2025 prices)
- https://www.notebookcheck.net/GPD-Win-5-released-globally-with-AMD-Ryzen-AI-Max-395-and-up-to-64-GB-RAM.1123906.0.html
- https://tech-insider.org/gpd-win-5-ryzen-ai-max-388-1722-2026/
- https://www.notebookcheck.net/GPD-Win-Max-3-Powerful-gaming-handheld-now-available-with-up-to-128-GB-RAM-and-better-warranty-options-via-third-party.1429224.0.html
- https://www.technetbooks.com/2026/09/gpd-win-max-3-handheld-gaming-pc-opens.html (Win Max 3 China presale)
- https://www.tweaktown.com/news/107731/gpd-win-5-gaming-handheld-starts-at-1400-with-amd-ryzen-ai-max-385-apu-32gb-ram-1tb-ssd/index.html (Win 5 385 price conflict)
- https://www.gpd.hk/newsinfo/1028841.html (Win Mini 2025 release news, 2025-04-11)
- https://liliputing.com/amd-strix-halo-handheld-gaming-pc-spec-shoot-out-ayaneo-next-ii-vs-gpd-win-5-vs-onexfly-apex/ (Win 5 stick conflict)
- https://www.notebookcheck.net/GPD-Win-4-2024-AMD-Ryzen-7-8840U-refresh-launches-before-Ryzen-5-8640U-release.810169.0.html
- https://droix.net/product/gpd-win-4-2024 (8640U config listing)
- https://geizhals.at/gpd-win-mini-2024-a3218471.html (Win Mini 2024 8640U listing)

Image caveats for the outline builder:
- The Win 4 `top` image shows the slider open (keyboard visible). It does not match the closed 220 x 92 mm footprint in `dims_mm`. Box it or trace with care.
- The Win Max 2 and Win Mini `top` images show the lid open from the front. `closed_top` is empty for every clamshell.
- Win Max 3 has no image.

Images: `https://retrocatalog.com/images/retro-handheld_front_<slug>` for gpd-win-4, gpd-win-mini-2024, gpd-win-mini-2025, gpd-win-max-2, gpd-win-5. Retrocatalog has no Win Max 3 page and no per-year Win 4 or Win Max 2 pages. The gpd.hk gallery pages load images by script; the Win Max 3 gallery has lifestyle photos only.

## Blocked or weak sources

- gpd.hk with curl or WebFetch: returns a script shell only. Firecrawl works.
- WebFetch on notebookcheck.net returned HTTP 403 once. Firecrawl worked.
- Archived gpd.hk overview pages (not the tech-spec pages) hold no text, so the Win Mini 2023 VRR and L4/R4 location stay unresolved.
- Win Max 2 (2024) has no sourced USD launch price; only the China pre-sale price (CNY 6,399).
- The Win 5 388 release month and price come from one secondary article (Tech Insider, citing VideoCardz).
