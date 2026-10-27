# AYN: crawler notes

Crawled on 2026-10-27 by the ZOTAC / Acer / sweep crawler. See the sweep table in `acer.md`.

## Variant list

| Row id | Model | SoC id | Status | Release | Launch price (base) |
|---|---|---|---|---|---|
| `ayn-loki-max` | Loki Max | `r7-6800u` | shipped | 2023-06 | $750 (16 GB / 512 GB) |

## Rows skipped

- Loki Zero (Athlon Silver 3050e) and Loki MiniPro (Intel): below the $450 price floor.
- Loki (Ryzen 5 6600U): not checked further. AYN cancelled several Loki configs in 2023 for low orders, and `data/socs/` has no Ryzen 5 6600U file.
- AYN Odin / Thor lines: ARM / Android, out of scope.

## Data notes

- AYN's product page is gone, so no `*` source exists. Each group cites a review or reseller page.
- SSD form factor: two reviews say M.2 2242; Liliputing says 2230. The row uses 2242 and records the conflict.
- Price: Retro Handhelds says $750 at release; other coverage says $775 (pre-order list price). The row uses $750 and records the conflict.
- Dimensions come from DROIX: "around 9.7 x 3.7 x 1.5 inches (24.8 x 9.6 x 3.5)", one line for both the Loki and the Loki Max. 1.5 in is 38 mm, so thickness is uncertain (35-38 mm). Other listings give 248 x 98 x 20-23.7 mm (not verified).
- Weight 575 g is the spec quoted by Retro Handhelds, not a scale reading. DROIX gives 573 g for the Loki and Loki Max together.
- `battery.charge_w` is null. DROIX bundles a 100 W charger, which is not a device charge-rate spec.

## URLs used

| URL | Used for |
|---|---|
| https://liliputing.com/ayn-loki-max-begins-shipping-to-some-customers-handheld-gaming-pc-with-6-inch-display-and-ryzen-7-6800u/ | SoC, RAM, battery, Hall sticks, first shipments |
| https://droix.net/blogs/ayn-loki-ayn-loki-max-review-with-video/ | Dims, ports and locations, SSD 2242, Hall triggers |
| https://retrohandhelds.gg/loki-max-reaching-the-summit/ | Price, weight, gyro, Wi-Fi / BT, SSD 2242 |
| https://www.computerbase.de/2022-05/ayn-loki-mini-max-zen3-rdna2-alder-lake-u/ | Announce date |
| https://www.notebookcheck.net/AYN-LOKI-Prices-and-configurations-revealed-as-AYN-Technologies-puts-reservations-on-hold.623725.0.html | Checked; no Loki Max detail |
