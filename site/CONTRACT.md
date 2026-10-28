# Artifact page contract

The claude.ai Artifact viewer enforces these rules on `site/dist/artifact.html`. The local `site/dist/index.html` is the same page wrapped in a full document. Build one template that satisfies both.

## Skeleton

- The artifact file is a **fragment**. The viewer wraps it in `<!doctype html><html><head>…</head><body>` at publish time. Do not write `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>` in the fragment.
- The viewer's head carries a charset and viewport meta (`viewport-fit=cover`), a light `color-scheme`, `:root` padded top and bottom by the phone safe-area insets, zero body margin, a 14px system font, `img{max-width:100%}`, and `[hidden]{display:none!important}`. Toggle visibility with `el.hidden`, not `style.display`. For an `<svg>` element use `el.toggleAttribute("hidden", on)`: `SVGElement` has no `hidden` property, so the assignment only adds a JS property.
- Put `<title>` and `<style>` at the top of the fragment. Only the first 8 KB is scanned for the title.
- Put `<meta name="claude:viewport-fit-sides" content="cover">` beside the title. It is only valid together with the two `max()` side paddings described under Responsive.
- Keep the `:root` padding the viewer adds.
- The local build wraps the same fragment in a real document: `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` + fragment head parts + `</head><body>` + fragment body + `</body></html>`. Simplest: keep the fragment a single file whose first elements are `<title>`, `<meta>`, `<link>`, `<style>`, followed by the markup and `<script>`. The wrapper moves nothing.

## Title

- `<title>` is a product name, two to four words: `Handheld Atlas`. No explainer after a dash or colon. Keep it the same across redeploys.

## External resources (CSP enforced)

- Scripts only from `https://cdnjs.cloudflare.com`, `https://cdn.jsdelivr.net/npm/`, `https://unpkg.com`, `https://cdn.tailwindcss.com`, `https://code.jquery.com`. Pin exact versions at least two weeks old.
- Stylesheets only from `https://fonts.googleapis.com` (font files from `fonts.gstatic.com`). Give every face a real fallback stack.
- Everything else is blocked silently: other hosts, external images, fetch/XHR, WebSocket. **Inline all CSS, JS, data, and SVG.** This page needs no library: vanilla JS + inline SVG.
- Mermaid renders natively via `<pre class="mermaid">`; do not load it. Not needed here.

## What the viewer frame allows

- No `alert()`, `confirm()`, `prompt()` (they return immediately). Build confirmations into the page.
- `window.print()` does nothing. No Print / Save as PDF buttons.
- `<a download>` and script-driven downloads are inert for viewers. Do not offer file downloads. (The local site may offer a CSV link, but gate it behind a `location.protocol !== 'https:'` check or leave it out.)
- Forms work as UI only; handle `submit` with `preventDefault()`.
- Copy buttons: `navigator.clipboard.writeText` inside the click handler, catch rejection, fall back to selecting text.
- `fetch()` works only for files published alongside the page. This page inlines its data so it needs no fetch.
- Links to `https://` sites open in a new tab. Use real `<a href target="_blank" rel="noopener">`.
- Only a plain `#anchor` reaches `location.hash`. Hash tokens for views are fine (`#compare`, `#overlay`, `#socs`); never `#/path` or `#key=value`. The address bar does not follow hash changes.
- `localStorage` works per viewer but may throw or be empty. Wrap every read and write in try/catch. Use it only for conveniences (chosen columns, selected devices, view, filters). The key is `handheld-atlas:v4`; v3 filters migrate on first load.
- Sound, camera, device APIs: not needed.

## Size

- Rendered page 16 MB or smaller, data URIs included. Inline SVG outline paths are small; keep each path under ~4 KB by simplifying contours.

## Responsive

- Must work at 400 px width. The body never scrolls horizontally.
- Side gutter at every width, on `body` or one outer wrapper:
  `padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));`
  Vertical padding via `padding-block`, never a `padding` shorthand that zeroes the sides.
- Flex/grid rows wrap or stack to one column when narrow. Any flex/grid child that holds text, code or a table gets `min-width: 0`.
- `max-width: 100%` on images and `aspect-ratio` boxes. No `min-width` wider than the screen.
- Wide tables and the SVG overlay may exceed the width only inside their own `overflow-x: auto` container.
- `position: sticky` cannot reach the viewport from inside an `overflow-x: auto` container (the container becomes the sticky root and never scrolls vertically). The compare grid header emulates it with a passive scroll listener and a `translateY` transform while the grid scrolls. Horizontal `position: sticky; left: 0` does work inside that container, so the grid's label column (and the header's hint cell, section titles and the hidden-rows note) stays frozen while the device columns scroll sideways; focus that lands under it scrolls clear.
- A sticky header uses `top: env(safe-area-inset-top, 0px)` and paints the band above with `body::before { content:""; position:fixed; inset:0 0 auto; height:env(safe-area-inset-top,0px); z-index:10; background: var(--bg) }`.
- `font-variant-numeric: tabular-nums` wherever digits line up.

## Theme-aware (required shape)

```css
:root { --bg: …; --fg: …; --muted: …; --line: …; --accent: …; /* every token, light values */ }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --bg: …; --fg: …; --muted: …; --line: …; --accent: …; color-scheme: dark }
}
:root[data-theme="dark"] { --bg: …; --fg: …; --muted: …; --line: …; --accent: …; color-scheme: dark }
body { background: var(--bg); color: var(--fg) }
```

- Every token is defined first on bare `:root`. The two dark blocks only redefine tokens.
- No component rule uses a literal color that reads in one theme only. Chart and SVG text use the tokens too.
- `body` sets an explicit background from a token (the host paints its own ground behind a transparent body).
- Per-device overlay colors: 8 hues that stay legible on both light and dark backgrounds, defined as tokens, each with a dash pattern as a second cue.

## Icon

- First publish passes `icon: "chart"`. Redeploys omit it.

## Design notes for this page

- The page is an app shell with four screens: Home, Browse, Compare, Detail. One sticky header holds the logo (the Home link), the Browse/Compare switch, the device search, the theme toggle, and the compare badge. Hash tokens: `#home`, `#browse`, `#compare`, and `#<device-id>` for a device sheet. A fresh visitor lands on Home; a stored route restores.
- Home is short: hero, stats and three cards. Browse holds a collapsed "How the reference works" panel and Compare a collapsed "How to compare" panel. Their examples are the live components (`.refb`, `.refpill`, `.dpill`, `.tag`, `.addb`), so the help cannot drift from the UI. Scripts that sync live controls select them with `[data-id]`, which the examples do not carry.
- The reference is optional. Pressing the reference again (target button, sheet button, or the Compare column tag) turns it off, and then no deltas show. Adding a device never sets the reference. When the reference is not in the compare list, the first column stands in as the baseline.
- Tokens follow the v3 design from the Claude Design project: cool slate greys, one blue accent (`#0768cf` light; in dark `#499fff` for outlines, text accents and focus rings and `#1f6fc0` behind white text, which keeps 4.5:1; checked marks sit on `--accent` with a dark `--fg-onaccent`, so the fill keeps 3:1 against the panel), green and red only for better and worse. Text uses `--fg` or `--fg-2`; `--fg-3` is for decoration only, since it is below 4.5:1 on both grounds. Panels use 10 px corners, controls 6 px, chips 4 px.
- Typography: Manrope for text, JetBrains Mono for every number, `font-feature-settings: "tnum"` on the body.
- Browse: cards by default, table on request. One facet panel (45 facets in 8 collapsible groups: multi-select lists with live counts, dual-range sliders, and must-have flag lists; price and release year carry a distribution histogram whose bars count the devices that pass the other filters and take the accent inside the range; release year has an "include devices with no release date" box; RAM is a slider over the sizes that exist and matches a device when any of its RAM options is in range) sits in the sidebar from 760 px and moves into the collapsible top panel below that. A quick-search box filters by name, chip, GPU or platform. Active filters show as removable chips. Facet lists and slider bounds come from the data. The table groups its columns (Price, Size, Performance, Display, Memory, Battery, Controls, Ports). A reference device pins to the top and drives the delta pills.
- Clamshells store their closed footprint. The 2D front and back views, the card silhouette and the sheet outline draw them open: deck below, a lid of the same footprint above, the screen in the lid, a hinge line with two knuckles. The 3D view draws them open and flat as well, each half with half the closed thickness, the screen on the lid's front face. When `dims_mm.without_battery` is smaller than the closed footprint (a front-edge battery module, GPD Win Max 3), the lid and the deck body take the size without the module and the module draws as a shaded strip at the front of the deck. Dimension lines and tiles stay on the closed size.
- Compare holds up to 8 devices with the `--dev-1` to `--dev-8` colours: blue, orange, aqua, yellow, magenta, olive, violet, rose, with darker steps for the dark stage. The order passes the dataviz palette validator on adjacent pairs in both modes (worst colour-blind ΔE 9.1 light, 8.4 dark; normal vision 19.6 and 19.3). Overlapping outlines put every pair together, which no eight-hue palette can separate, so each slot also has its own dash pattern, the legend shows both, and from five devices the side-by-side and 3D views wrap into two rows and the overlay suggests side by side. Green and red are not used, because they mean better and worse. The size panel draws 1 user unit = 1 mm inside a dot-grid stage with a scale bar. Views: Front and Back use the outlines, Top and Side are boxes from the stated size with a dashed `d_max` rect. The 3D view extrudes the front outline as stacked slices and rotates with pointer drag.
- Detail keeps the source linkage: every sourced value has a dotted underline that opens the source popover, and the Conflicts, Unresolved, and Sources groups stay.
- The list and the compare grid show the measured weight where a reviewer weighed a unit, else the stated weight. The device sheet shows both.
- Slider ranges come from the data, never from constants.
- Rows and cards are built once and reordered or hidden on filter and sort. Sliders re-apply on the next animation frame. The 3D drag writes one transform per frame and stores the angles on release.
- Give every form control a stable `id`. Visible keyboard focus. Respect `prefers-reduced-motion`.
- Avoid the generic AI look: cream + serif + terracotta, near-black + acid green, purple-blue gradient hero, emoji section markers, everything centered.
