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
- **accent.** Transformative teal `#2F6364` by default. It marks the grid:
  field rules, the title-band rule, registration crosses, the knockout
  chip, section numerals. It is never a body-text colour, and there is
  only one accent.
- **field count.** From content density, per the table in
  `muller-brockmann.md`: 8 for most decks, 16 or 20 for data-dense, 32
  for reference.

```bash
python3 scripts/grid.py --canvas 16:9 --body 22 --fields 8 \
  --advance 0.5 --leading 1.3 --accent "#2F6364" --out system/
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
7. a **title band**: the top field row set taller than the rest, so long
   headlines have room (Müller-Brockmann’s 21-field annual-report scheme);
8. type scale (title, headline, body, caption) as ratios of body;
9. colour roles (ink, ground, accent, muted).

## The layouts

Every layout is a fixed allocation of whole fields, applied identically on
every slide of its kind. The boundaries are drawn as accent hairlines so
the structure is visible. See `muller-brockmann.md` for the field schemes
these come from.

| Layout | Field allocation | For |
|---|---|---|
| `title` / `close` | full bleed, ink ground, headline on the lower third, a rule, a meta row | first and last slides |
| `section` | ink or teal ground, short knockout title top-left, oversized section numeral bleeding off an edge, a progress rail | dividers |
| `statement` | title band holds one sentence; the field grid below stays empty | a single claim, one keyword in the knockout chip |
| `wide-narrow` | body or list in the wide columns (fields 1..n−1), a narrow right column for the source, the date, the label | most content slides (the 18-field 2-wide-1-narrow scheme) |
| `field-grid` | content mapped to whole fields, every boundary ruled, registration crosses at the corners | comparisons, two- and three-part slides |
| `caption-band` | a block on the field grid, a four-column caption strip ruled off below it | a figure, a diagram, a data block |

`role` from the spine maps to a layout: `title`→`title`,
`section`→`section`, `claim`/`context`→`statement` or `wide-narrow`,
`evidence`/`data`→`field-grid` or `caption-band`, `objection`→`wide-narrow`,
`cta`→`close`.

`grid.py` writes the regions for each layout into `tokens.json` and a
class per layout into `theme.css` (`section.title`, `section.wide-narrow`,
and so on), plus a grid overlay you can toggle with a class while checking
alignment. No rounded corners anywhere; the accent shows only as rules,
crosses and the solid knockout chip.

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
