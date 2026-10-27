# Outline SVG format

One file per device and view: `outlines/<slug>.<view>.svg`. The view is `top`, `side` or `bottom`.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" width="Wmm" height="Hmm"
     data-device="slug" data-view="top" data-kind="traced" data-w="W" data-h="H"
     data-aspect-err="0.012" data-source="url or file"><path d="M … Z" fill="currentColor"/></svg>
```

## Rules

- 1 SVG unit = 1 mm.
- The origin is the top-left corner of the outline bounding box.
- `W` and `H` are the drawn extents in mm, rounded to 0.1 mm. `data-w` and `data-h` repeat them.
- The file has one `<path>`. Its `d` uses absolute `M`, `L` and `Z` commands only. Coordinates are rounded to 0.1 mm.
- The `d` string is under 4 KB.

## Attributes

| Attribute | Value |
|---|---|
| `data-device` | Device id (the file name of the device JSON) |
| `data-view` | `top`, `side` or `bottom` |
| `data-kind` | `traced` (from a render) or `box` (from the spec dimensions) |
| `data-w`, `data-h` | Width and height in mm |
| `data-aspect-err` | Traced only. `abs((bbox_h / bbox_w) / (h / w) - 1)` against the spec dimensions. Three decimals. |
| `data-source` | Traced: the image URL (or the image file path when no URL is known). Box: the device JSON path. |

## Views

| View | Across (x) | Down (y) |
|---|---|---|
| `top` | `dims_mm.handheld.w` | `dims_mm.handheld.h` |
| `bottom` | `dims_mm.handheld.w` | `dims_mm.handheld.h` |
| `side` | `dims_mm.handheld.h` | `dims_mm.handheld.d` |

A clamshell top view traced from `closed_top` uses `dims_mm.closed` when it is set.

## Traced outlines (`trace_outline.py`)

- `W` and `H` equal the spec width and height exactly. The traced silhouette is fitted to both (x and y scaled separately); `data-aspect-err` records how far the raw trace was from the spec aspect before that fit.
- The aspect check allows an error of 0.12. When the image fails as is, the tracer tries it rotated 90 degrees clockwise.
- No screen rectangle.

## Box outlines (`box_outline.py`)

- A rounded rectangle. Corners are line segments (8 per corner), so the path stays `M`/`L`/`Z`.
- Top and bottom corner radius: 14 mm for `classic`, 8 mm for the other form factors, capped at 0.2 x min(W, H).
- Side corner radius: 0.3 x min(H, D).
- The top view adds a centered `<rect class="screen" x y width height>` in mm, from `screen.size_in` and the `res_w:res_h` aspect (16:9 when unknown). There is no screen rect when `size_in` is null.

## Index

`outlines/index.json`:

```json
{ "<slug>": { "top": { "kind": "traced", "source": "https://…", "aspect_err": 0.009 },
              "side": { "kind": "box", "source": null, "aspect_err": null } } }
```
