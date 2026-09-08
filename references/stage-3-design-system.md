# Stage 3. Design system

Goal: a grid, a type scale and a colour set, all derived by
Müller-Brockmann’s maths (`muller-brockmann.md`), emitted as
`system/tokens.json` and `system/theme.css`.

## First question, always

**Is there a design system to work inside?** Ask before constructing
anything.

### Path A. The user has a design system

Locally, that is the `sinaida-grid-style` skill. Read its
`reference/grid-law.md` and `assets/tokens/tokens.json` and take:

- the type faces (Geist Pixel for display and body; Libre Franklin where
  Cyrillic is needed, since Geist Pixel is Latin only and fails loudly);
- the one red (`#CD0000` / `sinaidaRed`) and the grey steps;
- the baseline unit and the ground colours (`chalk`, `void`).

Do **not** add a second red, a second body face, or a spacing value off
the unit. Then run the grid maths below to derive columns, fields and the
type area for the deck canvas. The house style supplies the *materials*
and Müller-Brockmann supplies the *structure*.

Pass the ingested values in:

```bash
python3 scripts/grid.py --from system-in.json --canvas 16:9 --fields 8 --out system/
```

where `system-in.json` carries `{ "faces": {...}, "colours": {...},
"baseline_factor": 1.3, "advance": 0.489 }`.

### Path B. No design system (public, client, or first deck)

Construct one from `muller-brockmann.md`. This is the default for anything
shared publicly from the repo. Choose:

- **canvas.** `16:9` (1280×720 reference px) unless the venue dictates
  `4:3` or a specific projector size.
- **body size.** 20–24 px reference for a room; 18 only for a deck read on
  screens.
- **faces.** One grotesk family for everything. Name a real fallback
  stack. If the deck has Cyrillic, the family must cover it.
- **field count.** From content density, per the table in
  `muller-brockmann.md`: 8 for most decks, 20 for data-dense, 32 for
  reference.

```bash
python3 scripts/grid.py --canvas 16:9 --body 22 --fields 8 \
  --advance 0.50 --leading 1.3 --out system/
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
7. type scale (title, headline, body, caption) as ratios of body;
8. colour roles (ink, ground, accent = grid red, muted).

Output: `system/tokens.json` (the numbers) and `system/theme.css` (a Marp
theme that binds them: `section` padding = margins, `h1` = headline size,
and a background grid overlay you can toggle with a class while checking
alignment).

## Check the system before Stage 4

- Render one test slide with the longest headline and a full body block.
  The headline must not exceed two lines; the body must sit inside the
  type area with the bottom margin intact.
- Turn on the grid overlay. Every text baseline sits on a grid line, and
  any images span whole fields.
- If the test slide overflows, the fix is fewer words (back to Stage 2)
  or a larger field count. Shrinking the type by hand is not an option.

## Output

`system/tokens.json` and `system/theme.css`. These are inputs to Stage 4.
They are not edited by hand afterward; change the flags and re-run.
