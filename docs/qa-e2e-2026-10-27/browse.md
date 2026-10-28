# Browse screen findings

## Summary
- Scope: the Browse screen at 1280×800 (light theme, headless Chromium, `http://127.0.0.1:8765/index.html`). One extra pass at 1440×900 with all column groups on. One short check at 700×800 for the filter chips.
- Covered: initial load, all 15 sort headers (2 clicks each, compared with an order computed from `#atlas-data`), column groups, reference and delta pills (every visible pill for 5 references, about 5,000 pills), sidebar filters, cards layout, the compare queue, header search, keyboard focus, and the console.
- Count: 0 × S1, 3 × S2, 6 × S3, 2 × S4.
- Biggest risk: the reference row. It stays pinned when it fails the filters (F1). It can also be set without any visible sign (F2). Every fresh visitor has a reference, so F1 affects every filter use by default.
- Console: clean in every flow. The only entry was the known favicon 404.

## Findings

### F1. Reference row stays pinned when it fails the filters, so counts disagree and the empty state never shows  [S2]
- Where: Browse, table and cards, 1280×800, light. This is hunch H1, now confirmed.
- Steps:
  1. Run `localStorage.clear()` and reload. The reference is Steam Deck OLED (the default).
  2. Tick brand GPD.
  3. Reset. Tick brand Valve, then stick TMR.
  4. Reset. Tick brand AYANEO only (do not click "Show all").
- Expected: The visible rows equal `#lbar-n`. When nothing matches, `#empty` shows and its "Reset filters" button works.
- Actual:
  - Step 2: `#lbar-n` = "26 devices", but 27 rows show. Row 1 is `steam-deck-oled` (brand Valve).
  - Step 3: `#lbar-n` = "0 devices", 1 row shows (Steam Deck OLED), `#empty` is hidden, and `#tblw` is visible. The "Reset filters" button in the empty message cannot be reached.
  - Step 4: `#lbar-n` = "32 devices", but `#more-btn` reads "Show all 33 devices".
  - The same happens with the AYANEO+GPD / shipped / Hall combination (38 vs 39 rows), with USB4 added (33 vs 34), with max weight 600 g (25 vs 26), and in the cards layout.
- Control check: with the reference cleared (`#ref-clear`), Valve + TMR shows `#empty` and hides `#tblw`. The empty-state Reset then restores 134 devices. So the empty state itself works.
- Evidence: `empty-valve-tmr.png` (shows "0 devices" above one Steam Deck OLED row) and `empty-noref.png` (the control case), both in `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/browse/`. Read-out at step 3: `{"lbar":"0 devices","nVis":1,"vis":["steam-deck-oled"],"empty":false,"tblw":true}`.
- Code: site/src/index.html:1010 `applyList`. `list.unshift(ref)` adds the reference without a filter check. Lines 1016–1019 then use `list.length` (with the reference) for `#more-btn`, `#empty`, and `#tblw`, while line 1021 uses `filt.length`. CONTRACT says that "a reference device pins to the top", so the pin can be by design. But the counts and the empty state must then agree with what shows.
- Reproduced twice from clean state: yes

### F2. Adding a device while no reference is set makes it a hidden reference: no pill, no ref row, no deltas until reload  [S2]
- Where: Browse table, 1280×800. Uses the row checkbox `#q-<id>` or the header search `#hq`.
- Steps (short path, no popover needed):
  1. Clear and reload. Click `#ref-clear` (the queue still holds 4 devices). Click "Show all".
  2. Untick `#q-rog-xbox-ally-x`, then tick it again.
- Result of the short path: storage has `refId: "rog-xbox-ally-x"`, but there is no `.refpill`, no `tr.ref`, and 0 delta pills (2 runs). With header search instead (`#ref-clear`, remove one item in `#qpop`, add "ally x" from `#hq`), the result is the same: `refId: "rog-ally-x"`, no pill.
- Steps (long path, used for the jump and the reload):
  1. Clear and reload. Open `#badge`, click "Clear" (the queue and the reference are now empty), then click outside.
  2. Tick `#q-gpd-win-5-395`.
  3. Tick brand GPD in the sidebar.
  4. Reload.
- Expected: Either the new queue item becomes the reference in the UI too (ref pill, `tr.ref`, delta pills), or the reference stays empty.
- Actual (long path):
  - Step 2: storage has `refId: "gpd-win-5-395"`, but there is no `.refpill`, no `tr.ref`, no `aria-pressed=true` ref button, and 0 delta pills.
  - Step 3: the row jumps to position 1 (it is pinned by `applyList`) but still has no ref style and no pills. In G3D order, `gpd-win-5-388` must come first.
  - Step 4: the reference appears ("Reference: GPD Win 5", `tr.ref`, 221 pills).
  - The same happens when the first device comes from header search ("claw 8": `refId` = `msi-claw-7-ai-plus`, no pill).
- Evidence: short path after the re-tick: `{"stRef":"rog-xbox-ally-x","queue":4,"pill":null,"refRows":[],"pills":0}`. Long path after step 2: `{"stRef":"gpd-win-5-395","pill":null,"refRows":[],"pressed":[],"pills":0,"first":"ayaneo-next-ii-395"}`. After step 4: `{"pill":"Reference: GPD Win 5","refRows":["gpd-win-5-395"],"pills":221}`.
- Code: site/src/index.html:815 `addQ`. `if (!state.refId) state.refId = id;` sets the reference, but `afterQ()` does not call `afterRef()` (830), so rows, cards and the list bar do not rebuild.
- Reproduced twice from clean state: yes

### F3. Focus drops to `<body>` after you set or clear the reference  [S2]
- Where: Browse table and cards, 1280×800, keyboard and mouse.
- Steps:
  1. Clear and reload.
  2. Focus `#ref-gpd-win-5-388` and press Enter.
  3. Focus `#ref-clear` and press Enter.
  4. Switch to cards, focus `#cref-gpd-win-5-388` and press Enter.
- Expected: Focus stays on the control that you used, or moves to a sensible target (for example the same ref button in its new row, or the ref pill).
- Actual: `document.activeElement` is `BODY` after steps 2, 3 and 4. A Tab press after step 2 goes to `#open-gpd-win-5-388` in the first row. The keyboard user loses their place in the list. The same result came from real `page.click`.
- Evidence: `{"refEnter":"BODY","refClearEnter":"BODY","crefEnter":"BODY"}` (two identical runs).
- Code: site/src/index.html:1430 (`case "ref"`) → 825 `setRef` → 830 `afterRef`. `buildRows`/`buildCards`/`renderListBar` replace the focused node, and the code does not restore focus. The sort and group handlers do restore it (1435–1437).
- Reproduced twice from clean state: yes

### F4. Focus drops to `<body>` after other Browse controls that re-render or hide themselves  [S3]
- Where: Browse, 1280×800.
- Steps (each from a clean state): click or press Enter on `#lay-cards`, `#lay-table`, `#more-btn`, a `.xbtn` in `#qpop`, "Clear" in `#qpop`, and the "Reset filters" button in `#empty`.
- Expected: Focus stays on the control, or moves to a logical neighbour.
- Actual: `document.activeElement` is `BODY` after each one. The causes: the layout segs are rebuilt by `renderListBar`. `#more-btn` and the empty-state button become hidden. `renderQpop` replaces the `.xbtn`.
- Evidence: `{"layCardsEnter":"BODY","layTableEnter":"BODY","moreEnter":"BODY"}`, popover `afterX.active = "BODY."`, `afterClear.active = "BODY"`, `afterEmptyReset.active = "BODY."`.
- Code: site/src/index.html:1438 (`layout` → `syncLayout` 1029 → `renderListBar` 947). 1443 `show-all` (`#more-btn` hidden at 1016). 869 `renderQpop` (via `rm`/`clear-queue`, 1428–1429).
- Reproduced twice from clean state: yes for `#lay-cards`, `#lay-table`, `#more-btn` (2 runs). Once each for the popover `.xbtn`, popover "Clear", and the empty-state Reset (same code path: the control is replaced or hidden).

### F5. Delta percent rounds negative half values toward zero, so it is 1 point low  [S3]
- Where: the table delta pills and the card stat pills (the shared `delta()`), 1280×800.
- Steps:
  1. Clear and reload (reference = Steam Deck OLED, 50 Wh). Click "Show all". Read the Battery pill on `onexplayer-mini-1195g7` (40.25 Wh).
  2. Set the reference to `rog-xbox-ally-x` (80 Wh). Read the Battery pill on `legion-go-2` (74 Wh).
  3. Set the reference to `gpd-win-5-395` (RAM 64 GB). Read the RAM pill on `rog-xbox-ally-x` (24 GB).
- Expected: magnitude = `round(|v − r| / r × 100)`, so 20 %, 8 % and 63 %.
- Actual: "▼ 19%", "▼ 7%" and "▼ 62%". A positive tie rounds up (+7.5 % shows 8 %), so the same gap shows a different number depending on direction. In all, 1 to 15 pills were affected per reference. The direction and class (`up`/`dn`) were correct on every one of about 5,000 pills audited.
- Evidence: audit read-out, for example `{"id":"onexplayer-mini-1195g7","k":"battery","exp":"▼ 20%","got":"▼ 19%","v":40.25,"r":50}` and `{"id":"rog-xbox-ally-x","k":"ram","exp":"▼ 63%","got":"▼ 62%","v":24,"r":64}`. The cards audit shows the same Battery pill.
- Code: site/src/index.html:628 `delta`. `Math.abs(Math.round(p))` must be `Math.round(Math.abs(p))`. (`Math.round(-19.5)` is −19.) The Compare screen uses the same function.
- Reproduced twice from clean state: yes

### F6. List stays sorted by a hidden column with no visible sort indicator  [S3]
- Where: Browse table, 1280×800. Covers hunch H2 (confirmed).
- Steps (path A):
  1. Clear and reload (sorted by G3D ↓).
  2. Click `#g-performance` to hide the group.
- Steps (path B):
  1. Clear and reload. Click `#g-controls`, then `#th-stick` (Sticks ↑).
  2. Remove every group chip.
  3. Reload.
- Expected: When the sort column leaves the table, the sort falls back to a visible column, or the UI shows the active sort somewhere.
- Actual:
  - Path A: the order stays G3D-descending (`steam-deck-oled, ayaneo-next-ii-395, gpd-win-5-388, …`), and no `th` has `aria-sort` other than `none`, and there is no arrow.
  - Path B: after the reload, `groups` returns to the 6 defaults (Controls is not among them), `sortK` stays `stick`, the order stays by stick type, and no header shows an arrow. The user cannot see or toggle the active sort.
- Evidence: path A `{"sortK":"g3d","sortedHeaders":0,"arrows":[]}`. Path B after reload `{"groups":["Price","Size","Performance","Display","Memory","Battery"],"sortK":"stick","arrow":[],"first5":["steam-deck-oled","aokzoe-a1x-8840u","aokzoe-a1x","gpd-win-5-385","gpd-win-5-388"]}`.
- Code: site/src/index.html:1436 (`case "grp"`) does not check `state.sortK` against `visCols()`. 750 `loadState` drops an empty `groups` array and keeps `sortK` (`if (COL[s.sortK])` only checks that the column exists). 958 `renderHead` only marks visible columns.
- Reproduced twice from clean state: yes for path B (2 runs). Path A ran once.

### F7. Default table overflows its wrapper at 1280 and 1440; the Ref column is off-screen  [S3]
- Where: Browse table, 1280×800 (default groups) and 1440×900 (all 8 groups).
- Steps:
  1. Clear and reload at 1280×800.
  2. Measure `#tblw` (`clientWidth` vs `scrollWidth`) and each `th` position.
  3. Repeat at 1440×900 with `#g-controls` and `#g-ports` on.
- Expected: The default column set fits a common desktop width, or the table shows that it scrolls (for example a sticky device column or a visible scroll cue).
- Actual:
  - 1280×800, default groups: the table is 1333 px wide in a 982 px wrapper (351 px hidden). Refresh is clipped. RAM, SSD, Battery and Ref (the reference button) are off-screen.
  - 1440×900, all groups: 1574 px in a 1142 px wrapper (432 px hidden: SSD, Battery, Sticks, Triggers, Ports, Ref).
  - The only horizontal scrollbar is at the bottom of `#tblw` (y ≈ 2563 px with 30 rows). The device column and the header are not sticky.
  - There is no body overflow (`scrollWidth == clientWidth` at both widths), so CONTRACT is met. This is a usability issue.
- Evidence: `default-1280-cut.png`, `wide-allgroups-1440.png`, `wide-allgroups-1280.png` in the browse work dir. Read-out: `{"client":982,"scroll":1333, "Refresh@1200-1257(OFF)","RAM@1257-1389(OFF)",…,"Ref@1572-1606(OFF)"}`.
- Code: site/src/index.html:945 `visCols` / 958 `renderHead` (column set), with the CSS for `.tbl` / `.tblw` (lines 1–413).
- Reproduced twice from clean state: yes (2 runs at 1280, 1 at 1440)

### F8. Header search matches stray digits and keeps data order, so exact models rank below others  [S3]
- Where: header search `#hq`, any screen, 1280×800. This confirms the orchestrator's observation.
- Steps:
  1. Clear and reload. Untick one queued device so the list is not full.
  2. Type `win 5` in `#hq`.
  3. Also try `legion go s`, `claw 8`, `onexplayer 2`.
- Expected: GPD Win 5 entries first.
- Actual:
  - `win 5` lists `gpd-win-4-2023-7640u`, `gpd-win-4-2024-8640u`, `gpd-win-4-2025`, then the 3 Win 5 variants, then 2 Win Max 2 entries. The token `5` matches "Ryzen 5 7640U" and "2025" anywhere in the name or SoC.
  - `legion go s` lists Legion Go 2 first. `claw 8` lists Claw 7 AI+ first.
  - `onexplayer 2` fills the 8-item cap and drops 4 X2 variants that also match.
  - In the tested queries, no exact model fell outside the cap.
- Evidence: `win5Names = ["GPD Win 4 / 2023 (Ryzen 5 7640U)…","GPD Win 4 / 2024 (Ryzen 5 8640U)…","GPD Win 4 / 2025 (Ryzen AI 9 HX 370)…","GPD Win 5 / Ryzen AI Max 385…",…]`.
- Code: site/src/index.html:850–854 `searchDevs`. This is a substring test per token on `_search` (name + SoC name + SoC id), then `.slice(0, 8)` in data order, with no ranking.
- Reproduced twice from clean state: yes for `win 5` (the orchestrator probe and my run). The other queries ran once.

### F9. Count label says "1 devices"  [S3]
- Where: list bar `#lbar-n`, 1280×800.
- Steps: 1. Clear and reload. 2. Tick brand AYN.
- Expected: "1 device".
- Actual: "1 devices". F1 also applies, so 2 rows show.
- Evidence: `{"lbar":"1 devices","n":2}`.
- Code: site/src/index.html:949 `renderListBar` and 1021 `applyList` append " devices" without a plural check. 1017 (`#more-btn`) has the same pattern, but it only shows for more than 30 rows.
- Reproduced twice from clean state: yes

### F10. One slider step below the maximum also hides every device with no price or no weight  [S4]
- Where: sidebar `#f-price` (min 350, max 3500, step 50) and `#f-weight` (min 390, max 1430, step 10).
- Steps: 1. Clear and reload. 2. Focus `#f-price` and press ArrowLeft once (label "$3,450"). 3. Reset. Do the same on `#f-weight` (label "1420 g").
- Expected: Not specified. The label reads "Any" at the maximum, as expected.
- Actual: The price filter drops from 134 to 111 devices. Only 1 device costs more than $3,450 (`gpd-win-max-3-395`, $3,499). The other 22 have `msrp_usd: null`. The weight filter drops to 119: 13 devices have no weight. The UI gives no cue that "unknown" values are now hidden. The code clearly intends this (`d.msrp_usd != null && …`). It is a product question, not a defect.
- Evidence: `{"pv":3450,"pl":"$3,450","lbar":"111 devices","exp":111}`, with 22 ids in `nullPrice` and 13 in `nullWeight`.
- Code: site/src/index.html:929–930 `filtered`.
- Reproduced twice from clean state: yes ("$3,450 111 devices" and "1420 g 119 devices" both times)

### F11. "Clear" in the compare popover also clears the Browse reference  [S4]
- Where: `#badge` → `#qpop` → "Clear", 1280×800. This is hunch H3, confirmed.
- Steps: 1. Clear and reload. 2. Open `#badge`, click "Clear".
- Expected: The README and CONTRACT say nothing about this. CONTRACT ties the reference to Browse ("A reference device pins to the top and drives the delta pills"), not to the queue.
- Actual: The queue empties, `refId` becomes null, `.refpill` disappears, and no `tr.ref` remains. A user who set a reference for browsing loses it when they empty the compare list. Combined with F2, the next added device then becomes a hidden reference. Removing the reference device from the queue with `.xbtn` also moves the reference to the next queue item (`legion-go-2`).
- Evidence: `afterClear = {"queue":[],"ref":null,"pill":false,"refRows":0,"badge":"0/4"}`. `afterXref = {"ref":"legion-go-2","pill":"Reference: Lenovo Legion Go 2"}`.
- Code: site/src/index.html:1429 (`case "clear-queue"`: `state.refId = null`), 812 `removeQ`.
- Reproduced twice from clean state: yes

## Clean areas
- Initial load (clean storage): `#cnt` = 134. The eyebrow reads "134 x86 handhelds · 2022 onward". The queue holds the 4 default ids and the badge reads `4/4`. The ref pill shows "Valve Steam Deck OLED". Row 1 is `steam-deck-oled` with class `ref`. G3D has `aria-sort="descending"` and "↓". 30 rows show, plus "Show all 134 devices". After the click, 134 rows show and the button hides. `#empty` is hidden. The route is `#browse`.
- Sorting: all 15 headers, 2 clicks each, with all groups on and all rows shown. The visible order matched the order computed from `#atlas-data` on all 30 checks (nulls last both ways, name tie-break, `localeCompare` numeric for text). On the first click, `price`, `weight`, `soc`, `ssd`, `stick`, `trig` and `ports` sort ascending, and the others descending. `aria-sort` and the arrow were correct, only one header was marked, and the reference stayed first.
- Column groups: each of the 8 chips, toggled off and on. The header and row cell counts and the column order follow `GROUPS` order on every step. `aria-pressed` and "✓/+" were correct.
- Delta pills: 6 references (`steam-deck-oled`, `rog-xbox-ally-x`, `zotac-zone-pro` with no price, `gpd-win-5-395`, `legion-go-z1`, `ayaneo-slide`). Every visible pill was checked. Direction and `up`/`dn`/`eq` class were correct everywhere. There were no pills on `dims`, `res` or text columns, and none on the reference row. With no reference price, there were no price pills. `#ref-<id>` toggles and `#ref-clear` clears. The state persists.
- Filter counts: all 21 checkbox counts (13 brands, 3 statuses, 5 stick types) match the data. Brand + status + stick + USB4 combinations match a data-side recount (apart from F1). The $800 and 600 g slider values match. Reset restores all defaults (`maxPrice` 3500, `maxWeight` 1430, labels "Any", USB4 off, 134).
- Cards layout: same set and order as the table. Sort chips: 5 keys × 2 clicks, correct order, arrow and `aria-pressed`. All 119 cards have `svg.sil` with a path. Card stat pills are correct (apart from F5). The add button states "Add to compare" / "In compare ✓" / "List full" (disabled) are correct. `#cref-<id>` sets and clears the reference. Back to the table: sort, filters, queue, groups and checkboxes are kept.
- Compare queue: checkboxes up to 4. The other 130 become disabled, and a forced click on a disabled one does nothing. Untick re-enables them. The badge count follows. The popover shows items in queue order with s1–s4 colour dots. `.xbtn` removes an item. "Clear" empties the queue. "Open comparison" goes to `#compare` with the same 4 devices. Escape closes the popover and returns focus to `#badge`. An outside click closes it.
- Header search: the cap is 8 ("ayaneo": 32 matches, 8 shown). "Added" and "List full" items are disabled. A click on a result adds it, clears the input, and keeps focus in `#hq`. Outside click and Escape close the dropdown. Junk input shows "No device matches “zzqx<b>”." with the text escaped.
- Keyboard focus that is kept: `#th-<k>`, `#g-<slug>`, `#sort-c-<k>`, `.fchk` checkboxes, `#f-usb4`, `#f-reset`, `#q-<id>`, and (at 700 px) `#tf-toggle`, `#tf-brands-gpd`, `#tf-usb4`, `#tf-reset`.
- Persistence: filters, sliders, USB4, sort, groups and the reference survive a reload, with an identical DOM read-out.
- Overflow: no body horizontal scroll at 1280 or 1440. No element past `innerWidth` outside an `overflow-x:auto` container.
- Console: no errors or warnings in any flow (favicon 404 only, at first load).

## Observations (not bugs)
- Removing every column group leaves a table with only Compare / Device / Ref, and this is saved as `groups: []`. On reload, `loadState` ignores the empty array and restores the 6 defaults (site/src/index.html:750). The code is clearly intentional. F6 covers its side effect on the sort.
- Ports sorts by a hidden score (`portScore`) but follows the text rule, so the first click is ascending: the weakest ports come first under "Ports ↑" (site/src/index.html:652, 1026).
- Wording for unknown values differs. The SSD cell shows lowercase "not stated" for 5 devices with `form_factor: "other"` (for example `acer-nitro-blaze-7`), but `SSD_LABEL.other` is "Other" (site/src/index.html:593). The stick filter calls a null stick type "Not stated", while the Sticks cell shows "—" (code read only, not checked in the DOM).
- A device ticked in the table can be the reference while it is also in the queue. Removing it from the queue moves the reference to the next queue item, even if the user set it by hand in Browse.
- In headless Chromium, `#tblw` has no scrollbar gutter (`offsetHeight − clientHeight` = 0). On desktop browsers with classic scrollbars, the bar shows at the bottom of the table.
