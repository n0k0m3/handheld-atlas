# Valve: crawler notes

Crawled on 2026-10-27.

## Variant list

| Row id | Model | SoC id | Status | Release | Launch price (base) |
|---|---|---|---|---|---|
| `steam-deck-lcd` | Steam Deck LCD | `steam-deck-apu-lcd` | shipped | 2022-02-25 | $399 (64 GB eMMC) |
| `steam-deck-oled` | Steam Deck OLED | `steam-deck-apu-oled` | shipped | 2023-11-16 | $549 (512 GB) |

Valve made no other x86 handheld from 2022 to today.

## Rows merged

- `steam-deck-lcd`: the 64 GB eMMC, 256 GB NVMe, and 512 GB NVMe models share one row. Only storage and the 512 GB anti-glare glass differ.
- `steam-deck-oled`: the 512 GB, 1 TB, and 1 TB Limited Edition (translucent, $679) models share one row. Only storage, glass, and shell color differ.

## Rows skipped

- None.

## Seed row fixes

- The seed row for `steam-deck-oled` cited `https://www.steamdeck.com/en/tech/deck`. That URL is the **LCD** tech page (7 in, 7 nm, 5500 MT/s, 40 Wh, 669 g). The OLED tech page is `https://www.steamdeck.com/en/tech`. The new row cites the correct page.
- The seed had `ram.channels` = null. Valve states "quad 32-bit channels", so the value is now 4.
- The seed had `controls.stick_type` without a source. NotebookCheck names potentiometers for the OLED model, so the value stays `potentiometer` with a source.
- The seed had `trigger_lock: false` without a source. The value is now null plus an `unresolved` entry.

## URLs used

| URL | Used for |
|---|---|
| https://www.steamdeck.com/en/tech | OLED official specs (`*`) |
| https://www.steamdeck.com/en/tech/deck | LCD official specs (`*`) |
| https://www.notebookcheck.net/Steam-Deck-1-TB-OLED-review-Minimalist-performance-maximum-gaming-fun.802764.0.html | OLED measured weight (637 g), potentiometer sticks, BT conflict |
| https://www.tomshardware.com/video-games/handheld-gaming/how-to-upgrade-steam-deck-ssd | M.2 2230 slot, PCIe 3.0 x4, eMMC in the 64 GB LCD |
| https://www.tomshardware.com/news/valve-steam-deck-launches-feb25 | LCD release date, prices, capacities |
| https://www.tomshardware.com/news/valve-steam-deck-price-specs-release-date | LCD announce date (2021-07-15), anti-glare glass |
| https://gameinformer.com/2023/11/09/steam-deck-oled-announced | OLED announce date, release date, prices; LCD price cuts |
| https://www.steamdeck.com/en/press | Press renders for the image manifest |

## Open items

- `controls.trigger_type` is null on both rows. No fetched source names the trigger sensor.
- `controls.stick_type` is null on the LCD row. No fetched source names the LCD stick sensor.
- `weight_g.handheld.measured` is null on the LCD row. NotebookCheck has no English review of the LCD model.

## Blocked or limited sources

- Firecrawl hit its rate limit early in the run. Pages were fetched with curl instead.
- WebSearch does not allow theverge.com.
