# AOKZOE crawl notes

Crawled 2026-10-27. AOKZOE is a One-Netbook (ONEXPLAYER) sister brand. Its handhelds ship with OneXConsole.

## Variant list

| Row (slug) | Model | SoC | Status | Notes |
|---|---|---|---|---|
| `aokzoe-a1` | A1 | Ryzen 7 6800U | shipped | 48 Wh Standard and 65 Wh Ultimate (China: A1 / A1L) share one row. Row uses the 65 Wh version. |
| `aokzoe-a1-pro` | A1 Pro | Ryzen 7 7840U | shipped | |
| `aokzoe-a2` | A2 | Ryzen 7 7840U | shipped | |
| `aokzoe-a2-ultra` | A2 Ultra | Core Ultra 7 155H | shipped (China) | Dimensions copied from the A2; see below. |
| `aokzoe-a1x` | A1X | Ryzen AI 9 HX 370 | shipped | |
| `aokzoe-a1x-8840u` | A1X | Ryzen 7 8840U | shipped | Base SKU at launch; the store no longer lists it. |

## Skipped

| Model / option | Reason |
|---|---|
| A2 Ultra with Core Ultra 5 125H (also sold later as refurb "A2 Intel AOK 7") | Originally skipped (no SoC file). Now the aokzoe-a2-ultra-125h row; see the follow-up section. |
| A2 with Ryzen 7 6800U | Offered only during the Indiegogo campaign (Liliputing, 2023-12-21). No retail listing found, and no proof that it shipped. |
| A1 Pro with Ryzen 7 8840U | No evidence that it exists. |
| "A2 Pro" (8840U / HX 370) | Named only by an unreliable aggregator site (tech-insider.org); it looks like a mix-up with the A1X. Not a real model. |
| AOKZOE mini PC (Strix Halo, 2025) | Not a handheld. |
| 2026 models | None found on aokzoestore.com, the Liliputing AOKZOE tag, or a web search. |

## URLs used

Official:
- https://aokzoestore.com/products.json?limit=250 (Shopify catalog, one fetch for the whole store)
- https://aokzoestore.com/products/aokzoe-a1x (spec table text)
- https://aokzoestore.com/products/aokzoe-a1-pro (spec table text)
- https://aokzoestore.com/products/aokzoe-a2-7840u-handheld (partial text; full table is the image https://cdn.shopify.com/s/files/1/0650/6879/4073/files/A2-_B-__17.jpg)
- https://aokzoestore.com/products/refurbished-aokzoe-a1-65w-amd%C2%AE-ryzen%C2%AE-6800u-8-inch (A1 spec list)
- https://aokzoestore.com/products/refurbished-a2-intel-aok-7 (proves the 125H version was sold; no spec text)
- https://aokzoestore.com/products/joystick-for-aokzoe-a1-game-handheld (A1/A1 Pro sticks come as ALPS or Hall)
- https://aokzoestore.com/products/aokzoe-a1pro-worlds-1st-7840u-gaming-handheld ("Hall Joysticks")
- https://aokzoe.com/newest/2.html (official China launch article for the A1, 2022-09-21)
- https://aokzoe.com/product/ (lists A2, A1 Pro, A1 only; pages are images)

Third party:
- https://liliputing.com/aokzoe-a1-handheld-gaming-pc-with-ryzen-7-6800u-hits-kickstarter-for-899-and-up/
- https://liliputing.com/aokzoe-a1-pro-handheld-gaming-pc-with-ryzen-7-7840u-and-up-to-64gb-ram-hits-indiegogo-for-799-and-up/
- https://liliputing.com/aokzoe-a1-pro-and-a2-handheld-gaming-pcs-with-ryzen-7000-chips-are-on-the-way/ (date only, from the tag page)
- https://liliputing.com/aokzoe-a2-handheld-gaming-pc-has-a-7-inch-screen-and-ryzen-7-7840u/
- https://liliputing.com/aokzoe-a2-handheld-gaming-pc-hits-indiegogo-for-599-and-up/
- https://liliputing.com/aokzoe-a2-ultra-is-an-intel-meteor-lake-powered-handheld-gaming-pc/
- https://liliputing.com/aokzoe-a1x-handheld-gaming-pc-supports-up-to-a-ryzen-ai-9-hx-370-processor-crowdfunding/
- https://www.notebookcheck.net/Aokzoe-A1-gaming-handheld-review-Ambitious-with-room-for-improvement.751897.0.html (measured weight, port test)
- https://www.notebookcheck.net/Aokzoe-A1X-officially-released-ahead-of-schedule-with-up-to-AMD-Ryzen-AI-9-HX-370-and-64-GB-RAM.1036125.0.html
- https://www.notebookcheck.net/AOKZOE-A2-Ultra-gaming-handheld-gets-its-pricing-revealed.835764.0.html
- https://www.pcgamesn.com/aokzoe/a1x-review (A1X triggers, stick wording, port locations, MSRP)
- https://finance.sina.com.cn/tech/roll/2024-09-13/doc-incnyytq8970664.shtml (A2 Ultra hands-on: Hall sticks and triggers, RAM, weight)
- Search excerpts only: videocardz.com A1 Pro retail $999; droix.net A1 Pro guide dated 2023-07-13.
- retrocatalog.com: discovery and front image URLs only. It has pages for a1, a1-pro, a2, a1x. It has no A2 Ultra page.

## Decisions

- `ram.soldered` = true for every row. All rows use LPDDR5/LPDDR5X, which is soldered. Liliputing states it for the A1.
- USB 3.0 Type-A is recorded as `USB-A 3.2 Gen1` (5 Gbps). That is the same standard under a new name, not a guess.
- A1 Pro "USB-C 3.2" has no generation, so it is `USB-C unspecified`.
- A1 `stick_type` is null. AOKZOE sold it with a buyer's choice of Hall or ALPS potentiometer sticks.
- A1X `stick_type` is null. AOKZOE says "capacitive, contact-free" and does not name the sensor (PCGamesN says so too). An Amazon listing (https://www.amazon.com/AOKZOE-A1X-Ryzen-120Hz-OCuLink-PC/dp/B0GVD3S9LX) claims Hall-effect. The seller is unverified, so it is not used.
- A2 Ultra dimensions are NOT sourced. They are copied from the A2 spec sheet because the Kuai Technology hands-on says the A2 Ultra keeps the A2 design. The row has an `unresolved` entry for this.
- A1X MSRP: the store compare-at price ($1459 for HX 370 32GB/1TB, $1099 for 8840U) matches PCGamesN's "save up to 18% on the MSRP". The NotebookCheck release prices ($899 / $1138) were launch discounts.

## Blocked

- aokzoe.com has an expired TLS certificate. curl refused it. A Firecrawl fetch with TLS checks turned off was denied by the permission system. A normal Firecrawl fetch of https://aokzoe.com/newest/2.html worked.
- The aokzoe.com product pages (a1, a1pro, a2) are images only; not read.

## Follow-up changes (coordinator request)
- aokzoe-a1x and aokzoe-a1x-8840u: `controls.stick_type` = `capacitive`. AOKZOE wording via Liliputing ('capacitive joysticks with RGB lighting') and PCGamesN ('Capacitive Joysticks'; 'contact-free'). The Amazon listing that says 'Hall-Effect Controls' is a `conflicts[]` entry.
- Added aokzoe-a2-ultra-125h (Core Ultra 5 125H, 16 GB/512 GB, CNY 4,999; later the refurb 'A2 Intel' at https://aokzoestore.com/products/refurbished-a2-intel-aok-7). Chassis fields are copied from aokzoe-a2-ultra, whose size is itself copied from the A2.

