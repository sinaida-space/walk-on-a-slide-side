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
- **accent.** Pure red `#FF0000` by default. It marks the grid: the
  full-height left bar, field hairlines and the section numeral. It is
  never a body-text colour, and there is only one accent.
- **heading element.** A full-height accent bar at the left edge of every
  slide, one weight everywhere (~8 px). Never an underline, never an
  eyebrow.
- **type contrast.** The display type is huge (3× body or more). Every
  other piece of text is one small size (~15 px). A number label is set
  as an **oversized ghost** that echoes the section numeral: one fixed
  size across the whole deck (never scaled to fit a word), semi-
  transparent, sitting at the top-right of the box and straddling its top edge,
  with no rule ever running through it. It reads as a layer under the content, never as a small caps
  tag. No mid-sizes, no label chips. “The 9-point face is immediately
  distinguishable from the 6-point face”. Make that gap unmistakable, and
  keep the headline heavier than the ghost.
- **placement.** A section title, a single claim, and the title and close
  are set large and **centred vertically** in the frame (the “musica
  viva” principle). A content headline sits top-left in the title band and
  its supporting text goes below it, with ample white space between.
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

The deck reads like an art-museum booklet: big display type against one
small text size, generous white, strict alignment, one accent. Vary which
layout a slide uses so the deck is not one shape repeated. See
`muller-brockmann.md` for the field schemes these come from.

| Layout | Structure | For |
|---|---|---|
| `title` / `close` | ink ground, huge phrase centred vertically, the left bar, a tiny meta row at the foot | first and last slides |
| `section` | ink ground, huge title centred vertically, the left bar, an oversized accent numeral bleeding off the lower-right; nothing else | dividers |
| `statement` | the single accent phrase, set large and centred vertically, the left bar; a tiny source note under it; ample white above and below | a single claim |
| `index` / `modules` | huge headline in the band; below, a horizontal row of equal outlined boxes, one per item, each identical: a hairline outline, an oversized ghost number at the top-right, a short bold label and a small value inside; the row sits low with white space above | `index` for supporting points and checklists; `modules` for scope, spec, before/after, comparison (label / value pairs) |

`role` from the spine maps to a layout: `title`→`title`, `section`→`section`,
`claim`/`context`→`statement`, `evidence`/`objection`→`index`,
`data`→`modules`, `cta`→`statement` or `close`.

`grid.py` writes the regions into `tokens.json` and the classes into
`theme.css` (`section::before` is the left bar, plus `.ghost`,
`ul.index`, `.module`, `section.section`,
`section.statement`), plus a grid overlay you can toggle with a class
while checking alignment. No rounded corners, no circles, no registration
crosses, no accent box; the accent shows only as the left bar, the
field hairlines and the section numeral.

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
