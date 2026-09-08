# The construction method

Everything the design system uses comes from Josef Müller-Brockmann,
*Grid Systems in Graphic Design / Raster Systeme für die visuelle
Gestaltung* (Niggli). This file is the working extract. If a spacing or
type value cannot be derived from what is here, it does not enter the
system.

The grid is an ordering system. It expresses “a certain mental attitude”:
the will to systematise, to reduce, to make the argument legible. A deck
built on it should read as one object, page to page.

## Order of construction

The book is explicit that the grid is **conceived afresh for every job**,
in this order. Do not reorder it.

1. **Know the volume first.** How much text, how many images, of what
   kind. The grid answers the content, so it cannot be picked before the
   content is known. (This is why Stage 3 runs after the spine.)
2. **Type face, size, leading.** One family for both body and display.
   “Under no circumstances mix characters of the same style”, and there is
   no separate face for headings. Leading (`Zeilendurchschuss`) sets the
   baseline grid: every vertical measure from here on is a whole number of
   leading units.
3. **Column width from type size.** A reading line wants about 7 words,
   roughly 50–60 characters. Display and captions run shorter. Column
   width is derived from this figure.
4. **Type area (`Satzspiegel`) inside a margin zone.** Margins are
   proportioned. Equal margins are avoided; they “can never result in an
   interesting page; they always create an impression of indecision”.
5. **Divide the type area into grid fields (`Rasterfelder`).** 8, 20, 32
   are the worked examples; 18 and 36 also shown; any N×M is legal. Each
   field is a whole number of text lines deep and one column wide.
   Between two fields there is **exactly one blank leading line**, which
   also carries captions.
6. **Place elements on the fields.** Text columns, images and titles snap
   to field boundaries. An image top edge sits on a line’s cap-height,
   its bottom edge on a baseline.

## Margin proportions

The type area is “invariably surrounded by a marginal zone”. The book
avoids equal and near-equal margins and asks for “the maximum tension in
the proportions”.

- Classic book proportion shown: type area to page area ≈ **1 : 2**.
- Golden-section page, with a margin progression where **back (inner) <
  top < fore (outer) < tail (bottom)**. The worked “well-proportioned”
  figure runs roughly `1 : 1.5 : 2 : 2.5` on inner / top / outer / tail.
- A screen deck has no spine, so read “inner” as *left*. Keep the
  progression: left smallest, bottom largest, so the type area sits
  slightly high and left of centre and does not look like it is “falling
  out of the page”.

`grid.py` default for a 16:9 canvas sets margins as fractions of the short
side: left `0.075`, top `0.11`, right `0.085`, bottom `0.10`. These are
generous, museum-guide margins. They hold the progression and leave a
type area close to 1 : 2 of the frame.
Override per project and keep the ordering.

## The three formulas

```
baseline = round(body_size × leading_factor)     # vertical grid unit
gutter   = 1 × baseline                           # one blank leading line
columns  = floor(type_area_width /
                 (target_chars × mean_advance × body_size))
```

- `leading_factor`: 1.2 to 1.4 for a screen deck read at distance. The
  book’s own examples run tighter for print (10 pt on 2–4 pt lead); a
  projected slide wants the looser end. Default 1.3.
- `target_chars`: 32 for slide body (short lines, ragged right); 45–55
  only if a slide genuinely carries a paragraph; captions 20.
- `mean_advance`: measured from a mixed-case sample of the chosen face, in
  em. Geist Pixel ≈ 0.489. A generic grotesk ≈ 0.50. Pass it with
  `--advance` when the face is known.

## Vertical composition

The type-area depth is a whole number of baseline units. Divide it into
fields the way the book divides 53 lines:

```
N fields of M lines  +  (N − 1) blank lines  =  total lines
```

Worked splits from the book for 53 lines: 9×5+8, 6×8+5. For 59 lines it
lists 12×4, 10×5, 6×9, 5×11, 4×14, each with one blank line between. Pick
N from content density (below). The blank line between fields is always a
whole line. A half line drifts the field heights out of register.

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

“A comparatively small number of grid fields is usually all that is
needed.” Field count tracks how much the deck has to hold. Deck length
does not affect it.

| Fields | Arrangement (screen) | For |
|---|---|---|
| 8 | 4 cols × 2 rows | most decks: one idea per slide, lots of white |
| 12 | 3 cols × 4 rows, or 4 × 3 | decks with recurring two- and three-part slides |
| 20 | 4 cols × 5 rows | data-dense decks, comparison tables, dashboards |
| 32 | 4 cols × 8 rows | technical / reference decks, appendices |

An 8-field grid also subdivides cleanly into 16 (halve each field
vertically) for captions and small figures, with no second grid.

## Field schemes from the practical examples

The book’s practical chapter (pp. 104–131) shows the schemes to build
slide layouts from. These are the ones worth carrying:

- **Title band (21-field, IBM Annual Report).** The top field row is set
  taller than the rest so long titles have room at the head of every page,
  in the same place every time. On a slide this is the headline zone: one
  band across the top, ruled off below, the field grid underneath.
- **Wide and narrow columns (18-field, Kunsttopographie).** Three columns,
  two wide and one narrow. The running text goes in the wide columns; the
  notes, captions and references go in the narrow one, aligned to the same
  baseline. On a slide: body or list in the wide columns, a narrow right
  column for the source, the date, the label.
- **Caption strip (Louis Soutter, New Swiss Film).** Text in two columns,
  captions in four. A block sits on the field grid and a finer caption
  strip is ruled off below it, at a fixed relationship to the block.
- **Solid colour block, Farbfläche (photo/tint chapter, pp. 98–103).** A
  solid accent rectangle occupying whole grid fields, with the type
  knocked out of it or aligned to its edge. On a slide it carries the one
  key point of a content grid: a short label and a short value in the
  ground colour. Keep the text short; a long passage reversed out of pure
  red is hard to read.
- **The centred display phrase (musica viva poster, p. 111).** One phrase
  set large, its words positioned to make a rhythm, centred in the field.
  Small supporting text aligns to it. “A severe but elegant architecture.”
  This is the model for a section title and for a single-claim slide: the
  phrase sits on the optical centre, not at the top.
- **Negative on a solid ground (Rosenthal).** All text knocked out of a
  dark ground. It works only when the text is short and the leading is
  generous. Use it for section dividers, not for reading.

## Consistency (corporate-identity spec, pp. 133–134)

The kit is applied identically on every slide of its kind:

- titles the same size, in the same position, in the same face;
- subtitles the same size, the same distance from the text around them;
- captions the same size, the same relationship to the block they label;
- the same grid on every slide;
- marginal notes always in the narrow column, on the baseline;
- illustrations in whole-field sizes;
- the same colour for the same kind of content;
- the same leading throughout for a given size;
- one or two whole blank lines to divide text, never a half line.

## Images in the grid

- Every image is 1, 2, 3, 4 or more whole fields. “The fewer the
  differences in the size of the illustrations, the quieter the
  impression.”
- Image top edge aligns to the cap-line of a text line; bottom edge to a
  baseline. Captions sit in the blank line below, set on the field width.
- Full-bleed is allowed as a deliberate “monumental” move. Keep it for
  section dividers and the title. Content slides stay inside the grid.
- Müller-Brockmann marks the picture grid itself in coloured rules. In a
  constructed system the accent has that one job: the full-height left
  bar, field hairlines, the Farbfläche block and the section numeral. It
  is never a body-text colour.

## Type scale

One family. The contrast is extreme by design: the display type dominates
the slide and everything else is one small size. “The 9-point face is
immediately distinguishable from the 6-point face”. Push that gap as far
as it goes. There are no mid-sizes.

| Role | Size (relative to body = 1) | Weight | Placement |
|---|---|---|---|
| Deck title / section divider | 5 | bold | centred vertically |
| Single-claim phrase | 3 | bold | centred vertically |
| Content headline | 3.3 | semibold | top-left, in the title band |
| Oversized ghost label | 2.5 | semibold, ~16 % opacity | above its block, one size everywhere |
| Supporting text, list, source, caption, footer, page number | 1 | light / regular | below the headline, or at the foot |

The heading element is a full-height accent bar at the left edge of every
slide, one weight everywhere. A category label is set as an oversized ghost
that always reads lighter than the headline. A small caps tag is never
used. The supporting text is never set beside the headline and never
in a second size. Leave ample white space between them.

## Colour

- Historically headings were printed in a second colour. In single-colour
  work the book uses **type contrast** (size, weight) for emphasis
  instead.
- A constructed system has one ink, one ground, one accent. The default
  accent is pure red `#FF0000`. A supplied design system’s own accent
  replaces it. There is no second accent.
- The accent marks the grid: the full-height left bar, field hairlines,
  the Farbfläche block and the section numeral. On a dark ground, small
  accent text loses contrast, so keep the accent for rules and large
  blocks and set small text in ink or knocked out of the ground.
- No label chips, no eyebrow rules, no underline under a headline, no
  registration crosses, no highlighter behind a word. Emphasis is size,
  weight and the Farbfläche block.

## Page numbers

- A centred number reads static and restful; an outer-edge number reads
  dynamic. A deck usually wants it quiet: bottom, aligned to the outer
  margin or the type-area edge.
- Distance from the type area is one gutter (one blank baseline) or the
  column gap. No other value.

## What this buys the deck

The book’s claim, kept because it is the point: information set on a clear
grid “will not only be read more quickly and easily but the information
will also be better understood and retained”. The grid is a comprehension
tool, and every rule above serves that.
