# Handheld Atlas: e2e GUI test brief (shared by every tester agent)

Read this whole file before you touch the browser.

## 1. What you test

- Project: `/home/n0k0m3/Programming/handheld-atlas` (git repo, branch `main`).
- Page under test: `http://127.0.0.1:8765/index.html` (a `python -m http.server` that serves `site/dist/`). It is already running. Do not start or stop servers.
- The same page also works from `file:///home/n0k0m3/Programming/handheld-atlas/site/dist/index.html` (the README says users open it from `file://`).
- Source of truth for the UI code: `site/src/index.html` (1539 lines). Lines 1 to 413 are CSS. Lines 415 to 480 are the static HTML shell. Lines 481 to 1539 are one IIFE of vanilla JS. `site/dist/index.html` is the same template with a `<script id="atlas-data" type="application/json">` blob inlined (134 devices, SoCs, outline paths). Line numbers in findings must refer to `site/src/index.html`.
- Page rules the page must satisfy: `site/CONTRACT.md` (phone width 400 px, no horizontal body scroll, theme tokens, hash routing, no alert/confirm, and so on).
- This is a **read-only** test job. Do not edit, create, or delete any file inside the repo. Do not run git commands that change state. Do not rebuild the site.

## 2. Page map (so you can target things fast)

Three screens in one page, toggled with `hidden`:

| Screen | Root element | Hash token |
|---|---|---|
| Browse | `main#scr-browse` | `#browse` |
| Compare | `main#scr-compare` | `#compare` |
| Detail | `main#scr-detail` | `#<device-id>` for example `#steam-deck-oled` |

Header (`header#hdr`): logo button `#logo`, nav segs `#nav-browse` / `#nav-compare`, search input `#hq` with dropdown `#hq-dd`, theme button `#theme-btn`, compare badge `#badge` (count in `#badge-n`) that opens the queue popover `#qpop`.

Browse: filter sidebar `aside#side` (checkboxes `.fchk` with ids `f-brands-<slug>`, `f-status-<slug>`, `f-sticks-<slug>`; ranges `#f-price`, `#f-weight`; switch `#f-usb4`; reset `#f-reset`). Below 760 px the sidebar is hidden and a collapsible top panel `#topf` appears (`#tf-toggle`, chips `tf-<f>-<slug>`, ranges `#tf-price` / `#tf-weight`, `#tf-usb4`, `#tf-reset`). List bar `#lbar` holds the count `#lbar-n`, the reference pill with `#ref-clear`, column-group chips `#g-<slug>` (table layout) or sort chips `#sort-c-<k>` (cards layout), and the layout segs `#lay-table` / `#lay-cards` (desktop only). Table `#tbl` with header buttons `#th-<colkey>` (colkeys: price weight dims soc cpu g3d screen res hz ram ssd battery stick trig ports). Rows `tr[data-id]` hold a compare checkbox `#q-<id>`, the open button `#open-<id>`, cells, and a reference button `#ref-<id>`. Cards `#cards > article.card[data-id]` with `#cref-<id>`, `#copen-<id>`, `#add-<id>`. `#more-btn` shows all rows past the 30-row limit. `#empty` is the no-match message.

Compare: back button, `h1`, `#hide-same` toggle, size panel (`#size-open`, tabs `#tab-2d` / `#tab-3d`, view chips `#view-front` `#view-back` `#view-top` `#view-side` or 3D presets `#pre-iso` `#pre-front` `#pre-top` `#pre-side`, layout chips `#mode-overlay` / `#mode-side`, 2D stage `#stage2d` with the scale bar `#sbar`, 3D stage `#stage3d` with `#rot`), legend `.legend`, then the grid: header row `.cgrid.hd` with one `.ccol[data-id]` per device (role=button, click or Enter/Space sets it as reference; inside: remove `#crm-<id>`, open `#copen2-<id>`), an add slot with input `#sq` and dropdown `#sq-dd` while fewer than 4 devices, then sections `.csec` and rows `.cgrid` with `.clbl` label and `.ccell` cells (`.dpill` deltas, `.best` markers). `.hid-note` reports hidden identical rows.

Detail: back button, outline stage `.dstage svg`, tiles `.tiles`, PassMark panel `.panel.pm`, title card with `#dt-h1`, `#dt-add`, `#dt-ref`, "Open comparison" button, then groups `.panel.grp` with `dl.kv`. Every sourced value is a `button.sv[data-si]` that toggles the fixed popover `#pop` (role=dialog). Groups "Conflicts", "Unresolved", "Sources" render `ul.dl` lists with external links (`target=_blank rel=noopener`).

All clicks go through one delegated listener keyed on `data-act`. Action names: go, open, q, add, rm, clear-queue, ref, setref, clear-ref, theme, badge, sort, grp, layout, reset-f, tf-toggle, chip, usb4, show-all, hide-same, size-open, size-tab, size-view, size-mode, preset, sv.

State lives in `localStorage["handheld-atlas:v3"]` as JSON `{v:3, queue, refId, sortK, sortDir, f:{brands,status,sticks,maxPrice,maxWeight,usb4}, groups, layout, hideSame, sizeOpen, sizeTab, sizeView, sizeMode, theme, route, detailId}`. A fresh visitor gets a default queue of 4 devices (steam-deck-oled, rog-xbox-ally-x, legion-go-2, msi-claw-8-ai-plus) and the first of them as reference. The page migrates `handheld-atlas:v2` / `v1` (`{sel:[{id}]}`) if present.

The data object is reachable in the page with: `JSON.parse(document.querySelector('#atlas-data').textContent)`. Use it to compute expected values (sort orders, deltas, counts, dims ratios) instead of trusting the UI.

Useful edge-case device ids: no MSRP `zotac-zone-pro`, `legion-go-z1`; status announced `zotac-zone-pro`, `ayaneo-geek-6600u`; pre-order `gpd-win-max-3-388`; external battery pack `gpd-win-5-395`, `onexfly-apex-air`; clamshell / slider / 3-in-1 `ayaneo-flip-kb-8840u`, `ayaneo-slide`, `onexplayer-x1-pro-255h` (longest name); with conflicts `steam-deck-oled`, `ayaneo-next-ii-395`; measured weight exists on 22 devices (for example `steam-deck-oled`); `d_max` set on 62 devices; stick type null on 13 devices (shows "Not stated"; filter value `unknown`).

## 3. Tooling rules (playwright-cli, headless, your own session)

- Use `playwright-cli` with your **own session name** given in your task (`-s=<name>` on every call). Never use another name. Never run `playwright-cli attach`, never touch `http://127.0.0.1:9222` (that is the user's shared Chrome), never run `close-all` or `kill-all`.
- Run every playwright-cli command from your own work dir, given in your task, so screenshots and logs land there. The shell does not keep `cd` between calls. Prefix each command: `cd <workdir> && playwright-cli -s=<name> ...`.
- Open once: `playwright-cli -s=<name> open http://127.0.0.1:8765/index.html`. The default viewport is 1280×720. Resize with `playwright-cli -s=<name> resize <w> <h>`. Close at the very end with `playwright-cli -s=<name> close`. One browser per agent; do not open a second session.
- Headless Chromium has no `prefers-color-scheme` by default (it reports light). Use `set-color-scheme dark` to emulate dark, `set-reduced-motion reduce` for reduced motion.
- Read state with `--raw eval`, for example:
  `playwright-cli -s=<name> --raw eval "JSON.stringify({route: location.hash, n: document.querySelectorAll('#tbody tr:not([hidden])').length})"`
  For multi-line scripts write a file and use `playwright-cli -s=<name> run-code --filename=script.js` where the file exports `async page => { ... return value }` (a Playwright `page`).
- Check the console after every flow: `playwright-cli -s=<name> console` (and `console error`). The favicon 404 is known and is not a finding. Anything else (uncaught error, failed resource, warning) is.
- Take a screenshot only when a finding is visual (layout, overflow, color, clipping): `playwright-cli -s=<name> screenshot --filename=<short-name>.png`. Name files after the finding.
- Horizontal overflow check: `document.documentElement.scrollWidth > document.documentElement.clientWidth` must be false on every screen at every width. Also report any element whose `getBoundingClientRect().right > innerWidth` that is not inside an `overflow-x:auto` container.
- To reset state between scenarios: `localstorage-clear` then `reload`. To seed state, use `localstorage-set handheld-atlas:v3 '<json>'` then `reload`.
- Do not use `alert`, `confirm`, or `prompt` in your eval code.
- Budget: aim to finish in about 30 to 40 minutes of work. Prefer scripted checks (one `run-code` that loops) over one click at a time when a check repeats across many items.
- **Only the `playwright-cli` binary through Bash.** Never call any `mcp__playwright__*` or `mcp__claude-in-chrome__*` tool, and never load them with ToolSearch. Those drive the user's shared Chrome.
- **Actions go through `run-code` with real Playwright calls** (`page.click('#id')`, `page.fill`, `page.keyboard.press`, `page.mouse.move/down/up`, `page.setViewportSize`). Real pointer and focus events matter here: the search dropdown opens on `focusin`, the 3D drag listens to `pointerdown`. `playwright-cli click` needs snapshot refs; do not use it. Use `eval` only for reads.
- Do not run a bare `snapshot` on Browse (30 rows × 17 cells). Use `find "<text>"` or `--raw snapshot > file.yml`.
- `--raw eval` already JSON-encodes the result. Return the object itself, never `JSON.stringify(...)`, or you get a double-encoded string.
- One `open` at the start, one `close` at the end, no re-open in between. Memory on this box is tight; three headless browsers run at once.
- After a click that re-renders (filters, sort, size chips), wait about 100 ms before you read: sliders apply on the next animation frame.

Known-good `run-code` file shape (this exact probe ran clean):

```js
async page => {
  const errs = [];
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
  await page.click('#nav-compare');
  await page.waitForTimeout(100);
  const h1 = await page.textContent('#scr-compare h1');
  await page.fill('#hq', 'win 5');
  await page.waitForTimeout(100);
  const dd = await page.$$eval('#hq-dd .dd-item', els => els.map(e => e.textContent.trim().slice(0, 40)));
  const active = await page.evaluate(() => document.activeElement && document.activeElement.id);
  return { h1, dd, active, hash: page.url().split('#')[1], errs };
}
```

Run it with `cd <workdir> && playwright-cli -s=<name> run-code --filename=<file>.js`. The returned object prints under `### Result`. Register the `pageerror` and `console` listeners at the top of every `run-code` file that performs actions, and include the collected `errs` in the return value. Ignore the favicon 404 line.

## 4. How to test (method)

1. Start with the happy path of your scope, then boundaries, then odd sequences (do X, then Y, then undo X). After each step: look at the DOM state that should have changed, and at what should **not** have changed.
2. Compare the UI against the data, not against your expectation of the data. Compute the expected value from the `#atlas-data` JSON.
3. Verify every suspected bug a second time from a clean state (`localstorage-clear` + `reload`) before you write it down. Record the exact steps.
4. A finding needs evidence: the DOM read-out, console line, or screenshot that shows it. "Looks odd" is not evidence.
5. Do not report design choices as bugs unless `site/CONTRACT.md` or the README says otherwise. You may list them separately under "Observations" (short).
6. When a behaviour matches the code and the code is clearly intentional, say so and move on.
7. Hunches given to you in your task are **unverified**. Test them last. "Not reproducible" is a valid result. Never report a hunch without your own evidence.
8. Record what you tested and found clean, briefly (one line per area). That is part of the deliverable.

## 5. Severity scale

- **S1 blocker**: a screen does not render, an uncaught exception, data loss of the queue/filters, a wrong number shown as a fact (wrong delta direction, wrong sort, wrong scale), interaction impossible at 400 px.
- **S2 major**: a feature fails in a common flow, a control does nothing, state does not persist or restores wrong, content clipped or unreachable, focus lost for keyboard users on a primary flow.
- **S3 minor**: cosmetic, text, inconsistent counts, edge cases needing odd input, a11y attribute drift.
- **S4 note**: observations and possible improvements.

## 6. Report format

Write your findings to the file named in your task (Markdown). Structure:

```
# <scope> findings

## Summary
<3 to 6 lines: what you covered, how many findings per severity, the biggest risk.>

## Findings
### F1. <short title>  [S1|S2|S3|S4]
- Where: <screen, control, viewport width, theme>
- Steps: 1. ... 2. ... 3. ...
- Expected: ...
- Actual: ...
- Evidence: <DOM read-out or console text, and/or screenshot path>
- Code: site/src/index.html:<line> <function name> — <one-line cause if you found it>
- Reproduced twice from clean state: yes/no

### F2. ...

## Clean areas
- <area>: <what you did>, no issue.

## Observations (not bugs)
- ...
```

Your final message back to the orchestrator must contain the same list in compressed form: one line per finding `F<n> [S<x>] <title> — <file:line>` plus the path of your report file. Do not paste screenshots or long DOM dumps into the final message.
