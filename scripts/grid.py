#!/usr/bin/env python3
"""
grid.py — construct a slide design system by Müller-Brockmann's method.

It does not choose values by eye. Given a canvas, a body size, a leading
factor, a mean character advance and a field count, it derives the margin
zone, the type area, the baseline unit, the columns, the gutter, the field
arrangement, a taller title band, the wide/narrow column split, the type
scale, the colour roles and a set of named layout regions, then writes:

    <out>/tokens.json   the numbers and the layout regions
    <out>/theme.css     a Marp theme bound to those numbers

The accent has one job: it marks the grid (rules, registration crosses,
the knockout chip, section numerals). No rounded corners are emitted.
See references/muller-brockmann.md for why each step is what it is.

Usage:
    python3 grid.py --canvas 16:9 --body 22 --fields 8 --advance 0.5 --out system/
    python3 grid.py --from system-in.json --canvas 16:9 --fields 20 --out system/
"""

import argparse
import json
import math
import sys
from pathlib import Path

CANVASES = {
    "16:9": (1280, 720),
    "16:10": (1280, 800),
    "4:3": (1024, 768),
}

# Field-count -> (columns, rows), from the book's worked schemes.
# 18 is the "two wide, one narrow" scheme; any count not here falls back
# to the factor pair closest to the canvas aspect.
FIELD_ARRANGEMENTS = {
    8: (4, 2), 12: (4, 3), 16: (4, 4), 18: (3, 6),
    20: (4, 5), 21: (3, 7), 32: (4, 8), 36: (6, 6),
}

# Margin zone as fractions of the canvas SHORT side, ordered
# left < top < right < bottom so the type area sits slightly high and left.
DEFAULT_MARGINS = {"left": 0.055, "top": 0.075, "right": 0.075, "bottom": 0.110}

TYPE_SCALE = {"title": 2.9, "headline": 1.65, "body": 1.0, "caption": 0.7}

DEFAULT_COLOURS = {
    "ink": "#141413",
    "ground": "#F4F4F2",
    "accent": "#2F6364",   # transformative teal; marks the grid only
    "muted": "#8A8A86",
}


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def parse_canvas(value):
    if value in CANVASES:
        return CANVASES[value]
    if "x" in value.lower():
        w, h = value.lower().split("x")
        return int(w), int(h)
    if ":" in value:
        a, b = (float(x) for x in value.split(":"))
        return (round(720 * a / b), 720) if a >= b else (720, round(720 * b / a))
    raise ValueError(f"unrecognised canvas: {value}")


def field_arrangement(fields, aspect):
    if fields in FIELD_ARRANGEMENTS:
        return FIELD_ARRANGEMENTS[fields]
    best = None
    for cols in range(1, fields + 1):
        if fields % cols:
            continue
        rows = fields // cols
        err = abs((cols / rows) - aspect)
        if best is None or err < best[0]:
            best = (err, cols, rows)
    return best[1], best[2]


def build(canvas, body, leading, advance, fields, target_chars, faces, colours):
    page_w, page_h = canvas
    short = min(page_w, page_h)
    aspect = page_w / page_h

    m = {k: round(v * short) for k, v in DEFAULT_MARGINS.items()}
    area_x, area_y = m["left"], m["top"]
    area_w = page_w - m["left"] - m["right"]
    area_h_raw = page_h - m["top"] - m["bottom"]

    baseline = round(body * leading)
    area_units = area_h_raw // baseline
    area_h = area_units * baseline

    columns = max(1, math.floor(area_w / (target_chars * advance * body)))
    gutter = baseline
    col_w = (area_w - (columns - 1) * gutter) / columns

    f_cols, f_rows = field_arrangement(fields, aspect)
    field_w = (area_w - (f_cols - 1) * gutter) / f_cols

    # Title band: the top rows run taller so long headlines have room in
    # the same place on every slide (21-field annual-report scheme).
    band_units = 4
    grid_units = area_units - band_units - 1          # one blank row below the band
    field_rows_units = max(1, math.floor((grid_units - (f_rows - 1)) / f_rows))
    field_h = field_rows_units * baseline

    band = {"x": area_x, "y": area_y, "w": area_w, "h": band_units * baseline}
    grid_top = area_y + band["h"] + baseline

    # Wide/narrow split: the rightmost field column is the narrow margin
    # column for source, date and label; the rest is the wide reading area.
    narrow_w = field_w
    wide_w = area_w - narrow_w - gutter
    regions = {
        "band": band,
        "grid": {"x": area_x, "y": grid_top, "w": area_w,
                 "h": area_y + area_h - grid_top},
        "wide": {"x": area_x, "w": round(wide_w, 2)},
        "narrow": {"x": round(area_x + wide_w + gutter, 2), "w": round(narrow_w, 2)},
        "field_origin": {"x": area_x, "y": grid_top},
        "field_step": {"x": round(field_w + gutter, 2), "y": field_h + baseline},
    }

    scale = {k: round(body * r) for k, r in TYPE_SCALE.items()}

    tokens = {
        "canvas": {"w": page_w, "h": page_h, "aspect": round(aspect, 4)},
        "margins": m,
        "type_area": {"x": area_x, "y": area_y, "w": area_w, "h": area_h,
                      "units": area_units},
        "baseline": baseline,
        "leading_factor": leading,
        "columns": {"count": columns, "width": round(col_w, 2), "gutter": gutter},
        "fields": {"count": f_cols * f_rows, "cols": f_cols, "rows": f_rows,
                   "width": round(field_w, 2), "height": field_h,
                   "rows_in_baselines": field_rows_units},
        "regions": regions,
        "layouts": ["title", "close", "section", "statement",
                    "wide-narrow", "field-grid", "caption-band"],
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
            f"set body/target_chars/fields so they agree, or put body text on "
            f"{columns} columns and images on {f_cols} fields.")
    return tokens


def theme_css(t, name):
    c, m, s = t["colours"], t["margins"], t["type_scale"]
    cv, base = t["canvas"], t["baseline"]
    r = t["regions"]
    ar, ag, ab = hexrgb(c["accent"])
    field_w = t["fields"]["width"]
    step_x = r["field_step"]["x"]
    step_y = r["field_step"]["y"]
    grid_w = round(t["columns"]["width"] * t["columns"]["count"]
                   + t["columns"]["gutter"] * (t["columns"]["count"] - 1))
    return f"""/* @theme {name}
   Generated by grid.py from tokens.json. Do not edit by hand; change the
   grid.py flags and re-run. Every value here is derived, not chosen.
   The accent marks the grid only. No rounded corners. */

section {{
  width: {cv['w']}px; height: {cv['h']}px;
  padding: {m['top']}px {m['right']}px {m['bottom']}px {m['left']}px;
  background: {c['ground']}; color: {c['ink']};
  font-family: {t['faces'].get('body', 'Inter, system-ui, sans-serif')};
  font-size: {s['body']}px; line-height: {base}px; letter-spacing: 0;
}}
* {{ border-radius: 0 !important; }}

/* eyebrow: uppercase, tracked, an accent rule above it */
.eyebrow {{
  font-size: {s['caption']}px; font-weight: 600;
  letter-spacing: .12em; text-transform: uppercase;
  border-top: 2px solid {c['accent']}; padding-top: 6px; display: inline-block;
}}

/* title band: headline zone across the top, ruled off below */
h1 {{
  font-family: {t['faces'].get('display', 'inherit')};
  font-size: {s['title']}px; line-height: {round(base * 1.9)}px;
  font-weight: 700; margin: 0;
}}
h2 {{
  font-family: {t['faces'].get('display', 'inherit')};
  font-size: {s['headline']}px; line-height: {round(base * 1.35)}px;
  font-weight: 600; margin: 0;
  max-width: {grid_w}px;
  border-bottom: 1px solid {c['accent']}; padding-bottom: {base}px;
}}
p, ul, ol {{ margin: {base}px 0 0 0; }}
li {{ margin: 0 0 {base}px 0; list-style: none; }}
li::before {{ content: ""; display: inline-block; width: 18px;
  border-top: 1px solid {c['accent']}; vertical-align: middle;
  margin-right: 12px; }}

.source, .caption, footer {{
  font-size: {s['caption']}px; color: {c['muted']}; line-height: {base}px;
}}

/* section divider: knockout on the ink ground, oversized numeral */
section.title, section.section, section.close {{
  background: {c['ink']}; color: {c['ground']};
}}
section.section .numeral {{
  font-size: {round(s['title'] * 6)}px; line-height: 1;
  color: rgba({ar},{ag},{ab},.55); position: absolute; right: 0; bottom: -6%;
  font-weight: 300;
}}

/* the one accent chip: a solid rectangle, ground-colour text knocked out */
.chip {{ background: {c['accent']}; color: {c['ground']};
  padding: 0 .22em; box-decoration-break: clone; }}

/* wide / narrow content split (18-field scheme) */
section.wide-narrow .wide {{ width: {r['wide']['w']}px; float: left; }}
section.wide-narrow .narrow {{ width: {r['narrow']['w']}px; float: right;
  border-left: 1px solid {c['accent']}; padding-left: 16px; }}

/* field grid: boundaries as accent hairlines, crosses at the corners */
section.field-grid .cells, section.grid-overlay {{
  background-image:
    repeating-linear-gradient(to right,
      {c['accent']} 0 1px, transparent 1px {round(step_x)}px),
    repeating-linear-gradient(to bottom,
      {c['accent']} 0 1px, transparent 1px {round(step_y)}px);
  background-position: {r['field_origin']['x']}px {r['field_origin']['y']}px;
  background-size: {round(field_w + (step_x - field_w))}px 100%, 100% {round(r['grid']['h'])}px;
  background-repeat: no-repeat;
  opacity: .5;
}}
"""


def main(argv):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--canvas", default="16:9", help="16:9 | 4:3 | 1280x720")
    ap.add_argument("--body", type=float, default=22.0, help="body size, reference px")
    ap.add_argument("--leading", type=float, default=1.3, help="leading factor 1.2-1.4")
    ap.add_argument("--advance", type=float, default=0.5,
                    help="mean character advance of the body face, in em")
    ap.add_argument("--fields", type=int, default=8, help="8 | 16 | 18 | 20 | 32 ...")
    ap.add_argument("--target-chars", type=int, default=32,
                    help="target characters per body line (32 slide, 20 caption)")
    ap.add_argument("--accent", default=DEFAULT_COLOURS["accent"],
                    help="accent hex; marks the grid only (default transformative teal)")
    ap.add_argument("--from", dest="from_file", default=None,
                    help="json with {faces, colours, leading_factor, advance}")
    ap.add_argument("--name", default="walk-on-a-slide-side", help="Marp theme name")
    ap.add_argument("--out", default="system", help="output directory")
    args = ap.parse_args(argv)

    faces = {"display": "Inter, system-ui, sans-serif",
             "body": "Inter, system-ui, sans-serif"}
    colours = dict(DEFAULT_COLOURS)
    colours["accent"] = args.accent
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
    print(f"title band  {tokens['regions']['band']['w']}x{tokens['regions']['band']['h']}")
    print(f"columns     {tokens['columns']['count']} x {tokens['columns']['width']}px  "
          f"gutter {tokens['columns']['gutter']}px")
    print(f"fields      {tokens['fields']['cols']}x{tokens['fields']['rows']}  "
          f"{tokens['fields']['width']}x{tokens['fields']['height']}px")
    print(f"wide/narrow {tokens['regions']['wide']['w']}px / {tokens['regions']['narrow']['w']}px")
    print(f"accent      {tokens['colours']['accent']}")
    for note in tokens["notes"]:
        print(f"note        {note}")
    print(f"written     {out/'tokens.json'}, {out/'theme.css'}")


if __name__ == "__main__":
    main(sys.argv[1:])
