# ASUS: crawler notes

Crawled on 2026-10-27.

## Variant list

| Row id | Model | ASUS model no. | SoC id | Status | Release | Launch price (base) |
|---|---|---|---|---|---|---|
| `rog-ally-z1-extreme` | ROG Ally (2023) | RC71L | `z1-extreme` | shipped | 2023-06-13 | $699.99 |
| `rog-ally-z1` | ROG Ally (2023) | RC71L | `z1` | shipped | not sourced (2023) | $599 |
| `rog-ally-x` | ROG Ally X (2024) | RC72LA | `z1-extreme` | shipped | 2024-07-22 | $799.99 |
| `rog-xbox-ally` | ROG Xbox Ally (2025) | RC73YA | `z2-a` | shipped | 2025-10-16 | $599.99 |
| `rog-xbox-ally-x` | ROG Xbox Ally X (2025) | RC73XA | `z2-ai-extreme` | shipped | 2025-10-16 | $999 |
| `rog-xbox-ally-x20` | ROG Xbox Ally X20 (2026) | RC74XA | `z2-ai-extreme` | shipped | 2026-10-15 | $1,299.99 |

The search found no other ASUS handheld from 2026. The X20 is the only new 2026 model. A NotebookCheck rumor said ASUS "might" show a new handheld at Computex 2026; the model ASUS showed there was the X20.

## Rows merged

- `rog-ally-x`: the 1 TB (RC72LA-ALLYX.Z1X) and 2 TB (RC72LA-ALLYX.Z1X2TB) models share one row.
- `rog-xbox-ally-x20`: the standalone unit (RC74XA-XB-ALLYX.Z2E.24) and the bundle (RC74XA-XB-ALLYXBUN.Z2E.24) share one row. The bundle adds ROG XREAL R1 Edition 20 glasses, a Pelican case, and a dbrand Killswitch. The spec pages are identical apart from the "Included in the Box" list. Bundle price: $2,499.99.
- `rog-ally-z1-extreme`: black and white colorways share one row.

## Rows split

- `rog-ally-z1` and `rog-ally-z1-extreme` come from one ASUS spec page (RC71L) with two processor options. They are two rows because the SoC differs.

## Rows skipped

- None.

## Decisions

- **USB4 vs Thunderbolt.** ASUS writes "Type C support USB 4 (Thunderbolt 4 compliance, ...)" for the Ally X, Xbox Ally X, and X20. That is not Thunderbolt branding, so all three use `kind: "USB4"`. The ASUS wording is in the port note. NotebookCheck lists the X20 port as "Thunderbolt 4"; that is in `conflicts[]`.
- **Stick type.** The X20 is `tmr` (ASUS spec page). The Xbox Ally and Xbox Ally X are `potentiometer` (NotebookCheck GuliKit article names potentiometers). The 2023 Ally and the Ally X stay null: NotebookCheck and Tom's Hardware say only that the sticks are not Hall effect. No fetched source names the sensor.
- **Trigger type.** ASUS lists "L & R Hall Effect analog triggers" on every model, so all rows use `hall`.
- **Measured weight.** NotebookCheck's spec table can repeat the vendor value (the Steam Deck OLED review shows 640 g in the table and 637 g in the text). A measured value is kept only when the text gives a scale weight or the table differs from the ASUS figure. Kept: Ally Z1 Extreme 611 g, Ally X 685 g, Xbox Ally X 718 g. Not kept: Xbox Ally 670 g and X20 756 g (both equal the ASUS figure).
- **Port location.** ASUS spec pages give no locations. NotebookCheck photo captions put every port on the top edge.
- **pd_in_w.** ASUS gives only the bundled adapter rating (65 W, or 68 W for the X20). That value is on each port that ASUS says supports power delivery, with a note.
- **Dimensions.** ASUS gives "W x D x H" with a thickness range. `d` = thinnest value, `d_max` = grip value.

## URLs used

| URL | Used for |
|---|---|
| https://rog.asus.com/us/gaming-handhelds/rog-ally/rog-ally-2023/spec/ | Ally Z1 / Z1 Extreme official specs (`*`) |
| https://rog.asus.com/us/gaming-handhelds/rog-ally/rog-ally-x-2024/spec/ | Ally X official specs (`*`) |
| https://rog.asus.com/us/gaming-handhelds/rog-ally/rog-xbox-ally-2025/spec/ | Xbox Ally official specs (`*`) |
| https://rog.asus.com/us/gaming-handhelds/rog-ally/rog-xbox-ally-x-2025/spec/ | Xbox Ally X official specs (`*`) |
| https://rog.asus.com/us/gaming-handhelds/rog-ally/rog-xbox-ally-x20-2026/spec/ | X20 official specs (`*`) |
| https://rog.asus.com/us/gaming-handhelds/rog-ally/rog-xbox-ally-x20-bundle-2026/spec/ | X20 bundle, to confirm the same hardware |
| https://www.notebookcheck.net/Asus-ROG-Ally-Z1-Extreme-Review-Gaming-handheld-with-120-Hz-display-and-AMD-Zen4.716680.0.html | Ally weight 611 g, port locations, "no hall sensors for the sticks", two fans |
| https://www.notebookcheck.net/ASUS-ROG-Ally-Pre-orders-open-with-cheaper-AMD-Ryzen-Z1-model-to-follow.717043.0.html | Ally prices ($699.99 / $599) |
| https://liliputing.com/asus-rog-ally-is-a-handheld-gaming-pc-with-a-custom-amd-chip-its-real-despite-the-april-1-announcement/ | Ally announce date |
| https://liliputing.com/asus-rog-ally-handheld-gaming-pc-goes-up-for-pre-order-for-600-and-up-available-starting-june-13/ | Ally Z1 Extreme release date |
| https://www.notebookcheck.net/Asus-ROG-Ally-X-Review-The-best-gaming-handheld-thanks-to-faster-RAM-and-a-huge-80-Wh-battery.865721.0.html | Ally X weight 685 g, port locations, two fans, RAM conflict |
| https://www.tomshardware.com/video-games/console-gaming/asus-rog-ally-x-review | Ally X price, LPDDR5X-7500, stick note |
| https://liliputing.com/asus-rog-ally-x-handheld-gaming-pc-is-available-for-pre-order-for-800-bigger-battery-more-memory-more-storage/ | Ally X announce date |
| https://liliputing.com/asus-rog-ally-x-is-now-available-for-800-handheld-gaming-pc-with-bigger-battery-more-ram-and-usb4/ | Ally X release date, RAM conflict |
| https://www.notebookcheck.net/Slower-than-the-Steam-Deck-OLED-Asus-ROG-Xbox-Ally-handheld-review.1143681.0.html | Xbox Ally price, RAM and BT conflicts |
| https://www.notebookcheck.net/Xbox-Full-screen-Experience-for-Gaming-Handhelds-Asus-ROG-Xbox-Ally-X-Review.1139045.0.html | Xbox Ally X weight 718 g, LPDDR5x-8000, port locations, DP conflict |
| https://www.notebookcheck.net/GuliKit-launches-official-19-99-TMR-anti-drift-joysticks-for-Xbox-Ally-and-Ally-X.1190606.0.html | Xbox Ally / Xbox Ally X potentiometer sticks |
| https://liliputing.com/599-asus-rog-xbox-ally-and-999-rog-xbox-ally-x-now-available-for-pre-order/ | Xbox Ally announce month, Xbox Ally X price, RAM conflict |
| https://press.asus.com/news/press-releases/rog-xbox-ally-ally-x-launch-date/ | Xbox Ally / Xbox Ally X release date |
| https://www.notebookcheck.net/A-stunning-OLED-screen-Asus-ROG-Xbox-Ally-X20-Gaming-Handheld-Review.1425337.0.html | X20 RAM speed, port locations, availability, TB4 conflict |
| https://liliputing.com/asus-rog-xbox-ally-x20-bundle-brings-a-bigger-brighter-screen-and-a-pair-of-ar-glasses/ | X20 announce date |
| https://purexbox.com/news/2026/08/rog-xbox-ally-x20-pre-orders-go-live-today-release-date-and-prices-revealed | X20 release date and prices |

## Open items

- `rog-ally-z1.release_date`: sources only say "later this year" / Q3 2023.
- `controls.stick_type` on `rog-ally-z1`, `rog-ally-z1-extreme`, `rog-ally-x`: no source names the sensor.
- `cooling` on the three Xbox Ally rows: NotebookCheck says "fans" without a count.
- `storage.slots.0.lanes` on all rows: ASUS gives PCIe 4.0 but no lane count.

## Blocked or limited sources

- Firecrawl hit its rate limit early in the run. Pages were fetched with curl instead.
- ifixit.com returned HTTP 429 (GuliKit Ally X joystick page).
- wepc.com returned HTTP 403.
- WebSearch does not allow theverge.com.
- `https://rog.asus.com/us/gaming-handhelds/rog-ally-allmodels/` returned HTTP 404.
- The Xbox Ally row used one extra NotebookCheck news page to find review links. That page gave no facts.
