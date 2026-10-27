# MSI crawl notes

Crawled 2026-10-27. Official source: MSI spec pages at `https://www.msi.com/Handheld/<model>/Specification`, read with Playwright (WebFetch and curl return 403).

## Variant list

| Row id | Model | Model code | SoC (`soc_id`) | Status |
|---|---|---|---|---|
| `msi-claw-a1m-135h` | Claw A1M | A1M | Core Ultra 5 135H (`cu5-135h`) | shipped |
| `msi-claw-a1m-155h` | Claw A1M | A1M | Core Ultra 7 155H (`cu7-155h`) | shipped |
| `msi-claw-7-ai-plus` | Claw 7 AI+ | A2VM | Core Ultra 7 258V (`cu7-258v`) | shipped |
| `msi-claw-8-ai-plus` | Claw 8 AI+ | A2VM | Core Ultra 7 258V (`cu7-258v`) | shipped |
| `msi-claw-a8` | Claw A8 | BZ2EM | Ryzen Z2 Extreme (`z2-extreme`) | shipped |
| `msi-claw-8-ex-ai-plus` | Claw 8 EX AI+ | CG3EM | Intel Arc G3 Extreme (`arc-g3-extreme`) | shipped |
| `msi-claw-8-ex-ai-plus-cg3m` | Claw 8 EX AI+ | CG3M | Intel Arc G3 (`arc-g3`, file added by the SoC agent) | shipped (US store: In Stock) |

The MSI site menu (read 2026-10-27) lists these handhelds: Claw A8 BZ2EM, Claw 8 AI+ Polar Tempest Edition A2VM, Claw 8 AI+ A2VM, Claw 7 AI+ A2VM, Claw 8 EX AI+ CG3MX, Claw 8 EX AI+ CG3EM, Claw 8 AI+ Glacier Blue Edition A2VM. The Claw A1M spec page is still online.

## Claw 8 EX AI+ CG3M (Intel Arc G3)

The first crawl did not write this row because `data/socs/` had no `arc-g3` file. The coordinator asked for the row after the SoC agent added `arc-g3`. Until that file lands, the validator reports one expected error: `soc_id 'arc-g3' has no file in data/socs/`.

- Spec page: https://www.msi.com/Handheld/Claw-8-EX-AI-Plus-CG3MX/Specification
- CPU: Intel Arc G3. GPU: Intel Arc B370 (MSI spec page). The MSI US store lists "Arc Graphics build-in B390 12 Xe-Cores" for the same SKU; this is recorded as a conflict, and the spec page wins.
- Every other spec line matches the CG3EM page: 8" 1920x1200 48-120Hz VRR touch, LPDDR5x max 32GB, 1x M.2 2280 PCIe Gen4, Hall sticks and triggers, HD haptics, 6-axis IMU, fingerprint, Wi-Fi 7 + BT 6, 2x Thunderbolt 4, microSD Express, 80Wh 4-cell, 65W adapter, 296-321 x 130 x 25-48 mm, 785 g.
- Colour: Luminous Blue.
- US store: https://us-store.msi.com/Claw-8-EX-AI-CG3M-072USY. SKU CG3M-072USY, 32GB LPDDR5x, 512GB NVMe Gen4x4 2280, 500 nits, In Stock at $1,499.00 on 2026-10-27.
- Not found: announce date, first-sale date, launch price. Launch coverage (MSI COMPUTEX release, Engadget, Guru3D) names only the Arc G3 Extreme model.
- Variants now read "Arc G3 Extreme (CG3EM)" and "Arc G3 (CG3M)".

## Rows merged

- Claw A1M 155H 512GB and 1TB: one row (capacity only).
- Claw 8 AI+ colour editions: Polar Tempest Edition, Glacier Blue Edition, Polar Void Edition (limited, shown at CES 2026). Same A2VM hardware. The Glacier Blue spec page lists the same M.2 2230 slot, 258V, 80Wh and 795 g. Notebookcheck CES 2026 coverage said Glacier Blue would use M.2 2280; the MSI page does not confirm it.
- Super Pack and Launch Pack bundles: same hardware, different adapter or accessories.
- Claw A8 colours Neon Green and Polar Tempest: one row.

## Variants reported but not sold

- Claw 8 AI+ with Core Ultra 7 256V / 16GB: reported by VideoCardz in December 2024. No SKU found.
- Claw 8 AI+ with Core Ultra 5 228V: a prototype seen on Reddit. Notebookcheck says MSI dropped it.

## Port kind decisions

- Claw A1M, Claw 7 AI+, Claw 8 AI+, Claw 8 EX AI+: MSI says "Thunderbolt 4", so `kind` is `TB4`.
- Claw A8: MSI says "USB4 / DisplayPort / Power Delivery 3.0 / Thunderbolt 4 compatible". The port is AMD USB4, not Thunderbolt-certified, so `kind` is `USB4` with the MSI wording in `note`.

## URLs used

| Row | Official spec | Other sources |
|---|---|---|
| A1M rows | https://www.msi.com/Handheld/Claw-A1MX/Specification | https://en.wikipedia.org/wiki/MSI_Claw_A1M (CPU options, release dates, launch prices; uncited infobox); https://www.notebookcheck.net/MSI-Claw-review-The-gaming-handheld-with-an-Intel-Core-Ultra-processor-disappoints.848787.0.html (672 g, VRR, port locations) |
| `msi-claw-8-ai-plus` | https://www.msi.com/Handheld/Claw-8-AI-plus-A2VMX/Specification | https://www.notebookcheck.net/MSI-Claw-8-AI-review-The-best-gaming-handheld-thanks-to-Intel-Lunar-Lake.974004.0.html (258V, 793 g, $899.99); https://www.notebookcheck.net/MSI-confirms-launch-timeline-and-prices-of-its-new-Intel-Lunar-Lake-powered-Claw-gaming-handhelds.929552.0.html; https://lowyat.net/2024/338889/msi-claw-8-ai-officially-available; https://www.msi.com/Handheld/Claw-8-AI-Plus-Glacier-Blue-Edition-A2VMX/Specification |
| `msi-claw-7-ai-plus` | https://www.msi.com/Handheld/Claw-7-AI-plus-A2VMX/Specification | https://www.notebookcheck.net/MSI-confirms-launch-timeline-and-prices-of-its-new-Intel-Lunar-Lake-powered-Claw-gaming-handhelds.929552.0.html (258V, $799, 2025-01-15) |
| `msi-claw-a8` | https://www.msi.com/Handheld/Claw-A8-BZ2EMX/Specification | https://www.notebookcheck.net/8-inch-gaming-handheld-now-also-with-AMD-MSI-Claw-A8-review.1185107.0.html (765 g, LPDDR5x-8000 dual-channel); https://www.notebookcheck.net/MSI-expands-availability-of-Z2-Extreme-equipped-Claw-A8-gaming-handheld.1206980.0.html (China July 2025, US $1,149) |
| `msi-claw-8-ex-ai-plus` | https://www.msi.com/Handheld/Claw-8-EX-AI-Plus-CG3EMX/Specification | https://www.msi.com/news/detail/MSI-Debuts-Claw-8-EX-AI--Handheld-with-Intel--Arc-G3-Extreme-and-Titan-18-HX-Dragon-Edition-Draco-Epic-at-COMPUTEX-2026-148880 (announce 2026-06-01); https://www.notebookcheck.net/intel-s-arc-g3-extreme-changes-the-handheld-game-msi-claw-8-ex-ai-review.1325574.0.html (786 g, $1,799, chip detail); https://us-store.msi.com/Claw-8-EX-AI-CG3EM (dual-channel, 500 nits); https://us-store.msi.com/Claw-8-EX-AI-CG3EM-024US (1TB SKU); https://tech-insider.org/intel-arc-g3-extreme-handheld-msi-claw-8-2026/ (2026-06-23 launch) |

## Weak points to re-check

- A1M release dates and prices come from an uncited Wikipedia infobox.
- `msi-claw-8-ai-plus` `release_date` (2024-12) comes from a Lowyat note that MSI moved the launch to December 2024. MSI gave 2025-01-15 as the US shelf date.
- `msi-claw-8-ai-plus` `capacities_gb` includes 512 only from a Notebookcheck spec box that conflicts with its own text.
- `msi-claw-8-ex-ai-plus` `dims_mm.handheld.w` uses 321 mm, the larger of MSI's "296-321" width.
- No MSI page states the position of the M1/M2 macro buttons, so `rear_buttons` stays null.

## Blocked or limited sources

- msi.com and us-store.msi.com: WebFetch and curl return 403. Playwright works.
- liliputing.com: WebFetch returns 403. Firecrawl works. No Liliputing article was needed for MSI rows.
- Firecrawl hit its shared rate limit (about 12 requests per minute) several times.
