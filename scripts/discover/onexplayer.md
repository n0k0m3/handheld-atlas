# OneXPlayer (One-Netbook) crawl notes

Accessed 2026-10-27. Brand dir: `data/devices/onexplayer/` (35 rows). AOKZOE is in `aokzoe.md`.

## Summary
- 35 rows written, one per SoC option. RAM and SSD sizes share a row.
- Part 3 (follow-up) added 9 rows after the SoC files for 255H, 125H, 228V, 1360P, 1195G7, HX 470, 1260P and 5800U became available. The skip tables in Part 1 and Part 2 are kept for history; Part 3 says which skips are now rows.
- Excluded by decision: OneXPlayer Mini with Pentium Gold 8505, OneXPlayer Mini with Celeron 7305, and the 8.4-inch OneXPlayer with Ryzen 7 4800U.
- Excluded models: Super X and Super V (tablets without game controllers), OneXSugar Sugar 1 and Wallet (Snapdragon), GI58P (custom-order link), M1, OneXStation, OneXGPU (not handhelds).
- The store spec tables are images. The `*` source of each row is the store product page (or a Wayback snapshot for discontinued models); its note names the spec image when one was read.

## Part 1: 2022-2025 models, X1 family, X1 Air / X2 Air

### Method

1. Pulled the current store catalog from `https://onexplayerstore.com/products.json?limit=250`.
2. Listed every historical store product handle from the Wayback CDX index (`onexplayerstore.com/products/` prefix).
3. Fetched archived product JSON (`<handle>.js`) or archived HTML for discontinued models.
4. Read spec-sheet images on the store pages where the specs are images (X2 Air, X1 Air key features).
5. Filled the remaining fields from Liliputing, NotebookCheck, DroiX, XDA, and PC Gamer.

### Rows written

| Row | SoC | Status | Main official source |
|---|---|---|---|
| onexplayer-mini-pro-6800u | r7-6800u | shipped 2022-10 | Archived store deposit page; specs via Liliputing copy of the One Netbook table |
| onexplayer-2 | r7-6800u | shipped 2023-03 | Archived store page (Mar 2023) |
| onexplayer-2-pro | r7-7840u | shipped 2023-08 | Archived store page (Dec 2023) |
| onexplayer-2-pro-8840u | r7-8840u | shipped 2024-03 | Archived store page (May 2024) |
| onexfly-7840u | r7-7840u | shipped 2023-10 | Archived store page with spec table (Sep 2023) |
| onexfly-8840u | r7-8840u | shipped 2024-07 | Archived store page (Aug 2024) |
| onexplayer-x1-155h | cu7-155h | shipped 2024-03 | Current store page `x1-155h` + archived `x1` page + Indiegogo |
| onexplayer-x1-8840u | r7-8840u | shipped 2024-06 | Archived store pre-sale page with spec list (Jul 2024) |
| onexplayer-x1-mini | r7-8840u | shipped 2024-07 | Archived store page (Jul 2024) |
| onexplayer-x1-mini-hx370 | ai9-hx370 | shipped 2025-06 | NotebookCheck news; no official HX 370 page found |
| onexplayer-x1-pro | ai9-hx370 | shipped 2025-01 | Archived store page (Jan 2025) + official refurb page |
| onexplayer-x1-air | cu7-258v | shipped 2025-09 | Archived store page (Dec 2025) + key-features image |
| onexplayer-x2-air | cu7-258v | shipped (date unknown) | Current store page + X2 Air spec-sheet image |

### Merges and splits

- RAM and SSD sizes share one row per SoC.
- X1 Mini HX 370 (2025) kept the "X1 Mini" name. It is a separate row because the SoC differs. No "X1 Mini Pro" exists.
- X1 Air vs X2 Air: the X2 Air store listing is the renamed X1 Air listing (same Shopify product, created 2025-09-02; X1 Air image file names reused; a Reddit thread says it looks the same). The official X2 Air spec sheet differs from X1 Air sources in three ways: M.2 2280 instead of 2230, one 5400 RPM fan instead of two 8500 RPM fans, 6.7 mm Hall sticks. So two rows were written. The X2 Air row notes that the revision is unconfirmed.
- No X1 Pro 8840U row. The X1 Pro store title says "HX 370/8840U", but no 8840U X1 Pro SKU was seen; the 8840U 10.95-inch model is the X1 8840U row.

### Skipped (no SoC file in data/socs/)

| Device | Exact chip | Evidence |
|---|---|---|
| OneXPlayer X1 (entry SKU, 2024) | Intel Core Ultra 5 125H | Store and Indiegogo 16GB/1TB SKU |
| OneXPlayer X1 Pro EVA limited edition (Apr 2025) | Intel Core Ultra 7 255H | NotebookCheck news; Thunderbolt 4 |
| OneXPlayer X1 Pro refresh (2026) | AMD Ryzen AI 9 HX 470 | Current store page |
| OneXPlayer X1 Air (entry SKU) | Intel Core Ultra 5 228V | Liliputing / NotebookCheck |
| OneXPlayer 2 Pro Intel ("2 PRO 8.4", refurb listing) | Intel Core i7-1360P | Store refurb listing |
| OneXPlayer Mini Pro Intel (2022) | Intel Core i7-1260P | Liliputing Aug 2022 |
| OneXPlayer Mini (2022-11) | Intel Pentium Gold 8505 | Liliputing Nov 2022 |
| OneXPlayer Mini (refurb listing) | Intel Celeron 7305 | Store refurb listing |
| OneXPlayer Mini (Jan 2022) and OneXPlayer 1S / 8.4-inch | Intel Core i7-1195G7 | Liliputing Jan / Apr 2022 |
| OneXPlayer Mini and OneXPlayer 8.4-inch (2022) | AMD Ryzen 7 5800U | Liliputing Mar / Apr 2022 |
| OneXPlayer 8.4-inch (still sold Apr 2022) | AMD Ryzen 7 4800U | Liliputing Apr 2022 |

### Skipped for other reasons

- OneXPlayer Mini Pro Ryzen 7 7840U (store listing May-Jul 2024, $659+): the page reuses old Mini copy text and gives no dimensions or weight. A row needs handheld dimensions. Not written; needs a follow-up source.
- OneXFly with AMD Mendocino (announced Sept 2022): never shipped; the OneXFly launched with the 7840U.
- New OneXPlayer X1 with Core Ultra 5 338H (Geekbench leak, Dec 2025): no product found; out of scope for this fork.

### OneGx 2 vs G1

Liliputing reported a OneGx 2 teaser on 2024-11-26 (controllers above a split keyboard, detachable full keyboard, USB4, OCuLink; no specs). The OneXPlayer G1 (8.8-inch mini laptop with a detachable keyboard) launched shortly after with the same features. No product sold under the OneGx 2 name was found. The OneGx 2 teaser appears to be the G1 before its final name (inference, not confirmed by One Netbook).

### Field decisions

- Stick type: the official replacement-joystick listing (`/products/joystick`) lists Hall for X1, OneXFly, OneXPlayer 2/2 Pro, and Mini Pro 6800U. The X1 controllers page says "ALPS esports-grade joysticks" without naming the sensor, and the 2026 X1 Pro HX 470 page says "ALPS Pro Joysticks". Hall was recorded; the ALPS wording is in `stick_note`. The same listing says "Capacitor" for Apex and OneXPlayer 3 / X2 Mini Pro / X2 Mini (parent rows).
- Trigger type: Hall for the X1 family (controllers page: Hall linear triggers) and X2 Air (spec sheet). Null for OneXPlayer 2 / 2 Pro, OneXFly, Mini Pro (no sensor named).
- Ports: X1 155H recorded as TB4 because the official Indiegogo page says the USB4 ports have Thunderbolt 4 capabilities. OneXPlayer 2 / 2 Pro store text says the USB4 port "supports Thunderbolt technology"; recorded as USB4 with that wording in the note (AMD, no certification stated). 258V rows use USB4 (vendor says USB-C 4.0 full-function only).
- Handheld width for X1-series 3-in-1 rows: no official with-controllers size exists. DroiX measured 35.5 cm (X1 8840U), 35.56 cm (X1 Pro), 31.5 cm (X1 Mini). X1 155H, X1 Air, and X2 Air reuse the 35.5 cm figure because they use the same 252 mm tablet and the same X1-series controllers. `d_max` = 44 mm controller thickness (One Netbook figure via Liliputing).
- msrp_usd: the One Netbook retail/list price at launch; pre-order and crowdfunding prices are in `notes`.

### URLs used

- Store catalog JSON: https://onexplayerstore.com/products.json?limit=250
- Wayback CDX: https://web.archive.org/cdx/search/cdx?url=onexplayerstore.com/products/&matchType=prefix
- Official pages: https://onexplayerstore.com/products/joystick ; https://onexplayerstore.com/products/controllers-for-onexplayer-x1 ; https://onexplayerstore.com/products/x1-155h ; https://onexplayerstore.com/products/refurbish-onexplayer-x1-pro-amd-ryzen%E2%84%A2-ai-9-hx-370-10-95-3-in-1-redefining-handheld-gaming ; https://onexplayerstore.com/products/onexplayer-x2-air-portable-3-in-1-gaming-creator-pc-with-expandable-mini-ssd ; https://www.indiegogo.com/en/projects/one-netbook/onexplayer-x1-ultra-155h-10-95in-3-in-1-handheld
- Archived official pages (Wayback): onexplayer-mini-amd®-ryzen®-6800u-1920-1200 (2022-09-26), onexplayer-2-amd®-ryzen®-6800u (2023-03-28), onexplayer-2-pro (2023-12-29), onexplayer-2-pro-amd-ryzen-7-7840u-pre-order-ship-on-august-1st (2023-08-18), onexplayer-2-pro-8840u (2024-05-16), onexfly (2023-09-26, 2024-06-29), onexfly-gaming-handheld (2024-08-08), x1 (2024-03-19), onexplayer-x1-amd-ryzen™-7-8840u-…-pre-sale (2024-07-04), onexplayer-x1-mini-8840u-144hz-gaminghandheld (2024-07-31), onexplayer-x1-pro-…-hx-370-… (2025-01-11), onexplayer-x1-air-… (2025-12-29)
- Liliputing: Mini Pro 6800U (2022-09-20, 2022-10-28); OneXPlayer 2 (2022-12-19, 2023-02-08); 2 Pro (2023-07-31); 2 Pro 8840U (2024-03-13); OneXFly (2023-08-01); X1 (2024-01-23); X1 8840U (2024-06-12); X1 Mini (2024-06-05); X1 Pro (2024-12-29); X1 Air (2025-07-02, 2025-09-04); OneGx 2 (2024-11-26); 2022 Mini models (2022-01-13, 2022-03-04, 2022-04-28, 2022-08-01, 2022-11-21)
- NotebookCheck: OneXPlayer 2 review (732600); 2 Pro review (798258); X1 Pro review (983190); X1 Mini HX 370 news (1035462); X1 Mini pricing (844613); X1 8840U news (847325); X1 155H news (792599); X1 Air news (1105560); X1 Pro 255H news (998286); OneXFly pricing (736638); Mini Pro news (665773)
- Reviews: DroiX OneXFly, X1, X1 AMD, X1 Mini, X1 Pro, OneXPlayer 2; XDA X1 review; PC Gamer X1 Air review
- Retrocatalog front images (discovery and image only): onexplayer-2, onexfly, onexplayer-x1, onexplayer-x1-mini, onexplayer-x1-pro

### Blocked sources

- None blocked. Wayback returned HTTP 503 once (rate limit); retried with backoff.
- onexplayer.com (the brand site) is a Chinese single-page app with a page-config API; no spec text was extracted from it.

## Part 2: OneXFly F1 Pro, G1, Apex, Apex Air, X2, X2 Mini, X2 Mini Pro, OneXPlayer 3

### Method
- Store catalog: `https://onexplayerstore.com/products.json?limit=250` (Shopify JSON). It gives titles, variants, list (compare-at) prices, variant creation dates, and body text.
- The store body text has no spec table. The spec table is an image near the end of each product body. I read these images:
  - Apex: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/APEX_PC4_1.png?v=1788513726`
  - Apex Air: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/APEX_AIR_PC4_1.png?v=1788514428`
  - X2: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/Onexplayer_X2_Gaming_Handheld_PC-5.png?v=1789020990`
  - X2 Mini: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/pc17_c244f8f3-ba9f-431d-914f-9ac4aeb79fb4.png?v=1786429743`
  - X2 Mini Pro: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/17863282263688.png?v=1786328848`
  - OneXPlayer 3: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/ONEXPLAYER3_PC.png?v=1785236163`
  - F1 Pro (HX 370 vs 365): `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/onexfly_gaming_handheld_spec_compare.jpg?v=1730988117`
  - G1: `https://cdn.shopify.com/s/files/1/0557/8535/7492/files/G1_2400.jpg?v=1749787351`
- onexplayer.com is a Chinese Vue CMS. It has no simple spec endpoint, so I did not use it.

### Variant list (rows written)
| Slug | SoC | Status | Release | Notes |
|---|---|---|---|---|
| onexfly-f1-pro-hx370 | Ryzen AI 9 HX 370 | shipped | 2024-11 | store pre-sale 2024-11-07, $1,339 |
| onexfly-f1-pro-365 | Ryzen AI 9 365 | shipped | 2024-11 | $1,099 base; no longer on US store |
| onexfly-f1-pro-8840u | Ryzen 7 8840U | shipped | null | OLED F1 Pro; DroiX reviewed it by 2025-02-11; store re-listed it 2025-12-07 |
| onexplayer-g1 | Ryzen AI 9 HX 370 | shipped | 2025-05 | Indiegogo Jan 2025; store May 2025 |
| onexplayer-g1-8840u | Ryzen 7 8840U | shipped | 2025-05 | $1,099 list |
| onexfly-apex-385 | Ryzen AI Max 385 | shipped | 2026-01 | Indiegogo 2025-11-09; entry config |
| onexfly-apex-395 | Ryzen AI Max+ 395 | shipped | 2026-01 | Indiegogo 2025-11-09 |
| onexfly-apex-388 | Ryzen AI Max+ 388 | shipped | null | store now sells only 388 builds |
| onexfly-apex-air | Intel Arc G3 Extreme | shipped | 2026-09 | store late Aug 2026, $1,839 |
| onexplayer-x2 | Intel Arc G3 Extreme | shipped | 2026-07 | $2,099 list |
| onexplayer-x2-mini | Intel Arc G3 Extreme | shipped | 2026-08 | $2,199 MSRP |
| onexplayer-x2-mini-pro-388 | Ryzen AI Max+ 388 | shipped | 2026-07 | Indiegogo 2026-06-15 |
| onexplayer-3 | Intel Arc G3 Extreme | shipped | 2026-08 | store pre-order 2026-07-30, $1,499 |

### Rows merged, skipped, or excluded
- G1 with Intel Core Ultra 7 255H: sold on Indiegogo only. Skipped: no `data/socs/` file for that chip.
- X2 Mini Pro with Ryzen AI Max+ 395: only teased (April 2026, as "X2 Mini"). It launched with the 388. No row.
- Apex 385 and 395: sold during crowdfunding and early retail. The store later renamed the variants to Max+ 388. Separate rows per SoC.
- G1 form factor: the brief listed it as 3-in-1. The vendor sells a mini laptop with a removable keyboard over built-in controllers. Recorded as `clamshell`.
- F1 Pro 8840U vs OneXFly 8840U: two rows. The OneXFly 8840U (2024, IPS) had its own store product. The F1 Pro 8840U (OLED) is confirmed by the DroiX F1 Pro review (Feb 2025) and an Amazon listing. Its store gallery reuses images named `onexfly8840-*`.
- Super X (14" Strix Halo tablet, Max+ 388/395/PRO 495) and Super V (Core Ultra 358H tablet): excluded. They are tablets without game controllers. The store controller listings name only X1/X1 Mini/X1 Pro/X1 Air/X2 and OneXPlayer 3/X2 Mini Pro/X2 Mini.
- OneXSugar Sugar 1 and OneXSugar Wallet: Snapdragon. Excluded.
- GI58P (`gi58p-32gb-1tb`, $950, Feb 2026): a custom-order link with no product text. Excluded.
- M1, OneXStation, OneXGPU products: mini PCs and eGPUs. Excluded.

### Field decisions
- External-battery models (Apex, Apex Air, X2 Mini, X2 Mini Pro): the vendor gives weight without the battery and the battery weight. `weight_g.handheld.stated` is the sum; `without_battery` holds the vendor figure.
- X2 Mini weight: the sheet says "729 g (With battery)", but the battery alone is 380 g. Not used.
- X2 Mini first USB-C port: recorded as TB4. The store gallery says "Thunderbolt 4"; the spec sheet says "USB-C 4.0".
- X2 handheld size: the vendor gives only the tablet size (252 x 163.5 x 14 mm). The handheld width (355 mm) and d_max (44 mm) use the X1-series controllers, which the store lists as X2-compatible. Same method as the X1 Air and X2 Air rows.
- Stick type on the 2026 shells: the official joystick part page labels the Apex stick and the shared OneXPlayer 3 / X2 Mini Pro / X2 Mini stick as "Capacitor". The X2 Mini Pro store text says these capacitive sticks use non-contact Hall-effect sensing, so "capacitive" means touch sensing. Hall recorded for the Apex (Liliputing spec table), X2 Mini Pro (store text), OneXPlayer 3 (Liliputing), and X2 Mini (shared part). Apex Air stays null: it is not on the joystick page and no source names its sensor.
- msrp_usd: the first retail (non-crowdfunding) price from press. If press gives list and launch-discount prices, the list price. If press gives none, the store compare-at price at crawl time (noted in the row).

### URLs used
- Liliputing: F1 Pro announce and pre-order; G1 announce and Indiegogo; Apex teaser, China launch, crowdfunding, Strix Halo spec shoot-out; X2 Mini teaser; X2 Mini Pro Indiegogo; X2; OneXPlayer 3.
- NotebookCheck news: 914604 (F1 Pro launch), 1015993 (G1 store launch), 949058 (G1 prices), 1153452 and 1172313 (Apex launch and price rise), 1308640 and 1321358 (X2 Mini Pro), 1327954 and 1356089 (OneXPlayer 3), 1342355 (X2 and X2 Mini details), 1380446 (X2 Mini launch), 1382721 (Apex Air launch).
- DroiX Apex review (measured weight, port locations): https://droix.net/blogs/onexplayer-onexfly-apex-review-pc/
- DroiX F1 Pro review (8840U/365/HX 370, measured about 607 g, port locations): https://droix.net/blogs/onexplayer-onexfly-f1-pro-review/
- Official joystick part page: https://onexplayerstore.com/products/joystick
- VideoCardz "drops 395 for 388" URL redirects to an X2 Mini Pro article, not an Apex article.

### Blocked
- Guru3D Apex Air launch article: Cloudflare challenge.
- retrocatalog onexplayer-x2-mini: HTTP 500 page, 404 image.
- No NotebookCheck full reviews exist for these models; only news posts. Measured weights come from DroiX (Apex 395, F1 Pro) or are null.

## Part 3: Follow-up changes (coordinator request)

### Stick and trigger sensor
- Schema now allows `capacitive`. The official joystick part page (https://onexplayerstore.com/products/joystick) lists the type 'Capacitor' for 'Apex' and for 'Onexplayer 3/X2 Mini Pro/X2 Mini'; its other option is 'Hall'.
- `controls.stick_type` = `capacitive` on onexfly-apex-385/395/388, onexplayer-x2-mini, onexplayer-x2-mini-pro-388 and onexplayer-3. Each row quotes the part page and the spec-sheet wording in the source note. The Hall claims (store text 'non-contact Hall-effect technology', Liliputing, NotebookCheck) are `conflicts[]` entries.
- `controls.trigger_type` = `capacitive` on onexplayer-x2-mini-pro-388 (spec sheet: 'Capacitive Sensor Triggers'); store text 'Hall-effect' is a conflict.
- onexfly-apex-air stays null: the Apex Air is not on the joystick part page and its sheet names no sensor.
- onexplayer-mini-pro-1260p: stick type null; the part page lists Hall only for the Mini Pro 6800U.

### Thickness with the battery pack
- `dims_mm.handheld.d_max` = body thinnest point + 17.5 mm pack: 40.5 mm (Apex x3, Apex Air) and 39.5 mm (X2 Mini, X2 Mini Pro). The vendor gives no combined figure.

### Rows added (chassis copied from the sibling row; only SKU fields changed)
| Row | SoC | Sibling | Main SKU source |
|---|---|---|---|
| onexplayer-x1-pro-hx470 | Ryzen AI 9 HX 470 | onexplayer-x1-pro | Current store page (republished 2026-05-20); NotebookCheck 1308640 |
| onexplayer-x1-pro-255h | Core Ultra 7 255H (EVA Asuka limited edition) | onexplayer-x1-pro | NotebookCheck 998286 (TB4 ports, $1,649.99, ships Apr 2025) |
| onexplayer-g1-255h | Core Ultra 7 255H (Indiegogo only) | onexplayer-g1 | Liliputing G1 Indiegogo; NotebookCheck 949058 and 1015993 |
| onexplayer-x1-125h | Core Ultra 5 125H | onexplayer-x1-155h | Liliputing X1 China/Indiegogo launch ($989 regular) |
| onexplayer-x1-air-228v | Core Ultra 5 228V | onexplayer-x1-air | Liliputing X1 Air pre-order ($1,099 pre-order) |
| onexplayer-2-pro-1360p | Core i7-1360P | onexplayer-2-pro | Official refurb listing `refurbished-2-pro-8-4` only |
| onexplayer-mini-pro-1260p | Core i7-1260P | onexplayer-mini-pro-6800u (sources replaced) | Liliputing 2022-08-01 spec table; Gundam edition weight 619 g |
| onexplayer-mini-1195g7 | Core i7-1195G7 | none (new 2022 Mini chassis) | Liliputing 2022-01-13 launch; 2021-12-28 size article |
| onexplayer-mini-5800u | Ryzen 7 5800U | onexplayer-mini-1195g7 | Liliputing 2022-03-03 China launch; 2022-04-28 US price |

### Gaps in the added rows
- onexplayer-2-pro-1360p: no launch date, announce date, price, RAM type or speed. Liliputing (2023-03-30) reported a planned i7-1370P model; the shipped refurb SKU names the i7-1360P.
- onexplayer-g1-255h: Indiegogo only, so no retail price or release date.
- onexplayer-x1-air-228v: only the pre-order price is known.
- onexplayer-mini-pro-1260p: first ship date not found.
- onexplayer-mini-5800u: weight not published; dimensions copied from the Intel Mini; the AMD Edition has a larger 48 Wh battery.
- onexplayer-mini-1195g7 and -5800u: M.2 size, card slot, stick and trigger sensors not stated. No straight-on render (retrocatalog `onexplayer-mini` returns 404).
- Measured weights from sibling review units were not copied.

### Not added
- OneXPlayer 1S / 8.4-inch OneXPlayer (i7-1195G7, 5800U, 4800U): a different chassis (280 x 128 x 25 mm, 825 g). Noted only.
- OneXPlayer Mini Pentium Gold 8505, OneXPlayer Mini Celeron 7305, OneXPlayer 8.4-inch Ryzen 7 4800U: excluded by decision.

