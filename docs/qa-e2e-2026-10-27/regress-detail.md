# Detail re-test (findings 7, 8, 13, 14, 15, 16, 17, Also) findings

Page: `http://127.0.0.1:8765/index.html` (the dist build matches `site/src/index.html` apart from the data blob). Session `qa-rg-detail`, headless Chromium, 1280×800 and 400×800, light theme. Scripts and screenshots are in `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/regress-detail/`. All line numbers refer to `site/src/index.html`.

## Verdicts

| Finding | Verdict | Evidence |
|---|---|---|
| 7 Sources group clips notes | Fixed | 134 of 134 Sources panels have `scrollWidth === clientWidth` at 1280 and at 400. All 1249 `li` sit inside the panel. `#ayaneo-2` at 1280: panel 280/280 (was 280/466), widest `li` 256 px, right edge 945 < panel 958. `#ayaneo-flip-1s-ds-8840u` at 400: panel 366/366, `li` right 371 < 384. 40 sheets have a URL or a long token in a source note; none clip. |
| 8 Focus on Detail | Fixed | `#dt-add` and `#dt-ref` keep focus after Enter, Space and mouse click (queue of 1, 9 presses). `scrollY` stays at 150 (1280) and 686 (400). Back from row `#open-onexplayer-x2-mini` at 1500: focus on that button, `scrollY` 1500, next Tab goes to `#ref-onexplayer-x2-mini`. Back from card `#copen-acer-predator-atlas-7` (keyboard and mouse): focus on it, `scrollY` 1500. Back from a sheet opened with `#copen2-steam-deck-oled`: focus on `#lbar`. "Open comparison (n)": focus on `#cmp-h1` (`tabindex=-1`), next Tab goes to `#hide-same`. See F3 for two off-screen cases. |
| 13 URL-hash part | Fixed | A fresh load of `#constructor`, `#__proto__`, `#toString`, `#hasOwnProperty` or `#valueOf` shows Browse and rewrites the address to `#browse`. Storage holds `route: "browse"` and `detailId: null` (the key exists with the value null). A reload and a later load with no hash also show Browse. A seeded `detailId: "constructor"` with no hash shows Browse. There is no exception. |
| 14 Unknown hash on an open sheet | Fixed | On `#steam-deck-oled` I set the hash to `#no-such-device`, `#constructor`, `#__proto__`, `#toString`, `#hasOwnProperty`, `#` and `#Steam-Deck-OLED`. The sheet stays each time and the hash returns to `#steam-deck-oled`. The stored `detailId` stays `steam-deck-oled`. On Compare the hash returns to `#compare`, and on Browse to `#browse`. A valid id (`#legion-go-2`) still opens that sheet. |
| 15 Popover note runs outside | Fixed | `#ayaneo-air-1s-7840u` `$899`: `#pop` 358/358 (was 358/507), right edge 1156 of 1280, children end at 1141. At 400: right edge 388, children end at 373. The same holds for `ayaneo-2` "36.1 mm", `ayaneo-air-1s-limited` "$1,129" and `ayaneo-flip-1s-ds-8840u` "$999". In the sweep, 1795 of 1795 popovers per width have `scrollWidth === clientWidth` and every child inside the box and the viewport. |
| 16 Popover stays fixed on scroll | Fixed (side effects in F1, F2) | After `#sv-2` and a 300 px wheel, the value bottom is 159 and the popover top is 165 (gap 6). The popover closes when the value bottom is at −41 and stays closed after a scroll back. A popover above its value (flipped near the bottom edge) follows the value and closes when the value top reaches 800. At 400, after a 150 px wheel the gap is 6. A wheel with the pointer over the popover scrolls the page. |
| 17 Popover links by keyboard | Fixed (side effect in F2) | Enter on `#sv-0` focuses `#pop`, `aria-label` "Source for 637 g". Tab goes to the first link. Tab from the last link closes the popover and focuses `#sv-1` (the expected next focusable). Shift+Tab from the first link or from `#pop` focuses `#sv-0` and closes the popover. Escape from `#pop` or from a link focuses `#sv-0`. The 2-link popover (`aokzoe-a1x` `#sv-4`): Tab goes link 0, link 1, Shift+Tab back to link 0, Tab from link 1 goes to `#sv-5`. From the last value `#sv-8`, Tab goes to the `steamdeck.com` source link. A second mouse click closes the popover. A click on another value moves it and updates the label. In the sweep, 1795 of 1795 `el.click()` calls put focus on `#pop` and set the right label. |
| Also: Closed/Tablet thickness | Fixed | `ayaneo-flip-kb-8840u` Closed reads "180 × 102 × 29.8 / 37.5 mm". All 48 Closed, Tablet only and With keyboard rows on the 134 sheets match `w × h × d / d_max mm`. |

## Summary
- Coverage: I swept all 134 sheets at 1280 and at 400 and clicked 1795 `button.sv` per width. I checked PassMark, tiles, the title card and the groups against `#atlas-data` with 3 different references, and hand-checked 7 devices. I also ran keyboard and mouse flows for focus, the popover, hash routing and scroll.
- All 8 items in scope are fixed. The regression sweep has 0 failures and the console has 0 errors and 0 warnings.
- New defects: S1 0, S2 0, S3 2, S4 1. All three are side effects of the new popover and focus code.
- Biggest risk: a keyboard user who scrolls while a source popover is open loses focus to `body`. The next Tab then goes to `#logo` (F2).

## Findings

### F1. The source popover covers the sticky header while its value is behind the header  [S3]
- Where: Detail, `#pop`, 1280×800 and 400×800, light theme.
- Steps: 1. Clear storage and load `#steam-deck-oled`. 2. Click `#sv-2` ("2,201"). 3. Scroll down until the value bottom is at about 20 px from the top of the viewport (under the header).
- Expected: The popover closes, or it stays below the header, when its value goes behind the sticky header.
- Actual: The popover stays open at top 26 to 126. It paints over the header (logo, nav segments, search) because its z-index is higher. `elementFromPoint` at the value returns the header, so the value is not visible. The popover closes only when the value bottom goes below 0.
- Evidence: 1280: `{btnTop:1, btnBottom:20, hdrBottom:53, popTop:26, popOverHeader:true, valueCoveredBy:"header"}`. 400: the same with `hdrBottom:90`. The wheel run gave `{btnTop:-10, btnBottom:9, popTop:15, popHidden:false}`. Screenshots: `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/regress-detail/pop-over-header-1280.png`, `/tmp/claude-1000/-home-n0k0m3-Programming-handheld-atlas/c2568e76-13ba-4d96-a37b-14b7fe0fee0b/scratchpad/qa/regress-detail/pop-over-header-400.png`.
- Code: site/src/index.html:1472 placePop — the close test is `r.bottom < 0`, not `r.bottom < header bottom` (`--hdr-h`). `#pop` has `z-index: 60` (line 396) and `.hdr` has `z-index: 30` (line 84).
- Reproduced twice from clean state: yes (scroll16.js and hdrpop.js, each with goto, clear and reload).

### F2. When the popover closes by itself on scroll or resize, focus drops to `body`  [S3]
- Where: Detail, `#pop`, 1280×800 (keyboard); resize at 400 → 500.
- Steps: 1. Clear storage and load `#steam-deck-oled`. 2. Focus `#sv-0` and press Enter (focus goes to `#pop`). 3. Press PageDown (or Tab into the link and press ArrowDown several times). 4. Press Tab.
- Expected: When the popover closes because its value left the viewport, focus goes back to the value, as with Escape. The next Tab continues from the value.
- Actual: After step 3 the popover closes and `document.activeElement` is `BODY`. The next Tab focuses `#logo` at the top of the page. The keyboard user loses their place on the sheet. A window resize closes the popover in the same way: focus goes to `BODY`.
- Evidence: `open sv-0 by Enter → #pop sy 0` → `PageDown → BODY sy 700, popHidden true` → `Tab → #logo sy 700`. With ArrowDown ×20 from the link: `BODY sy 800` → `Tab → #logo`. Resize 400 → 500 with the popover open: `hidden true, active BODY`. 2 of 2 runs (repro.js, narrow.js).
- Code: site/src/index.html:1472 placePop and line 1690 (resize handler) call `closePop()` (line 1492), which does not move focus. Since fix 17, `#pop` holds focus (`pop.focus()` in openPop, line 1481), so closing it drops focus. The Escape branch at line 1618 shows the pattern: it calls `popBtn.focus()` after `closePop()`. A fix: when `pop.contains(document.activeElement)`, focus `popBtn` with `preventScroll: true` before the popover closes.
- Reproduced twice from clean state: yes.
- Severity note: S3, because it needs a keyboard scroll or a resize while a popover is open. The BRIEF puts "focus lost for keyboard users on a primary flow" at S2. Raise it if you count scroll-while-open as a primary flow.

### F3. "← Back to list" can put focus on a target that is off-screen  [S4]
- Where: Detail → Browse, 1280×800, table layout.
- Steps (a): 1. Clear storage and load `#browse`. 2. Scroll to 900. 3. Press Enter on `#nav-compare`. 4. Press Enter on `#copen2-steam-deck-oled`. 5. Press Enter on "← Back to list". 6. Press Tab.
- Steps (b): 1. Clear storage and load `#browse`. 2. Scroll to 1500. 3. Press Enter on the visible `#open-onexplayer-x2-mini`. 4. Press Enter on `#dt-ref` (the device becomes the reference). 5. Press Enter on "← Back to list". 6. Press Tab.
- Expected: The focused element is visible after the scroll restore. Otherwise the scroll follows the focus.
- Actual (a): `scrollY` is 900 and focus is on `#lbar`, at top −737 (off-screen). The next Tab goes to `#ref-clear` and the page jumps to `scrollY` 0.
- Actual (b): `scrollY` is 1500 and focus is on `#open-onexplayer-x2-mini`. That row is now the pinned reference row at the top, at −1190 (off-screen). The next Tab goes to `#ref-onexplayer-x2-mini` and the page jumps to 0.
- Evidence: `{active:"#lbar", sy:900, activeTop:-737}` → `Tab {active:"#ref-clear", sy:0}`. `{active:"#open-onexplayer-x2-mini", sy:1500, activeTop:-1190, firstRow:"onexplayer-x2-mini"}` → `Tab {active:"#ref-onexplayer-x2-mini", sy:0}`. 2 of 2 runs (repro.js).
- Code: site/src/index.html:1523 go() restores `browseY`, then lines 1528 to 1529 focus the target with `preventScroll: true` and do not check that the target is in view. Both cases match FIXNOTES literally (`#lbar` when the opener is not on Browse; the opener otherwise), so this is a note, not a failed fix.
- Reproduced twice from clean state: yes.

## Clean areas
- 134-sheet sweep at 1280 and at 400 (pageerror and console listeners on): every sheet visible; `#dt-h1` equals `model`; the hash equals the id; no `undefined`, `NaN` or `[object Object]`; no horizontal page overflow; `path.o` present; the outline label ends in "traced" or "spec box" as the data says; 4 tiles; 3 `.pm-r`; a Sources group with http links; every link has `target=_blank rel=noopener`. Every `.panel.grp` (all groups, not only Sources) has `scrollWidth === clientWidth`, and every `li`, `dt`, `dd` and `.gnote` sits inside its panel. 0 failures at both widths.
- Popovers in the sweep: 1795 `button.sv` clicked per width. Each opened `#pop` with at least one http link, inside the viewport, `aria-expanded="true"` on the value and `"false"` on the previous one, `aria-label` "Source for <value>", no overflow. 27 Escape samples closed it and focused the value. 107 second clicks closed it.
- Focus after `el.click()` inside the page: 1795 of 1795 left focus on `#pop` (openPop calls `pop.focus()`), at both widths.
- Popover mouse checks (2 runs): a click on the `h4` or the note inside keeps it open; a click on a `dt` closes it; `#nav-browse` closes it; a hash change closes it.
- PassMark on 134 sheets with 3 references (`steam-deck-oled`, `gpd-win-5-395`, `rog-ally-z1`): bar `style` equals `score / max × 100` to one decimal, the rank `#r/n` counts distinct values, the tick `left` equals `refScore / max × 100`, and the pill class and text match `Math.round(Math.abs(p))`. 399 pills and 399 ticks per reference, 0 failures. No tick, no pill and no "Tick mark" note on the reference's own sheet. No pill on Detail has an exact −x.5 percent, so the rounding change (finding 10) cannot be told apart here. The formula and the class are correct.
- Tiles and title card on 134 sheets with the 3 references: Width, Height, Thickness (`d / d_max mm`) and Weight match; price or "Price TBA", the status tag, "Released …", the variant line, the `#dt-add` label and `disabled` state, the `#dt-ref` label and "Open comparison (n) →" are correct.
- Groups on 134 sheets: 862 `.gnote` texts match the data notes (including "PassMark: " mapping notes). "No reviewer figure" shows on exactly the 112 sheets with no measured weight. Conflicts (80 sheets) and Unresolved (134 sheets) show exactly when the arrays are non-empty, with the right `li` count, fields, value links and "Chosen:" reasons. The Sources `li` count equals `sources.length`. All URLs are http(s).
- Hand checks at 1280 and 400: `steam-deck-oled` (measured 637 g with its notebookcheck.net link, Conflicts `wireless.bt` with 2 links and a reason, HDR "Yes"); `zotac-zone-pro` ("Price TBA", `tag info` "Announced", Released "Not stated"); `gpd-win-5-395` ("940 g with pack", Thickness "24.2 / 42.3 mm", External pack "Yes, it clips on outside the shell", Without pack 590 g); `ayaneo-flip-kb-8840u` (Clamshell, Closed "180 × 102 × 29.8 / 37.5 mm", Keyboard "Yes"); `onexplayer-x1-pro-255h` (no clipping in the title card or tiles, Tablet only "252 × 163 × 13 mm"); `acer-nitro-blaze-7` (Sticks "Not stated" with a sub-note); `acer-nitro-blaze-8` ("…, spec box").
- 400 px pass: no horizontal overflow on any sheet; every popover inside the viewport (left 28, right 388); `#dt-add` and `#dt-ref` keep focus and `scrollY`; the popover follows a wheel scroll (gap 6) and closes on resize.
- Console: 0 errors and 0 warnings in every run (`playwright-cli console`: 0 messages). Only the known favicon 404 on the first open.

## Observations (not bugs)
- My check for "digit/digit" in the Size group hit `acer-predator-atlas-8` and `acer-predator-atlas-8-g3`. The match is vendor text inside a `.gnote` ("Acer lists 299 x 127.4 x 28.5/58.37 mm"), not a rendered value.
- An unknown hash on an open sheet calls `go("detail", id)` again (line 1541). The sheet re-renders, an open popover closes and focus moves to `#dt-h1`. This is harmless, because the user edited the address bar.
- After a `#constructor` load, storage keeps the key `detailId` with the value `null`. Nothing reopens a blank sheet.
- 46 sheets still show "null" inside data notes (data wording, unchanged).
- A mouse click on a `dt` that closes the popover leaves focus on `body`. This is normal for a click on text.
