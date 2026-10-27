# Lenovo crawl notes

Crawled 2026-10-27. Official source: Lenovo PSREF spec sheets (PDF), one per machine type.

## Variant list

| Row id | Model | Machine type | SoC (`soc_id`) | OS | Status |
|---|---|---|---|---|---|
| `legion-go` | Legion Go | 8APU1 (83E1) | Ryzen Z1 Extreme (`z1-extreme`) | Windows 11 | shipped |
| `legion-go-z1` | Legion Go | 8APU1 (83E1) | Ryzen Z1 (`z1`) | Windows 11 | shipped (regional SKUs only) |
| `legion-go-s-z2-go` | Legion Go S | 8ARP1 | Ryzen Z2 Go (`z2-go`) | Windows 11, SteamOS | shipped |
| `legion-go-s-z1-extreme` | Legion Go S | 8APU1 | Ryzen Z1 Extreme (`z1-extreme`) | Windows 11, SteamOS | shipped |
| `legion-go-2` | Legion Go 2 | 8ASP2 | Ryzen Z2 Extreme (`z2-extreme`) | Windows 11 | shipped |
| `legion-go-2-z2` | Legion Go 2 | 8AHP2 | Ryzen Z2 (`z2`) | Windows 11 | shipped |

## Rows added beyond the starting list

- `legion-go-z1`: the PSREF model tab for 8APU1 lists 9 models with the Ryzen Z1 (6C/12T): 83E1000CBR, 83E1000DBR (Brazil, 2024-03-30), 83E1004RMJ, 83E1004SMJ, 83E1004TMJ (2024-06), 83E1004XVN, 83E10050TA, 83E10051VN (2024-07), 83E10057AR (2024-11). No US model. The row copies the legion-go chassis data.
- `legion-go-2-z2`: PSREF 8AHP2 is a Legion Go 2 with the Ryzen Z2 (Zen 4), not the Z2 Extreme. It was the $1,099.99 base model at launch.

## Rows merged

- Legion Go S Windows and SteamOS: same hardware per SoC. Both PSREF sheets list Windows 11 and SteamOS. One row per SoC with both OS values.
- Legion Go 2 SteamOS edition ("Legion Go, powered by SteamOS (8.8", 2)"): announced at CES 2026 for June 2026 from $1,199, same hardware. No source confirms that it shipped, and both PSREF sheets (May and August 2026) list Windows only. The rows keep `os: ["Windows 11"]` and an `unresolved` entry for `os`.
- RAM and SSD capacity options share one row per SoC.

## Rows skipped

- Legion Go Fold (MWC 2026): concept prototype, not a product.
- Legion Go (8.8", 2) prototype shown at CES 2025: the same product as Legion Go 2 before final specs.
- Legion C700: Android, out of scope.

## Storage slot finding

- Legion Go (8APU1): true M.2 2242 slot.
- Legion Go S (8ARP1, 8APU1) and Legion Go 2 (8ASP2, 8AHP2): PSREF lists "One M.2 2280 PCIe 4.0 x4 slot", but the factory 512GB / 1TB drives are M.2 2242. The Go 2 Z2 Extreme also ships a 2TB M.2 2280 drive. Notebookcheck found a 2280 SSD in its 2TB Go 2 unit.

## URLs used

| Row | Official spec | Other sources |
|---|---|---|
| `legion-go` | https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_Go_8APU1/Legion_Go_8APU1_Spec.pdf | https://news.lenovo.com/pressroom/press-releases/legion-go-gaming-handheld-device-and-accessories/ (Hall sticks, port locations, haptics, date); https://www.notebookcheck.net/Lenovo-Legion-Go-gaming-handheld-review-Good-idea-not-quite-perfectly-executed.794034.0.html (845 g / 641 g measured); https://www.noticias3d.com/noticia/93250/lenovo-legion-go-disponible-precio.html (release date, $699.99) |
| `legion-go-z1` | same PSREF PDF | https://psref.lenovo.com/Product/Legion/Legion_Go_8APU1?tab=model (model list, read with Playwright) |
| `legion-go-s-z2-go` | https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_Go_S_8ARP1/Legion_Go_S_8ARP1_Spec.pdf | https://news.lenovo.com/pressroom/press-releases/lenovo-legion-unleashes-next-gen-gaming-power-at-ces-2025/ (Hall sticks, dates, prices); https://www.notebookcheck.net/Lenovo-Legion-Go-S-gaming-handheld-review-Steam-Deck-killer-or-Windows-victim.961296.0.html (Hall triggers, 738 g, port locations); https://www.notebookcheck.net/Lenovo-s-SteamOS-gaming-handheld-now-live-for-preorder-on-Best-Buy-but-with-a-50-price-bump.982704.0.html (SteamOS prices); https://liliputing.com/lenovo-legion-go-s-with-windows-launches-this-month-steamos-model-coming-in-may/ |
| `legion-go-s-z1-extreme` | https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_Go_S_8APU1/Legion_Go_S_8APU1_Spec.pdf | same as the Z2 Go row |
| `legion-go-2` | https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_Go_8ASP2/Legion_Go_8ASP2_Spec.pdf | https://news.lenovo.com/pressroom/press-releases/legion-gaming-devices-ai-tablets-software-best-in-customer-choice/ (Hall sticks, date); https://www.notebookcheck.net/Gaming-handheld-with-great-144-Hz-OLED-and-detachable-controllers-Lenovo-Legion-Go-2-review.1225235.0.html (922 g, VRR, port locations, single fan); https://www.notebookcheck.net/Lenovo-releases-Legion-Go-2-for-1-349-with-AMD-Ryzen-Z2-Extreme-and-32-GB-RAM.1106113.0.html (prices); https://gamingonlinux.com/2025/09/the-lenovo-legion-go-2-launches-in-october-its-heavier-and-very-pricey (launch month); https://www.androidauthority.com/lenovo-legion-go-2-steamos-launched-3628420/ (SteamOS edition) |
| `legion-go-2-z2` | https://psref.lenovo.com/syspool/Sys/PDF/Legion/Legion_Go_8AHP2/Legion_Go_8AHP2_Spec.pdf | same as `legion-go-2` |

## Weak points to re-check

- Release dates for `legion-go-s-z2-go` (2025-01), `legion-go-s-z1-extreme` (2025-05-25) and both Go 2 rows (2025-10) come from announced or retailer-listed dates, not confirmed first-sale dates.
- `legion-go-s-z2-go` `msrp_usd` (549.99) is the SteamOS 16GB/512GB price. The Windows 32GB/1TB model launched first at $729.99.
- `legion-go-s-z1-extreme` `msrp_usd` (749.99) comes from a Best Buy pre-order listing. Other outlets report $829.99 for a Z1 Extreme config.
- Trigger sensor type for the Legion Go and Legion Go 2 is not stated by any source checked.

## Blocked or limited sources

- liliputing.com: WebFetch returns 403. Firecrawl works.
- androidauthority.com: WebFetch returns 403. Firecrawl works.
- techradar.com, tomsguide.com: Firecrawl does not support them; WebFetch returned only the title.
- PSREF product pages render with JavaScript. The model tab needed Playwright. The spec PDFs download with curl.
- Firecrawl hit its shared rate limit (about 12 requests per minute) several times.
