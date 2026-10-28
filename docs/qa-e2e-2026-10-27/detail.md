# Detail screen findings

## Summary
- Coverage: a scripted sweep over all 134 device sheets at 1280×800, with 1795 `button.sv` popovers opened and checked (27 closed with a real `Escape`). Other scripted passes checked the PassMark panel, tiles, the title card, groups, notes, conflicts and popover content against `#atlas-data` for every device. A further pass ran at 400 px. Hand checks used real `page.click` and keyboard input.
- Data and numbers are correct everywhere: no `undefined` / `NaN` / `[object Object]` in the DOM. Bars, ticks, ranks, delta pills, tiles, prices, status tags and outline labels match the data on all 134 sheets. The console was clean (only the known favicon 404).
- Findings: S1 0, S2 3, S3 5, S4 0 (observations are listed apart).
- Biggest risk: the Sources group clips source notes and URLs at the panel edge on 39 of 134 sheets. Keyboard users also lose focus after the main sheet actions (Add to compare, Set as reference, Back to list).
- Hunches: H1 is partly confirmed (focus is lost, but the scroll does not jump) and is reported as F2. H2 and H3 are not reproducible.

## Findings

### F1. Sources group clips notes and URLs at the panel edge  [S2]
- Where: Detail, "Sources" group, 1280×800 and 400×800, light and dark.
- Steps: 1. `localstorage-clear`, then open `index.html#ayaneo-2` (or `#ayaneo-flip-1s-ds-8840u`). 2. Scroll to the "Sources" group.
- Expected: Every source item wraps inside the panel. The notes and URLs are fully readable.
- Actual: Each `li` grows to the width of its longest unbreakable token (a raw URL inside the note). The panel has `overflow:hidden`, so the right part of every line in the list is cut off. Short notes are cut too, because they wrap at the widened `li` width and not at the panel width (for example "Two USB4 ports and the microSD reader on the to…").
- Evidence: `#ayaneo-2` at 1280: Sources panel `clientWidth 280`, `scrollWidth 466`, `overflow-x: hidden`, first `li` width 454. `#ayaneo-flip-1s-ds-8840u`: `li` right edge at 1398 px with the panel right edge at 958 px (1280 wide) and at 737 px with the panel right edge at 384 px (400 wide). Affected: 39 of 134 devices at 1280, 37 of 134 at 400 (only the Sources group; Conflicts, Unresolved and the `dl.kv` groups are clean). Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/detail/sources-clip-1280.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/detail/sources-clip-400.png`.
- Code: site/src/index.html:377 `.dl .why` has no `overflow-wrap:anywhere` (only `.dl .url` at line 378 has it). With `.dl` as `display:grid` (line 375), the grid items keep `min-width:auto` and grow to the min-content width. `.grp { overflow:hidden }` (line 364) then clips them. The markup comes from grpLists at lines 1313-1314.
- Reproduced twice from clean state: yes

### F2. Focus goes to `body` after "Add to compare" or "Set as reference" on the sheet  [S2]
- Where: Detail, title card buttons `#dt-add` and `#dt-ref`, 1280×800 and 400×800.
- Steps: 1. Open `index.html#zotac-zone-pro` from a clean state. 2. Scroll to `scrollY = 150`. 3. Focus `#dt-ref` and press Enter (or click it with the mouse). 4. Press Tab.
- Expected: Focus stays on the button that was pressed (the button now reads "Reference device" or "In compare list ✓"). The next Tab goes to the next button.
- Actual: After step 3, `document.activeElement` is `BODY`. The next Tab focuses "← Back to list" and the page jumps to `scrollY = 0`. Mouse clicks also leave focus on `BODY`. The same happens with `#dt-add` (Enter or click).
- Evidence: `focus: dt-ref sy=150` → `Enter #dt-ref: BODY sy=150 label=Reference device` → `Tab: BUTTON ← Back to list sy=0`. The same result came from `#dt-add` on `#legion-go-2` and `#steam-deck-oled` at 1280 and at 400.
- Code: site/src/index.html:1352 renderDetail replaces `#scr-detail.innerHTML`. It runs from afterQ (line 809) and afterRef (line 833), and nothing focuses the new `#dt-add` / `#dt-ref` again.
- Reproduced twice from clean state: yes
- Note: this is hunch H1. The focus part is confirmed. The scroll part is not reproducible: `scrollY` stays the same after the click (150 at 1280; 726 to 728 at 400).

### F3. Focus goes to `body` after "← Back to list", so the next Tab jumps to the footer  [S2]
- Where: Detail "← Back to list" button, going to Browse, 1280×800.
- Steps: 1. Open `#browse` from a clean state. 2. Scroll to 1500. 3. Focus `#open-msi-claw-8-ex-ai-plus-cg3m` and press Enter. 4. Press Shift+Tab to reach "← Back to list" and press Enter. 5. Press Tab.
- Expected: Focus goes back to the row's open button (`#open-<id>`), or to a known place in the list.
- Actual: The scroll is restored to 1500, but `document.activeElement` is `BODY`. The next Tab focuses the footer link `retrocatalog.com` and the page scrolls to 1987. The keyboard user loses their place in the list.
- Evidence: `Enter on back -> BODY sy=1500 hash=#browse`, then `Tab -> A retrocatalog.com sy=1987` (2 of 2 runs).
- Code: site/src/index.html:1382-1400 go(): it restores `browseY` (line 1398) but does not restore focus. The focused back button sits inside the now-hidden `#scr-detail`.
- Reproduced twice from clean state: yes

### F4. Popover note text runs outside the popover box  [S3]
- Where: Detail, source popover `#pop`, 1280×800 and 400×800.
- Steps: 1. Open `#ayaneo-air-1s-7840u` from a clean state. 2. Click the `$899` value (Launch price).
- Expected: The note wraps inside the popover (max width 360 px).
- Actual: The note holds a long URL (`https://cdn.ayaneo.com/ayaneo/article/2023/07/09/6095d2023…`). The popover box ends at x=1156, but the text runs on to x=1304, which is past the 1280 px viewport. At 400 px the text runs past the right edge of the screen and is cut off.
- Evidence: `pop.clientWidth 358`, `pop.scrollWidth 507`. 11 of 134 devices have at least one such popover (for example `ayaneo-2` "36.1 mm", `ayaneo-air-1s-limited` "$1,129", `ayaneo-flip-1s-ds-8840u` "$999"). Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/detail/pop-overflow-1280.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/detail/pop-overflow-400.png`.
- Code: site/src/index.html:383 `#pop .why` has no `overflow-wrap:anywhere`. The markup comes from openPop at line 1363.
- Reproduced twice from clean state: yes

### F5. The open popover stays in place while the page scrolls and drifts away from its value  [S3]
- Where: Detail, `#pop`, 1280×800.
- Steps: 1. Open `#steam-deck-oled` from a clean state. 2. Click `#sv-2`. 3. Scroll the page 300 px with the mouse wheel.
- Expected: The popover closes on scroll, or it moves with its button.
- Actual: The popover stays open at the same viewport position (top 665) while its button moves up 300 px (bottom 659 → 359). It now points at an unrelated row.
- Evidence: `b0 {btnBottom:659, popTop:665}` → `b1 {sy:300, btnBottom:359, popTop:665, popHidden:false}`.
- Code: site/src/index.html:380 `#pop { position: fixed }`. Only `resize` closes it (line 1513). No `scroll` listener exists (openPop at lines 1358-1372).
- Reproduced twice from clean state: yes

### F6. Keyboard users cannot reach the links in the source popover  [S3]
- Where: Detail, `button.sv` → `#pop` (role=dialog), 1280×800.
- Steps: 1. Open `#steam-deck-oled`. 2. Focus `#sv-0` and press Enter. 3. Press Tab three times.
- Expected: Focus moves into the dialog (or the next Tab reaches its link). The dialog closes when focus leaves it.
- Actual: Focus goes `sv-1`, `sv-2`, `sv-3`. It never enters `#pop`, and the popover stays open over the page. `#pop` is the last element in `body`, so its links come after the whole sheet and footer in the tab order.
- Evidence: Tab sequence `["sv-1 pop-open","sv-2 pop-open","sv-3 pop-open"]` (2 of 2 runs). `pop.contains(document.activeElement) === false`.
- Code: site/src/index.html:1358-1372 openPop does not move focus. `#pop` is defined at line 478 after all screens. The `aria-label="Source"` is fixed and does not name the value.
- Reproduced twice from clean state: yes

### F7. Hashes like `#constructor` or `#toString` open a blank device sheet and save it as the last route  [S3]
- Where: Routing to Detail, any width.
- Steps: 1. `localstorage-clear`, then open `index.html#constructor` (also `#toString`, `#__proto__`, `#hasOwnProperty`). 2. Reload. 3. Click "Set as reference".
- Expected: An unknown token falls back to Browse, as `#no-such-device` does.
- Actual: A blank sheet renders: empty `h1`, "Price TBA", "Size as held 0 × 0 × 0 mm", every field "Not stated", an empty Sources list, and an outline labelled "Outline of , spec box". `detailId: "constructor"` goes into localStorage, so the blank sheet opens again on reload (seen with the hash still in the URL; a load without a hash reopens it through `go(state.route, state.detailId)` at line 1534, which follows from the code but was not run). "Set as reference" on this sheet has `data-id=""`, and a click clears the real reference (`refId` steam-deck-oled → null). No exception is thrown.
- Evidence: `{hash:"#hasOwnProperty", detail:true, h1:"", size:"0 × 0 × 0 mm", stored:"hasOwnProperty", refBefore:"steam-deck-oled", refAfter:null}`. Screenshot: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/detail/proto-constructor.png`.
- Code: site/src/index.html:503 `const BY_ID = {}` is a plain object, so the inherited keys are truthy. The checks at lines 1405 (routeFromHash), 1383 (go), 759 (loadState) and 1322 (renderDetail) all accept them. An `Object.create(null)` map or a `hasOwnProperty` check would fix it.
- Reproduced twice from clean state: yes

### F8. An unknown hash set while a sheet is open leaves the old sheet and a wrong URL  [S3]
- Where: Detail, hash routing, any width.
- Steps: 1. Open `#steam-deck-oled`. 2. Change the hash to `#no-such-device` (edit the address bar, or `location.hash = '#no-such-device'`).
- Expected: Fall back to Browse (as a direct load of `#no-such-device` does), or reset the hash to `#steam-deck-oled`.
- Actual: The Steam Deck OLED sheet stays on screen, and the address shows `#no-such-device`. After a reload, the hash snaps back to `#steam-deck-oled`.
- Evidence: `{hash:"#no-such-device", detail:true, h1:"Steam Deck OLED"}` (2 of 2 runs).
- Code: site/src/index.html:1402-1408 routeFromHash returns false for an unknown token, and the `hashchange` listener ignores that result.
- Reproduced twice from clean state: yes

## Clean areas
- 134-device sweep at 1280×800: `#scr-detail` visible; `#dt-h1` equals `model`; no `undefined` / `NaN` / `[object Object]`; no horizontal page overflow; `path.o` has a non-empty `d`; the aria-label says `traced` for all 103 traced outlines and `spec box` for all 31 boxes, in line with both `outlines/index.json` and the inlined data; 4 tiles and 3 `.pm-r` on every sheet; a Sources group with at least one http link on every sheet; every external link has `target=_blank rel=noopener`.
- Popovers: 1795 `button.sv` clicked. Each one opened `#pop` with at least one http link, stayed inside the viewport, and set `aria-expanded="true"` (and reset the previous button to false). The `Sources` heading appears exactly when there is more than one item. Each item's `field · accessed` and note match the data. 27 `Escape` samples closed the popover and returned focus to the button. 107 second clicks on the same button closed it.
- Popover hand checks (real clicks): it moves to the next button on a click; it closes on a click outside (on a `dt`); it stays open on a click inside it; it closes on `Escape` with focus back on the button; it closes on the Browse nav and on a hash change to another device; it flips above the button near the bottom edge (button top 720, popover 597 to 714). The several-source case `aokzoe-a1x` port rows shows "Sources" with 2 items, each with field, date and note.
- PassMark, all 134 sheets: the bar width equals `score / max × 100` per metric (the CSSOM shows `47%` for the markup `width:47.0%`; the style attribute is correct). The rank `#r/n` counts distinct values. The tick `left` equals `refScore / max × 100`. The pill class and text match `delta()` (`up` for higher). When the sheet's device is the reference, there is no tick, no pill, and no "Tick mark" in the note.
- Tiles, title card, all 134 sheets: Width, Height, Thickness (`d / d_max mm`) and Weight (measured, else stated) match the data. Price or "Price TBA", the status tag, "Released …", the variant line, the `#dt-add` label for the default queue, the `#dt-ref` label, and "Open comparison (n)" are all correct.
- Groups, all 134 sheets: the `.gnote` count and text match the data notes (including "PassMark: " mapping notes). "No reviewer figure" appears exactly when `measured` is null. Conflicts and Unresolved appear exactly when the arrays are non-empty, with the right `li` counts, fields, value links and `Chosen:` reasons. The number of Sources `li` equals `sources.length`. No conflict value or source has a missing or non-http URL.
- Hand spot checks: `steam-deck-oled` (measured 637 g with its own notebookcheck source, a Conflicts group for `wireless.bt` with 2 links and a reason, HDR "Yes"); `zotac-zone-pro` ("Price TBA", tag `info` "Announced", "Released: Not stated"); `gpd-win-5-395` ("940 g with pack", Thickness "24.2 / 42.3 mm", "External pack: Yes…", "Without pack, weight 590 g"); `ayaneo-flip-kb-8840u` (Clamshell, Closed "180 × 102 × 29.8/37.5 mm", Keyboard "Yes"); `onexplayer-x1-pro-255h` (the title card and tiles have no clipping, screenshot `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/detail/x1pro-full.png`); `acer-nitro-blaze-7` (stick_type null → "Not stated" with a sub-note); `acer-nitro-blaze-8` ("…, spec box").
- Action buttons: `#dt-add` toggles "Add to compare +" ↔ "In compare list ✓", `aria-pressed` follows, and the badge follows (4/4 → 3/4 → 4/4). With 4 other devices queued, it is `disabled`, reads "Compare list full +", and a forced click does nothing. `#dt-ref` toggles "Set as reference" ↔ "Reference device", and the ticks and pills go away when the device becomes the reference. "Open comparison (n)" shows the queue length and goes to `#compare` with the right columns.
- Back and scroll restore: from a table row (`#open-…`), a card (`#copen-…`, cards layout) and Compare (`#copen2-…`), "← Back to list" goes to `#browse` and restores `scrollY` to 1500 (2 of 2 runs).
- Direct load: a fresh `#steam-deck-oled`, `#onexplayer-x1-pro-255h` or `#zotac-zone-pro` renders the sheet with `activeElement === #dt-h1`. A fresh `#no-such-device` falls back to `#browse`. A load with no hash and a stored detail route reopens the sheet.
- 400 px pass over all 134 sheets: no horizontal page overflow, and every popover box stays inside the viewport. The only clipping is F1 and F4.
- Dark scheme (emulated): the outline, dimension lines, h1, `.na` and popover all use theme tokens and are legible.
- Console: 0 errors and 0 warnings in every flow (only the known favicon 404 on the first open).
- H2 (toggle vs. flicker): not reproducible. Two real clicks on `#sv-0` open and then close it, and `aria-expanded` returns to false.
- H3 (drawn dimension vs. Width tile): not reproducible. The largest gap between `outlines[id].top.w/h` and `dims_mm.handheld.w/h` over all 134 devices is 0.05 % (for example onexfly-7840u, h 98.2 vs 98.25). The build scales the traced paths to the stated size.

## Observations (not bugs)
- Data notes use internal field names and the word "null" in visible text, on 46 sheets. Examples: "…not named, so stick_type stays null." (acer-nitro-blaze-7); "…per-port PD input; null subfields are unstated" (gpd-win-4/5/mini/max-2/max-3 family, 26 sheets); "…PD input, or location left null where no source states it" (onexplayer/onexfly family, 19 sheets); "…opened presales only; kept null" (gpd-win-max-3-388/395). This is data wording, not a render bug.
- When the reference device is removed from the queue with `#dt-add`, the reference moves to `queue[0]` without notice (line 822). The sheet then shows "Set as reference" and ticks for the new reference. A reference set to a device outside the queue does not move. This matches the code.
- "← Back to list" always goes to Browse, also when the sheet was opened from Compare.
- Opening a sheet uses `history.replaceState` (line 1397), so `history.length` does not grow. The browser Back button leaves the page and does not go back to the list. This is in line with the CONTRACT note that the viewer address bar does not follow hash changes.
- Rows that rely only on the `*` ("most fields") source show plain text, not a dotted `button.sv` (for example HDR "Yes" on steam-deck-oled). This matches the footer text.
- Formatting differs: the Thickness tile shows `24.2 / 42.3 mm` (with spaces), and the "Closed" size row shows `29.8/37.5 mm` (no spaces). On gpd-win-5-395 at 1280, the Thickness tile wraps "mm" onto a second line.
- At 400 px, `#dt-ref` moves up 16 px after a click because the PassMark note above it gets shorter. The scroll position does not change.
