# Artifact page contract

The claude.ai Artifact viewer enforces these rules on `site/dist/artifact.html`. The local `site/dist/index.html` is the same page wrapped in a full document. Build one template that satisfies both.

## Skeleton

- The artifact file is a **fragment**. The viewer wraps it in `<!doctype html><html><head>…</head><body>` at publish time. Do not write `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>` in the fragment.
- The viewer's head carries a charset and viewport meta (`viewport-fit=cover`), a light `color-scheme`, `:root` padded top and bottom by the phone safe-area insets, zero body margin, a 14px system font, `img{max-width:100%}`, and `[hidden]{display:none!important}`. Toggle visibility with `el.hidden`, not `style.display`.
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
- `localStorage` works per viewer but may throw or be empty. Wrap every read and write in try/catch. Use it only for conveniences (chosen columns, selected devices, view).
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
- Per-device overlay colors: pick 6 hues that stay legible on both light and dark backgrounds, define them as tokens, and use 35 % fill with a 1.5 px stroke.

## Icon

- First publish passes `icon: "chart"`. Redeploys omit it.

## Design notes for this page

- It is a tool, scanned and operated, not read top to bottom. Summary before detail. Encode state in form (pills for stick type, chips for port kinds, a stripe for status).
- Semantic color (good / warn / critical) is separate from the accent and does not count as the accent.
- Typography: Google Fonts allowed. Pair a display face with a body face and a tabular numeric face for data. Avoid Inter / Space Grotesk as the "safe" choice.
- Neutrals carry a slight hue bias toward the accent. No pure mid-grey.
- Use layout (`gap`) for spacing, not per-element margins.
- Repeated elements (cards, rows, chips) share edges, baselines, and padding.
- The page is complete at rest: every section visible on load, no observer-gated opacity.
- The overlay SVG uses one scale: 1 user unit = 1 mm, then a zoom transform. Leave room in the viewBox for the ruler labels. Every shape has an explicit fill.
- Give every form control a stable `id`.
- Visible keyboard focus. Respect `prefers-reduced-motion`.
- Avoid the generic AI look: cream + serif + terracotta, near-black + acid green, purple-blue gradient hero, emoji section markers, everything centered, rounded cards everywhere.
