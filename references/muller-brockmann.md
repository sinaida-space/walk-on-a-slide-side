# The construction method

Everything the design system uses comes from Josef Müller-Brockmann,
*Grid Systems in Graphic Design / Raster Systeme für die visuelle
Gestaltung* (Niggli). This file is the working extract. If a spacing or
type value cannot be derived from what is here, it does not enter the
system.

The grid is not decoration. It is "the expression of a certain mental
attitude" — the will to systematise, to reduce, to make the argument
legible. A deck built on it should read as one object, page to page.

## Order of construction

The book is explicit that the grid is **conceived afresh for every job**,
in this order. Do not reorder it.

1. **Know the volume first.** How much text, how many images, of what
   kind. The grid answers the content; it cannot be picked before the
   content is known. (This is why Stage 3 runs after the spine.)
2. **Type face, size, leading.** One family for everything — body and
   display. "Under no circumstances mix characters of the same style" —
   no second face for headings. Leading (`Zeilendurchschuss`) sets the
   baseline grid: every vertical measure from here on is a whole number
   of leading units.
3. **Column width from type size.** A reading line wants about 7 words,
   roughly 50–60 characters. Display and captions run shorter. Column
   width is derived from this, not chosen.
4. **Type area (`Satzspiegel`) inside a margin zone.** Margins are
   proportioned, never equal. Equal margins "can never result in an
   interesting page; they always create an impression of indecision".
5. **Divide the type area into grid fields (`Rasterfelder`).** 8, 20, 32
   are the worked examples; 18 and 36 also shown; any N×M is legal. Each
   field is a whole number of text lines deep and one column wide.
   Between two fields there is **exactly one blank leading line**, which
   also carries captions.
6. **Place elements on the fields.** Text columns, images, titles all
   snap to field boundaries. Image top edge sits on a line's cap-height,
   image bottom edge on a baseline.

## Margin proportions

The type area is "invariably surrounded by a marginal zone". The book
rejects equal and near-equal margins and asks for "the maximum tension in
the proportions".

- Classic book proportion shown: type area to page area ≈ **1 : 2**.
- Golden-section page and a margin progression where **back (inner) <
  top < fore (outer) < tail (bottom)** — the worked "well-proportioned"
  figure runs roughly `1 : 1.5 : 2 : 2.5` on inner / top / outer / tail.
- For a screen deck there is no spine, so read "inner" as *left*. Keep
  the progression: left smallest, bottom largest, so the type area sits
  slightly high and left of centre and does not look like it is "falling
  out of the page".

`grid.py` default for a 16:9 canvas: margins as fractions of the short
side — left `0.055`, top `0.075`, right `0.075`, bottom `0.11` — which
holds the progression and leaves a type area close to 1 : 2 of the frame.
Override per project; keep the ordering.

## The three formulas

```
baseline = round(body_size × leading_factor)     # vertical grid unit
gutter   = 1 × baseline                           # one blank leading line
columns  = floor(type_area_width /
                 (target_chars × mean_advance × body_size))
```

- `leading_factor` — 1.2 to 1.4 for a screen deck read at distance. The
  book's own examples run tighter for print (10 pt on 2–4 pt lead); a
  projected slide wants the looser end. Default 1.3.
- `target_chars` — 32 for slide body (short lines, ragged right), 45–55
  only if a slide genuinely carries a paragraph. Captions 20.
- `mean_advance` — measured from a mixed-case sample of the chosen face,
  in em. Geist Pixel ≈ 0.489. A generic grotesk ≈ 0.50. Pass it with
  `--advance` when the face is known.

## Vertical composition

The type area depth is a whole number of baseline units. Divide it into
fields the way the book divides 53 lines:

```
N fields of M lines  +  (N − 1) blank lines  =  total lines
```

Worked splits from the book for 53 lines: 9×5+8, 6×8+5. For 59 lines it
lists 12×4, 10×5, 6×9, 5×11, 4×14, each with one blank line between. Pick
N from content density (below). The blank line between fields is never
half a line — always whole — or the field heights drift out of register.

Within a field:

```
field top (on a baseline)
  headline cap-line     display size, one or two lines, same family
  1 blank baseline
  body cap-line
  body rows at 1 baseline each
field bottom (on a baseline)
```

## How many fields

"A comparatively small number of grid fields is usually all that is
needed." Field count tracks how much the deck has to hold, not how big
the deck is.

| Fields | Arrangement (screen) | For |
|---|---|---|
| 8 | 4 cols × 2 rows | most decks: one idea per slide, lots of white |
| 12 | 3 cols × 4 rows, or 4 × 3 | decks with recurring two- and three-part slides |
| 20 | 4 cols × 5 rows | data-dense decks, comparison tables, dashboards |
| 32 | 4 cols × 8 rows | technical / reference decks, appendices |

An 8-field grid also subdivides cleanly into 16 (halve each field
vertically) for captions and small figures without a second grid.

## Images in the grid

- Every image is 1, 2, 3, 4 or more whole fields. "The fewer the
  differences in the size of the illustrations, the quieter the
  impression."
- Image top edge aligns to the cap-line of a text line; bottom edge to a
  baseline. Captions sit in the blank line below, set on the field width.
- Full-bleed is allowed but is a deliberate "monumental" move — use it
  for section dividers and the title, not for content slides.
- Müller-Brockmann marks the picture grid itself in **red rules**. That
  is the origin of the red-rule language in `sinaida-grid-style`; when
  constructing bespoke, red is the grid-marking colour, not a body colour.

## Type scale

One family. Sizes must be unmistakably different — "the 9-point face is
immediately distinguishable from the 6-point face". Do not put two sizes
one step apart on the same slide.

| Role | Size (relative to body = 1) | Weight |
|---|---|---|
| Deck title / section divider | 2.6–3.2 | bold |
| Slide assertion headline | 1.5–1.8 | semibold or bold |
| Body | 1 | regular |
| Caption, source, footer, page number | 0.7 | regular |

Weight steps carry grey value: regular = light grey mass, semibold =
medium, bold = dark. Pick steps that are clearly separated; do not use
semibold where the eye expects either regular or bold.

## Colour

- Historically headings were printed in red; in single-colour work the
  book says use **type contrast** (size, weight) for emphasis instead.
- A constructed system: one ink, one ground, one accent. The accent is
  the grid-marking red unless the ingested design system says otherwise.
  No second accent.
- On a dark ground, lift small text off pure values — a hairline red on
  black fails contrast below ~14 pt; use a legible red at body size and
  reserve pure red for rules and large display.

## Page numbers

- Centred = static and restful; outer-edge = dynamic. A deck usually
  wants the number quiet: bottom, aligned to the outer margin or the
  type-area edge.
- Distance from the type area = one gutter (one blank baseline) or the
  column gap, never an arbitrary value.

## What this buys the deck

The book's claim, kept because it is the point: information set on a clear
grid "will not only be read more quickly and easily but the information
will also be better understood and retained". The grid is a
comprehension tool. Every rule above serves that, not the look.
