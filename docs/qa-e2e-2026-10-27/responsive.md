# Responsive, dark theme and accessibility findings

## Summary
- Scope: all three screens at 400, 600, 759, 760, 800, 850, 880, 900, 960, 1100, 1280, 1440 and 1600 px wide, in light and emulated dark, plus reduced motion. Headless Chromium through `playwright-cli -s=qa-responsive`. All actions used real Playwright clicks, keys and mouse events.
- Findings: S1 0, S2 2, S3 5, S4 3. Observations are listed apart.
- Biggest risk: the Compare grid is wider than the window from 760 to 899 px, so the whole page scrolls sideways (CONTRACT: "The body never scrolls horizontally"). The header search dropdown does the same at 400 px when a result has a long sub-line.
- Wave 1 items that I confirmed but do not report again: compare.md F1 (sticky header row below 760 px, hunch H2), compare.md F3 (add-slot dropdown, hunch H1), compare.md F6 (nested buttons in `.ccol`), detail.md F1 and F4. Details are under "Clean areas".
- Console: no errors or warnings in any flow (only the known favicon 404).

## Findings

### F1. The Compare grid is wider than the window from 760 to 899 px, so the page scrolls sideways  [S2]
- Where: Compare, grid `.cmpw`, widths 760 to 899 px, 4 grid columns (4 devices, or 3 devices plus the add slot). Theme-independent (measured in light).
- Steps: 1. `localstorage-clear`, reload. 2. Resize to 800×900. 3. Open `#compare` (default queue of 4). 4. Read `document.documentElement.scrollWidth`.
- Expected: No horizontal page scroll. The grid fits, or it scrolls inside its own `overflow-x: auto` container.
- Actual: The grid needs 860 px (`180px + 4 × minmax(170px, 1fr)`). The panel is only 712 to 832 px wide, and it is not a scroll container above 759 px. The 4th column runs past the right edge of the window, and the page gets a horizontal scroll bar. With 3 devices the add slot is the 4th column and does the same (slot at x 715..885). At 900 to 909 px the page does not scroll, but the grid still sticks 1 to 8 px out of the panel border.
- Evidence: `scrollWidth` / `clientWidth`: 760 → 885/760, 800 → 885/800, 850 → 885/850, 880 → 885/880, 900 → 900/900. Widest element: `div.ccol.s4` right edge 885. Same values with 3 devices at 800 (`scrollX 0`, slot 715..885). Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/cmp-800-overflow.png` (4th column cut at the window edge), `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/cmp-800-3dev.png` (after a click near the right edge the window scrolled 85 px sideways and the page header is cut on the left).
- Code: site/src/index.html:1128 `gridHtml`. Columns are `180px repeat(n, minmax(170px, 1fr))` and `minW` is `"0"` on desktop (line 1129). The `scroll` class (line 1141, CSS line 298) is added only when `isNarrow()` (`innerWidth < 760`, line 774). Nothing protects the 760 to 899 px band.
- Reproduced twice from clean state: yes (4 runs: sweep, width scan, 800 px check, 3-device check)

### F2. Header search dropdown rows are wider than the box; at 400 px the page scrolls sideways and "+ Compare" is off-screen  [S2]
- Where: Header search `#hq` / `#hq-dd`, 400×800 and 1280×800, any query with a long sub-line (for example "ayaneo air").
- Steps: 1. Seed a queue of 1 device (so the items are enabled), reload. 2. Resize to 400×800. 3. Click `#hq` and type `ayaneo air`. 4. Read the rects of `#hq-dd`, each `.dd-item` and each `.dd-a`, and `documentElement.scrollWidth`.
- Expected: Each row fits in the dropdown. The sub-line ends with an ellipsis (CSS line 111 asks for `text-overflow: ellipsis`). The "+ Compare" label is visible. No page scroll.
- Actual: Every row grows to the width of the longest sub-line ("Ultra Thin & Light Limited Edition (Ryzen 7 7840U) · Ryzen 7 7840U"). At 400 px the box ends at x 384, the rows end at x 475, and all 7 "+ Compare" labels sit at x 405..467, off-screen. The ellipsis never shows. While the dropdown is open, `scrollWidth` is 475 for a 400 px window. At 1280 px the labels sit at x 774..836 and the box ends at 805, so they paint outside the box over the page.
- Evidence: 400 px: `{dd:[16,384], sw:458, cw:366, item right 475, ".dd-a" 405-467, docSW 475}`. 1280 px: `{dd:[385,805], item right 844, ".dd-a" 774-836}`. With the default full queue: `sw 438 / cw 366`. Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/hq-dd-400-overflow.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/hq-dd-1280-overflow.png`.
- Code: site/src/index.html:105 `.dd { display: grid }` has no column template. The `.dd-item` rows (line 106) are grid items with `min-width: auto`, so the implicit track grows to the min-content width of the `nowrap` sub-line (line 111). `.dd-item > div { min-width: 0 }` (line 109) only acts inside the flex row. A fix is `grid-template-columns: minmax(0, 1fr)` on `.dd` or `min-width: 0` on `.dd-item`. compare.md F3(b) found the same cause in `#sq-dd`; this finding is the header control.
- Reproduced twice from clean state: yes

### F3. The theme button icon never changes: it always shows the moon  [S3]
- Where: Header `#theme-btn`, all widths, light and dark.
- Steps: 1. `localstorage-clear`, `set-color-scheme dark`, reload. 2. Look at the theme button. 3. Alternatively, in light, click `#theme-btn` twice.
- Expected: The sun icon shows in dark (the label says "Switch to light"). The moon icon shows in light.
- Actual: The moon shows in every state. The `aria-label` changes correctly, but the icon does not.
- Evidence: After each click: `{theme:"dark", label:"Switch to light", sunAttr:true, moonAttr:false, sunShown:false, moonShown:true}` and the same for "auto" and "light". `'hidden' in SVGElement.prototype` is `false`. Under emulated dark on load: `ic-sun.hidden === false` (a plain JS property) but its computed `display` is `none`. Screenshot: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/theme-btn-after-dark.png`.
- Code: site/src/index.html:782 `syncThemeBtn` sets `$("#ic-sun").hidden` and `$("#ic-moon").hidden`. `hidden` is an `HTMLElement` property; `SVGElement` does not have it, so the assignment creates an expando and the `hidden` attribute from the markup (line 437) never changes. Use `toggleAttribute("hidden", …)` or wrap the icons in `<span>`. The code follows the CONTRACT rule "Toggle visibility with `el.hidden`"; that rule does not hold for SVG elements, so the CONTRACT note may need a fix too.
- Reproduced twice from clean state: yes (emulated dark on load, and a light → dark → light toggle)

### F4. Literal `#fff` on `--accent` fails contrast in dark: "Reference" tag, checkbox tick, switch knob  [S3]
- Where: Compare `.ccol .tag.ref` ("Reference"), Browse `.qbox:checked` tick, the `.sw` switches (`#f-usb4`, `#hide-same`) when on. Dark theme, all widths.
- Steps: 1. `set-color-scheme dark`, `localstorage-clear`, reload. 2. Open `#compare`. 3. Compute the contrast of the "Reference" tag text against its background.
- Expected: Text reaches 4.5:1 (11 px bold is small text). UI marks (tick, knob) reach 3:1 (WCAG 1.4.11). CONTRACT: "No component rule uses a literal color that reads in one theme only."
- Actual: `--accent` changes from `#0768cf` (light) to `#499fff` (dark), but the foreground stays a literal `#fff`. White on `#499fff` is 2.73:1. In light the same pair is 5.4:1.
- Evidence: Contrast audit at 1280 and 400: `span.tag.ref "Reference" fg rgb(255,255,255) bg rgb(73,159,255) ratio 2.73`. Computed pairs: `tagRef_white_on_accent 2.73` (dark) vs `5.4` (light); knob and tick use the same pair. Screenshot: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/dark-compare-3d-1280.png` (the "Reference" tag on the Steam Deck OLED column).
- Code: site/src/index.html:310 `.tag.ref { background: var(--accent); color: #fff; }`; line 216 `.qbox:checked::after` (`#fff` borders on `--accent`, line 215); line 165 `.sw::after { background: #fff }` on `--accent` (line 166). A fix is `--fg-onbrand` on `--bg-brand`, or a dark-specific token.
- Reproduced twice from clean state: one clean dark run (audit at 1280 and at 400) plus the computed token pairs; the cause is static CSS.

### F5. `--fg-3` text is below WCAG AA in both themes; brand-blue badge text is just below AA in dark  [S3]
- Where: Browse sidebar counts `.chk .n`, Detail Sources URLs `.dl .url`, all input placeholders, the badge text and count. Light and dark, all widths.
- Steps: 1. Load from clean in light, then in emulated dark. 2. For each visible text node, compute the WCAG ratio of `color` against the nearest opaque background.
- Expected: 4.5:1 for text under 18.66 px bold or 24 px.
- Actual:
  - `--fg-3` on `--bg`: 2.91:1 in light (`#8e98a8` on `#fff`), 3.45:1 in dark (`#6f7a8c` on `#222731`). It is used for 11 px counts, 11 px source URLs and the search placeholders.
  - Badge "Compare" and `#badge-n` (`--fg-onbrand` on `--bg-brand`): 4.34:1 in dark. The count sits on an extra 22 % white layer: about 3.04:1 in dark and 3.62:1 in light.
  - Near misses in light (4.37 to 4.47:1): `--fg-2` on `--bg-subtle` / `--bg-selected` (inactive segs, `#cnt`, "Set as ref" tag, `.dev-b` in the ref row), `--good` on `--good-bg` (`.dpill.up`, "Shipped").
- Evidence: Audit output, light 1280: `span.n "7" rgb(142,152,168) on rgb(255,255,255) 2.91`, `span.url 2.91`; dark: `span.n 3.45`, `span.url 3.45`, `#badge-n 4.34` (flat brand), computed `badgeN_white_on_brand22 3.04` (dark) / `3.62` (light).
- Code: site/src/index.html:162 `.chk .n { color: var(--fg-3) }`, line 378 `.dl .url`, line 69 `input::placeholder`, line 122 `.badge.on .badge-n { background: rgba(255,255,255,.22) }`; token values at lines 11 and 25.
- Reproduced twice from clean state: yes (light and dark runs)

### F6. At 400 px the sticky header takes three rows (130 px): the theme button and the badge do not fit on the first row  [S3]
- Where: Header `#hdr`, 400 to at least 520 px wide (90 px at 600 to 899, 53 px from 900). All screens.
- Steps: 1. Clear and reload at 400×800. 2. Read the rects of `#logo`, `.segs`, `.hdr-r`, `#hsrch`.
- Expected: The narrow CSS moves only the search to its own row (`.srch { order: 5; flex-basis: 100% }`). Logo, screen switch, theme button and badge share the first row, for a two-row header.
- Actual: Row 1 holds the logo (16..189) and the segs (205..361). The theme button and badge wrap to row 2 (y 49..81, `.hdr-r` x 233..384). The search is row 3 (y 89..121). The sticky header uses 130 of 800 px (16 %) on every screen and pushes the compare sticky offset to 130 px. `--hdr-h` tracks it correctly (130 = 130 after every resize).
- Evidence: `{"#logo":[16,12,189,36], ".segs":[205,8,361,41], ".hdr-r":[233,49,384,81], "#hsrch":[16,89,384,121], "--hdr-h":"130px", offsetHeight:130}`. Resize sync: 400 → 130, 520 → 130, 600 → 90, 759 → 90, 760 → 90, 900 → 53. Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/browse-400.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/compare-400.png`.
- Code: site/src/index.html:394 (narrow block) only moves the search. Row 1 needs about 173 + 16 + 156 + 16 + 151 = 512 px, but `.hdr-in` is 368 px wide at 400. The logo text, the `#cnt` pill and the "Compare" word in the badge (line 118) are not shortened below 760 px.
- Reproduced twice from clean state: yes

### F7. Below 760 px the header Tab order does not follow the visual order  [S3]
- Where: Header, 400×800 (any width below 760 where the search drops to its own row). All screens.
- Steps: 1. Clear and reload at 400×800. 2. Click an empty area, then press Tab 6 times.
- Expected: Focus follows the reading order: logo, Browse, Compare (row 1), theme, badge (row 2), search (row 3). WCAG 2.4.3.
- Actual: Focus goes logo → Browse → Compare → search `#hq` (row 3, y 90) → theme (row 2, y 49) → badge (row 2). Focus jumps down one row and then back up.
- Evidence: Tab sequence at 400: `logo@16,12, nav-browse@207,10, nav-compare@278,10, hq@49,90, theme-btn@233,49, badge@273,49, tf-toggle@17,273 …`.
- Code: site/src/index.html:394 `.srch { order: 5 }` changes only the visual order; the DOM order keeps `#hsrch` (line 427) before `.hdr-r` (line 435).
- Reproduced twice from clean state: once as a Tab run; the cause is the static DOM order, also seen in every header rect read-out.

### F8. Range sliders announce raw numbers, not the visible label  [S4]
- Where: `#f-price`, `#f-weight`, `#tf-price`, `#tf-weight`, all widths.
- Steps: 1. Clear and reload. 2. Read the attributes of `#tf-price`.
- Expected: A screen reader hears the same text as the visible label ("Any", "$900", "1130 g").
- Actual: `{aria-label:"Max price", aria-valuetext:null, value:"3500"}`. At the maximum the visible label says "Any", but assistive tech reads "3500" with no unit.
- Code: site/src/index.html:886 `range` builder; `syncRanges` (line 913) writes only the visible label.
- Reproduced twice from clean state: once; the cause is static markup.

### F9. The 3D stage name is lost: `aria-label` on a `div` with no role  [S4]
- Where: Compare, size panel, 3D tab, `#stage3d`.
- Steps: 1. Open `#compare`, click `#tab-3d`. 2. Read `role`, `aria-label`, `tabindex` of `#stage3d`.
- Expected: The stage is announced (for example `role="img"` with the label, or a group with a name).
- Actual: `{role:null, label:"3D view. Drag to rotate.", tabindex:null}`. ARIA does not allow a name on a generic `div`, so most screen readers ignore it. The 3D content is not announced at all (the slices are `aria-hidden`). The preset chips give keyboard users an alternative to drag, which is good.
- Code: site/src/index.html:1061 `sizePanelHtml`.
- Reproduced twice from clean state: once; the cause is static markup.

### F10. The Browse compare checkbox renders at 14×14, not the 16×16 the `.qbox` rule asks for  [S4]
- Where: Browse table `.qbox`, 760 px and wider.
- Steps: 1. Clear and reload at 760×800. 2. Measure `.qbox` rects.
- Expected: 16×16 (CSS line 214).
- Actual: 14×14 on all 30 rows.
- Code: site/src/index.html:71 `input[type="checkbox"] { width: 14px; height: 14px }` has specificity (0,1,1). It beats `.qbox` (0,1,0) at line 214.
- Reproduced twice from clean state: once (seeded queue of 1); the cause is static CSS.

## Clean areas
- Horizontal overflow sweep (Browse; Compare 2D and 3D with 4 devices and the size panel open; Detail `steam-deck-oled` and `onexplayer-x1-pro-255h`) at 400, 600, 759, 760, 960, 1100, 1440: `scrollWidth == clientWidth` everywhere except F1 (Compare 760 to 899) and the open dropdowns (F2, compare.md F3). Wide content stays inside `#tblw` and `.cmpw.scroll`.
- Header at 400: `--hdr-h` equals `#hdr.offsetHeight` after every resize (400, 520, 600, 700, 759, 760, 800, 900, 1000, 1280, back to 400). `#qpop` fits (x 64..384, items end at 379). `#badge` `aria-expanded` follows open, close and outside click.
- Browse below 760: `#side` hidden, `#topf` shown, `#lpanel.flat`, one 366 px card column, no layout segs, sort chips sort and keep focus. `#tf-toggle` sets `aria-expanded` true/false and `#tf-sum` reads "134 results +" / "−". Brand chips wrap to 3 rows inside the panel (max right 361). Both sliders work by mouse and by keyboard; after a resize to 1280, `#f-price` reads 900 / "$900" and `#f-weight` 1130 / "1130 g", and the table shows the same set and order as the cards. All 134 card silhouettes stay inside their plates. `#more-btn` and `#empty` span x 17..383 inside the 16..384 panel.
- Browse 759 ↔ 760: the layout swaps without reload in both directions (sidebar/table vs top panel/cards). Filters, sort, reference and the user's "cards" layout choice carry across. The table and cards show the same set and the same reference row. No console errors.
- Compare below 760: `.cmpw.scroll` has `overflow-x: auto`, inner `min-width: 704px`, window `scrollWidth` 400. Columns are 104 px + 4 × 150 px. Long names wrap ("OneXPlayer X1 Pro" 2 lines, `scrollWidth == clientWidth`). Stage is 240 px tall; the scale bar (x 41..185, bottom 645) sits inside the stage (bottom 653). `.size-b` is one column at 400 and 960, two at 961. The 3D stage drags with `page.mouse` at 400 (`rotateX(-14) rotateY(-30)` → `rotateX(-26) rotateY(2)`, `.drag` removed on release, presets unpressed).
- Confirmed wave 1, not re-reported: compare.md F1 (hunch H2). At 400 the header row covers "Overview", "MSRP" and "Released" (`elementFromPoint` hits `.cgrid.hd`); at 759 it covers "Overview" and "MSRP"; at 760 nothing. With the grid top 400 px above the window, the row is at top −269 at 400 px but stays at 53 at 1280. Screenshot `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/cmp-400-hd-gap.png`.
- Confirmed wave 1, not re-reported: compare.md F3 (hunch H1). `#sq-dd` overflows the window at 960 (box 766..1086, `scrollWidth` 1106), 1280 (1006..1326, 1346) and 1440 (1126..1446, 1466). At 400 the box (x 246..566) is cut by the scroll container at x 384; only 138 of 320 px show and the "+ Compare" labels are hidden. It is not cut vertically (container 1991 px tall, box bottom 678). `page.click` on the first item worked because Playwright scrolls the container first. Screenshots `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/sq-dd-400.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/sq-dd-1280.png`.
- Detail below 760: tiles in 2 columns with the right borders (`[0,0]`, `[1,0]`, `[0,1]`, `[1,1]` px left/top), PassMark rows `90px 240px` with the value row below the bar, `dl.kv` `96px 270px`, no `dd` overflow, `#dt-add` full width (33..367), outline stage fits (svg 41..359 in 17..383). `#pop` for the right-most `button.sv` sits at 28..388 in a 400 px window; near the bottom it flips above the button. Only detail.md F1 and F4 remain.
- Other widths: 960 (`.dgrid` and `.size-b` one column; 961 two), 1100 (`.sgrid` one column; 1101 two). At 1440 everything fits; at 1600 `main` and `.hdr-in` span 80..1520 (centred, 1440 max).
- Dark theme (emulated, clean storage): Browse, Compare (2D and 3D) and Detail at 1280 and 400 render with theme tokens. `.logo-ic` white on `#247bd2` is an icon (3:1 is enough). The dot grid, `.dpill` up/down (6.9:1 and 7.6:1), the `.best` tag (7.8:1 on `--bg`) and the 3D slices (`.sl` `#424b59`, front face `--bg` with the device colour stroke) read well. Only F4 and F5 fail. Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/dark-browse-1280.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/dark-compare-1280.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/dark-steam-deck-oled-1280.png`, the same at 400, and `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/dark-compare-3d-1280.png`.
- Reduced motion: `#rot`, `.sw`, `.sw::after` and `.size-h .ic` have `transition: none 0s`. After `#pre-front` the computed transform is `matrix(1,0,0,1,0,0)` at 0 ms. No other element has a transition.
- Accessibility code checks at 1280 and 400 on all three screens: no duplicate `id` (the hidden Compare and Detail screens keep their markup; `f-*`/`tf-*`, `q-`/`add-`, `ref-`/`cref-`, `open-`/`copen-`/`copen2-` are distinct). Every `input`, `button`, `[role=button]` and link has a name. Every `svg` has `aria-hidden` or `role=img` with a label. No inline `display` styles. No positive `tabindex`. `aria-expanded` tracks `#badge`, `#tf-toggle`, `#size-open` and `button.sv` (previous button resets, Escape resets). `aria-pressed` matches the visual state for segs, chips, view and mode chips, the `#hide-same` toggle and `.ccol`. `#pop` has `role=dialog`, a name and an `h4`. `#theme-btn` has no `aria-pressed`; it uses an action label ("Switch to dark" / "Switch to light") that flips correctly, which is a valid pattern (only the icon is wrong, F3). Nested buttons in `.ccol[role=button]` are compare.md F6.
- Live region `#lbar-n`: filter changes update its text in place (same node, "26 devices"), so the count is announced. `renderListBar` replaces the node on sort, reference and layout changes, but the count does not change then, so nothing is lost.
- Tab order at 400 (apart from F7): no focus trap. Browse, Compare (into the horizontally scrolled grid) and Detail reach every control in order. With an open queue slot, Tab from `#hq` moves into the first `.dd-item` and the list stays open. With a full queue every item is `disabled`, so Tab skips the list (by design).
- Hunch H3 (header 1 px off at 400): not reproducible. `#hdr` rect is exactly 0..400 and `scrollWidth` is 400.
- Hunch H4 (`.bgrid` past the window at 760 and 800): not reproducible. `.bgrid` spans 24..736 and 24..776; the table scrolls inside `#tblw` (462/1333 and 502/1333 px); no page overflow.
- Console: 0 errors and 0 warnings in every run; `playwright-cli console` shows only the favicon 404.

## Observations (not bugs)
- Touch targets under 24×24 CSS px at 400 (WCAG 2.5.8): `.refpill .xbtn` (`#ref-clear`) 16×16; `.plate .refb` (card reference) 22×22; `#qpop .xbtn` 22×22; `.ccol .xbtn` (`#crm-*`) 22×22; `button.sv` 18.8 px tall (inline in text, may fall under the inline exception); `.btn-t` links ("← Back to list", "Reset filters") 17.4 px tall; `.card-n` open buttons 19.2 px tall; range inputs 16 px tall. Chips are 25.4 px tall and pass. `.qbox` (14×14) and the table `.refb` (22×22) show only at 760 px and up.
- All 12 visible `th` carry `aria-sort` (11 × "none", 1 × "descending"). ARIA allows "none", but advises to set `aria-sort` on one header only (line 962). The sorted header's name also includes the "↓" glyph.
- The pressed seg differs from the unpressed one by 1.11:1 (light) and 1.15:1 (dark) in background; its `rgba(0,0,0,.12)` shadow (line 100) is invisible in dark. The state relies on the text colour.
- An "off" switch in light shows a white knob on `#d5dae3` (1.4:1), on a white panel (1.4:1).
- In dark, the back 3D slice `.sl.k` (`#111318`) is 1.1:1 against the stage. It is the back face, so it does not hide information.
- `REDUCED` (line 508) is defined and never used. The CSS media query alone handles reduced motion.
- `#stage3d` has `touch-action: none` and fills a 342×240 band at 400 px. A swipe that starts on it cannot scroll the page.
- At widths below 760 the row labels (`.clbl`) scroll away with the grid (at `scrollLeft` 200 they sit at x −183..−79). There is no sticky first column. Screenshot `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/cmp-400-hscroll.png`.
- `button.sv` has `aria-haspopup="dialog"` but no `aria-controls="pop"`.
- From 1101 px to about 1300 px the Detail groups are two columns of about 239 px; the `dl.kv` value column is about 129 px wide.
- Mixed chip group "Sticks · Status · Ports" in `#topf` has no visual break between the three filter kinds.
- Reference screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/browse-1440.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/compare-1440.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/browse-400.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/responsive/compare-400.png`.
