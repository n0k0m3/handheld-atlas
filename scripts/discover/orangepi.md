# Orange Pi: crawler notes

Crawled on 2026-10-27 by the ZOTAC / Acer / sweep crawler. See the sweep table in `acer.md`.

## Variant list

| Row id | Model | SoC id | Status | Release | Price (base, latest announced) |
|---|---|---|---|---|---|
| `orange-pi-neo-7840u` | Neo | `r7-7840u` | announced | — | $450 (16 GB / 512 GB); $499 in March 2024 |
| `orange-pi-neo-8840u` | Neo | `r7-8840u` | announced | — | $550 (32 GB / 512 GB); $599 in March 2024 |

The Neo was announced with Manjaro Gaming Edition. The developers put it "on ice" in March 2026 because of DDR5 and SSD prices. It has US and EU certifications but no launch date.

## Rows merged

- Each SoC row covers all its RAM and SSD sizes (16 / 32 GB; 512 GB to 2 TB).

## Data notes

- The official spec page (neo.manjaro.org) lists only the 7840U. The 8840U row reuses the shared chassis, ports, screen and controls from that page.
- No weight is published.
- `announce_date` is null for the 7840U row. The 7840U model was public before the March 2024 pricing article, but no fetched source gives the first reveal date. The 8840U row uses 2024-03, when that option was announced.
- `msrp_usd` is the latest announced price; the March 2024 price is in `conflicts[]`.

## URLs used

| URL | Used for |
|---|---|
| https://neo.manjaro.org/ | Official spec table (`*`) |
| https://www.gamingonlinux.com/2024/03/orange-pi-neo-linux-gaming-handheld-starts-at-499-with-ryzen-7840u-ryzen-8840u-at-599/ | 2024 prices, 8840U option |
| https://www.gamingonlinux.com/2025/06/pricing-announced-for-the-orange-pi-neo-gaming-handheld-with-manjaro-linux/ | 2025 prices |
| https://forum.manjaro.org/t/development-q-a-orangepi-neo-01/156450 | 8840U ships with 32 GB |
| https://liliputing.com/orange-pi-neo-linux-powered-handheld-gaming-pc-delayed-indefinitely-due-to-ram-ssd-increases/ | On-hold status (2026-03-01) |
