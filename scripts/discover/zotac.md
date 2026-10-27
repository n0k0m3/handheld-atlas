# ZOTAC: crawler notes

Crawled on 2026-10-27.

## Variant list

| Row id | Model | SoC id | Status | Release | Launch price (base) |
|---|---|---|---|---|---|
| `zotac-zone` | Zone | `r7-8840u` | shipped | 2024-09 | $799 (16 GB / 512 GB) |
| `zotac-zone-pro` | Zone Pro | `ai9-hx370` | announced | — | not announced |

The Zone Pro was first shown as an "upgraded Zone" at CES 2025. Press also called it "Zone 2". ZOTAC renamed it Zone Pro at Computex/Gamescom 2025, with a ZOTAC build of Manjaro Linux. ZOTAC targeted October 2025. VideoCardz reported in late 2025 that no retail launch happened. No 2026 launch news was found.

## Rows merged

- `zotac-zone`: one retail config (16 GB / 512 GB). Open-box units share the row.

## Rows skipped

- None.

## Blocked sources

- `https://www.zotac.com/page/zotac-gaming-zone-portable-handheld`: SafeLine WAF "Confirm You Are Human" captcha. Firecrawl got HTTP 468. The agent browser got the same captcha, so I skipped it.
- `tomsguide.com`: Firecrawl does not support the site.
- `techpowerup.com` review: Firecrawl query mode returned no text. The agent browser read the spec table.

## Data notes

- Zone dimensions use the TechPowerUp retail spec table (285 x 115 x 35 mm). The Computex 2024 prototype figures (310 x 125-135 x 40 mm) do not apply.
- Zone Pro dimensions (310 x 135 x 40 mm, 692 g) come from PCGH. They match the first Zone's prototype figures, so treat them as provisional.
- No reviewer scale weight was found for either row.

## URLs used

| URL | Used for |
|---|---|
| https://www.zotacstore.com/us/gaming-console | Zone official spec table (`*`) |
| https://www.techpowerup.com/review/zotac-zone/ | Zone dims, weight, battery, screen, controls, MSRP |
| https://www.notebookcheck.net/Zotac-Zone-review-Display-galore-with-class-leading-inputs.895001.0.html | Zone port locations, trigger mode switch, measured brightness, fingerprint |
| https://lowyat.net/2024/330597/zotac-zone-gets-12-september-launch-date-preorders-start-at-e849 | Zone release date |
| https://liliputing.com/zotac-gaming-zone-is-a-ryzen-7-8840u-handheld-gaming-pc-with-an-amoled-screen-and-a-webcam/ | Zone announce (Computex 2024) |
| https://www.pcgameshardware.de/Handheld-PC-Hardware-279763/Specials/Zotac-Zone-Pro-Gamescom-2025-1480299/ | Zone Pro spec table (all groups) |
| https://videocardz.com/newz/amd-ryzen-powered-zotac-zone-pro-and-acer-nitro-blaze-miss-planned-launch-window | Zone Pro status and first showing |
