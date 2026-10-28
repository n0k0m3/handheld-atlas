# Compare screen findings

## Summary
- Scope: the Compare screen at 1280×800, with extra passes at 1440×900, 760, 759, 700 and 400 px. Light theme. Headless Chromium through `playwright-cli -s=qa-compare`.
- I checked every grid text, delta pill and Best marker against `#atlas-data` in 58 queue/reference combinations. I checked the 2D scale in 88 view/layout/queue combinations.
- Findings: 0 × S1, 3 × S2, 3 × S3. There are also 8 observations.
- Biggest risk: below 760 px the grid header row is pushed down by the page-header height. It covers the "Overview" label and the MSRP and Released rows. At the contract phone width (400 px) the user cannot see the MSRP row.
- The core promise holds: the shapes are at true scale within 1 %, and the scale bar is correct within 1 px in all tested states.
- Console: clean in every flow (only the known favicon 404).

## Findings

### F1. Below 760 px the grid header row does not stick, and it covers the first grid rows  [S2]
- Where: Compare, grid `.cmpw.scroll`, widths 400, 700 and 759 px (all widths below the 760 px breakpoint). Light theme.
- Steps: 1. Clear storage and reload. 2. Open `#compare`. 3. Set the viewport to 400×800 (or 700×800). 4. Scroll to the grid.
- Expected: The header row with the device names sits at the top of the grid. It sticks under the page header while the user scrolls, as it does on desktop. All rows are visible.
- Actual:
  - The header row is drawn `--hdr-h` px below the top of the panel. An empty band appears above it, and the row covers the rows under it.
  - At 400 px (header 130 px): "Overview" (0..39 px), "MSRP" (39..77), "Released" (77..114) are fully under the header row. "Form factor" (114..152) is mostly under it.
  - At 700 px (header 90 px): "Overview" and "MSRP" are fully covered. "Released" is mostly covered.
  - The row does not stick to the viewport. At scrollY 1300 on 400 px, `.cgrid.hd` top is -212. The device names leave the screen for the remaining ~35 rows.
  - At 760 px and 1280 px the header row is at offset 1 px from the panel top and sticks at `top = 53` (= header height). Desktop is correct.
- Evidence: `s9c.js` read-out: `400: {scroll:true, hdOffsetFromPanelTop:131, hdH:130, hdrH:130, covered:["sec:Overview 0..39","MSRP 39..77","Released 77..114","Form factor 114..152"]}`, `700: {hdOffsetFromPanelTop:91, covered:["sec:Overview 40..79","MSRP 79..117","Released 117..154"]}`, `760: {scroll:false, hdOffsetFromPanelTop:1, covered:[]}`. Screenshot: `qa/compare/grid-header-covers-rows-400.png`. The MSRP row and the Overview label are not visible.
- Code: site/src/index.html:300 `.cgrid.hd { position: sticky; top: calc(var(--hdr-h) …) }` together with site/src/index.html:298 `.cmpw.scroll { overflow-x: auto; }`. The cause: `overflow-x:auto` makes the panel the scroll container for the sticky row. The panel never scrolls vertically, so the `top` offset only pushes the row down into the content.
- Reproduced twice from clean state: yes (three runs: `s9.js`, `s9b.js`, `s9c.js`).

### F2. Keyboard focus drops to `body` after each Compare control that re-renders the screen (hunch H1 confirmed)  [S2]
- Where: Compare, 1280×800. The controls are `#hide-same`, `#size-open`, `#view-*`, `#mode-*`, `#tab-2d`, `#tab-3d`, `.ccol` (Enter and Space), `#crm-<id>`, and the `.hid-note` "Show all rows" button.
- Steps: 1. Clear storage and reload on `#compare`. 2. Focus `#view-top`. 3. Press Enter. 4. Read `document.activeElement`. 5. Press Tab.
- Expected: Focus stays on the control that the user pressed, or moves to a logical next element. The page already does this for Browse controls.
- Actual: `document.activeElement` is `BODY` after all 13 tested activations. The next Tab goes to the first button of the screen ("← Back to list"). A keyboard user must Tab again through the header and the size panel to get back. Exception: the 3D preset chips `#pre-*` keep focus, because they do not call `renderCompare()`.
- Evidence: `h1.js` (two runs): `{"sel":"#view-top","before":"#view-top","after":"BODY","nextTab":"BUTTON.btn-t"}`. The same result occurs for `#hide-same`, `#size-open`, `#view-side`, `#view-front`, `#mode-side`, `#mode-overlay`, `#tab-3d`, `#tab-2d`, `.ccol[rog-xbox-ally-x]` + Enter, `.ccol[legion-go-2]` + Space, and `#crm-msi-claw-8-ai-plus` + Enter. Result for presets: `{"sel":"#pre-top","after":"#pre-top","nextTab":"#pre-side"}`.
- Code: site/src/index.html:1444-1448 (`hide-same`, `size-open`, `size-tab`, `size-view`, `size-mode`), :1431 (`setref`), :1462 (Enter/Space on `.ccol`), :1428 (`rm`). Each one calls `renderCompare()` (:1037), which replaces `#scr-compare` innerHTML. The handlers do not refocus. Compare this with :1435 `sort`, the `grp` case and the `chip` case: they refocus with `document.getElementById(t.id).focus()`.
- Reproduced twice from clean state: yes.

### F3. The add-slot dropdown overflows the viewport: the page scrolls horizontally and the "+ Compare" labels are off-screen  [S2]
- Where: Compare, add slot `#sq` / `#sq-dd`, at 1280×800 and 1440×900 with 2 or 3 devices, and at 400 px.
- Steps: 1. Clear storage and reload on `#compare`. 2. Click `#crm-msi-claw-8-ai-plus` (3 devices are left). 3. Click `#sq`. 4. Type `ayaneo`.
- Expected: The dropdown stays inside the viewport. Each item shows its action label ("+ Compare", "Added", "List full"). The body does not scroll horizontally (CONTRACT.md rule).
- Actual: There are two separate problems:
  - (a) The `.dd` box is placed from the left of the slot with a fixed 320 px width. With 3 devices at 1280 px the box spans x 1006..1326. At 1440 px it spans 1126..1446. The box extends past the right edge of the viewport even for short results ("steam": `scrollWidth` 1326 vs 1280).
  - (b) The `.dd-item` rows are wider than the `.dd` box when the sub-line is long. The items reach x = 1465 (3 devices) or 1377 (2 devices). All 8 "+ Compare" labels are off-screen (`actOffscreen 8/8`). The document gets horizontal scroll: `scrollWidth` 1465 vs `clientWidth` 1280. A horizontal scroll of 185 px shows the labels outside the dropdown box.
  - At 400 px the box spans x 246..566. The `.cmpw.scroll` wrapper clips it at 384, so the right part of each item is cut off.
- Evidence: `ovf2.js`: `"1280/3/ayaneo": {ddL:1006, ddR:1326, itemMaxR:1465, actOffscreen:"8/8", sw:1465, cw:1280}`, `"1280/2/ayaneo": {ddL:918, ddR:1238, itemMaxR:1377, actOffscreen:"8/8", sw:1377}`, `"1440/3/steam": {ddR:1446, sw:1446, cw:1440}`. `ovf.js` lists the overflowing elements: `BUTTON.dd-item r=1377 w=454` in a 320 px dropdown. Screenshots: `qa/compare/sq-dd-overflow-1280-3dev.png`, `qa/compare/sq-dd-overflow-1280-3dev-scrolledX.png`, `qa/compare/sq-dd-400.png`.
- Code: site/src/index.html:315 `.cslot .dd { left: 12px; right: auto; width: min(320px, calc(100vw - 48px)); }`. The box is anchored to the slot, not to the viewport. Also site/src/index.html:105 `.dd { … display: grid; }` with :111 `.dd-s { white-space: nowrap; … }`. The grid track takes the min-content width of the nowrap sub-line, so the item grows past the box. Note for the Header tester: `#hq-dd` uses the same `.dd` / `.dd-item` CSS.
- Reproduced twice from clean state: yes (`ovf.js`, `ovf2.js`, `ovf3.js`).

### F4. Negative deltas at an exact half percent round down by 1 (asymmetric rounding)  [S3]
- Where: Compare grid delta pills and the legend weight pill, all widths.
- Steps: 1. Clear storage and reload on `#compare` (default queue). 2. Click the ROG Xbox Ally X column to make it the reference. 3. Read the Battery › Capacity row.
- Expected: The magnitude is `round(|v − r| / r × 100)`. Steam Deck OLED 50 Wh vs Ally X 80 Wh = −37.5 %, so the pill reads "▼ 38%". The positive case +37.5 % reads "▲ 38%".
- Actual: The pill reads "▼ 37%". Other examples from the data:
  - Legion Go 2 74 Wh vs 80 Wh = −7.5 % shows "▼ 7%".
  - With Legion Go 2 (144 Hz) as reference, Steam Deck OLED 90 Hz = −37.5 % shows "▼ 37%".
  - With MSI Claw 8 AI+ (8″) as reference, Ally X 7″ = −12.5 % shows "▼ 12%".
  - Negative half-points occur in 17 of the 58 queue/reference combinations that I tested.
  - No other value differed. All texts, directions, classes and Best markers matched the data.
- Evidence: `s3.js`: `"Battery|Capacity [0] pill dom=▼ 37%/dn exp=▼ 38%/dn"`, `"Display|Size [1] pill dom=▼ 12%/dn exp=▼ 13%/dn"`, `"Display|Refresh [0] pill dom=▼ 37%/dn exp=▼ 38%/dn"`. `s4.js`: `{checks:58, out:[], roundingOnly:17}`.
- Code: site/src/index.html:628 `delta` — `Math.abs(Math.round(p))`. JS `Math.round(-37.5)` is `-37` (it rounds toward +∞), so negative half-points lose 1. The same expression shows "▼ 0%" for p = −0.5 exactly, where `= 0%` or "▼ 1%" is expected. The fix is `Math.round(Math.abs(p))`.
- Reproduced twice from clean state: yes.

### F5. Compare labels a different device "Reference" than Browse when the global reference is not in the queue  [S3]
- Where: Compare header `.ccol`, the legend, and the Browse reference pill. 1280×800.
- Steps: 1. Clear storage and reload on `#browse`. 2. Click `#ref-steam-deck-lcd` (the device is not in the compare queue). 3. Click `#nav-compare`. 4. Click `#nav-browse`.
- Expected: Both screens agree on which device is the reference. If Compare must fall back because the reference is not in the queue, it should say so.
- Actual:
  - Browse shows "Reference: Valve Steam Deck LCD".
  - Compare shows the Steam Deck OLED column with tag "Reference" and `aria-pressed="true"`. The legend shows "REF" on Steam Deck OLED, and all deltas are against the OLED.
  - The stored `refId` stays `steam-deck-lcd`, and Browse still shows the LCD afterwards.
  - When the user clicks any column, the global reference changes, and the Browse pill follows ("Reference: Lenovo Legion Go 2"). This part is consistent with the design of one global reference.
  - Judgment: the fallback to column 1 is intentional, and the one global reference is intended. The issue is only that Compare presents its fallback as "the" reference, with no hint, while Browse names another device.
- Evidence: `s3c.js`: `{browsePill:"Reference: Valve Steam Deck LCD", cmp:{cols:["steam-deck-oled|true|Reference", …], legendRef:["Valve Steam Deck OLED"], lsRef:"steam-deck-lcd"}, browsePill2:"Reference: Valve Steam Deck LCD"}`. `s3b.js` gives the same result with a seeded `refId`, and Browse changes to `ref-legion-go-2` after a column click.
- Code: site/src/index.html:1040 `renderCompare` — `cref = ref && inQ(ref.id) ? ref : (cols[0] || null)`. The cause: a silent fallback that the UI labels as "Reference".
- Reproduced twice from clean state: yes (a seeded run and a natural Browse flow).

### F6. The column header (`role="button"`) contains two nested buttons  [S3]
- Where: Compare header `.ccol[role=button][tabindex=0]`. It contains `#crm-<id>` (Remove) and `#copen2-<id>` (open device).
- Steps: 1. Open `#compare`. 2. Read the accessibility tree of `.cgrid.hd .ccol`.
- Expected: An element with role `button` has no interactive descendants. The ARIA `button` role has presentational children, and axe reports this as "nested-interactive".
- Actual: `- button "Use Valve Steam Deck OLED as reference" [pressed]: - button "Remove Valve Steam Deck OLED" - button "Steam Deck OLED"`. Each `.ccol` has 2 focusable descendants. Some screen readers flatten the content of a button, so the Remove and open buttons can be hard to reach. Mouse and keyboard behaviour is correct: the inner buttons do not change the reference.
- Evidence: `a11y.js`: `nested:[2,2,2,2]` and the aria snapshot above.
- Code: site/src/index.html:1145 `gridHtml` — the `.ccol` div gets `role="button"` and wraps the `xbtn` and `ccol-n` buttons.
- Reproduced twice from clean state: yes (the markup is static).

## Clean areas
- Default state: `h1` "Compare 4 handhelds", `.ccol` classes s1..s4, Steam Deck OLED has the `Reference` tag and `aria-pressed=true`, no add slot.
- Remove and add: `#crm-<id>` shows the slot. A search pick from `#sq` adds the device. When the queue goes from 2 to 3, the input clears, keeps focus, and the dropdown closes. Keyboard Tab + Enter in the dropdown adds the device. At 4 devices the slot goes. When the user removes all devices, the empty panel shows, and its "list" link goes to `#browse`.
- Differences only: the default queue has 5 identical rows (Status, Touch, Card slot, Gyro, OCuLink). The note says "5 identical rows hidden." The toggle off shows 39 rows, and all 34 differing rows carry `.diff`. The toggle state survives a reload in both directions. "Show all rows" works.
- Reference switching: a click, Enter, or Space on `.ccol` moves `.ref`, the tag, `aria-pressed`, the ref cells and all pills. A click on `#copen2-` opens the detail screen without a change to the reference. A remove of a non-reference column keeps the reference. A remove of the reference column moves it to the first column.
- Deltas and Best: 58 queue/reference combinations matched the data for every text, arrow, class (`up`/`dn`, `eq` for Width/Height), and Best marker (min for low rows, max for high rows, ties give several Best, none when all values are equal). The only difference is F4. Null values (`zotac-zone-pro`, `legion-go-z1` MSRP) show "—" with no pill and no Best. With a null reference value, the row has no pills.
- Size panel 2D: `#size-open` collapses and expands, and the state survives a reload. All 4 views × 2 layouts: sane `viewBox`, one `g.s<i>` per device with a `<title>` naming it, and an `aria-label` that names the view. In 88 combinations (11 queues), the shape width and height in px divided by the outline mm equal the SVG px/mm within 1 %, and the pairwise ratios match. The scale bar is correct within 1 px (max error 0.09 px). Top view grips have height = `d_max`. Side view grips have width = `d_max`. Grips appear only when `d_max > d`. Front screens are inside the outlines. Side-by-side shapes do not overlap. All shapes are inside the stage.
- Scale bar after resize: 1280 → 1440×900 → 1280 and 1280 → 700 → 1280, in Overlay and Side by side. The bar re-fits each time (error ≤ 0.04 px).
- Legend: W×H×D text, weight text, bar widths proportional to the heaviest device (±1 %), weight pill against the reference, and `REF` on the reference. Checked for 11 reference choices, including a device with no weight (`onexplayer-x1-pro-255h`).
- 3D: one `.dev3` per device. Slice counts 16/9/14/8 (inside 6..24). Width, height and depth use one scale. Each preset sets the exact `rotateX/rotateY` and `aria-pressed`. A real mouse drag changes the transform (−14/−30 → −33.2/18 as computed), `.drag` is removed on release, and all presets read `aria-pressed=false`. The X angle clamps at 89°. A right-button drag does nothing. The angle persists across a 2D/3D switch. The devices fit the stage at 1280, 700 and 400 px.
- Resize across 760 px: the screen re-renders. The grid gets `.scroll`, `min-width: 704px` and narrow columns, and returns to normal at 1280. No document horizontal overflow (except F3).
- Sticky header on desktop: at 1280×800, with scrollY of 563, 600, 883 and 1200, the `.cgrid.hd` top = 53 = header height.
- Console: no errors or warnings in any flow (favicon 404 excepted).
- H2 (scroll jump on chip click): not reproducible. My first run showed scrollY 200 → 0, but the chip was under the sticky header (`top` −6), so `page.click` auto-scrolled it into view. A second run with `page.mouse.click` at visible coordinates kept `scrollY` the same in all 15 cases (view, mode and tab chips, presets, `.ccol` clicks at scrollY 900/1200, `#hide-same`, `#size-open`, and "Show all rows" at the page bottom).
- H3 (long names overflow `.ccol`): not reproducible. With `onexplayer-x1-pro-255h`, `ayaneo-air-1s-limited`, `acer-predator-atlas-7` and `rog-xbox-ally-x` at 1280, 700 and 400 px, no child extends past its column and `scrollWidth = clientWidth`. Variants wrap. Screenshots: `qa/compare/h3-longname-1280.png`, `h3-longname-400.png`.

## Observations (not bugs)
- 3D angles are not saved. After a reload the view returns to 3/4 (−14°, −30°). `rx`/`ry` are not in `save()`.
- When the user adds the 4th device, the slot and `#sq` are removed, so focus falls to `body`. The code cannot refocus a removed input. It could move focus to the new column.
- When the reference value is 0 (for example NPU "None", or 0 trackpads), no column gets a pill. This is not even "= 0%" for equal values. The cause is the `!r` guard in `delta` (division by zero).
- The 2D SVG `aria-label` reads "Size overlay, Front view" in Side by side mode too.
- In the empty state, the heading reads "Compare 0 handhelds".
- The legend weight for an external-pack device (GPD Win 5, 940 g) has no "with pack" note. The grid row shows "940 g with pack".
- Dropdown sub-lines repeat the chip name when the variant equals the SoC name ("Ryzen 7 7840U · Ryzen 7 7840U"). This is a Header/search scope item.
- Test method note: `localStorage.clear()` followed by a hash change (for example `goto('#browse')` from `#compare`) runs `go()` → `save()`, which writes the in-memory state back. To get a clean state, navigate first, then clear, then reload.
