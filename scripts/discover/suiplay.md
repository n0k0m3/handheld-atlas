# SuiPlay: crawler notes

Crawled on 2026-10-27 by the ZOTAC / Acer / sweep crawler. See the sweep table in `acer.md`.

## Variant list

| Row id | Model | SoC id | Status | Release | Launch price (base) |
|---|---|---|---|---|---|
| `suiplay-0x1` | SuiPlay0X1 | `r7-7840u` | shipped | 2025 | $599 (16 GB / 512 GB, only config) |

The device comes from Mysten Labs (Sui) and was built with Playtron. It runs Playtron GameOS. Pre-orders opened in 2024. Mysten Labs produced 10,000 units. By 2025-08-22, 2,000 units had shipped. Shipping paused over US import duties, then resumed. The official site now shows "Sold Out".

## Rows skipped

- None.

## Data notes

- No source in the fetch budget lists the ports, the stick sensor or the trigger sensor. These stay null with `unresolved` entries.
- Battery is given as "48Wh - 50Wh"; the row uses 48 Wh.
- One Reddit post lists 239 x 102 x 13.9 mm / 398 g "with Joy-Con attached". That describes a different device and was ignored.

## URLs used

| URL | Used for |
|---|---|
| https://www.suiplay0x1.com/ | Official spec block (`*`), price, sold-out status |
| https://decrypt.co/247583/mysten-labs-unveils-specs-and-updates-on-suiplay0x1-the-first-blockchain-based-handheld-gaming-device | Dimensions, weight (Mysten Labs press release) |
| https://decrypt.co/336347/crypto-gaming-handheld-shipments-delayed-excessive-import-duties | Shipped units (release date) |
