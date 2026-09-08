# The built-in design system

This is the skill's own design system: an art-museum-booklet reading of
Müller-Brockmann. Every deck the skill renders without a user system uses
it as-is. When the user supplies a system, that one **layers on top** (see
below).

The example that this file describes is committed at the repository root
as `EXAMPLE-SLIDE-DECK.pdf`.

## Layering

The built-in system is **materials + structure**.

- **Materials** the user's system replaces: the type faces, the one
  accent colour, the grey steps, the ground and ink colours, the baseline
  unit. Pass them to `grid.py --from system-in.json`.
- **Structure** stays whatever the materials are: the full-height left
  bar, the title band, vertically-centred display phrases, the oversized
  ghost number, the five layouts, the one-small-size rule, the ample
  white space, the section numeral bleeding off the divider.

If the user's system contradicts a structural rule (wants an underline
under the headline, a second accent, small caps tags, rounded corners),
stop and ask which wins. Do not merge silently.

`grid.py` reads the materials, derives the grid maths from
`muller-brockmann.md`, and emits `system/tokens.json` and
`system/theme.css`. Nothing here is chosen by eye.

## Tokens (built-in defaults)

| Token | Default | Note |
|---|---|---|
| canvas | 1280 × 720 (16:9) | `4:3` only if the venue dictates |
| margins (fraction of short side) | left .075, top .11, right .085, bottom .10 | proportioned, left < top < right < bottom; generous, museum-guide |
| ink | `#111111` | body and display type |
| ground | `#FAFAF8` | light slides |
| accent | `#FF0000` | pure red; the grid-marking colour only |
| muted | `#8A8A86` | source notes, footer, page number |
| body size | 16 px reference | 20–24 for a deck read across a room |
| leading factor | 1.3 | baseline = round(body × 1.3) |
| type scale | title 5×, headline 3.3×, ghost 5.5× (one fixed size), body 1×, caption 0.82× | extreme headline-to-body jump; no mid-sizes |
| left bar | 8 px | full slide height, at `x: 0` |

## The heading element

A **full-height accent bar at the left edge of every slide**, one weight
everywhere (~8 px, `section::before`). It is the only heading mark. Never
an underline, never an eyebrow, never a rule beside the phrase.

## The oversized ghost number

Every box in an `index` or `modules` row carries a number set as a
**ghost**: one fixed size across the whole deck (never scaled to fit a
word), semi-transparent (~17 % on light, a dark knockout only if it must
sit on a solid colour), at the **top-right** of the box, straddling its
top edge via a negative offset so no rule ever runs through it. The label
and value stay top-left, clear of it. It echoes the section numeral. It
replaces every small-caps tag. It always reads lighter than the headline.

## The layouts

Five. Vary which one a slide uses so the deck is not one shape repeated.

| Layout | Composition |
|---|---|
| `title` / `close` | ink ground; the phrase huge and centred vertically (the "musica viva" principle); the left bar; a tiny meta row at the foot |
| `section` | ink ground; the section title huge and centred vertically; the left bar; an oversized accent numeral bleeding off the lower-right; nothing else |
| `statement` | light ground; one accent phrase, huge, centred vertically; the left bar; a tiny source note beneath; ample white above and below |
| `index` | huge headline in the title band; below, a horizontal row of equal outlined boxes, one per item, each with the ghost number top-right and one small size of text; the row sits low with white space above |
| `modules` | the same box row as `index`, for label / value pairs (scope, spec, before/after, comparison). Every box is identical: a hairline outline, the ghost number, a short bold label, a light value. **No accent box.** |

`role` from the spine maps to a layout: `title`→`title`,
`section`→`section`, `claim`/`context`→`statement`,
`evidence`/`objection`→`index`, `data`→`modules`,
`cta`→`statement` or `close`.

## Colour

One ink, one ground, one accent, one grey. The accent (`#FF0000` by
default, or the user's) marks the grid only: the left bar, field
hairlines, the section numeral. It is never a body-text colour, never a
fill behind a word, never a second hue. Section dividers and the
title/close run on the ink ground with the type knocked out; short text,
generous leading.

## Type

One family for display and body. The headline dominates the slide; every
other piece of text is one small size. Supporting text goes below the
headline or at the foot, never beside it, with ample white space between.
Section titles, the single claim, and the title and close are centred
vertically. A content headline sits top-left in the title band.

## Never

- No eyebrow, no label chip, no small-caps tag.
- No underline under a headline.
- No registration crosses.
- No mid-size type. Headline, one small size, and the ghost. Nothing
  between.
- No accent fill box. The accent is a rule, a numeral, the left bar.
- No rounded corners, no circles.
- No second accent, no second body face, no spacing value off the
  baseline.

## grid.py

```bash
python3 scripts/grid.py --canvas 16:9 --body 16 --fields 8 \
  --advance 0.5 --leading 1.3 --accent "#FF0000" --out system/
# with a user system:
python3 scripts/grid.py --from system-in.json --canvas 16:9 --fields 8 --out system/
```

`system-in.json` carries `{ "faces": {...}, "colours": {...},
"leading_factor": 1.3, "advance": 0.5 }`. Output: `system/tokens.json`
(the numbers, the layout regions) and `system/theme.css` (`section::before`
the left bar, plus `.ghost`, `ul.index`, `.module`, `section.section`,
`section.statement`, and a grid overlay you can toggle while checking
alignment).
