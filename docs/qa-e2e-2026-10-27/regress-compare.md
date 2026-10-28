# Compare re-test (regress) findings

Session `qa-rg-compare`, headless Chromium through `playwright-cli` 0.1.22, page `http://127.0.0.1:8765/index.html#compare`, light theme. Scripts and screenshots are in `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/regress-compare/`. Line numbers refer to `site/src/index.html` (1726 lines now).

## Verdicts

| Finding | Verdict | Evidence |
|---|---|---|
| 1 Grid wider than the window 760 to 890 px | **Fixed** | 4 and 3 devices at 760, 800, 850, 880, 899, 900, 960, 1280: `scrollWidth === clientWidth` in all 16 cells. `.cmpw.scroll` is on exactly when 860 px > panel width: on at 909 (panel 859), off at 910 (panel 860). 2 devices (690 px) at 760/800: off. Resize without reload 1280→960→900→899→…→760→…→1280 and back: the wrapper toggles at each crossing (`f1.js`, `f1b.js`). |
| 2 `#sq-dd` rows wider than the box | **Fixed** | 1280, 1440, 960 with 3 and 2 devices, queries `ayaneo`, `steam`, `onexplayer x1`: every `.dd-item` right ≤ box right (box 923..1243, items ≤ 1238 at 1280). `.dd-s` has `text-overflow: ellipsis` and 3 of 8 sub-lines truncate. All "+ Compare" / "Added" labels inside the box and hit-testable. No document overflow (`f3.js`). |
| 3 Add-slot dropdown anchored to the slot's left | **Fixed** | Box right = slot right − 12 at every width (1280: 1243 vs 1255; 1440: 1403 vs 1415; 960: 923 vs 935). At 400 px after `scrollLeft` to the slot: box 51..371 inside the container 16..384, 3 and 2 devices (`f3.js`). |
| 4 Header row covers rows below 760 px, does not stick | **Fixed** | 400 and 700: at scroll 0 the row is 1 px below the panel top, transform empty, covers nothing. Grid 600 px up: `translateY(600px)`, row top 91.1 (400) / 90.5 (700) vs `#hdr` bottom 89.8; device names on top of the rows (hit test). Wheel +400: follows. Past the grid end (viewport 300 px tall): the row stops with its bottom at the panel bottom. Container `scrollLeft` 180 while translated: header columns and row columns share x (−163, −59, 91, 241, 391). `#sq-dd` opens 16 px under the slot box inside the translated row and follows a further wheel scroll; keyboard add from there works. Screenshot `f4-translated-header-dd-400.png`. Residual 1 px offset: see F4 below (S4). |
| 8 Focus after Compare controls | **Partly** | Real Enter/Space on `#hide-same`, `#size-open` (both directions), `#tab-2d`, `#tab-3d`, `#view-*` ×4, `#mode-*` ×2, `#pre-*`, `#cref2-<id>` ×3: focus stays on the same id, next Tab is the next control, `scrollY` unchanged. "Show all rows" → `#hide-same`. "← Back to list" and empty-state "list" → `#lbar`. `#copen2-` → `#dt-h1`. `#nav-compare` and queue "Open comparison" → `#cmp-h1`; nav click on the same screen keeps focus. **Not as specified:** `#crm-<id>` always focuses the first column's remove button, not the next column's or `#sq` (F2 below). |
| 10 Rounding of negative half values | **Fixed** | Ally X reference: Steam Deck OLED 50 vs 80 Wh = "▼ 38%" (was 37), Legion Go 2 74 Wh = "▼ 8%". Zero reference (trackpads 0): equal 0 → "= 0%", 1 and 2 → no pill. 49 queue/reference combinations × hideSame on/off = 98 checks, 3,195 pills and 1,462 Best markers, 0 mismatches (`f10.js`). |
| 21 Headings | **Fixed** (headings) | "Compare 1 handheld" with one device; "Nothing to compare yet" with none. The hidden-rows note still has no plural check: F1 below. |
| 22 Fallback column labelled "Reference" | **Fixed** | Seeded `refId: "steam-deck-lcd"`, default queue: column 1 tag "Baseline", legend "BASE", hint "The reference (Valve Steam Deck LCD) is not in this list, so deltas compare against the first column. …". Same result from the natural flow (Browse, filter Valve, `#ref-steam-deck-lcd`, `#nav-compare`). Click `#cref2-legion-go-2`: tag "Reference", legend "REF", stored `refId` legion-go-2, Browse pill "Reference: Lenovo Legion Go 2", `tr.ref` legion-go-2. |
| 23 `.ccol` role=button wraps buttons | **Fixed** | `.ccol` has no `role`, `tabindex`, `aria-pressed` (`tabIndex` −1). `#cref2-<id>` is a `BUTTON` with `aria-pressed` and `aria-label "Use … as reference"`. No button or `[role=button]` in `#scr-compare` has a focusable descendant. Tab order per column: `crm-`, `copen2-`, `cref2-` for all 4 columns. Mouse click on the column body still sets the reference. |
| 34 `#stage3d` has no role | **Fixed** | `role="img"`, aria snapshot `img "3D view. Drag to rotate."`. |
| Also: 3D angles persist | **Fixed** | Real drag +100/+50 px from iso: `rotateX(-34deg) rotateY(10deg)` = expected, stored `rx −34, ry 10`, all presets unpressed; same after reload. `#pre-top` → reload → `rotateX(-80deg)`, `#pre-top` pressed. |
| Also: legend "with pack" | **Fixed** | GPD Win 5 "940 g with pack", OneXFly Apex Air "1,109 g with pack"; 13 legend runs, 0 issues. |

## Summary
- Covered findings 1, 2 (`#sq-dd`), 3, 4, 8 (Compare controls), 10, 21 (headings), 22, 23, 34 and the two "Also" items, plus the regress list from the original Compare report.
- Verdicts: 11 Fixed, 1 Partly (finding 8, remove-button neighbour).
- New findings: 0 × S1, 0 × S2, 3 × S3, 1 × S4.
- Biggest risk: the grid container loses its horizontal scroll on every Compare re-render. The restored focus then sits off-screen. The finding 1 fix extends this to 760 to 909 px (F3).
- Console: only the known favicon 404 in the whole session. Every `run-code` `errs` array was empty.

## Findings

### F1. Hidden-rows note reads "1 identical rows hidden."  [S3]
- Where: Compare, `.hid-note` under the grid, any width.
- Steps: 1. Go to `#compare`, clear storage. 2. Seed `{"v":3,"queue":["ayaneo-air-5560u","onexplayer-x1-8840u","steam-deck-oled","onexplayer-mini-pro-6800u"],"refId":"ayaneo-air-5560u","route":"compare","hideSame":true}`. 3. Reload. 4. Read `.hid-note`.
- Expected: "1 identical row hidden." (finding 21 added a plural helper for the other counts).
- Actual: "1 identical rows hidden. Show all rows". Only the Status row is identical (all four "Shipped").
- Evidence: `f21b.js` and `fextra.js` `note1: "1 identical rows hidden. Show all rows"`. In a model sweep, no pair has fewer than 3 identical rows, but 3- and 4-device queues with exactly one identical row exist.
- Code: site/src/index.html:1273 `gridHtml` — `hidden + ' identical rows hidden. '` does not use `plural()`.
- Reproduced twice from clean state: yes.

### F2. Removing a column moves focus to the first column, not the next one  [S3]
- Where: Compare header, `#crm-<id>`, 1280×800 (same at 400).
- Steps: 1. Clean state, default queue on `#compare`. 2. Focus `#crm-legion-go-2` (column 3). 3. Press Enter. 4. Read `document.activeElement`.
- Expected (FIXNOTES 8): the next column's remove button (`#crm-msi-claw-8-ai-plus`), or `#sq` when no column follows.
- Actual: `#crm-steam-deck-oled` (column 1) in every case: remove column 2, 3 or 4 of 4, and column 2 of 3 (where `#sq` follows). Only the removal of column 1 matches, because the next column becomes the first one. The `#sq` fallback can never run: with zero columns the empty state shows and focus goes to `#cmp-h1`.
- Evidence: `f8.js` and `fextra.js`: `remove legion-go-2 of [4] -> active=crm-steam-deck-oled`, `remove msi-claw-8-ai-plus of [4] -> active=crm-steam-deck-oled`, `remove rog-xbox-ally-x of [3] -> active=crm-steam-deck-oled`. Focus is not lost to `body`, but a keyboard user goes back to column 1.
- Code: site/src/index.html:1564 `restoreFocus` case `rm` — `$("#scr-compare .ccol .xbtn")` takes the first match. It needs the removed column's index (kept before `removeQ`), then the column at that index, else `#sq`. If the author meant "next" as "first remaining", this is only a wording mismatch with FIXNOTES. The `#sq` fallback is still dead code.
- Reproduced twice from clean state: yes.

### F3. The grid container scrolls back to column 1 after every re-render; the focused control is then off-screen  [S3]
- Where: Compare grid inside `.cmpw.scroll`: 400 px, and since the finding 1 fix also 760 to 909 px. Keyboard and mouse.
- Steps: 1. Clean state, default queue, viewport 400×800 (or 800×800). 2. Scroll the grid container to the right end (`scrollLeft` 338 at 400, 110 at 800). 3. Press Enter on `#cref2-msi-claw-8-ai-plus` (or click it).
- Expected: the grid stays where the user scrolled it, and the focused "Reference" button stays visible.
- Actual: `scrollLeft` returns to 0. Focus is restored to `#cref2-msi-claw-8-ai-plus` with `preventScroll`, so the button sits at x 642..709 (400 px) or 806..873 (800 px), outside the container (right edge 384 / 776). The user sees columns 1 and 2 and no focus ring. Every Compare control that re-renders does the same: size chips, `#hide-same`, remove.
- Evidence: `fhscroll.js`: `400 key: scrollLeft 338 -> 0 … btnVisible:false`, `800 mouse: scrollLeft 110 -> 0 … btnVisible:false`. `fhscroll3.js` at 400: `#hide-same: 200 -> 0`, `#view-top: 200 -> 0`, `#crm-msi-claw-8-ai-plus: 200 -> 0`. Screenshots `hscroll-before-400.png`, `hscroll-reset-after-400.png`.
- Code: site/src/index.html:1140 `renderCompare` replaces `#scr-compare` innerHTML and does not carry over `.cmpw.scrollLeft`; site/src/index.html:1554 `focusId` uses `focus({ preventScroll: true })`, so the browser does not scroll the restored control into view either. The reset existed below 760 px before. The new focus restore and the wider scroll band make it more visible.
- Reproduced twice from clean state: yes (key and mouse, two widths).

### F4. The translated header row ignores the panel's 1 px border  [S4]
- Where: Compare grid inside `.cmpw.scroll`, 400 and 700 px.
- Steps: 1. Clean state, default queue, 400×800. 2. Scroll so the grid top is 600 px above `#hdr` bottom. 3. Compare `.cgrid.hd` top with `#hdr` bottom. 4. At 400×300, scroll to the page end.
- Expected: the row top equals `#hdr` bottom; at the grid end the row bottom equals the panel's inner bottom.
- Actual: the row top is 1.3 px (400) / 0.7 px (700) below `#hdr` bottom. Hit tests at y 90 and 91 still return the header row, so no row text shows through. At the grid end the row bottom is 1.3 px below the panel's outer edge. The wrapper then has `scrollHeight` 2011 against `clientHeight` 2009, so it can scroll 2 px vertically (`scrollTop = 50` gives 2). This only happens when the grid end passes the page header, which needs a viewport about 300 px tall or less.
- Evidence: `f4.js` (`hdTop 91.1`, `hdrBottom 89.8`), `f4b.js` (`hdBottomMinusWrapBottom: 1.3`), `f4c.js` (`sh 2011, ch 2009, tryScroll 2`).
- Code: site/src/index.html:1225 `syncGridHead` — `clamp(top - wr.top, 0, wr.height - hd.offsetHeight)` uses the border box. Subtract the top border from `y` and both borders from the maximum (or use `wr.top + w.clientTop`).
- Reproduced twice from clean state: yes.

## Clean areas (regress)
- 2D scale: 4 queues (4, 4, 3, 2 devices, with `zotac-zone-pro`, `legion-go-z1`, `gpd-win-5-395`, `ayaneo-slide`, `ayaneo-flip-kb-8840u`, `gpd-win-max-3-388`, `onexfly-apex-air`) × 4 views × 2 layouts = 32 states. Shape px/mm equals the SVG px/mm within 1 %, pairwise ratios match `OUT[id].top/bottom` or dims, grips and screens correct, no overlap in Side by side, all shapes inside the stage. Scale bar error ≤ 0.15 px. Resize 1280 → 1440 → 1280 and 1280 → 700 → 1280 in both layouts: the bar re-fits (error ≤ 0.03 px).
- Grid texts, deltas, Best: 49 queue/reference combinations (default queue, two queues with no-MSRP devices, odd form factors, 10 random queues of 2 to 4, and 3 with the reference outside the queue), each with hideSame on and off: 0 mismatches against the data model. `hideSame` note count equals the model count in all 49; no `.diff` rows when on; `.diff` rows equal the differing rows when off; the toggle survives a reload.
- Remove and add: remove → slot appears, badge follows, the reference stays when its column goes (FIXNOTES 32). `#sq` search + mouse pick: input clears, keeps focus, dropdown closes. `#sq` + Tab into the dropdown + Enter adds the device and keeps `#sq` focused. Add of the 4th device: slot goes, focus to the new `#cref2-<id>`. Remove all: "Nothing to compare yet" panel; its "list" button goes to `#browse` and focuses `#lbar`.
- 3D: slices 16/9/14/8 at 1280, 7/6/6/6 at 400 (all in 6..24). Presets set exact angles and `aria-pressed`. Real drag matches the computed angles; `.drag` removed on release. X clamps at +89 and −89. Right-button drag changes nothing. Angle survives a 2D/3D switch and a reload. Devices fit the stage at 1280, 700 and 400; no document overflow.
- Sticky header on desktop: 1280 (4 and 2 devices), 1440, 960 (3 devices) at scrollY 600 and 1200: `position: sticky`, no transform, `.cgrid.hd` top 53 = `#hdr` bottom. Resize while scrolled 1280 → 800 → 1280 → 400 → 1280: the header re-attaches each time (translated below 910, sticky above).
- Console: favicon 404 only.

## Observations (not bugs)
- With a reference outside the queue, the "Baseline" button has `aria-pressed="true"`, although the global reference is another device. Pressing it makes that column the reference. A screen reader hears "pressed" for a control that still changes state.
- "Show all rows" sits at the bottom of the grid. Its re-render moves focus to `#hide-same` at the top of the page with `preventScroll`, so the focus ring is off-screen (scrollY 1711 unchanged). The next Tab goes to `#size-open`. FIXNOTES names no neighbour for this button.
- A mouse click on the column body (not a button) moves focus to `#cmp-h1`, because the div is no longer focusable. Not a keyboard path.
- At 960×800 with 2 devices the add slot sits low in the header row. Its dropdown opens below the fold (top 817 in an 800 px window). The page scrolls normally.
