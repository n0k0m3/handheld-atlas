# Responsive, theme and a11y of the new features: findings

## Summary
- Coverage: overflow sweep of Home, Browse (cards and table, panel open and closed, 9 to 13 chips, long search), Compare with 4 clamshells (side by side and overlay) and 2 clamshell sheets. The sweep ran at 9 widths in both themes.
- Coverage also included the header, the Home layout, the facet panel (sidebar, top panel, move across 759/760, mouse drags at 400), WCAG contrast, the a11y code checks, reduced motion and clamshell screenshots.
- Findings: 0 × S1, 1 × S2, 3 × S3, 4 × S4.
- Biggest risk: F1. A quick-search text of about 50 characters at 400 px (or about 70 at 760 px) makes the body scroll sideways. The search box itself then runs off the screen.
- Console: clean during all flows. The only entry was the known favicon 404.

## Findings

### F1. Long quick-search text widens the filter bar past the viewport  [S2]
- Where: Browse, `.fbar` (`#fq` and `#fchips`). Seen at 400, 520 and 760 px, light and dark.
- Steps:
  1. Open `#browse` at 400×800 from a clean state.
  2. Type `gpd win max 2 2025 ryzen ai 9 hx 370 radeon 890m oled` (53 chars) into `#fq`.
  3. Read `document.documentElement.scrollWidth`.
  4. Repeat at 760 px with a 72-char query (`… oled 120hz 32gb lpddr5x`).
- Expected: The body never scrolls sideways (CONTRACT, Responsive). The "Search: …" chip truncates with its ellipsis (`.fchip span` has `text-overflow: ellipsis`).
- Actual: At 400, `scrollWidth` is 406 and `.fq-box` ends at x=406. At 760, `scrollWidth` is 778. `.fbar` grid column is `389.86px` in a 368 px column. The chip span never truncates, because its container grows to fit it. With an 80-char seeded query, `scrollWidth` reaches 569 at 400 and 825 at 760. The overflow also happens at 520. At 600 and 759 an 80-char query still fits.
- Evidence:
  - DOM: `{len:53, sw:406, fbarW:368, fqBoxR:406, iw:400}` and `{len:72, sw:778, fbarW:464, fqBoxR:778, iw:760}`.
  - Overflow probe: `div.srch-box.fq-box L16 R569`, `#fx-q L16 R569`.
  - Screenshot: `qa/feat-responsive/fchips-long-search-400.png` (the box and the chip × are cut at the right edge).
- Code: site/src/index.html:200 `.fbar { display: grid; … }` has no `grid-template-columns`. The implicit `auto` track takes the min-content width of `#fchips`, which is the full `nowrap` text of `.fchip span` (line 206). `min-width: 0` sits on `.fbar` but not on its grid items. CONTRACT asks for `min-width: 0` on such children. `grid-template-columns: minmax(0, 1fr)` would contain the overflow.
- Reproduced twice from clean state: yes. Two typed runs at each width gave the same numbers.

### F2. Focus drops to `body` when the facet panel moves across 759/760  [S3]
- Where: Browse facet panel `#fpanel`, any focused control in it, resize across the breakpoint in either direction.
- Steps:
  1. Open `#browse` at 1280 from a clean state.
  2. Click the "GPD" label. Focus is now on `#f-brands-gpd`.
  3. Resize to 700. Read `document.activeElement`.
  4. Open `#tf-toggle`, press Tab (focus is now on `#f-reset`), and resize to 1000.
- Expected: FEATURES and the task say that the node moves and that focus survives with the open groups, checked values and slider positions.
- Actual:
  - The node is the same object (`fp === window.__fp`).
  - Open groups (`general,performance,display`), checked values, slider values, "Show more" state and `#tf-toggle` state all survive.
  - Focus goes to `BODY` on every crossing: 1280→759, 759→760, 760→400 and 759→1280.
  - A resize that stays on one side (400→759) keeps the focus (`f-brands-gpd`).
- Evidence: `{before:"f-brands-gpd", after1280to700:"BODY", pre:"f-reset", after700to1000:"BODY"}`, the same in both runs. facet2.js has the full log.
- Code: site/src/index.html:1210 `placeFilterPanel()`. `host.appendChild(fp)` removes the subtree and inserts it again, and Chromium blurs the focused descendant. The code does not keep `document.activeElement` and does not focus it again (with `preventScroll`) after the move. Note: on a move to narrow while `#topf-b` is closed, the control is hidden anyway. The top panel would have to open for focus to stay.
- Reproduced twice from clean state: yes.

### F3. Range value label wraps to two lines in the 232 px sidebar  [S3]
- Where: Sidebar facet panel at 760 px and wider, light and dark. Facets "PassMark single thread" (`#f-st-l`) and "RAM speed" (`#f-ramspeed-l`).
- Steps:
  1. Seed a v4 state with every range set to `[min+step, max-step]`, and open all groups.
  2. At 760, 960 or 1280, measure `.fct[data-k=st] .st`.
- Expected: The label and the value fit on one line, as they do at 400 to 759 in the top panel.
- Actual: `.st` is 32 px high. The value breaks as "2,250 –" / "4,300". RAM speed breaks as "4,300 MT/s – 8,500 MT/s" over two lines. There is no overlap and no clipping.
- Evidence: Probe output `st: st h 32 [PassMark single thread | 2,250 – 4,300 | stW 206]`. Screenshot: `qa/feat-responsive/side-st-wrap.png`.
- Code: site/src/index.html:183-184 `.st` / `.st .m`. The value span has no `white-space: nowrap`, and the label does not give way first.
- Reproduced twice from clean state: one clean seed, confirmed at 760, 960 and 1280 in both themes (deterministic CSS).

### F4. The chips row `aria-label` does not reach assistive tech  [S3]
- Where: Browse `#fchips`.
- Steps:
  1. Seed 6 filters.
  2. Run `locator('.fbar').ariaSnapshot()`.
- Expected: The row is announced as "Active filters" (FEATURES and the task: "the chips row has aria-label").
- Actual: The attribute is present (`aria-label="Active filters"`, `role=null`). The aria snapshot lists the chip buttons but no group and no "Active filters" name. A plain `div` has the generic role, and ARIA does not allow a name on that role, and the aria snapshot shows no group node and no "Active filters" name.
- Evidence: `fbarAria: "- searchbox \"Filter the list\" … - button \"Remove filter Brand: GPD\" …"`. The output has no group node.
- Code: site/src/index.html:590 `<div class="fchips" id="fchips" aria-label="Active filters">`. It needs a role such as `group` (or `region` or `list`) for the label to apply.
- Reproduced twice from clean state: yes (code-level, static markup).

### F5. Summary focus ring is clipped at the sides inside the sidebar  [S4]
- Where: `details.fsec > summary` in `aside#side`, at 760 px and wider.
- Steps:
  1. Open `#browse` at 1280.
  2. Focus `#f-reset` and press Tab.
- Expected: A full visible focus ring.
- Actual: The ring (2 px, offset 1 px) shows only its top and bottom lines. The summary spans the full inner width (x 25 to 255). `.side` has `overflow: auto`, so it clips the left and right parts. The ring is still visible. At 400 (top panel, no overflow) the full ring shows.
- Evidence: `summary-ring-1280.png` (sides clipped) and `summary-ring-400.png` (full ring).
- Code: site/src/index.html:180 `.side { … overflow: auto }` together with line 65 `:focus-visible { outline-offset: 1px }`. A negative offset on `.fsec > summary:focus-visible` would keep the ring inside.
- Reproduced twice from clean state: yes.

### F6. Overlapping thumbs move in one direction only  [S4]
- Where: Any dual-range facet, at 400 (mouse drag) and at 1280.
- Steps:
  1. At 400, set TDP lo to about 90 W and hi to 90 W, so both thumbs sit in the upper half.
  2. Drag from the shared point to the right.
- Expected: The range widens upwards.
- Actual: The minimum thumb sits on top (`zIndex 4`, line 1231). It gets the drag and is clamped to the maximum, so nothing moves (`[90, 90]` stays). A drag to the left works. In the lower half the maximum thumb is on top, so a drag to the left is blocked. With both at the top end or at the bottom end, the thumbs are still reachable, as the code intends.
- Evidence: facet4.js `["shared (upper half) drag right to 0.95", {hit:"f-tdp-lo", v:["90","90","90 W – 90 W"]}]`.
- Code: site/src/index.html:1231 `syncRange()` z-index rule and lines 1237-1238 `rangeInput()` clamp. This is the usual limit of two stacked native ranges. The keyboard path works.
- Reproduced twice from clean state: yes (price and TDP runs).

### F7. `#home-h1` focus ring is tight against the hero text  [S4]
- Where: Home, after keyboard navigation (logo + Enter).
- Steps:
  1. Open `#browse` at 400 or 1280.
  2. Focus `#logo` and press Enter.
  3. Read `document.activeElement` and its computed outline.
- Expected: The same ring as the other screen titles. `#cmp-h1` uses `outline-offset: 4px`.
- Actual: `#home-h1` gets `solid 2px off 1px`. The ring touches the descenders of the 32/52 px hero. The mouse path correctly shows no ring (`fv:false`).
- Evidence: `home-h1-kbd-400.png`, and `{id:"home-h1", fv:true, outline:"solid 2px off 1px"}` vs `{id:"cmp-h1", outline:"solid 2px off 4px"}`.
- Code: site/src/index.html:148 `.phead h1:focus-visible` does not match `#home-h1`, because that heading sits in `.hhero` (line 540).
- Reproduced twice from clean state: yes (400 and 1280).

### F8. Guide demos drift a little from the live components  [S4]
- Where: Home guides, at all widths, both themes.
- Steps:
  1. Open `#home`.
  2. Look at step 1 of "Compare sizes at true scale" and step 1 of "Set a reference device".
- Expected: The demo matches the text colour and spacing of the live `.addb` and `#dt-ref`.
- Actual:
  - The demo "Add to compare +" renders as "Add to compare+" with no gap. `.addb` uses `justify-content: space-between` and needs the full card width to separate the "+".
  - Demo `.btn-o` ("Set as reference") and `.addb` text inherit `--fg-2` from `.steps`. The live `#dt-ref` and the card `.addb` use `--fg`. Contrast still passes (5.46 and 6.78).
- Evidence: `home-1280-light.png` (step 1 of "Compare sizes").
- Code: site/src/index.html:563 (markup), 174 (`.demo .btn-o.sm, .demo .addb.sm`), 164 (`.steps { color: var(--fg-2) }`).
- Reproduced twice from clean state: yes (static markup).

## Clean areas
- Horizontal overflow: clean in 138 combinations except F1. Home, Browse cards (9 chips, panel closed and open with all 8 groups open), Browse table (760 to 1440, short-chip set only; F1 does not depend on the layout, because `.fbar` sits outside `#lpanel`), Compare side by side and overlay with 4 clamshells, and the sheets for `gpd-win-max-2-2025` and `ayaneo-flip-kb-8840u` were all tested at 9 widths in both themes.
- Header: 90 px with two rows at 400, 520, 600 and 759. `--hdr-h` matches `offsetHeight` on Home, Browse and Compare at all widths. The Tab order after a reload is logo, Browse, Compare, `#hq`, theme, badge at 400, 520, 760 and 1280.
- Home:
  - The cards use 1 column at 400.
  - No `.demo` part crosses its `li` box at any width.
  - The `.step-n` badges are 24×24.
  - The stats do not overlap and nothing clips.
  - The screenshots at 1280 and 400 in both themes look correct.
- Facet panel at 1280:
  - The panel is in `#side`.
  - The sidebar is sticky at 69 px (header 53 + 16).
  - The sidebar has a `max-height` of 635 px and scrolls inside (scrollHeight 7023).
  - `overscroll-behavior` keeps the page still at the end.
  - The groups open and close by mouse, by Enter and by Space.
- Facet panel at 400: the panel is in `#topf-b` behind `#tf-toggle` (`aria-expanded` syncs). The summary text `#tf-sum` updates.
- Move across 759/760: the same node moves. Open groups, checked boxes, both slider values, "Show more" state and the label text survive. Focus does not survive (F2).
- Sliders at 400 (`page.mouse`):
  - Both thumbs are reachable.
  - The fill, the label and `aria-valuetext` follow every drag.
  - The minimum thumb clamps at the maximum.
  - With both thumbs at the top end, the lo thumb lifts (`zIndex 4`) and drags down.
  - With both at the bottom end, the hi thumb drags up.
  - `.rng-e` end labels never overlap at any width.
  - `#lbar-x` reports "22 without a price hidden".
- Contrast (WCAG formula, both themes): every text pair passes 4.5:1. The lowest are `.fchip` 4.77 light, `.dpill.dn` 4.82 light, `.dpill.eq` and `.tag` 4.91 light, and `.fsec-n` 5.13 dark.
  - Checked text pairs: `.fsec-n`, `.fchip` (also hover), `.st .hint`, `.rng-e`, `.chk.zero` labels and counts, `.fmore`, `.step-n`, `.hstat`, `.hcard` text and links, the eyebrow and the lede, all `.demo` examples, `#tf-sum` and `#lbar-x`.
  - UI parts: fill vs track is 3.85 light and 3.23 dark. The thumb border vs the panel is 5.40 and 5.48. The summary chevron is 5.46 and 6.78 (5.01 and 6.26 on hover).
- Accessibility:
  - No duplicate ids on Home, Browse cards, Browse table, Compare or Detail.
  - Every `input` and `button` has a name.
  - Each `summary` has its group text as its name.
  - All 17 range pairs carry "<label>, minimum/maximum".
  - `aria-valuetext` equals the end labels at rest and follows keyboard changes ("≤ 9,000" after Home).
- Heading focus after a route change: `#home-h1` and `#cmp-h1` take focus after a mouse click (logo, segs, Home CTA) with no `:focus-visible`. After keyboard Enter they show `:focus-visible`. This holds at 1280 and 400.
- Tab through the panel: no trap at 1280 (96 stops, then on to `#fq`) or at 400 (97 stops, then on to `#sort-c-g3d`). No stop repeats. Shift+Tab goes back into the panel. Controls in closed groups are skipped.
- Reduced motion: with `reduce`, a full scan of Browse, Compare and Home finds no transition or animation. The new UI adds none. Only `.sw` and `.sw::after` transition with `no-preference`.
- Clamshell visuals:
  - Compare front view, side by side, 4 clamshells: 4 `path.lid` and 4 `line.hinge`. All shapes stay inside the stage at 1280 and 400 in both themes. `.dnote` shows.
  - Cards: lid and hinge are present, and the silhouette stays inside the plate without touching the reference button.
  - Sheets (4 ids at 400, 2 at 1280, both themes): lid, hinge and `.dnote` are present, and no shape leaves `.dstage`.
  - In dark the lid reads by its stroke. Its fill is `fill-opacity .03`, as the code intends.
- Console: clean (favicon 404 only).

## Observations (not bugs)
- Touch targets at 400 under 24×24:
  - `#f-reset` and `#fx-clear` are 46 to 49 × 17.4.
  - `.fmore` is 73 × 17.4.
  - The range thumbs are 16×16 on a 22 px input.
  - The checkbox inputs are 14×14, but the whole `.chk` row (350 × 24.8) is the target.
  - These pass. `.fchip` is ≥92 × 24, `summary` is 366 × 38 and `#tf-toggle` is 366 × 39.
- The unfilled range track is `--border-strong` on `--bg`: 1.40:1 light and 1.70:1 dark. The thumbs and the fill carry the meaning, so this is not a required pair.
- The `.demo .refb` border is 1.40 and 1.70 against `--bg`. It is decoration, and the icon is 5.46 and 6.78.
- Between 760 px and about 850 px the header wraps to 90 px. The theme button and the badge sit alone on row 2 (`hdr-760.png`). From 860 px the header is one row.
- At 520 to 759 px, the Home card grid has 2 columns, so the third card ("Reference") sits alone on row 2.
- Each `summary` name includes a bare count ("General 2"), with no word for what the number means.
- `REDUCED` (site/src/index.html:648) is declared but never read.
- The dashed hinge line hardly shows in either theme. It is drawn at `y = o.h`, the same place as the solid lid edge and deck edge, and in the same colour (`var(--c)` in Compare, `--fg-2` under `--fg` edges on the sheet). The open state reads from the two stacked shapes, not from the dashes. See `qa/feat-responsive/hinge-cmp-dark-zoom.png` and `hinge-sheet-dark-zoom.png` (3x DPR). Code: site/src/index.html:349-350, 770.
