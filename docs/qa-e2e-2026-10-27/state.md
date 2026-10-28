# State, routing, persistence, theme and keyboard findings

## Summary
- Scope: hash routing, prototype-key hashes, persistence round trip, corrupt and foreign storage, v1/v2 migration, theme (toggle, system, forced `?theme=`, dark scans), `file://` loading, keyboard focus, floating layers, resize, and the console. Headless Chromium, session `qa-state`, 1280×800, with resize passes from 1280 down to 380 px.
- Count: 0 × S1, 2 × S2, 6 × S3. Observations are listed apart.
- Biggest risk: a stored `sortK` that names an Object prototype member (for example `constructor`) throws at boot (F1). The page then has no route, a wrong badge, and no sort or row limit until the user clicks a sort header. No UI path writes such a value, so only hand-edited or foreign storage triggers it.
- Most common risk for real users: four route buttons drop keyboard focus to `body`, and the next Tab jumps to the footer (F2).
- Console: clean in every flow, except the uncaught `c.v is not a function` in F1. The favicon 404 is known and is ignored.
- Hunches: H1 confirmed (it extends detail F7, same cause, so no new finding). H2 not reproducible through the UI, but reproducible through stored data (F5). H3 not reproducible (the label follows live system changes), but the icon never swaps (F3, a different cause). H4 not reproducible.

## Findings

### F1. A stored sort key such as `constructor` throws at boot and leaves the page half-initialised  [S2]
- Where: boot, any screen, any width, both themes.
- Steps: 1. Clear storage. 2. Set `handheld-atlas:v3` to `{"v":3,"sortK":"constructor","queue":["steam-deck-oled","legion-go-2"],"refId":"steam-deck-oled"}`. 3. Load `index.html` (no hash). 4. Repeat with `"sortK":"toString"`, and with `#compare` in the URL.
- Expected: `loadState` drops the unknown key and uses the default sort (`g3d`). No console error.
- Actual: an uncaught `TypeError: c.v is not a function` stops the init. `location.hash` stays empty (with `#compare` in the URL, the Browse screen shows, not Compare). The badge reads `0/4` although 2 devices are queued, and their compare checkboxes are not ticked. All 134 rows show in data order, with no 30-row limit and no pinned reference row. The bad value stays in storage, so every reload throws again. A click on `#nav-compare` works. A click on a sort header (for example `#th-price`) writes a valid `sortK` and repairs the page.
- Reachability: no UI control writes such a value. Only hand-edited storage, an old or foreign build, or another page on the same origin can do it. On `file://`, Chromium shares one storage origin for all local files. The scale lists an uncaught exception as S1. I chose S2 because the trigger needs odd input. The orchestrator can promote it.
- Evidence: `pageerror: c.v is not a function @ index.html:933:20 / Array.sort / sorted (index.html:932:25)`. Read-out: `{"hash":"","badge":"0/4","rows":134,"refRow":true,"more":true}`. Screenshot: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/state/F-sortk-crash.png`.
- Code: site/src/index.html:740 `loadState` — `if (COL[s.sortK])` accepts inherited keys, because `COL` (line 654) is a plain object. Then site/src/index.html:933 `sorted` — `COL[state.sortK] || COL.g3d` returns `Object`, and `c.v(a)` throws. A `hasOwnProperty` check or an `Object.create(null)` map fixes it.
- Reproduced twice from clean state: yes (3 runs: `constructor` twice, `toString` once).

### F2. Four route buttons drop keyboard focus to `body`, and the next Tab jumps to the footer  [S2]
- Where: compare popover `#qpop` "Open comparison", Compare "← Back to list", Detail "Open comparison (n)", and the Compare empty-state "list" button. 1280×800.
- Steps: 1. Clear storage and reload. 2. Focus `#badge` and press Enter. 3. Focus "Open comparison" in `#qpop` and press Enter. 4. Read `document.activeElement`. 5. Press Tab. 6. Focus "← Back to list" on Compare, press Enter, and press Tab. 7. Open `#steam-deck-oled`, focus "Open comparison (4)", press Enter, and press Tab.
- Expected: focus goes to a known place on the new screen (for example the `h1`, as `go()` already does for Detail), or it stays on a control that is still visible.
- Actual: after each Enter, `document.activeElement` is `BODY`. After Compare "← Back to list", the next Tab focuses the footer link `retrocatalog.com` and the page scrolls to `scrollY = 1987`. After Detail "Open comparison", the next Tab also goes to the footer (`scrollY = 1709`). After the popover button, the next Tab goes to "← Back to list".
- Not in wave 1: detail F3 covers Detail "← Back to list" only. Compare F2 covers the controls that re-render Compare. The four controls here are new places with the same cause.
- Evidence (2 of 2 runs): `qpop Open comparison: Enter -> BODY #compare`; `compare Back: Enter -> BODY #browse, next Tab -> A "retrocatalog.com" sy=1987`; `detail Open comparison (4): Enter -> BODY #compare, next Tab -> A "retrocatalog.com" sy=1709`; `empty-state list: Enter -> BODY #browse`. The header nav buttons and `#logo` keep focus, because they stay visible.
- Code: site/src/index.html:1382 `go` — it hides the screen that holds the pressed button (lines 1389–1391) and closes `#qpop` through `closeFloating`. It moves focus only for the Detail route (line 1399).
- Reproduced twice from clean state: yes

### F3. The theme button icon never changes: the moon shows in dark mode  [S3]
- Where: header `#theme-btn`, every screen, every width.
- Steps: 1. Clear storage and reload (light). 2. Click `#theme-btn`. 3. Look at the icon. 4. Reload. 5. Also load with the system scheme set to dark and no stored theme.
- Expected: in dark mode `#ic-sun` shows and `#ic-moon` hides.
- Actual: `#ic-moon` shows in all states. The title and `aria-label` change correctly ("Switch to light"). The JS `.hidden` property changes, but the `hidden` attribute does not. `#ic-sun` keeps its markup `hidden` attribute (computed `display: none`). `#ic-moon` never gets one (`display: block`).
- Evidence: `after toggle | dt=dark btn="Switch to light" | sun: prop=false attr=true display=none | moon: prop=true attr=false display=block | SVGElement has hidden IDL: false`. Screenshot: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/state/F-theme-icon-dark.png`. Also visible in `dark-browse.png` and `dark-compare-2d.png` in the same folder.
- Code: site/src/index.html:782 `syncThemeBtn` — `$("#ic-sun").hidden = !dk`. The two icons are `<svg>` elements. `SVGElement` has no `hidden` property, so the assignment only adds a JS property. Use `toggleAttribute("hidden", …)`.
- Reproduced twice from clean state: yes

### F4. A `?theme=` URL erases the theme that the user saved  [S3]
- Where: forced theme on `127.0.0.1`, `localhost` and `file://`.
- Steps: 1. Clear storage and load `index.html`. 2. Click `#theme-btn` (stored `theme: "dark"`). 3. Load `index.html?theme=light`. 4. Load `index.html` again.
- Expected: the forced theme applies to that load only. The saved `dark` stays in storage and comes back on the next plain load.
- Actual: step 3 writes `theme: null`. Step 4 shows the light (system) theme. The saved choice is lost. A toggle on a forced page also changes the theme for that load only, and the reload goes back to the forced theme.
- Evidence: `B user picks dark | stored.theme="dark"` → `B load ?theme=light | dt=light | stored.theme=null` → `B plain load after forced | dt=null | stored.theme=null`. The same happened from `file://` (`?theme=light` → `theme: null`).
- Code: site/src/index.html:760 `loadState` — `if (forcedTheme) state.theme = forcedTheme` overwrites the loaded value. Then site/src/index.html:767 `save` writes `forcedTheme ? null : state.theme`. `go()` calls `save()` at boot, so a plain visit is enough. Keep the loaded theme in its own variable and write that back.
- Reproduced twice from clean state: yes (once on `http://127.0.0.1:8765`, once on `file://`)

### F5. Stored ids such as `constructor` pass the queue and reference checks: blank compare columns, a full badge, and an empty reference pill  [S3]
- Where: `loadState` and the v1/v2 migration. Browse, Compare and the badge popover.
- Steps: 1. Clear storage. 2. Set `handheld-atlas:v3` to `{"v":3,"queue":["constructor","steam-deck-oled","__proto__","toString"],"refId":"steam-deck-oled"}`. 3. Load `#compare`. 4. Open `#badge`. 5. Then set `{"v":3,"queue":["steam-deck-oled"],"refId":"constructor"}` and load `#browse`. 6. Then remove v3 and set `handheld-atlas:v2` to `{"sel":[{"id":"constructor"},{"id":"rog-ally-x"}]}`, and reload.
- Expected: unknown ids are dropped, as they are for `"a"`, `"zzz"` and `"bogus"`.
- Actual:
  - Step 3: "Compare 4 handhelds" with 3 blank columns ("—", "Set as ref"). The badge reads `4/4`, and the add slot `#sq` is gone, so the user cannot add a real device. The blank columns have `data-id=""`.
  - Step 4: "Compare list 4 of 4" with 3 blank items. Their `.xbtn` remove buttons work (`4/4` → `3/4`).
  - Step 5: the pill reads "Reference: " with no name. Only 29 rows show in the 30-row cut. The button reads "Show all 135 devices", but the data has 134. No delta pills show.
  - Step 6: the migration keeps `constructor` as the queue's first id and as the reference (pill "Reference: ").
  - The same plain-object check affects other keys. `"sizeView":"constructor"` gives the 2D stage the aria-label "Size overlay, function Object() { [native code] } view", and no view chip is pressed. `"f":{"brands":["constructor"]}` shows "0 devices" and the empty state, with no checkbox ticked. "Reset filters" repairs it.
- Reachability: no UI path writes these ids. On a `#constructor` sheet, "Add to compare" has `data-id=""` and does nothing (H2 is not reproducible through the UI). Only odd stored data triggers this.
- Relation to wave 1: detail F7 reports the `#constructor` hash and the stored `detailId`. This finding has the same root cause (plain-object lookups), but it affects the queue, the reference, the migration, `sizeView` and the brand filter. The fix for F7 alone does not cover `COL`, `VIEW_NAME` or `CNT.brand`.
- Evidence: `protoQueue {"badge":"4/4","h1":"Compare 4 handhelds","cols":["—Set as ref","ValveSteam Deck OLED$549Refere","—Set as ref","—Set as ref"],"slot":false}`; `protoQpop {"head":"Compare list 4 of 4","items":["(blank)","Valve Steam Deck OLEDValve","(blank)","(blank)"]}`; `protoRef {"pill":"Reference: ","visRows":29,"more":"Show all 135 devices","lbar":"134 devices","pills":0}`; `v2proto {"queue":["constructor","rog-ally-x"],"refId":"constructor"}`.
- Code: site/src/index.html:737 (`queue` filter `BY_ID[id]`) and 739 (`refId`) in `loadState`. `BY_ID` is a plain object (line 503). Also line 1010 `applyList` unshifts the bogus reference into the list. Line 755 accepts `VIEW_NAME[s.sizeView]`, and line 743 accepts `CNT.brand[v]` (`count` at line 711 builds a plain object).
- Reproduced twice from clean state: yes

### F6. Keyboard moves leave two floating layers open at once  [S3]
- Where: header, Browse and Detail, 1280×800.
- Steps: 1. Store a queue of 1 device and reload. 2. Focus `#badge` and press Enter (`#qpop` opens). 3. Press Shift+Tab twice (focus on `#hq`). 4. Type `ayaneo`. 5. Separately, open `#steam-deck-oled`, focus `#sv-0`, press Enter, then move focus to `#hq` and type `legion`.
- Expected: one floating layer at a time, as with the mouse. A click on `#hq` closes `#qpop` and `#pop`.
- Actual: after step 4, `#qpop` and `#hq-dd` are both open and overlap the list. After step 5, `#pop` and `#hq-dd` are both open. In one extra run, `#qpop` also stayed open after Tab moved focus out of it into the filter sidebar.
- Evidence (2 of 2 runs): `#hq hqdd=open qpop=open pop=closed` and `#hq hqdd=open qpop=closed pop=open`. Screenshot: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/state/F-two-layers.png`.
- Code: site/src/index.html:1474 `focusin` and the `input` handler at 1469–1473 call `renderDD` but not `closePop` or `toggleQpop(false)`. Only the click handler (lines 1411–1422) closes the other layers.
- Reproduced twice from clean state: yes (the `#qpop` Tab-out case: once)

### F7. Header search dropdown: Tab past the last item leaves it open, and Escape on an item drops focus to `body`  [S3]
- Where: header search `#hq` / `#hq-dd`, 1280×800.
- Steps: 1. Store a queue of 1 device and reload. 2. Focus `#hq` and type `ayaneo`. 3. Press Tab 9 times (8 items, then out). 4. Read the state. 5. Focus `#hq`, type `legion`, press Tab (focus on the first item), then press Escape.
- Expected: the dropdown closes when focus leaves it. Escape closes it and returns focus to `#hq`.
- Actual: after step 3, focus is on `#theme-btn` and `#hq-dd` stays open over the page. After step 5, the dropdown closes and `document.activeElement` is `BODY`.
- Not in wave 1: browse lists Escape and outside clicks with focus in the input only.
- Evidence (2 of 2 runs): `Tab past 8 items: #theme-btn | hqdd=open`; `Escape on item: BODY. | hqdd=closed`.
- Code: site/src/index.html:1475–1480 `focusout` acts only when the target is `#hq` or `#sq`, not a `.dd-item`. Site/src/index.html:1459 (the Escape branch of `keydown`) calls `hideDD()` and does not refocus the input.
- Reproduced twice from clean state: yes

### F8. Two open tabs overwrite each other's saved state: a removed compare device comes back  [S3]
- Where: any two tabs of the page (same origin), any screen.
- Steps: 1. Clear storage and load the page in tab A. 2. Load it in tab B. 3. In tab A, remove `legion-go-2` from the queue (stored queue: 3 devices). 4. In tab B, click `#theme-btn` (or `#nav-compare`). 5. Reload tab A.
- Expected: tab A's change stays. The page can listen to the `storage` event, or merge before it writes.
- Actual: tab B writes its whole old state. After the reload, tab A shows `4/4` with `legion-go-2` back in the queue. The same happens with filters, the reference and the theme. The last tab that writes wins.
- Evidence (2 of 2 runs): `afterA: ["steam-deck-oled","rog-xbox-ally-x","msi-claw-8-ai-plus"]` → `afterReloadA: ["steam-deck-oled","rog-xbox-ally-x","legion-go-2","msi-claw-8-ai-plus"]`.
- Code: site/src/index.html:762 `save` writes the full in-memory state on every change. No `storage` listener exists. The CONTRACT calls storage a convenience, so this is S3.
- Reproduced twice from clean state: yes

## Clean areas
- Fresh hash loads: `#compare`, `#browse` and `#steam-deck-oled` open the right screen. `#SteamDeck`, `#Steam-Deck-OLED`, `#no-such-device`, no hash, `#`, `#browse?x=1`, `#compare%20` and `#steam-deck-oled/` all fall back to `#browse`. `replaceState` rewrites the hash. The nav `aria-pressed` values are correct (Browse is pressed on Detail, by design). Focus is on `#dt-h1` on Detail.
- In-page `location.hash` changes: `#compare`, a device id and `#browse` route correctly through `hashchange`.
- Persistence round trip: through real clicks I changed the queue, the reference, the sort (price ↓), two brands and one status, the weight slider (1130 g), USB4, three column groups, the cards layout, "Differences only" off, the size panel collapsed, the 3D tab, the Top view, Side by side, dark theme and the Compare route. After a reload, every item was restored in the UI (chips, `aria-pressed`, `aria-expanded`, checkbox and slider values, ref pill, 27 visible cards, column headers). A Detail route (`gpd-win-5-388`) is restored with or without the hash.
- Corrupt storage: `not json`, `[]`, `null`, `3` and `{"v":4,…}` give fresh defaults. `{"v":3}` and all-null fields give safe defaults. The big mixed seed gives the queue `["steam-deck-oled"]`, `refId: null`, `sortK: g3d`, `maxPrice` clamped to 350, `maxWeight` clamped to 1430, brands `["GPD"]`, the default groups, the table layout, the system theme and the Browse route. A 5-id queue is cut to 4. Wrong value types (string queue, string `maxPrice`) are ignored. No console errors (apart from F1).
- Migration: v2 `{"sel":[rog-ally-x, bogus, legion-go]}` gives the queue `["rog-ally-x","legion-go"]` and the reference `rog-ally-x`. v1 works the same way (duplicates and nulls are dropped). v2 wins over v1. v3 wins over v2. A broken v2 gives the defaults.
- Blocked storage (a `localStorage` getter that throws): the page boots with 134 devices. The theme, routes, queue edits and Detail all work. No console error.
- Theme: clean light has no `data-theme`. The toggle sets `dark`, the body background changes from `rgb(247,247,248)` to `rgb(25,29,36)`, `color-scheme` becomes dark, the stored value is `dark`, and a reload keeps it. With the system set to dark and no stored theme, the page uses the dark tokens and offers "Switch to light". A click stores `light` and sets `data-theme="light"`. `?theme=dark` and `?theme=light` apply and do not write a value. `?theme=DARK`, `?theme=blue` and `?theme=` are ignored.
- H3 (live system change): the title and `aria-label` follow `prefers-color-scheme` changes without a reload. The stored value stays `null`. Not reproducible as a defect (the icon problem is F3).
- Dark scans, all screens (Browse table and cards, popover, search dropdown, Compare 2D overlay and side by side, 3D, grid, Detail and the source popover): no white boxes, no dark text on a dark ground, and visible borders. The only literal colours found are intentional: the white logo glyph, the `.badge-n` overlay, the light `--dev-4` in dark, and the dark `--slice-back` screens. The 2D and Detail dot grids are visible in dark. The 3D slices use the tokens.
- `file://`: the count is 134. Browse, Compare and Detail work. Hash routing, the in-page hash, the theme toggle and reload persistence work. `?theme=` forcing works. No console errors. H4 is not reproducible: `replaceState` and the hash work on `file://`.
- Keyboard: the header Tab order is logo, Browse, Compare, search, theme, badge. Each one has a visible ring (`2px solid` accent). `#hq` uses the `.srch-box:focus-within` border as its indicator. Enter on `#badge` opens `#qpop`. Escape closes it and focuses `#badge`. Tab into the search dropdown and Enter adds the device, clears the input and keeps focus in `#hq`. Wave 1 confirmed the sort headers and `button.sv`.
- Floating layers with the mouse: `#qpop` closes when `#hq` is clicked. `#hq-dd` closes when `#badge` is clicked. `#pop` closes when `#badge` is clicked. `#logo` with `#pop` open closes it and shows Browse. A hash change closes `#qpop`.
- Resize 1280 → 700 → 1280 on each screen: `--hdr-h` follows the header (53 / 90 / 53 px). A sweep from 1280 to 380 px gave 53 px down to 840, 90 px from 820 to 560, and 130 px from 540 down. The sidebar `top` is `--hdr-h + 16` (69 px at 1280, 106 px at 800 with a two-row header). The `.cgrid.hd` top follows. No horizontal scroll and no console errors.
- Console: no errors or warnings in any flow, except F1.

## Observations (not bugs)
- History: in-page clicks use `replaceState`, so `history.length` does not grow, and Back leaves the page. A user who edits the hash (`location.hash = …`) creates entries, and Back and Forward then route through `hashchange`. This matches the CONTRACT.
- H1: confirmed. With a stored `detailId: "constructor"` (or `__proto__`, `toString`, `hasOwnProperty`, `valueOf`), a load with no hash reopens the blank sheet and rewrites the URL to `#constructor`. Detail F7 has the same cause, so this is not a new finding.
- An unknown hash with stored state opens the stored route, not Browse. For example, `#no-such-device` after a visit to a sheet reopens that sheet and rewrites the hash (line 1534). Fresh storage falls back to Browse.
- `{"v":3}` with no queue gives an empty queue and no reference, because the code treats only missing or foreign storage as "fresh".
- `"f":{"maxPrice":-5}` clamps to the data minimum (350), so the list shows "0 devices" and the empty state. Clamping works as the code intends.
- `"f":{"usb4":"no"}` turns on the USB4 filter, because of `!!s.f.usb4` (line 748).
- Storage with `"v":4` (a newer build) is treated as fresh and is overwritten at boot.
- These are not saved: the 3D angles (`rx`, `ry`), the row limit, and the open state of the narrow filter panel. A reload resets the 3D view to 3/4. The CONTRACT says the drag "stores the angles on release". The code stores them in memory only.
- After the first theme toggle, no control returns the page to "follow the system".
- If `#qpop` is open and focus has moved on, Escape pulls focus back to `#badge` (seen once).
