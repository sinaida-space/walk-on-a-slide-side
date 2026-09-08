# Stage 3. Design system

Goal: a grid, a type scale, a colour set and a small set of named layouts,
all derived by Müller-Brockmann’s maths (`muller-brockmann.md`), emitted
as `system/tokens.json` and `system/theme.css`.

## First question, always

**Is there a design system to work inside?** Ask before constructing
anything.

### Path A. The user supplies a design system

A tokens file, a brand spec, or an existing deck to match. Take from it:

- the type faces (one family for display and body; a real fallback stack;
  a face that covers every script the deck uses);
- one accent colour and the grey steps;
- the baseline unit and the ground colours.

Do **not** add a second accent, a second body face, or a spacing value
off the unit. Then run the grid maths below to derive columns, fields and
the type area for the deck canvas. The supplied system provides the
*materials*; Müller-Brockmann provides the *structure*.

```bash
python3 scripts/grid.py --from system-in.json --canvas 16:9 --fields 8 --out system/
```

where `system-in.json` carries `{ "faces": {...}, "colours": {...},
"leading_factor": 1.3, "advance": 0.5 }`.

### Path B. No design system (public, client, or first deck)

Construct one from `muller-brockmann.md`. This is the default for anything
shared publicly. Choose:

- **canvas.** `16:9` (1280×720 reference px) unless the venue dictates
  `4:3` or a specific projector size.
- **body size.** 20–24 px reference for a room; 18 only for a deck read on
  screens.
- **faces.** One grotesk family for everything. Name a real fallback
  stack. The family must cover every script the deck uses.
- **accent.** Pure red `#FF0000` by default. It marks the grid: the short
  rule by the headline, field rules, registration crosses, the section
  numerals, the progress rail. It is never a body-text colour, and there
  is only one accent.
- **type contrast.** The headline is huge (3× body or more); every other
  piece of text is one small size (~15 px). No mid-sizes, no label chips,
  no eyebrow. “The 9-point face is immediately distinguishable from the
  6-point face”. Make that gap unmistakable.
- **placement.** The headline sits top-left in the title band. The
  supporting text goes low (anchored to the bottom margin) or in the
  right column, never beside the headline. Leave ample white space
  between the two.
- **field count.** From content density, per the table in
  `muller-brockmann.md`: 8 for most decks, 16 or 20 for data-dense, 32
  for reference.

```bash
python3 scripts/grid.py --canvas 16:9 --body 16 --fields 8 \
  --advance 0.5 --leading 1.3 --accent "#FF0000" --out system/
```

## What grid.py derives

`grid.py` does not guess. From canvas, margins, body, leading and fields
it computes, as the book does:

1. margin zone (proportioned, left < top < right < bottom);
2. type area (≈ 1 : 2 of the frame);
3. baseline unit = `round(body × leading)`, and the type-area depth
   snapped to a whole number of units;
4. columns = `floor(area_width / (target_chars × advance × body))`;
5. gutter = one baseline;
6. field arrangement N×M with one blank baseline between rows;
7. a **title band**: the top rows set taller than the rest, sized from the
   headline’s own leading, so the big headline has room in the same place
   on every slide (Müller-Brockmann’s 21-field annual-report scheme);
8. type scale (title, headline, body, caption) as ratios of body, with an
   extreme headline-to-body jump;
9. colour roles (ink, ground, accent, muted).

## The layouts

Every layout puts the huge headline top-left in the title band and the
small supporting text low or right. The structure is drawn with accent
hairlines and registration crosses. Vary which layout a slide uses so the
deck is not one shape repeated. See `muller-brockmann.md` for the field
schemes these come from.

| Layout | Structure | For |
|---|---|---|
| `title` / `close` | ink ground, huge headline lower-left, a short accent rule, a tiny meta row | first and last slides |
| `section` | ink ground, huge title top-left, an oversized accent numeral bleeding off the lower-right, a five-segment progress rail | dividers |
| `statement` | one big sentence in the band, a short accent rule, then open space; a tiny source note on the bottom margin; a sparse row of registration crosses | a single claim |
| `right-column` | huge headline in the band; a short list in the right column, one small size, each item on an accent tick, an accent rule down the column’s left edge | supporting points behind a claim |
| `bottom-block` | huge headline in the band; three or four short lines anchored to the bottom margin under a short accent rule; open space between | before/after, resources, a short set of facts |
| `field-grid` | huge headline in the band; a ruled two-by-two (or one-by-n) grid below, accent hairlines, registration crosses at the corners, a tiny label and a small value per cell | scope, spec, comparison |

`role` from the spine maps to a layout: `title`→`title`, `section`→`section`,
`claim`/`context`→`statement`, `evidence`→`right-column` or `bottom-block`,
`data`→`field-grid`, `objection`→`bottom-block`, `cta`→`statement` or
`close`.

`grid.py` writes the regions into `tokens.json` and a class per layout
into `theme.css` (`section.section`, `section.wide-narrow`,
`section.headline-bottom`, and so on), plus a grid overlay you can toggle
with a class while checking alignment. No rounded corners, no circles; the
accent shows only as rules, crosses and the section numerals.

## Check the system before Stage 4

- Render one test slide per layout, each with the longest headline and a
  full body block. The headline must sit inside the title band; the body
  must sit inside the type area with the bottom margin intact.
- Turn on the grid overlay. Every text baseline sits on a grid line, the
  field rules land on field boundaries, and any images span whole fields.
- If the test slide overflows, the fix is fewer words (back to Stage 2)
  or a larger field count. Shrinking the type by hand is not an option.

## Output

`system/tokens.json` and `system/theme.css`. These are inputs to Stage 4.
They are not edited by hand afterward; change the flags and re-run.
