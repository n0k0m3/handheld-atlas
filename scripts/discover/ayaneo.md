# AYANEO discovery notes

Crawl date: 2026-10-27. Brand dir: `data/devices/ayaneo/`. Scope: AYANEO x86 handhelds that shipped or were announced from 2022 to today. ARM models (Pocket series, KONKR Pocket series, Gaming Pad) are out of scope.

## Method

1. Get the product list from https://ayaneo.com/product (links only).
2. Download each product page with curl. Most spec tables are images near the end of the page. Download the images, tile them, and read them.
3. Get store variants, current prices, and renders from the Shopify JSON at https://shop.ayaneo.com/products.json. Current store prices are not launch prices.
4. Get launch prices, ship dates, and reviewer weights from AYANEO news articles, Liliputing, NotebookCheck, IT Home, and other reviews.
5. Validate with `uv run validate.py ../data/devices/ayaneo/*.json`. Result: 32 files. The only errors are `soc_id` errors for the seven rows added on request (`r5-5560u`, `r7-5825u`, `r7-5800u`, `r5-6600u`, `ai9-hx470`); they clear when the SoC files land. Two warnings: battery 28 Wh on `ayaneo-air-1s-limited` and `ayaneo-air-5560u` is below the 30 Wh range check; both values are official.

Hazard: the Geek 1S product page has a hidden Chinese spec block that is a copy of the AYANEO 2S sheet. Do not use it for other models.

## Variant list (rows written)

| id | Model | SoC | Status | Note |
|---|---|---|---|---|
| `ayaneo-2` | AYANEO 2 | `r7-6800u` | shipped |  |
| `ayaneo-2s-7840u` | AYANEO 2S | `r7-7840u` | shipped | Ryzen 7 7840U |
| `ayaneo-2s-8840u` | AYANEO 2S | `r7-8840u` | shipped | Ryzen 7 8840U |
| `ayaneo-3-8840u` | AYANEO 3 | `r7-8840u` | shipped | Ryzen 7 8840U |
| `ayaneo-3-hx370` | AYANEO 3 | `ai9-hx370` | shipped | Ryzen AI 9 HX 370 |
| `ayaneo-air-1s-7840u` | Air 1S | `r7-7840u` | shipped | Ryzen 7 7840U (Standard Edition) |
| `ayaneo-air-1s-8840u` | Air 1S | `r7-8840u` | shipped | Ryzen 7 8840U |
| `ayaneo-air-1s-limited` | Air 1S | `r7-7840u` | shipped | Ultra Thin & Light Limited Edition (Ryzen 7 7840U) |
| `ayaneo-air-5560u` | Air | `r5-5560u` | shipped | Ryzen 5 5560U (Lite and Standard) |
| `ayaneo-air-plus-6800u` | Air Plus | `r7-6800u` | shipped | Ryzen 7 6800U |
| `ayaneo-air-pro-5560u` | Air Pro | `r5-5560u` | shipped | Ryzen 5 5560U |
| `ayaneo-air-pro-5825u` | Air Pro | `r7-5825u` | shipped | Ryzen 7 5825U |
| `ayaneo-flip-1s-ds-8840u` | Flip 1S DS | `r7-8840u` | announced | Ryzen 7 8840U |
| `ayaneo-flip-1s-ds-hx370` | Flip 1S DS | `ai9-hx370` | shipped | Ryzen AI 9 HX 370 |
| `ayaneo-flip-1s-kb-8840u` | Flip 1S KB | `r7-8840u` | announced | Ryzen 7 8840U |
| `ayaneo-flip-1s-kb-hx370` | Flip 1S KB | `ai9-hx370` | shipped | Ryzen AI 9 HX 370 |
| `ayaneo-flip-ds-7840u` | Flip DS | `r7-7840u` | shipped | Ryzen 7 7840U |
| `ayaneo-flip-ds-8840u` | Flip DS | `r7-8840u` | shipped | Ryzen 7 8840U |
| `ayaneo-flip-kb-7840u` | Flip KB | `r7-7840u` | shipped | Ryzen 7 7840U |
| `ayaneo-flip-kb-8840u` | Flip KB | `r7-8840u` | shipped | Ryzen 7 8840U |
| `ayaneo-geek-1s` | Geek 1S | `r7-7840u` | shipped |  |
| `ayaneo-geek-6600u` | Geek | `r5-6600u` | announced | Ryzen 5 6600U |
| `ayaneo-geek-6800u` | Geek | `r7-6800u` | shipped | Ryzen 7 6800U |
| `ayaneo-konkr-fit-hx370` | KONKR Fit | `ai9-hx370` | pre-order | Ryzen AI 9 HX 370 |
| `ayaneo-konkr-fit-hx470` | KONKR Fit | `ai9-hx470` | pre-order | Ryzen AI 9 HX 470 |
| `ayaneo-kun-7840u` | Kun | `r7-7840u` | shipped | Ryzen 7 7840U |
| `ayaneo-kun-8840u` | Kun | `r7-8840u` | shipped | Ryzen 7 8840U |
| `ayaneo-next-5800u` | NEXT | `r7-5800u` | shipped | Ryzen 7 5800U (NEXT Advance) |
| `ayaneo-next-5825u` | NEXT | `r7-5825u` | shipped | Ryzen 7 5825U (NEXT, NEXT Pro) |
| `ayaneo-next-ii-385` | Next II | `ai-max-385` | shipped | Ryzen AI Max 385 |
| `ayaneo-next-ii-395` | Next II | `ai-max-395` | shipped | Ryzen AI Max+ 395 |
| `ayaneo-slide` | Slide | `r7-7840u` | shipped |  |

## Rows merged or split

- One row per SoC. Rows that differ only by RAM, SSD, or colour share one row.
- `id` gets an SoC suffix only when a model has more than one SoC row. Example: `ayaneo-2s-7840u` and `ayaneo-2s-8840u`. The suggested ids `ayaneo-2s`, `ayaneo-air-1s`, `ayaneo-kun`, and `ayaneo-next-ii` changed for this reason. `ayaneo-geek` became `ayaneo-geek-6800u` because the Geek also had a Ryzen 5 6600U option.
- AYANEO 2S, Air 1S, and Kun: the 8840U refresh (pre-order 2024-05-24, https://ayaneo.com/article/833) is a separate row.
- Air 1S Limited Edition (`ayaneo-air-1s-limited`): same 7840U as the standard Air 1S, but a separate row because it is thinner (18 mm vs 21.6 mm), lighter (405 g vs 450 g), and has a smaller battery (28 Wh vs 38 Wh). Merge it into `ayaneo-air-1s-7840u` if the atlas must keep one row per SoC.
- Merged into the base row: Air 1S Retro Power colour, Air 1S 8840U Eiyuden Chronicle edition, Kun optional 4G module, AYANEO 2S B.Duck and Retro Power editions, Geek and Geek 1S 800P and 1200P panels (row uses the base panel; `screen.note` names both), AYANEO 3 OLED and LCD panels (same price, size, and weight; main fields describe the OLED, `screen.note` describes the LCD).
- Flip 1S DS and Flip 1S KB: the official spec tables list Ryzen AI 9 HX 370 and Ryzen 7 8840U. The 8840U rows have status `announced`. In late December 2025 AYANEO said the 8840U supplier could not deliver and offered backers an exchange (for example to an AYANEO 3). No 8840U unit is known to have shipped. Delete those two rows if the atlas keeps only shipped hardware.
- Flip DS and Flip KB: AYANEO cancelled all open orders on 2025-02-25 (NotebookCheck). Units shipped from about May 2024, so the status stays `shipped`.
- KONKR Fit: KONKR is an AYANEO sub-brand sold on ayaneo.com. The row uses brand `AYANEO`, model `KONKR Fit`. Status is `pre-order` because no source confirms shipment (newest source 2026-06-29).
- Rows added on coordinator request after the SoC agent took on the missing SoC files: `ayaneo-air-5560u`, `ayaneo-air-pro-5560u`, `ayaneo-air-pro-5825u`, `ayaneo-next-5800u`, `ayaneo-next-5825u`, `ayaneo-geek-6600u`, `ayaneo-konkr-fit-hx470`.
- AYANEO Air: the Lite (8GB LPDDR4X-3200, 128GB) and Standard (16GB LPDDR4X-4266, 256GB or 512GB) share `ayaneo-air-5560u`; same chassis (18 mm, about 398 g, 28 Wh).
- AYANEO Air Pro: the official table lists both a 5560U (16GB, 512GB or 1TB) and a 5825U (16GB/1TB, 32GB/2TB), so it has two rows (21.6 mm, about 440 g, 38 Wh).
- AYANEO NEXT: the official edition table gives NEXT Advance = Ryzen 7 5800U (16GB/2TB), NEXT = 5825U (16GB, 1TB or 2TB), NEXT Pro = 5825U (32GB/2TB). So `ayaneo-next-5800u` holds the Advance only, and `ayaneo-next-5825u` merges NEXT and NEXT Pro (they differ by RAM and SSD only).
- Geek 6600U (`ayaneo-geek-6600u`): announced 2022-06-07 as the "AYANEO 2 GEEK" with a China pre-order at a US price of $699. The November 2022 Indiegogo launch offered the 6800U only, and no source confirms a 6600U shipment, so the status is `announced` and `msrp_usd` is null.
- Slide: only a 7840U model exists. The Antec Core HS is a rebadged Slide under another brand; it is not written here.

## Excluded: budget re-releases

These variants are excluded on coordinator instruction. Reason: budget re-releases under about $500, outside the atlas scope.

| Device | Exact chip | Facts found |
|---|---|---|
| Air Plus (Mendocino) | AMD Ryzen 3 7320U | 237 x 91.4 x 23.1 mm, 510 g, 8/16 GB LPDDR5-5500, two USB 3.2 Type-C, $549 for 8 GB/128 GB |
| Air Plus (Mendocino) | AMD Ryzen 5 7520U | Same dims and weight as the 7320U, $649 for 16 GB/512 GB |
| Air Plus (Intel) | Intel Core i3-1215U | 237 x 91.4 x 23.1 mm, 510 g, 8/16 GB LPDDR5-5200, two USB4 Type-C |
| Air Plus (Intel) | Intel Pentium Gold 8505 | Listed on the official page; NotebookCheck says AYANEO cancelled it |
| AYANEO NEXT Lite (2024) | AMD Ryzen 5 4500U, AMD Ryzen 7 4800U | Announced 2024-01; $299 to $399; only the 4500U was orderable at first (NotebookCheck) |

## Not written: out of scope or no data

- AYANEO Flip 11: announced 2025-07-28 as a mini gaming laptop with a full keyboard. No product page, store listing, or specs.
- Unnamed compact Windows handheld and unnamed KONKR device: teased 2026-07-03 as silhouettes only.
- REMAKE (https://ayaneo.com/product/REMAKE): a landing page for retro-styled products (Pocket DMG, Pocket Micro, AM01S, eGPU, power bank). No new handheld.
- Mini PCs (AM01, AM01S, AM02, AM03), the Graphics Starship eGPU, and all ARM handhelds.
- AYANEO 2021 and 2021 Pro: shipped in 2021, before the scope start.

## Blocked or empty sources

- liliputing.com returns HTTP 403 to WebFetch. Firecrawl reads it.
- trustedreviews.com: Firecrawl does not support the site, and WebFetch returns HTTP 530.
- windowscentral.com (2S, Flip DS, and Slide reviews) and tomsguide.com: page body came back empty or truncated.
- techradar.com (AYANEO 2 and Air Plus reviews): truncated.
- notebookcheck.net returned HTTP 403 to WebFetch once (article 1334406); Firecrawl read it.
- web.archive.org returned HTTP 429 rate limits.
- retrocatalog: `ayaneo-flip-1s-ds` and `ayaneo-flip-1s-kb` pages return HTTP 500, and their front images return 404. No Geek page exists.
- tomshardware.com (NEXT Pro review): an hCaptcha page appeared, so the source was skipped.
- tweaktown.com (NEXT prices): HTTP 403 to WebFetch; Liliputing gave the same price list.
- No login page or Duo prompt appeared.

## Source URLs per row

Each list comes from the row's `sources[]`. Other pages read for context:
https://ayaneo.com/product, https://shop.ayaneo.com/products.json, https://en.wikipedia.org/wiki/Ayaneo,
https://retrohandhelds.gg/ayaneo-details-upcoming-slate-of-x86-products/, https://droix.net/blogs/ayaneo-2s-kun-models-get-a-8840u-refresh/,
https://retrohandhelds.gg/the-ayaneo-flip-ds-and-flip-kb-are-finally-available/, https://archive.overkill.wtf/ayaneo-flip-ds-kb-indiegogo/,
https://www.notebookcheck.com/Ayaneo-Flip-Gaming-Handheld-startet-mit-zweitem-Display-im-Nintendo-DS-Stil-oder-mit-Tastatur-und-auch-mit-Ryzen-7-8840U-und-OCuLink.797525.0.html,
https://www.inverse.com/tech/ayaneo-next-lite-handheld-gaming-pc-price-release-date.

### `ayaneo-2`

- https://ayaneo.com/product/AYANEO-2
- https://ayaneo.com/product/AYANEOGEEK
- https://en.wikipedia.org/wiki/Ayaneo_2
- https://www.notebookcheck.net/AMD-Ryzen-7-6800U-powered-GEEK-AYANEO-2-handheld-gaming-consoles-by-AYANEO-to-ship-starting-in-December.657642.0.html

### `ayaneo-2s-7840u`

- https://ayaneo.com/product/AYANEO-2S
- https://droix.net/blogs/aya-neo-2s-review-with-video/
- https://www.notebookcheck.com/Ayaneo-2S-Erster-Gaming-Handheld-mit-AMD-Ryzen-7-7840U-wird-ausgeliefert.723939.0.html
- https://www.windowscentral.com/gaming/ayaneo-2s-review-an-impressive-gaming-handheld-with-a-price-thats-hard-to-swallow
- https://archive.overkill.wtf/ayaneo-2s-campaign-now-available-on-indiegogo/

### `ayaneo-2s-8840u`

- https://ayaneo.com/product/AYANEO-2S
- https://droix.net/blogs/aya-neo-2s-review-with-video/
- https://liliputing.com/ayaneo-upgrades-the-ayaneo-2s-air-1s-and-kun-handheld-gaming-pcs-with-ryzen-7-8840u-chips/
- https://ayaneo.com/article/833
- https://www.ithome.com/0/770/622.htm

### `ayaneo-3-8840u`

- https://ayaneo.com/product/AYANEO-3
- https://ayaneo.com/article/859
- https://www.notebookcheck.net/Ayaneo-3-gaming-handheld-now-available-with-AMD-Ryzen-AI-9-HX-370-OLED-display-OCuLink-and-up-to-64-GB-of-RAM.952195.0.html
- https://shop.ayaneo.com/products/ayaneo-3-8840u

### `ayaneo-3-hx370`

- https://ayaneo.com/product/AYANEO-3
- https://ayaneo.com/article/859
- https://www.notebookcheck.net/Ayaneo-3-gaming-handheld-now-available-with-AMD-Ryzen-AI-9-HX-370-OLED-display-OCuLink-and-up-to-64-GB-of-RAM.952195.0.html
- https://shop.ayaneo.com/products/ayaneo-3-amd-ai-9-hx370

### `ayaneo-air-1s-7840u`

- https://ayaneo.com/product/AYANEOAIR1S
- https://www.ayaneo.com/article/773
- https://liliputing.com/aya-neo-air-1s-crowdfunding-starts-july-11-ships-in-august-handheld-gaming-pc-with-5-5-inch-oled-display-and-ryzen-7-7840u-2/
- https://www.notebookcheck.net/Ayaneo-Air-1S-Retro-Power-gaming-handheld-in-test-Zen4-Power-for-your-pocket.761047.0.html

### `ayaneo-air-1s-8840u`

- https://ayaneo.com/product/AYANEOAIR1S
- https://ayaneo.com/article/833
- https://liliputing.com/ayaneo-upgrades-the-ayaneo-2s-air-1s-and-kun-handheld-gaming-pcs-with-ryzen-7-8840u-chips/
- https://www.ithome.com/0/770/622.htm
- https://www.notebookcheck.net/AYANEO-releases-three-new-refresh-gaming-handhelds-with-powerful-AMD-APUs-shortly-before-ASUS-ROG-Ally-X-announcement.841043.0.html
- https://www.notebookcheck.net/Ayaneo-Air-1S-Retro-Power-gaming-handheld-in-test-Zen4-Power-for-your-pocket.761047.0.html
- https://www.notebookcheck.com/450g-leichter-Ayaneo-Air-1S-Gaming-Handheld-mit-AMOLED-Display-erhaelt-Upgrade-auf-AMD-Ryzen-7-8840U.839726.0.html
- https://www.notebookcheck.net/AIR-1S-AYANEO-announces-AMD-Ryzen-7-8840U-refresh-with-Eiyuden-Chronicle-limited-edition-model.839063.0.html

### `ayaneo-air-1s-limited`

- https://ayaneo.com/product/AYANEOAIR1S
- https://www.ayaneo.com/article/773
- https://liliputing.com/aya-neo-air-1s-crowdfunding-starts-july-11-ships-in-august-handheld-gaming-pc-with-5-5-inch-oled-display-and-ryzen-7-7840u-2/
- https://www.notebookcheck.net/Ayaneo-Air-1S-Retro-Power-gaming-handheld-in-test-Zen4-Power-for-your-pocket.761047.0.html

### `ayaneo-air-5560u`

- https://ayaneo.com/product/AYANEOAIR
- https://www.notebookcheck.net/AYA-NEO-AIR-Full-specifications-and-prices-confirmed-for-multiple-configurations.622991.0.html

### `ayaneo-air-plus-6800u`

- https://ayaneo.com/product/AYANEO-AIR-Plus
- https://www.notebookcheck.net/AYA-NEO-Air-Plus-New-gaming-handheld-revealed-at-higher-than-expected-prices.698162.0.html
- https://www.notebookcheck.net/AYA-NEO-AIR-Plus-launches-as-new-affordable-gaming-handheld-with-AMD-and-Intel-processor-options.705177.0.html

### `ayaneo-air-pro-5560u`

- https://ayaneo.com/product/AYANEOAIR
- https://www.notebookcheck.net/AYA-NEO-AIR-Full-specifications-and-prices-confirmed-for-multiple-configurations.622991.0.html
- https://en.wikipedia.org/wiki/Ayaneo

### `ayaneo-air-pro-5825u`

- https://ayaneo.com/product/AYANEOAIR
- https://www.notebookcheck.net/AYA-NEO-AIR-Full-specifications-and-prices-confirmed-for-multiple-configurations.622991.0.html
- https://en.wikipedia.org/wiki/Ayaneo

### `ayaneo-flip-1s-ds-8840u`

- https://ayaneo.com/product/AYANEO-Flip-1S-DS
- https://ayaneo.com/article/887
- https://droix.net/blogs/ayaneo-flip-1s-ds-review/
- https://retrohandhelds.gg/ayaneo-refuses-to-accept-responsibility-puts-blame-on-everyone-else-for-delays/

### `ayaneo-flip-1s-ds-hx370`

- https://ayaneo.com/product/AYANEO-Flip-1S-DS
- https://ayaneo.com/article/887
- https://droix.net/blogs/ayaneo-flip-1s-ds-review/
- https://shop.ayaneo.com/products/ayaneo-flip-1s-ds
- https://retrohandhelds.gg/ayaneo-refuses-to-accept-responsibility-puts-blame-on-everyone-else-for-delays/

### `ayaneo-flip-1s-kb-8840u`

- https://ayaneo.com/product/AYANEO-Flip-1S-KB
- https://ayaneo.com/article/887
- https://droix.net/blogs/ayaneo-flip-1s-ds-review/
- https://retrohandhelds.gg/ayaneo-refuses-to-accept-responsibility-puts-blame-on-everyone-else-for-delays/

### `ayaneo-flip-1s-kb-hx370`

- https://ayaneo.com/product/AYANEO-Flip-1S-KB
- https://ayaneo.com/article/887
- https://droix.net/blogs/ayaneo-flip-1s-ds-review/
- https://shop.ayaneo.com/products/ayaneo-flip-1s-kb
- https://retrohandhelds.gg/ayaneo-refuses-to-accept-responsibility-puts-blame-on-everyone-else-for-delays/

### `ayaneo-flip-ds-7840u`

- https://ayaneo.com/product/AYANEO-FLIP-DS
- https://ayaneo.com/article/810
- https://www.notebookcheck.net/Ayaneo-issues-official-statement-and-resolutions-for-outstanding-Flip-DS-and-Flip-KB-orders.968352.0.html
- https://overkill.wtf/ayaneo-flip-kb-review/
- https://steamdeckhq.com/news/ayaneo-flip-ds-review/

### `ayaneo-flip-ds-8840u`

- https://ayaneo.com/product/AYANEO-FLIP-DS
- https://ayaneo.com/article/810
- https://www.notebookcheck.net/Ayaneo-issues-official-statement-and-resolutions-for-outstanding-Flip-DS-and-Flip-KB-orders.968352.0.html
- https://overkill.wtf/ayaneo-flip-kb-review/
- https://steamdeckhq.com/news/ayaneo-flip-ds-review/

### `ayaneo-flip-kb-7840u`

- https://ayaneo.com/product/AYANEO-FLIP-KB
- https://ayaneo.com/article/810
- https://www.notebookcheck.net/Ayaneo-issues-official-statement-and-resolutions-for-outstanding-Flip-DS-and-Flip-KB-orders.968352.0.html
- https://overkill.wtf/ayaneo-flip-kb-review/
- https://www.notebookcheck.net/Ayaneo-Flip-KB-review-handheld-console-with-great-functionality-powered-by-the-less-efficient-AMD-Ryzen-7-8840U.902381.0.html

### `ayaneo-flip-kb-8840u`

- https://ayaneo.com/product/AYANEO-FLIP-KB
- https://ayaneo.com/article/810
- https://www.notebookcheck.net/Ayaneo-issues-official-statement-and-resolutions-for-outstanding-Flip-DS-and-Flip-KB-orders.968352.0.html
- https://overkill.wtf/ayaneo-flip-kb-review/
- https://www.notebookcheck.net/Ayaneo-Flip-KB-review-handheld-console-with-great-functionality-powered-by-the-less-efficient-AMD-Ryzen-7-8840U.902381.0.html

### `ayaneo-geek-1s`

- https://ayaneo.com/product/AYANEOGEEK1S
- https://archive.overkill.wtf/ayaneo-2s-campaign-now-available-on-indiegogo/
- https://www.notebookcheck.com/Ayaneo-2S-und-Geek-1S-Neue-Handhelds-mit-Phoenix-APU-koennen-noch-mit-Rabatt-vorbestellt-werden.716276.0.html

### `ayaneo-geek-6600u`

- https://ayaneo.com/product/AYANEOGEEK
- https://www.notebookcheck.net/AYA-NEO-2-and-AYA-NEO-GEEK-arrive-on-Indiegogo-with-AMD-Ryzen-7-6800U-and-Radeon-680M-offering.666266.0.html
- https://ayaneo.com/article/205
- https://www.notebookcheck.net/AYA-NEO-2-GEEK-AYA-NEO-announces-another-gaming-handheld-powered-by-AMD-Ryzen-6800U-and-Radeon-680M-silicon.624341.0.html
- https://www.notebookcheck.net/AMD-Ryzen-7-6800U-powered-GEEK-AYANEO-2-handheld-gaming-consoles-by-AYANEO-to-ship-starting-in-December.657642.0.html

### `ayaneo-geek-6800u`

- https://ayaneo.com/product/AYANEOGEEK
- https://www.notebookcheck.net/AMD-Ryzen-7-6800U-powered-GEEK-AYANEO-2-handheld-gaming-consoles-by-AYANEO-to-ship-starting-in-December.657642.0.html
- https://en.wikipedia.org/wiki/Ayaneo_2
- https://www.notebookcheck.net/AYA-NEO-2-and-AYA-NEO-GEEK-arrive-on-Indiegogo-with-AMD-Ryzen-7-6800U-and-Radeon-680M-offering.666266.0.html

### `ayaneo-konkr-fit-hx370`

- https://ayaneo.com/product/KONKR-FIT
- https://ayaneo.com/article/918
- https://liliputing.com/ayaneo-unveils-konkr-fit-handheld-gaming-pc-with-ryzen-ai-9-hx-470/
- https://shop.ayaneo.com/products/konkr-fit
- https://retrohandhelds.gg/ayaneos-konkr-fit-is-now-up-for-pre-order-but-wont-ship-until-end-of-april/
- https://finalboss.io/handhelds/ayaneo-konkr-fit

### `ayaneo-konkr-fit-hx470`

- https://ayaneo.com/product/KONKR-FIT
- https://ayaneo.com/article/918
- https://liliputing.com/ayaneo-unveils-konkr-fit-handheld-gaming-pc-with-ryzen-ai-9-hx-470/
- https://shop.ayaneo.com/products/konkr-fit
- https://retrohandhelds.gg/ayaneos-konkr-fit-is-now-up-for-pre-order-but-wont-ship-until-end-of-april/
- https://finalboss.io/handhelds/ayaneo-konkr-fit

### `ayaneo-kun-7840u`

- https://ayaneo.com/product/AYANEO-KUN
- https://liliputing.com/aya-neo-kun-and-ayn-odin2-gaming-handhelds-ship-this-month-crowdfunding/
- https://www.notebookcheck.net/Ayaneo-Kun-gaming-handheld-in-review-Performance-beast-for-individualists.797526.0.html

### `ayaneo-kun-8840u`

- https://ayaneo.com/product/AYANEO-KUN
- https://ayaneo.com/article/833
- https://liliputing.com/ayaneo-upgrades-the-ayaneo-2s-air-1s-and-kun-handheld-gaming-pcs-with-ryzen-7-8840u-chips/
- https://www.ithome.com/0/770/622.htm
- https://www.notebookcheck.net/Ayaneo-Kun-gaming-handheld-in-review-Performance-beast-for-individualists.797526.0.html

### `ayaneo-next-5800u`

- https://ayaneo.com/product/ayaneo-next-pro
- https://www.notebookcheck.net/AYA-NEO-NEXT-revealed-with-an-AMD-Ryzen-7-5800U-APU-up-to-32-GB-and-an-extraordinary-price.590158.0.html
- https://en.wikipedia.org/wiki/Ayaneo
- https://droix.net/blogs/ayaneo-next-faq-ayas-next-windows-gaming-handheld/
- https://liliputing.com/aya-neo-next-is-a-handheld-gaming-pc-with-ryzen-7-5800u-and-up-to-32gb-of-ram/

### `ayaneo-next-5825u`

- https://ayaneo.com/product/ayaneo-next-pro
- https://www.notebookcheck.net/AYA-NEO-NEXT-revealed-with-an-AMD-Ryzen-7-5800U-APU-up-to-32-GB-and-an-extraordinary-price.590158.0.html
- https://en.wikipedia.org/wiki/Ayaneo
- https://droix.net/blogs/ayaneo-next-faq-ayas-next-windows-gaming-handheld/
- https://liliputing.com/aya-neo-next-is-a-handheld-gaming-pc-with-ryzen-7-5800u-and-up-to-32gb-of-ram/

### `ayaneo-next-ii-385`

- https://ayaneo.com/product/AYANEO-NEXT-%E2%85%A1
- https://ayaneo.com/article/905
- https://ayaneo.com/article/940
- https://tbreak.com/ayaneo-next-ships-globally-late-july-top-model/
- https://tbreak.com/ayaneo-next-2-price-2026/
- https://shop.ayaneo.com/products/ayaneo-next-2

### `ayaneo-next-ii-395`

- https://ayaneo.com/product/AYANEO-NEXT-%E2%85%A1
- https://ayaneo.com/article/905
- https://ayaneo.com/article/940
- https://tbreak.com/ayaneo-next-ships-globally-late-july-top-model/
- https://tbreak.com/ayaneo-next-2-price-2026/
- https://shop.ayaneo.com/products/ayaneo-next-2

### `ayaneo-slide`

- https://ayaneo.com/product/AYANEO-SLIDE
- https://liliputing.com/aya-neo-slide-hits-indiegogo-for-700-and-up-ryzen-7840u-handheld-gaming-pc-with-a-keyboard-and-slide-up-display/
- https://www.notebookcheck.com/Ayaneo-Slide-Gaming-Handheld-mit-Tastatur-ist-ab-sofort-bestellbar.785097.0.html
- https://www.notebookcheck.net/Antec-Core-HS-launches-as-rebadged-Ayaneo-Slide-but-with-a-launch-price-starting-at-499.876565.0.html
