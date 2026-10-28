# What changed in site/src/index.html after the 2026-10-27 report (read before you re-test)

The page was rebuilt (`site/dist/index.html`) and is served again at `http://127.0.0.1:8765/index.html`. The numbers below are the finding numbers in `/home/n0k0m3/Programming/handheld-atlas/docs/QA-e2e-2026-10-27.md`. The old raw reports (steps, read-outs) are in `/home/n0k0m3/Programming/handheld-atlas/docs/qa-e2e-2026-10-27/`.

## Intended new behaviour (judge against this, not against the old behaviour)

- 1: the Compare grid gets the `scroll` wrapper (class `.cmpw.scroll`, inner `min-width`) whenever it needs more width than the panel has, at any window width, not only below 760 px.
- 2: `.dd` dropdown rows can no longer grow past the box (`grid-template-columns: minmax(0,1fr)`, `.dd-item { min-width: 0 }`); the sub-line ellipsis now applies.
- 3: the Compare add-slot dropdown is anchored to the slot's right edge (`right: 12px`).
- 4: inside the scroll wrapper the grid header row is no longer CSS sticky. A passive scroll listener translates it so it follows the page header while the grid is on screen (`transform: translateY(..)` on `.cgrid.hd`). At scroll position 0 the transform is empty and the row sits at the panel top. Desktop (no scroll wrapper) still uses CSS sticky.
- 5: the reference row stays pinned on top, but counts follow the filtered set: `#lbar-n` shows the filtered count, a new `#lbar-x` note reads "plus the pinned reference" when the reference fails the filters, `#more-btn` and the row limit use the filtered count (the pinned row does not eat a slot), and the empty state shows when nothing passes (the pinned row is hidden then).
- 6: adding a device while no reference is set makes it the reference and rebuilds the list at once (pill, `tr.ref`, delta pills appear without reload).
- 7, 15: `.dl > li`, `.dl .why`, `#pop li`, `#pop .why` wrap long tokens (`overflow-wrap: anywhere`).
- 8: focus is restored after every re-render: the same control by id where it survives; otherwise a neighbour (after `#more-btn`: the first newly shown row's device button; after a popover remove `#qrm-<id>`: the next `#qrm-` or `#qpop-clear`; after a Compare remove `#crm-<id>`: the next column's remove button or `#sq`; after the empty-state reset: `#f-reset`). After a route change caused by a click: Detail focuses `#dt-h1` (unchanged), Compare focuses `#cmp-h1` (new id, `tabindex=-1`), Browse focuses the row or card button that opened the sheet (`#open-<id>` / `#copen-<id>`) or `#lbar` (now `tabindex=-1`). Header nav clicks that stay on the same screen do not move focus.
- 9, 13: `BY_ID`, `COL`, `SOC`, the filter counts and the row/card maps are null-prototype objects and every stored or URL value is checked with `hasOwnProperty`. `#constructor` and friends fall back to Browse; stored `constructor` ids, sort keys, views and brands are dropped; no exception.
- 10: `delta()` uses `Math.round(Math.abs(p))`. A zero reference value now yields "= 0%" when the value is also zero, else no pill.
- 11: the theme icons swap through `toggleAttribute("hidden")`.
- 12: a `?theme=` load no longer writes `theme: null`; the saved theme is kept.
- 14: a hash change to an unknown token keeps the current screen and rewrites the hash to its token.
- 16, 17: the source popover takes focus on open (`#pop` has `tabindex=-1` and an `aria-label` "Source for <value>"), repositions on scroll and closes when its value leaves the viewport, Tab from its last link closes it and moves to the next focusable after the value, Shift+Tab from its first link returns to the value, Escape returns to the value (unchanged).
- 18: when the sort column's group is hidden (or missing after a reload), the sort falls back to G3D, else the first visible numeric column; the header always shows the active sort.
- 19: the Ref column is gone. The ref button sits inside the device cell (`.dcell .dwrap .refb`, id `ref-<id>` unchanged). The checkbox column and the device column are sticky (`th/td.stk.c0` at left 0, `.stk.c1` at left 36 px) so they stay while the table scrolls sideways. The table uses `border-collapse: separate`.
- 20: header search ranks results: phrase match in the name (+8), name starts with the query (+4), token at a word start (+2), token elsewhere in the name (+1); ties by name. Cap is still 8. Sub-lines no longer repeat the SoC when the variant equals it.
- 21: "1 device", "Compare 1 handheld". The empty Compare heading reads "Nothing to compare yet".
- 22: when the Browse reference is not in the queue, the first column's tag reads "Baseline" (not "Reference"), the legend pill reads "BASE", and the hint names the reference and says deltas compare against the first column. Clicking a column still sets the global reference, after which the tag reads "Reference".
- 23: `.ccol` is a plain div (no `role`, `tabindex`, `aria-pressed`). The "Set as ref" / "Reference" tag is a real `<button id="cref2-<id>" data-act="setref" aria-pressed>`. The whole column is still clickable with the mouse. Enter/Space on the column div does nothing any more; use the button.
- 24, 25: focus into `#hq` or `#sq` closes the queue popover and the source popover. Tab out of a dropdown, the queue popover or the source popover closes it (checked on the next tick, so re-renders do not close them). Escape on a dropdown item returns focus to the input and closes the dropdown.
- 26: a `storage` event from another tab reloads the shared state into the page (queue, reference, filters, sort, groups, layout, size panel, theme) without touching the current route and without writing back.
- 27, 28: tokens: light `--fg-2` is `#5f6a7d`, light `--good` is `#00733c`, dark `--bg-brand` is `#1f6fc0` and `--bg-brand-hover` `#1a62ab`. `.tag.ref`, the checked `.qbox` and the on-state `.sw` use `--bg-brand` + `--fg-onbrand`. `.chk .n`, `.dl .url` and placeholders use `--fg-2`. The badge count box is `rgba(0,0,0,.22)`. `.chip .n` opacity is .8.
- 29, 30: below 760 px the header is a two-row grid in DOM order: row 1 logo + screen segs, row 2 search + theme/badge. `--hdr-h` is 90 px at 400 px. Tab order equals visual order. The search placeholder reads "Search devices" below 760 px.
- 31: when a max slider is below "Any", `#lbar-x` reads "N without a price hidden" / "N without a weight hidden" (devices with null values are still excluded).
- 32: queue "Clear" and removing the reference device from the queue leave the reference alone.
- 33: range inputs carry `aria-valuetext` equal to the visible label ("Any", "$900", "1130 g").
- 34: `#stage3d` has `role="img"`.
- 35: `.qbox` is 16×16; `.xbtn` and `.refb` are at least 24×24.
- Also: 3D angles persist across reload (`rx`, `ry` saved on release and on presets); the legend weight says "with pack" for external packs; the SSD cell says "Not stated" (capital); the Closed/Tablet size rows format thickness as "29.8 / 37.5 mm"; a stored `usb4` must be boolean `true` to apply.

## Things that did not change
- One global reference. The default queue and reference for a fresh visitor. Row limit 30. The 8-result cap. `replaceState` routing (no history entries). The CONTRACT rule set apart from the three notes added to `site/CONTRACT.md`.
