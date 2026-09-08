#!/usr/bin/env python3
"""
grid.py — construct a slide design system by Müller-Brockmann's method.

It does not choose values by eye. Given a canvas, a body size, a leading
factor, a mean character advance and a field count, it derives the margin
zone, the type area, the baseline unit, the column count and width, the
gutter, the field arrangement, the type scale and the colour roles, then
writes:

    <out>/tokens.json   the numbers
    <out>/theme.css      a Marp theme bound to those numbers

See references/muller-brockmann.md for why each step is what it is.

Usage:
    python3 grid.py --canvas 16:9 --body 22 --fields 8 --advance 0.50 --out system/
    python3 grid.py --from system-in.json --canvas 16:9 --fields 20 --out system/
"""

import argparse
import json
import math
import sys
from pathlib import Path

# --- canvas presets, in reference pixels -----------------------------------

CANVASES = {
    "16:9": (1280, 720),
    "16:10": (1280, 800),
    "4:3": (1024, 768),
}

# Field-count -> (columns, rows) arrangements from the book's worked
# examples (8, 20, 32) plus two useful screen ratios. Any count not here
# falls back to the factor pair closest to the canvas aspect.
FIELD_ARRANGEMENTS = {
    8: (4, 2),
    12: (4, 3),
    16: (4, 4),
    18: (3, 6),
    20: (4, 5),
    32: (4, 8),
    36: (6, 6),
}

# Margin zone as fractions of the canvas SHORT side. Ordered so the type
# area sits slightly high and left of centre: left < top < right < bottom.
# This holds Müller-Brockmann's rejection of equal margins and keeps the
# type area near a 1:2 relation to the frame.
DEFAULT_MARGINS = {"left": 0.055, "top": 0.075, "right": 0.075, "bottom": 0.110}

# Type scale as ratios of the body size (see muller-brockmann.md).
TYPE_SCALE = {"title": 2.9, "headline": 1.65, "body": 1.0, "caption": 0.7}

DEFAULT_COLOURS = {
    "ink": "#111111",
    "ground": "#F6F6F6",
    "accent": "#CD0000",   # the grid-marking red; not a body colour
    "muted": "#737373",
}


def parse_canvas(value):
    if value in CANVASES:
        return CANVASES[value]
    if "x" in value.lower():
        w, h = value.lower().split("x")
        return int(w), int(h)
    if ":" in value:
        # an aspect with no size -> scale to 720 on the short side
        a, b = (float(x) for x in value.split(":"))
        if a >= b:
            return round(720 * a / b), 720
        return 720, round(720 * b / a)
    raise ValueError(f"unrecognised canvas: {value}")


def field_arrangement(fields, aspect):
    """(columns, rows) for a field count, closest to the canvas aspect."""
    if fields in FIELD_ARRANGEMENTS:
        return FIELD_ARRANGEMENTS[fields]
    best = None
    for cols in range(1, fields + 1):
        if fields % cols:
            continue
        rows = fields // cols
        ratio_err = abs((cols / rows) - aspect)
        if best is None or ratio_err < best[0]:
            best = (ratio_err, cols, rows)
    return best[1], best[2]


def build(canvas, body, leading, advance, fields, target_chars, faces, colours):
    page_w, page_h = canvas
    short = min(page_w, page_h)
    aspect = page_w / page_h

    # 1. margin zone (proportioned, never equal)
    m = {k: round(v * short) for k, v in DEFAULT_MARGINS.items()}

    # 2. type area
    area_x, area_y = m["left"], m["top"]
    area_w = page_w - m["left"] - m["right"]
    area_h_raw = page_h - m["top"] - m["bottom"]

    # 3. baseline unit, and type-area depth snapped to a whole number of units
    baseline = round(body * leading)
    area_units = area_h_raw // baseline
    area_h = area_units * baseline

    # 4. columns from type size (about `target_chars` per line)
    columns = max(1, math.floor(area_w / (target_chars * advance * body)))

    # 5. gutter = one blank leading line
    gutter = baseline
    col_w = (area_w - (columns - 1) * gutter) / columns

    # 6. field arrangement: N columns x M rows, one blank baseline between rows
    f_cols, f_rows = field_arrangement(fields, aspect)
    # each field row is K baselines deep: M*K + (M-1) blanks == area_units
    field_rows_units = max(1, math.floor((area_units - (f_rows - 1)) / f_rows))
    field_h = field_rows_units * baseline
    field_w = (area_w - (f_cols - 1) * gutter) / f_cols

    # 7. type scale in px
    scale = {k: round(body * r) for k, r in TYPE_SCALE.items()}

    tokens = {
        "canvas": {"w": page_w, "h": page_h, "aspect": round(aspect, 4)},
        "margins": m,
        "type_area": {
            "x": area_x, "y": area_y, "w": area_w, "h": area_h,
            "units": area_units,
        },
        "baseline": baseline,
        "leading_factor": leading,
        "columns": {"count": columns, "width": round(col_w, 2), "gutter": gutter},
        "fields": {
            "count": f_cols * f_rows, "cols": f_cols, "rows": f_rows,
            "width": round(field_w, 2), "height": field_h,
            "rows_in_baselines": field_rows_units,
        },
        "type_scale": scale,
        "advance": advance,
        "target_chars": target_chars,
        "faces": faces,
        "colours": colours,
        "notes": [],
    }

    if columns != f_cols:
        tokens["notes"].append(
            f"reading columns ({columns}) differ from field columns ({f_cols}); "
            f"set body/target_chars or field count so they agree, or place body "
            f"text on {columns} columns and images on {f_cols} fields."
        )
    return tokens


def theme_css(t, name):
    c = t["colours"]
    m = t["margins"]
    s = t["type_scale"]
    cv = t["canvas"]
    base = t["baseline"]
    col_w = t["columns"]["width"]
    gutter = t["columns"]["gutter"]
    return f"""/* @theme {name}
   Generated by grid.py from tokens.json. Do not edit by hand — change the
   grid.py flags and re-run. Every value here is derived, not chosen. */

section {{
  width: {cv['w']}px;
  height: {cv['h']}px;
  padding: {m['top']}px {m['right']}px {m['bottom']}px {m['left']}px;
  background: {c['ground']};
  color: {c['ink']};
  font-family: {t['faces'].get('body', 'Inter, system-ui, sans-serif')};
  font-size: {s['body']}px;
  line-height: {base}px;
  letter-spacing: 0;
}}

h1 {{ /* deck title / section divider — use _class: title or section */
  font-family: {t['faces'].get('display', 'inherit')};
  font-size: {s['title']}px;
  line-height: {base * 2}px;
  font-weight: 700;
  margin: 0;
}}

h2 {{ /* the assertion headline — one full sentence, <= two lines */
  font-family: {t['faces'].get('display', 'inherit')};
  font-size: {s['headline']}px;
  line-height: {base}px;
  font-weight: 600;
  margin: 0 0 {base}px 0;
  max-width: {round(col_w * t['columns']['count'] + gutter * (t['columns']['count'] - 1))}px;
}}

p, ul, ol {{ margin: 0 0 {base}px 0; }}
li {{ margin: 0; }}

.caption, footer, section::after {{
  font-size: {s['caption']}px;
  color: {c['muted']};
  line-height: {base}px;
}}

section.title, section.section {{
  background: {c['ink']};
  color: {c['ground']};
  display: flex;
  align-items: center;
}}
section.title h1, section.section h1 {{ color: {c['ground']}; }}

section.cta h2 {{ color: {c['accent']}; }}

/* alignment check: add class="grid-overlay" while verifying */
section.grid-overlay {{
  background-image:
    repeating-linear-gradient(to right,
      rgba(205,0,0,.18) 0 1px,
      transparent 1px {round(col_w)}px,
      transparent {round(col_w)}px {round(col_w + gutter)}px),
    repeating-linear-gradient(to bottom,
      rgba(205,0,0,.12) 0 1px,
      transparent 1px {base}px);
  background-position: {m['left']}px {m['top']}px;
  background-size:
    {round(col_w * t['columns']['count'] + gutter * (t['columns']['count'] - 1))}px 100%,
    100% {t['type_area']['h']}px;
  background-repeat: no-repeat;
}}
"""


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--canvas", default="16:9", help="16:9 | 4:3 | 1280x720")
    ap.add_argument("--body", type=float, default=22.0, help="body size in reference px")
    ap.add_argument("--leading", type=float, default=1.3, help="leading factor (1.2–1.4)")
    ap.add_argument("--advance", type=float, default=0.50,
                    help="mean character advance of the body face, in em")
    ap.add_argument("--fields", type=int, default=8, help="8 | 12 | 20 | 32 | ...")
    ap.add_argument("--target-chars", type=int, default=32,
                    help="target characters per body line (32 slide, 20 caption)")
    ap.add_argument("--from", dest="from_file", default=None,
                    help="json with {faces, colours, leading_factor, advance} to ingest")
    ap.add_argument("--name", default="walk-on-a-slide-side", help="Marp theme name")
    ap.add_argument("--out", default="system", help="output directory")
    args = ap.parse_args(argv)

    faces = {"display": "Inter, system-ui, sans-serif",
             "body": "Inter, system-ui, sans-serif"}
    colours = dict(DEFAULT_COLOURS)
    leading, advance = args.leading, args.advance

    if args.from_file:
        ingested = json.loads(Path(args.from_file).read_text())
        faces.update(ingested.get("faces", {}))
        colours.update(ingested.get("colours", {}))
        leading = ingested.get("leading_factor", leading)
        advance = ingested.get("advance", advance)

    canvas = parse_canvas(args.canvas)
    tokens = build(canvas, args.body, leading, advance, args.fields,
                   args.target_chars, faces, colours)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "tokens.json").write_text(json.dumps(tokens, indent=2) + "\n")
    (out / "theme.css").write_text(theme_css(tokens, args.name))

    print(f"canvas      {canvas[0]}x{canvas[1]}")
    print(f"margins     L{tokens['margins']['left']} T{tokens['margins']['top']} "
          f"R{tokens['margins']['right']} B{tokens['margins']['bottom']}")
    print(f"type area   {tokens['type_area']['w']}x{tokens['type_area']['h']}  "
          f"({tokens['type_area']['units']} baselines of {tokens['baseline']}px)")
    print(f"columns     {tokens['columns']['count']} x {tokens['columns']['width']}px  "
          f"gutter {tokens['columns']['gutter']}px")
    print(f"fields      {tokens['fields']['cols']}x{tokens['fields']['rows']}  "
          f"{tokens['fields']['width']}x{tokens['fields']['height']}px")
    print(f"type scale  {tokens['type_scale']}")
    for note in tokens["notes"]:
        print(f"note        {note}")
    print(f"written     {out/'tokens.json'}, {out/'theme.css'}")


if __name__ == "__main__":
    main(sys.argv[1:])
