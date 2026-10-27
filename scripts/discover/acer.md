# Acer: crawler notes

Crawled on 2026-10-27.

## Variant list

| Row id | Model | SoC id | Status | Release | Launch price (base) |
|---|---|---|---|---|---|
| `acer-nitro-blaze-7` | Nitro Blaze 7 (GN771) | `r7-8840hs` | shipped | not found | no US price (EU EUR 849 / 512 GB; UK GBP 699 / 1 TB) |
| `acer-nitro-blaze-8` | Nitro Blaze 8 (GN782U) | `r7-8840hs` | announced | — | $899 announced |
| `acer-nitro-blaze-11` | Nitro Blaze 11 (GN7112U) | `r7-8840hs` | announced | — | $1,099 announced |
| `acer-predator-atlas-8` | Predator Atlas 8 (PA08-I51), Arc G3 Extreme | `arc-g3-extreme` | shipped | 2026-09 (UK) | $1,299.99 (24 GB / 512 GB) |
| `acer-predator-atlas-8-g3` | Predator Atlas 8 (PA08-I51), Arc G3 | `arc-g3` | announced (UK "Coming Soon") | — | no US price (UK GBP 999.99, 16 GB / 512 GB) |
| `acer-predator-atlas-7` | Predator Atlas 7 (PA07-I51), Arc G3 Extreme | `arc-g3-extreme` | announced | — | not announced |
| `acer-predator-atlas-7-g3` | Predator Atlas 7 (PA07-I51), Arc G3 | `arc-g3` | announced | — | not announced |

## Rows merged

- `acer-nitro-blaze-7`: 512 GB, 1 TB and 2 TB SKUs share one row.
- `acer-predator-atlas-8`: Arc G3 Extreme SKUs (24 / 32 GB, 512 GB US and 1 TB UK, 80 Wh) share one row.
- `acer-predator-atlas-8-g3`: Arc G3 SKUs (16 / 24 GB, 512 GB, 60 Wh) share one row. Acer UK SKU table via GamingOnLinux.
- `acer-predator-atlas-7-g3`: Arc G3 SKUs share one row. Acer publishes no RAM, storage or battery mapping per SoC, so those fields are empty or null.
- `acer-predator-atlas-7`: G3 Extreme SKUs share one row. The carbon-film vs TMR stick option is per SKU, and Acer gives no SKU-to-SoC mapping, so `stick_type` is null.

## Rows skipped

- None after the coordinator's follow-up. The Arc G3 (non-Extreme) rows were added once the SoC agent took on `arc-g3`.
- **Nitro Blaze Link (GN722)**: a game-streaming handheld (1 GB LPDDR4, 8 GB eMMC, Debian-based OS). It is not a standalone gaming PC.
- **Project DualPlay Mini**: concept only (IFA 2026).

## Status notes

- Nitro Blaze 7: sold in Europe and Taiwan (Acer UK store in stock, Acer Taiwan NT$24,900). No US launch. The first retail date was not found.
- Nitro Blaze 8 and 11: announced at CES 2025 for Q2 2025. VideoCardz (late 2025) found no retail listings. TechPowerUp and Guru3D (January 2026) report the US launch on hold.
- Predator Atlas 8: UK deliveries from mid-September 2026 (NotebookCheck 2026-09-19). US launch at $1,299.99 in late October 2026 (IGN).
- Predator Atlas 7: North America Q4 2026, EMEA November 2026.

## Conflicts recorded

- Atlas 8 sticks: the US product page and button diagram say TMR. The May 2026 press spec table says "Carbon Film" analog sticks. The row uses `tmr` and records the conflict.
- Atlas 8 RAM: resolved. The Acer UK SKU table has a 32 GB Extreme SKU, so the Extreme row lists 24 and 32 GB.
- Atlas 7 Extreme battery: Acer does not map battery to SoC. The row keeps 80 Wh / 750 g by analogy with the Atlas 8 and says so in `battery.note`.
- Blaze 8 / 11 SoC: Liliputing says Ryzen 7 8845HS. Acer says 8840HS. The rows use 8840HS.
- Blaze 11 refresh: Acer says 120 Hz. Some coverage says 144 Hz (that applies to the Blaze 8).
- Blaze 7 sticks: Acer's table names Hall only for the triggers, and Gizmodo says the sticks have no Hall sensors. No source names the sensor, so `stick_type` is null.

## Blocked sources

- Acer UK PDP pages render empty in the agent browser. Firecrawl read them.
- Best Buy: the agent browser tab was taken over by another session. The price came from a search snippet and IGN.
- The agent browser is shared with other crawlers, and its "current tab" moved between sessions. Firecrawl was used for the rest of the run.

## URLs used

| URL | Used for |
|---|---|
| https://news.acer.com/acer-debuts-its-first-handheld-gaming-pc-the-nitro-blaze-7 | Blaze 7 spec table (`*`) |
| https://www.acer.com/us-en/handheld-gaming/nitro-handheld-gaming/nitro-blaze-7 | Blaze 7 product page |
| https://gizmodo.com/acer-nitro-blaze-7-hands-on-staying-within-the-speed-limit-2000495157 | Blaze 7 sticks (not Hall), no back buttons |
| https://store.acer.com/en-gb/acer-nitro-blaze-acer-nitro-blaze-7-handheld-gn771-08hs7-black-dh-e4jem-001 | Blaze 7 status (in stock) |
| https://www.lowyat.net/2024/331441/acer-nitro-blaze-7-official/ | Blaze 7 EU price and 512 GB SKU |
| https://store.acer.com/zh-tw/gn771 | Blaze 7 Taiwan listing |
| https://news.acer.com/acer-expands-handheld-gaming-portfolio-with-new-nitro-blaze-8-and-nitro-blaze-11 | Blaze 8 / 11 spec tables, prices (`*`) |
| https://www.acer.com/us-en/handheld-gaming/nitro-handheld-gaming/nitro-blaze-8 | Blaze 8 product page |
| https://www.acer.com/us-en/handheld-gaming/nitro-handheld-gaming/nitro-blaze-11 | Blaze 11 product page (Hall sticks, 120 Hz) |
| https://liliputing.com/acer-expands-nitro-blaze-line-of-handheld-gaming-pcs-with-new-8-and-11-inch-models/ | Blaze 8 / 11 cross-check |
| https://videocardz.com/newz/amd-ryzen-powered-zotac-zone-pro-and-acer-nitro-blaze-miss-planned-launch-window | Blaze 8 / 11 status |
| https://www.techpowerup.com/344992/acer-nitro-blaze-gaming-handheld-on-ice | Blaze 8 / 11 status (2026-01) |
| https://news.acer.com/acer-expands-gaming-portfolio-with-predator-atlas-8-handheld-powered-by-intel | Atlas 8 spec table (`*`) |
| https://www.acer.com/us-en/predator/handheld-gaming/predator-atlas/predator-atlas-8 | Atlas 8 product page (TMR, Hall triggers, diagram) |
| https://www.acer.com/gb-en/predator/handheld-gaming/predator-atlas/predator-atlas-8/pdp/NH.U7XEF.001 | Atlas 8 G3 Extreme SKU spec (gyro, 24 GB, 1 TB) |
| https://www.notebookcheck.net/Acer-Predator-Atlas-8-First-units-arrive-initial-impressions-surface.1403487.0.html | Atlas 8 first UK deliveries, owner weight report |
| https://www.ign.com/articles/acer-predator-atlas-8-intel-arc-g3-extreme-handheld-gaming-pc-is-now-available | Atlas 8 US price |
| https://news.acer.com/acer-expands-gaming-handheld-portfolio-with-predator-atlas-7 | Atlas 7 spec table, availability (`*`) |
| https://www.gamingonlinux.com/2026/07/acer-predator-atlas-8-handheld-with-intel-arc-g3-gets-uk-pricing-and-launch-month/ | Atlas 8 UK SKU table (SoC, RAM, SSD, battery, price), "every Atlas 8" TMR |
| https://www.acer.com/gb-en/predator/handheld-gaming/predator-atlas/predator-atlas-8/pdp/NH.U7XEF.003 | Atlas 8 Arc G3 SKU spec (B370, 24 GB, 512 GB, gyro) |
| https://store.acer.com/en-gb/predator-atlas-8-handheld-pa08-i51-black | Atlas 8 Arc G3 status (Coming Soon, GBP 1,099.99) |
| https://www.acer.com/us-en/predator/handheld-gaming/predator-atlas/predator-atlas-7 | Atlas 7 product page (TMR on select models) |

## Sweep of other brands

The other crawlers cover Valve, ASUS, Lenovo, MSI, GPD, OneXPlayer, AOKZOE and AYANEO. This crawler checked the rest.

| Candidate | Result | Reason |
|---|---|---|
| AYN Loki Max (Ryzen 7 6800U) | added (`ayn/`) | Shipped June 2023, about $750 |
| SuiPlay0X1 (Ryzen 7 7840U) | added (`suiplay/`) | Shipped 2025, $599 |
| Orange Pi Neo (7840U and 8840U) | added (`orangepi/`, 2 rows) | Announced at $499 / $599, re-priced $450 / $550, on hold since March 2026 |
| TECNO Pocket Go | reported, not written | See `tecno.md` |
| AYN Loki Zero, Loki MiniPro | rejected | Below $450 |
| Anbernic Win600 | rejected | Below $450 (about $265-335) |
| Hyperstrix OmniOne | rejected | Intel N150, no game controls, crowdfunding |
| Acer Nitro Blaze Link | rejected | Streaming-only; not a standalone gaming PC |
| Tencent 3D One (Lunar Lake) | not pursued | China-only design related to the Blaze 11; no price or launch data found in the time budget |
