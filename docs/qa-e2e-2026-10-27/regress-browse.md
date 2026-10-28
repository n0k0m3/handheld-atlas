# Browse and state re-test findings (regress-browse)

| Finding | Verdict | Evidence |
|---|---|---|
| 5 | Fixed | Valve + TMR: `#lbar-n` "0 devices", 0 rows, `#empty` shown, pinned row hidden, empty-state Reset reachable. GPD: "26 devices" + `#lbar-x` "plus the pinned reference", 27 rows. AYANEO: "32 devices", 31 rows, "Show all 32 devices" (the pinned row does not take a slot). Cards give the same counts. |
| 6 | Fixed | No reference, re-tick `#q-rog-xbox-ally-x`: pill "Reference: ASUS ROG Xbox Ally X", `tr.ref`, 997 pills at once. Header search ("ally x") and card `#add-` paths give the same result. |
| 8 | Partly | Route buttons and header nav pass (keyboard): `#qpop-open` → `#cmp-h1`; Compare "← Back to list" → `#lbar`; Detail "← Back to list" → `#open-gpd-win-5-388` (table) and `#copen-gpd-win-5-388` (cards); `#nav-compare` → `#cmp-h1`; same-screen nav and `#logo` keep focus. Mouse clicks give `:focus-visible` false on `#cmp-h1`, `#lbar`, `#dt-h1`. Browse controls pass (`#ref-`, `#cref-`, `#ref-clear` → `#lbar`, `#lay-*`, `#more-btn` → `#open-<row 31>`, `#qrm-<item 2>` → `#qrm-<next>`, last `#qrm-` → previous, final `#qrm-` → `#qpop-clear`, popover Clear). **Not fixed:** the empty-state "Reset filters" still drops focus to `BODY` (Enter, Space and mouse). See F1. |
| 9 | Fixed | Stored `sortK` `constructor` / `toString` / `__proto__` / `hasOwnProperty`: no pageerror, hash `#browse` (or `#compare`), badge "2/4", 30 rows, stored `sortK` repaired to `g3d`. |
| 10 | Fixed | 0 mismatches against `Math.round(Math.abs(p))`: 6 references × 2,010 table cells (5,760 pills, 74 exact half-percent cases, direction and class), 4 references × 536 card stats. Named cases now read "▼ 20%", "▼ 8%", "▼ 63%". |
| 11 | Fixed | Dark: `#ic-sun` display block (no `hidden` attribute), `#ic-moon` `hidden`; light: the reverse. Screenshot `f11-dark-icon.png`. |
| 12 | Fixed | Stored "dark", load `?theme=light`, navigate, toggle: stored theme stays "dark"; the next plain load is dark. Same on `file://`. `?theme=DARK`, `blue`, empty are ignored. |
| 13 | Fixed | Fresh load of `#constructor`, `#__proto__`, `#toString`, `#hasOwnProperty`, `#valueOf` → `#browse`. Stored queue `[constructor, steam-deck-oled, __proto__, toString]` → 1 column, badge "1/4", add slot shown. Stored `refId`, `sizeView`, brand, `detailId` "constructor" are dropped. v2 `{sel:[constructor, rog-ally-x]}` → queue `[rog-ally-x]`. |
| 14 | Fixed | On a sheet, `location.hash = '#no-such-device'` and `'#constructor'` keep the sheet and rewrite the hash to `#steam-deck-oled`. Same on Compare (`#zzz` → `#compare`) and Browse (`#Steam-Deck-OLED`, empty hash → `#browse`). |
| 18 | Fixed | Every group toggle (16 steps) shows exactly one sorted header. Hide Performance while on G3D → MSRP ↑, order matches the data. Stored `sortK: "stick"` with groups `[Price, Size]` → MSRP ↑. Remove all groups and reload → G3D ↓. |
| 19 | Fixed | `scrollLeft = 300` on `#tblw`: checkbox cells stay at left 273–309 px and device cells at 309–544.5 px (before and after); the MSRP cell moves from 544.5 to 244.5 px under them. `#ref-<id>` sits inside `.dcell`. Hover and `tr.ref` backgrounds equal the row background on both sticky cells. Light and dark screenshots look right (`f19-scrolled-hover.png`, `f19-dark-scrolled.png`). |
| 20 | Fixed | Ranking matches an independent score of the data for 8 queries. `win 5` → 3 × GPD Win 5 first; `claw 8` → Claw 8 AI+ first; `legion go s` → 2 × Legion Go S first; `onexplayer 2` → 4 × OneXPlayer 2 first; `zzqx<b>` → escaped no-match line. No "X · X" sub-line (AOKZOE A1 shows "Ryzen 7 6800U" once). |
| 21 | Fixed | "1 device" (brand AYN), "Compare 1 handheld", "Nothing to compare yet". |
| 24 | Fixed | `#qpop` open with Enter, Shift+Tab ×2 to `#hq`: `#qpop` closes; typing opens only `#hq-dd`. Source popover open on a sheet, focus `#hq`: `#pop` closes. Tab out of `#qpop` closes it; Tab inside keeps it open. |
| 25 | Fixed | Tab past the last dropdown item: `#hq-dd` closes (focus on `#badge`). Escape on an item: focus `#hq`, dropdown closed. Shift+Tab from the first item back to `#hq` keeps the list open. |
| 26 | Fixed | Tab B (`page.context().newPage()`) on `#compare`. Tab A removes Legion Go 2: B shows "3/4" and 3 columns at once, stays on `#compare`, and calls `setItem` 0 times. A's reference, filter, sort and groups reach B. B's theme toggle reaches A; A's queue stays 3 after reload. B on a sheet stays on the sheet when A clears the queue. |
| 31 | Fixed | `$3,450`: "111 devices", `#lbar-x` "22 without a price hidden". `1420 g`: "13 without a weight hidden". `$850` + `1130 g`: "20 without a price and 2 without a weight hidden" (matches the data). |
| 32 | Fixed | Popover Clear: queue empty, reference stays Steam Deck OLED (pill, `tr.ref`, 221 pills). Removing the reference device from the queue keeps it as reference. |
| 33 | Fixed | `aria-valuetext` equals the label on `#f-price`, `#f-weight`, `#tf-price`, `#tf-weight` ("Any", "$3,450", "$850", "1130 g", "1420 g"). |
| 35 (`.qbox`) | Fixed | `.qbox` 16×16, `#tbody .refb` 24×24, `#cards .refb` 24×24, `#ref-clear` 24×24, `#qpop .xbtn` 24×24. |
| Also: SSD wording | Fixed | All 5 devices with `form_factor: "other"` read "Not stated"; 0 cells with lowercase "not stated". |
| Also: `usb4` boolean | Fixed | Stored `usb4`: `"no"`, `1`, `"true"` → off, 134 devices; `true` → on, 120 devices. |

## Summary
- Scope: Browse controls, route buttons and header nav focus, table and card pills, state, routing and storage. Viewport 1280×800, headless Chromium, session `qa-rg-browse`.
- Result: 21 of 22 items are fixed. Finding 8 is partly fixed: one control still drops focus.
- New issues: 0 × S1, 0 × S2, 1 × S3 (F2), plus F1, which is the open part of finding 8 (S3).
- Regression: all items in the regress list still hold (see "Clean areas").
- The source and dist changed twice during the run (17:24:49 and 17:31:09). The final full pass of every script ran against the 17:31:09 build, and the build did not change during that pass. Results below are from that build. The 17:31:09 build also fixed the popover remove focus (it went to the first item before).
- Console: no error or warning in any flow (favicon 404 excepted).
- Scripts, raw outputs (`*.final.out`) and screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/regress-browse/`.

## Findings

### F1. Empty-state "Reset filters" still drops focus to `body` (open part of finding 8)  [S3]
- Where: Browse, `#empty` button, table and cards, 1280×800, light.
- Steps: 1. Clear storage and reload. 2. Tick brand Valve, then stick TMR (the empty state shows). 3. Focus the "Reset filters" button in `#empty` and press Enter (or Space, or click it).
- Expected: focus moves to `#f-reset` (FIXNOTES 8).
- Actual: `document.activeElement` is `BODY`. The filters reset correctly.
- Evidence: Enter → `BODY`, Space → `BODY`, mouse → `BODY`. A probe listener that runs after the app's click handler sees `document.activeElement` still equal to the Reset button (inside the now hidden `#empty`). One animation frame later it is `BODY`. For `#more-btn` the same probe shows the focus already moved to `#open-<row 31>`.
- Code: site/src/index.html:1626 (click handler) calls `restoreFocus` only when `document.activeElement === document.body`. At that moment the button is inside `#empty`, which `applyList` (line 1096) has just hidden. Chromium removes the focus only at the next style update, so the guard is false and `restoreFocus` (case `reset-f`, line 1575) never runs. The button has no id (line 489). A fix: test whether the active element is still rendered (`offsetParent === null`) or call `restoreFocus` for `reset-f` without the guard.
- Reproduced twice from clean state: yes (4 runs over 3 builds, the last on the 17:31:09 build).

### F2. Empty state shows "plus the pinned reference" while the pinned row is hidden  [S3]
- Where: Browse list bar, table and cards, 1280×800.
- Steps: 1. Clear storage and reload (reference Steam Deck OLED). 2. Tick brand Valve, then stick TMR. Or: tick MSI, set max price $1,000, tick TMR.
- Expected: when nothing passes, the pinned row is hidden (FIXNOTES 5), so the list bar does not mention it.
- Actual: the list bar reads "0 devices  plus the pinned reference" above "No devices match these filters." No pinned row shows.
- Evidence: `{"lbar":"0 devices","x":"plus the pinned reference","nVis":0,"empty":true}`; screenshot `new-empty-note.png`.
- Code: site/src/index.html:996 `listNote` adds the note whenever the reference is outside `filt`; it does not check `filt.length`, while `applyList` (line 1088 `cut = filt.length ? … : 0`) hides the pinned row when `filt` is empty.
- Reproduced twice from clean state: yes.

## Clean areas
- Sort: all 15 headers, 2 clicks each, with all groups and all rows: the order matches an independent sort of `#atlas-data` (nulls last, name tie-break, numeric collation for text) in 30 of 30 checks. The first-click direction is right, exactly one header has `aria-sort` and an arrow, and the reference row stays first.
- Column groups: 8 chips off and on in `GROUPS` order: header and row cell counts match, `aria-pressed` and "✓/+" are right, exactly one sorted header at every step.
- Delta pills: table (6 references, 12,060 cells) and cards (4 references, 2,144 stats): direction, class and magnitude all match; no pills on the reference row, `dims`, `res`, text columns or the sticky cells.
- Filters: all 21 checkbox counts match the data. 9 combinations (brands, statuses, sticks, USB4, $800, 600 g, $850 + 1130 g, MSI + $1,000 + TMR) match a data recount. Reset restores `maxPrice` 3500, `maxWeight` 1430, "Any", USB4 off, 134. The empty state shows and its Reset works.
- Cards: same order as the data sort, 5 sort chips × 2 clicks correct, add button states ("In compare ✓", "List full +" disabled), `#cref-` sets and clears the reference, table state kept on return.
- Queue: 4 max, 130 disabled checkboxes, a forced fifth click does nothing, untick re-enables, badge follows, popover lists items in order with s1–s4 dots, `#qrm-` removes, Clear keeps the reference, "Open comparison" opens the same 4 devices, outside click and Escape close it.
- Header search: cap 8 ("ayaneo": 32 matches), "Added" and "List full" disabled, click adds + clears + keeps focus in `#hq`, Tab into the list + Enter adds and refocuses `#hq`, outside click and Escape close, no-match text escaped.
- Persistence: queue, reference, sort (price ↓), 2 brands + 1 status, weight 1130 g, USB4, 3 group changes and cards layout: the DOM read-out after reload equals the one before.
- Corrupt storage: `not json`, `[]`, `null`, `3`, `{"v":4,…}` → default queue of 4 and reference Steam Deck OLED; `{"v":3}` → empty queue. v2 migration drops `bogus`; v1 drops duplicates and nulls.
- Blocked storage (getter throws): boot with 134 devices, queue edit, theme, filter, Compare and Detail all work, no console error.
- `file://`: 134 devices, Browse/Compare/Detail, in-page hash routing, theme toggle, reload persistence, `?theme=light` keeps the stored "dark".
- Theme: toggle and reload, system dark with no stored theme ("Switch to light", sun icon), live system change, click under system dark stores "light".
- Overflow at 1280: no body horizontal scroll; no element past `innerWidth` outside an overflow container.
- Console: 0 errors and 0 warnings across all flows (favicon 404 excepted).

## Observations (not bugs)
- `onexplayer 2`: the ranking follows FIXNOTES exactly, but the 4 OneXPlayer X2 variants still fall outside the 8-item cap. X1 and G1 entries score 4 because "228V", "255H" and "2026" start with "2" (+2), while "X2" gets only +1. Low impact: the exact OneXPlayer 2 models come first.
- `applyList` has its first comment line twice (site/src/index.html:1079 and 1080).
- When another tab writes, `syncFromStorage` calls `closeFloating()`, so an open queue popover in this tab closes. This is by design.
- The stored `route` belongs to the last tab that wrote. A reload keeps its own hash, so this has no visible effect.
- Test harness note for other testers: the app rewrites the hash with `replaceState` and saves on `hashchange`. A same-document `goto` after seeding storage overwrites the seed, and a reload after an unknown-hash boot reloads the rewritten hash. Seed first, then do a full navigation (for example add `?r=<n>`).
