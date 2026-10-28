# Home and Browse filters (new features) findings

## Summary
- Scope: Home screen, the facet panel (47 facets, counts, ranges, "Show more", group badges), quick search `#fq`, the active-filter chips, storage v4 and the v3 migration, plus a regression pass on Browse. Viewport 1280×900, light theme. Session `qa-ft-browse`, headless Chromium.
- Method: I wrote my own facet engine from `#atlas-data` (FEATURES.md definitions). I compared every `#fn-*` count and the result set in 1 clean state, 4 combined states, 10 seeded random states and 17 range states.
- Findings: S1 0, S2 1, S3 4, S4 2.
- Biggest risk: F1. The "SSD interface → PCIe 4.0" count is wrong in every state. It counts a device once per slot, not once per device. The clean state shows 129, but only 114 devices match.
- No console errors or warnings in any flow. The only console line was the known favicon 404.

## Findings

### F1. "SSD interface: PCIe 4.0" count counts devices twice  [S2]
- Where: Browse, facet panel, group "Memory & storage", facet `pcie`, 1280×900, light.
- Steps: 1. Load `#browse` from a clean state. 2. Open "Memory & storage". 3. Read the count next to "PCIe 4.0". 4. Tick "PCIe 4.0".
- Expected: The count is 114. That is the number of devices with at least one PCIe 4.0 slot, and the list then shows 114 devices.
- Actual: The count shows 129, and after the tick the list shows "114 devices". The three options sum to 9 + 129 + 11 = 149, which is more than the 134 devices.
- Evidence: My scripted check found this as the only mismatch among all multi and all facets. It occurs in every state that contains the affected devices:

  | Filter state | Shown | Expected |
  |---|---|---|
  | clean | 129 | 114 |
  | status shipped + price 350–2,550 + hz 60–135 | 59 | 54 |
  | hz 60–135 | 75 | 70 |
  | RAM 24 or 32 + LPDDR5 | 9 | 8 |
  | ports usb4+ocu + G3D ≥ 8,000 | 9 | 8 |

  The 15 affected devices have two slots that are both PCIe 4.0 (2280 + 2230 or 2280 + Mini SSD): `ayaneo-next-ii-385/395`, `gpd-win-5-385/388/395`, `gpd-win-max-2-*` (8 ids), `gpd-win-max-3-388/395`. Screenshot: `scratchpad/qa/feat-browse/F-pcie-count.png`.
- Code: site/src/index.html:909 (`pcie` facet `v`): the value list is one entry per slot and has no de-duplication. site/src/index.html:1299 `syncFacetUI`: the multi count adds 1 per value occurrence, not 1 per device. `ssd` (line 908) has the same shape, but no device in the current data has two slots of the same form factor. Filtering (`passFacet`) is correct. Only the count is wrong.
- Reproduced twice from clean state: yes. Steps 1 to 4 ran clean three times, and the seeded states ran clean twice.

### F2. "How to set one" hides the guide heading under the sticky header  [S3]
- Where: Home, third card link "How to set one ↓" (`a[href="#guide-ref"]`), 1280×700 and 1280×600, light. At 1280×900 the page cannot scroll far enough, so the bug is masked.
- Steps: 1. Load `#home` from a clean state. 2. Resize to 1280×700. 3. Click the link, or focus it and press Enter.
- Expected: The page scrolls so that the heading "Set a reference device" is visible below the header. The address stays `#home`.
- Actual: The address stays `#home` (correct). But the heading lands at top 17 px to 43 px. The sticky header ends at 53 px, and `elementFromPoint` on the heading returns the header.
- Evidence: `{hash:"#home", h2Top:17, h2Bottom:43, hdrBottom:53, coveredBy:"header"}`. Screenshot: `scratchpad/qa/feat-browse/F-guide-under-header-1280x700.png`.
- Code: site/src/index.html:1888 (hashchange handler) calls `el.scrollIntoView({ block: "start" })`. No `scroll-margin-top` on `#guide-ref` and no `scroll-padding-top` exist for the sticky `.hdr` (line 83).
- Reproduced twice from clean state: yes (700 px and 600 px, mouse and keyboard).

### F3. Unchecking an option past the "Show more" cut drops focus to body  [S3]
- Where: Browse, any facet with a `#fmore-<key>` toggle (brands, soc, platform, cpuarch, gpu), 1280×900.
- Steps: 1. Load `#browse` from a clean state. 2. Press "Show 11 more" under Platform. 3. Tick "Strix Halo" (16th option). 4. Press "Show fewer". "Strix Halo" stays visible because it is checked (correct). 5. Focus the "Strix Halo" checkbox and press Space to untick it.
- Expected: The filter clears and keyboard focus stays on a visible control.
- Actual: The checkbox gets hidden at once (`display:none`), and `document.activeElement` becomes `BODY`. The mouse path gives the same result. The next Tab goes to `#fmore-platform`.
- Evidence: `{tgt:"f-platform-strix-halo", after:{active:"BODY#", visible:false, checked:false}}`. The same happens on Brand with `f-brands-valve`.
- Code: site/src/index.html:223 `.fct:not(.open) .fo-x:not(.on) { display:none }`. `syncFacetUI` (line 1300) removes `.on`, so the row hides. Then the change handler at line 1990 calls `focusId(t.id)`, which refuses a hidden element (`offsetParent === null`). No fallback exists.
- Reproduced twice from clean state: yes.

### F4. A long search chip does not truncate and pushes the page wider than 400 px  [S3]
- Where: Browse, `#fchips` and `#fq`, 400×800 (narrow layout), light.
- Steps: 1. Load `#browse` from a clean state at 400×800. 2. Type a query of about 50 characters or more into `#fq`, for example `ayaneo next ii ryzen ai max+ 395 strix halo 64gb oled 2025` (58 characters).
- Expected: The chip "Search: …" truncates with an ellipsis inside the column. No horizontal page scroll occurs (CONTRACT: no horizontal body scroll at 400 px).
- Actual: The chip keeps its full width and does not show an ellipsis. The chip and the `.fq-box` end at x = 420. `documentElement.scrollWidth` is 420 and `clientWidth` is 400. The chip's × and the end of the search box are off-screen. With an 80-character query, the overflow grows to x = 614.
- Evidence: `{qLen:58, scrollW:420, clientW:400, chipRight:420, fbarRight:384, fqBoxRight:420, ellipsis:false}`. Screenshots: `scratchpad/qa/feat-browse/F-long-chip-400.png`, `scratchpad/qa/feat-browse/chips-long-400.png`. Realistic facet chips stay narrower than the column. The widest is "CPU architecture: Redwood Cove + Crestmont" at 292 px.
- Note: This breaks the CONTRACT rule "no horizontal body scroll at 400 px". It needs a long query, so I rate it S3. Raise it to S2 if the contract rule takes priority.
- Code: site/src/index.html:200 `.fbar { display:grid }` has no `grid-template-columns`, so its implicit `auto` column grows to the min-content of the chip (a `white-space:nowrap` span). The `max-width:100%` and `text-overflow:ellipsis` at lines 205–206 never apply. The `.fbar` box stays at 384 px, but its items overflow it.
- Reproduced twice from clean state: yes.

### F5. Search text over 80 characters: the filter ignores the tail, then the input is cut  [S3]
- Where: Browse, `#fq`, 1280×900.
- Steps: 1. Load `#browse` from a clean state. 2. Type an 86-character query (`legion go extreme extreme … oled`). 3. Tick any facet, for example Status → Shipped.
- Expected: The input and the filter use the same text, for example through a `maxlength="80"` on the input.
- Actual: After step 2 the input shows 86 characters, but `state.f.q` keeps only the first 80. The last token "oled" plays no part in the result. After step 3, `syncFilters` rewrites the input to the first 80 characters, so the user's text changes without warning (it now ends "…treme extrem").
- Evidence: `{typedLen:86, d0:{input:86, stored:80}, d1:{inputLen:80, tail:"treme extrem"}}`.
- Code: site/src/index.html:1996 (`state.f.q = t.value.slice(0, 80)`). site/src/index.html:1216 `syncFilters` writes the value back. site/src/index.html:589: `#fq` has no `maxlength`.
- Reproduced twice from clean state: yes.

### F6. "Show N more" overstates the hidden count while a checked option past the cut is visible  [S4]
- Where: Browse, any facet with "Show more".
- Steps: 1. Expand Platform. 2. Tick "Strix Halo". 3. Press "Show fewer".
- Expected: "Show 10 more", because 10 options are hidden.
- Actual: "Show 11 more", but only 10 options are hidden. The checked option is already visible. Brand shows the same: "Show 5 more" with 4 options hidden.
- Evidence: `{btn:"Show 11 more", hiddenCount:10}`.
- Code: site/src/index.html:1956 and 1191 use `fc.opts.length - fc.more` and do not subtract the visible checked options.
- Reproduced twice from clean state: yes.

### F7. Removing the last chip focuses the previous chip, not `#fq`  [S4]
- Where: Browse, `#fchips`, 1280×900.
- Steps: 1. Seed search "ryzen", brands AYANEO and GPD, panel IPS, price 500–2,000. The chips are q, AYANEO, GPD, Price, IPS. 2. Click the × on the last chip, `#fx-panel-ips`.
- Expected (FEATURES.md): "Removing a chip moves focus to the next chip, else `#fq`." No next chip exists, so focus goes to `#fq`.
- Actual: Focus goes to the chip before it (`#fx-price`). Focus goes to `#fq` only when no chip is left. The first and middle chips behave as the spec says: × on `#fx-brands-gpd` focuses `#fx-price`, and × on `#fx-q` focuses `#fx-brands-ayaneo`.
- Evidence: `removeLast: "fx-panel-ips -> fx-price"` in two clean runs. In an earlier run, Enter on the last chip `#fx-ports-usb4` also moved focus to the previous chip `#fx-hz`.
- Code: site/src/index.html:1915 `restoreFocus` case `"fx"` uses `cs[Math.min(prevChip, cs.length - 1)]`, which picks the previous chip when the removed chip was the last one. The behaviour is reasonable, but it does not match the spec text. Fix the code or the spec.
- Reproduced twice from clean state: yes.

## Clean areas
- Home on a fresh load: the page lands on `#home`, Browse stays hidden, and both header segs read `aria-pressed="false"`.
- Home stats: `#home-n` 134, `#home-socs` 36, `#home-traced` 103 (my count of `outlines[id].top.kind === "traced"` is also 103), `#home-date` 2026-10-27. All match the data.
- Home routing: both hero buttons and both card buttons route correctly. Browse focuses `#lbar`, Compare focuses `#cmp-h1`, and `#logo` returns to `#home` and focuses `#home-h1`. The segs follow the route.
- Home guides: the `innerHTML` of the 3 guide sections stays identical in four states: after the queue is cleared, after 4 devices are queued through `#hq` (badge 4/4), after the reference is cleared, and after a new reference is set. The demo "Add to compare +" never turns into "List full".
- Home keyboard: Tab reaches all 5 Home controls in order, each with a visible 2 px accent focus ring.
- Facet panel structure: 47 facets and 8 groups. General and Performance start open. No option slug collides within a facet. The DOM holds no missing or extra options against my option lists. The `min`/`max`/`step` of all 17 range sliders match the data bounds rounded to the step.
- Facet counts: every multi and all facet matches my engine (except F1) in the clean state and in 4 combined states: maker Intel + RAM 32; AYANEO + OLED + price ≤ $1,000; ports usb4+ocu + G3D ≥ 8,000; "ryzen" + touch + gyro + classic/clamshell + 2024/2025 + hz ≥ 120 + weight ≤ 800. The `zero` and `on` classes and the checkbox states also match.
- Results: in 10 seeded random states (multi, all and range facets, search tokens, reference in or out of the set, cards and table layouts) plus the 4 states above, the visible cards or rows minus the pinned reference equal my result set, and `#lbar-n` matches. Two states use price and refresh rate with null values. `#lbar-x` matches my text exactly, for example "plus the pinned reference · 8 without a price, 21 without a refresh rate hidden". The empty state shows when the result is 0.
- Range sliders, keyboard: on all 17 range facets, ArrowRight on min, ArrowLeft on max, then Home and End give the correct state, label, `aria-valuetext`, chip, result count and `#lbar-x`. The last step clears the filter, so the label reads "Any" and the chip goes away. PageUp/PageDown on price move the value 300 up and back.
- Range sliders, limits: min cannot pass max, and max cannot pass min (keyboard End/Home/Arrow and mouse drags past the other thumb).
- Range sliders, mouse: with both thumbs at the top end, the min thumb is lifted (z-index 4), and a real mouse drag pulls it back down. With both thumbs at the bottom, the max thumb drags up. A drag to the full span clears the filter and its chip. The fill `left`/`right` percentages equal the selected span.
- Quick search: "890m" (19), "strix" (30), "Strix Halo" (11), "ayaneo flip" (8), "steam deck oled" (1), "z2 extreme" (4), "8840hs", "r7-8840hs", "lunar lake", "radeon 780m", "win max 2" and extra spaces all equal my AND-of-tokens result. The counts stay correct while a search is active. Deleting text, Backspace, the native × and Escape each clear the search and remove the chip without errors. Search combined with facets updates the counts.
- Chips: one chip exists per value, per range and for the search. × with a click, Enter or Space removes exactly that filter. Focus moves to the chip that now takes its place, and to `#fq` when no chip is left (for the last chip in the row, see F7). "Clear all", "Reset all" and the empty-state "Reset filters" each clear the search and every facet.
- Show more: present on brands, soc, platform, cpuarch and gpu (8 shown). `aria-expanded` and the "Show fewer" text toggle. A checked option past the cut stays visible.
- Group badges: the badge count equals the active facets per group (General 3, Display 1, Battery 1, Controls 2). Groups with saved filters open on load. The `details` open state survives facet ticks, search, chip removal, Reset all and a resize to 600 px and back.
- Persistence: a UI-driven v4 round trip (2 brands, usb4, RAM 32, price 550–2,000, size ≥ 6.5″, hz ≥ 80, search "ryzen 7") restores the state, checkboxes, slider values, labels, chips, `#fq`, counts and result exactly after a reload.
- v3 migration: brands, status and sticks move to `sel` (unknown brand dropped, "unknown" stick kept). `usb4:true` becomes `sel.ports:["usb4"]`. `maxPrice` 1200 becomes `rng.price [350,1200]`, and `maxWeight` 900 becomes `rng.weight [390,900]`. The layout becomes cards, and 19 cards show (18 + pinned reference). Queue, reference, sort and groups carry over, and the matching filter groups open. No-op v3 values (string brands, `maxPrice` 99999, `usb4:"yes"`) give no filter.
- Corrupt v4: these inputs all load safely with no console error and no prototype pollution:
  - prototype names (`__proto__`, `constructor`, `toString`, `hasOwnProperty`, `valueOf`) as keys and as values;
  - unknown values, duplicate values and non-string values;
  - a range key inside `sel` and a multi key inside `rng`;
  - a reversed range (swapped), an out-of-range span (dropped) and non-numbers (`"a"`, `null`, `true`, `1e400`);
  - short or long range arrays, and `q` as a number, array or object;
  - `f` as an array, string or null;
  - non-JSON storage, and `v` as a string.
- Regression: in the table layout, sorting by G3D (default, descending), price ascending and descending, and weight ascending matches the data (nulls last, reference pinned first), and `aria-sort` follows. The column-group chips work, and hiding the sort column falls back to G3D. The reference pill, the price delta pills (134 rows, direction and colour checked) and `#ref-clear` work. The queue checkboxes work, and the others are disabled at 4/4. The card add buttons ("In compare", "List full") and the `#hq` dropdown add work. `#more-btn` reads "Show all 134 devices", shows all and moves focus.

## Observations (not bugs)
- When both thumbs sit at the same value, only one direction drags. Below the midpoint the max thumb is on top, so a drag to the left does nothing. Above the midpoint the min thumb is on top, so a drag to the right does nothing. The keyboard and a drag the other way still work. Evidence: price [1000,1000] with dx −60 stays [1000,1000], and dx +60 gives [1000,2000].
- A range value in storage that is off the step (for example `price [523,1234]`, only from hand-edited storage) shows "$523 – $1,234", while the thumbs snap to 500 and 1,250. The next key press on either thumb silently changes the stored minimum to 500 (lines 1224 and 1034, where `cleanF` does not snap to the step). v3 values are always on the step, so the migration is safe.
- `#lbar-x` "N without x hidden" counts only devices that pass every other filter. A device that has neither a price nor a refresh rate (7 devices) appears in neither number when both ranges are active. This matches the code comment and the parts-picker rule.
- A range with min = max reads "$450 – $450". "= $450" would be shorter.
- The v3 key stays in storage after the migration. It is harmless, because v4 takes priority.
- Hunch 1 (the count of a checked option in an "all" facet): that count equals the current result count (devices with every selected flag). This is consistent with FEATURES. Not a bug.
- Hunch 2 (a range facet with a single distinct value): not reproducible. The smallest distinct count in the data is 5 (`hz`, `usbc`). The code handles the case with `max = min + step`.
- Hunch 3 (show-more with a checked option past the cut, then unchecked): reproduced. See F3 and F6.
