# Stage 4. Build

Goal: assemble `deck.md` from `spine.md` and `system/`, render to the
format(s) the user picks, and verify the rendered output before handing
it over.

## Pick the format

Ask with `AskUserQuestion`; more than one answer is allowed.

| Format | Command | Use when |
|---|---|---|
| **Marp HTML** | `marp deck.md --theme system/theme.css -o deck.html` | web-first, in version control, live editing, exports its own PDF |
| **PDF** | `marp deck.md --theme system/theme.css --pdf --allow-local-files -o deck.pdf` | a fixed artefact to send or print |
| **PDF, print-grade** | Typst (below) | tight grid control, crop marks, print production |
| **PPTX** | `marp deck.md --theme system/theme.css --pptx -o deck.pptx` | the recipient needs the layout in PowerPoint |
| **PPTX, editable** | the `pptx` skill, fed `spine.md` and `tokens.json` | the recipient will rewrite the content |

Marp is the single source for HTML, PDF and a layout-only PPTX. Reach for
Typst only when print production needs it. Reach for the `pptx` skill only
when the file must be truly editable, since Marp’s PPTX is pictures of
slides.

Install Marp if absent: `npm i -g @marp-team/marp-cli`.

## Assemble deck.md

One Marp slide per `spine.md` row.

```markdown
---
marp: true
theme: <name from theme.css>
paginate: true
---

<!-- _class: title -->
# <deck title>

---

## Manual screening costs the team a day a week

<!-- one idea. body sits in the grid the theme defines. -->

- 4.2 h/week logged on manual screening (time log, Q2)
- across 6 people, that is ~25 h/week

<!-- data slide: the chart states the takeaway in its own title -->

---

<!-- _class: cta -->
## We need budget sign-off by Friday to start in Q3

Owner: <name>. Decision needed: <amount>.
```

- Slide title is the assertion headline copied verbatim from the spine.
- `_class: title` / `section` / `cta` map to the theme’s full-bleed and
  emphasis layouts.
- Charts: generate as SVG sized to a whole number of fields (see
  `tokens.json` key `field`), title the chart with its takeaway, embed
  with `--allow-local-files`. Keep to one comparison.
- Speaker notes go in `<!-- ... -->` HTML comments. Marp keeps them out of
  the slide and puts them in presenter view and the PDF notes.

## Typography

Run the whole `deck.md` through `typocheck.py` before rendering. The deck
inherits every rule from Stage 1. Headlines especially: no em-dash, no
contrastive “not A, but B”, and a non-breaking space gluing the last two
words of every headline so nothing widows on wrap.

```bash
python3 ~/.claude/skills/typography/scripts/typocheck.py deck.md
```

## Verify. Do not skip

After rendering, open the output and go slide by slide:

1. **Headlines read as sentences.** Walk them top to bottom as a
   paragraph; they should argue the thesis.
2. **Nothing overflows.** Body inside the type area, bottom margin intact,
   headline at most two lines. If a slide overflows, cut words (Stage 2).
   Shrinking the type is not an option.
3. **One idea per slide.** Any slide you can describe with an “and” goes
   back to Stage 2 to be split.
4. **Data slides carry their takeaway** in the chart title and show one
   comparison.
5. **Last slide is the ask**, with an owner and a specific action.
   “Thank you” is not a call to action.
6. **Grid holds.** Spot-check three slides with the theme’s grid-overlay
   class; baselines land on grid lines.

### Consistency audit

Then run one pass across the whole deck, not slide by slide:

- **Type.** One family, one headline size, one small size, one ghost
  size. No stray mid-size.
- **Colour.** One ink, one ground, one accent. The accent only ever marks
  the grid.
- **Spacing and alignment.** Every element on the grid; the left bar,
  margins, footer and page number in the same place on every slide.
- **Numbering.** Section numbers and box numbers run in sequence, same
  format.
- **Density and contrast.** No slide is crowded; text holds contrast
  against its ground at the size it is set. A slide that reads as anxious
  goes back to Stage 2 for cutting.
- **Audience.** The emphasis still matches the pattern chosen in Stage 2.

Then screenshot the rendered deck (a contact sheet of all slides is
ideal) and send it to the user with `SendUserFile`. State the format(s)
built and where the files are. Never describe a deck you have not looked
at as done.

## Typst route (print-grade only)

When the user asked for print-grade PDF, emit a `deck.typ` that reads the
same `tokens.json`, sets `page` to the canvas, `margin` to the token
margins, and a `grid` / `place` layout on the baseline. Render with
`typst compile deck.typ deck.pdf`. Keep the type scale, colours and field
maths identical to `tokens.json`. The Typst deck and the Marp deck are
the same design in two renderers.

## Output

`deck.md`, then `deck.html` / `deck.pdf` / `deck.pptx` as chosen, and a
screenshot sent to the user.
