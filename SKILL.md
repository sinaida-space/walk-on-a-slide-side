---
name: walk-on-a-slide-side
description: >
  The full pipeline for building a slide deck from raw material — content
  cleaning, then narrative structure, then a Müller-Brockmann design system,
  then a rendered deck (Marp HTML, PDF, or PPTX). USE THIS whenever the user
  asks to make, build, or design a presentation, slide deck, pitch deck,
  keynote, talk deck, or "slides from these notes", or invokes
  /walk-on-a-slide-side. It runs all four stages in order and asks which
  output format to render. If the content is still a loose idea, it hands
  off to the for-tee-too skill first. All prose in the deck goes through
  the typography skill.
---

# walk-on-a-slide-side

An ultimate slide-deck maker. It does not start at "design". It starts at
"what are you actually saying", forces that into a spine of one idea per
slide, builds the grid from Müller-Brockmann's construction method, and
only then renders. Four stages, run in order:

```
1  CONTENT        raw material → clean, sourced, framework-shaped argument
2  STRUCTURE      argument → slide-by-slide spine, one idea per slide
3  DESIGN SYSTEM  grid, type scale, colour — Müller-Brockmann maths
4  BUILD          render to Marp HTML · PDF (Marp/Typst) · PPTX
```

Each stage produces a file the next stage reads. A stage can be re-run
without redoing the ones before it. Do not skip forward: a deck designed
before its spine exists is a deck you rebuild.

## On launch

Say, in one or two sentences, that this is the full four-stage process and
name the stages. Then run this gate before Stage 1:

**Is the content ready to shape?** Ready means the user can state, in
their own words, what the deck argues and what they want the audience to
do. If they can only describe a topic or a feeling, stop and hand off:

> The material is still a subject, not an argument. Run `/for-tee-too`
> first to scope it — problem, audience, goal — then come back here with
> the notes it produces.

`for-tee-too` lives at https://github.com/sinaida-space/for-tee-too (and
as the local `for-tee-too` skill). Do not try to do its job inside this
skill. Come back when there is a position to build on.

If the content is ready, ask the two framing questions (audience, and the
one action the deck should produce) with `AskUserQuestion`, then enter
Stage 1.

## Stage 1 — Content

Read `references/stage-1-content.md`.

Clean the raw material into a sourced, framework-shaped argument. Pick the
narrative framework from what the deck is *for*, not from taste:

| The deck is for… | Framework |
|---|---|
| diagnosing a problem and recommending action | McKinsey 7-step problem solving |
| introducing a project, product or initiative for buy-in | Project / product intro (12-point) |
| a talk, lecture or pitch that is not a business case | SCQA narrative |

Framework files are in `references/frameworks/`. Load only the one you
pick. If the deck genuinely fits none, build a bespoke outline from the
same primitives (claim → evidence → implication → ask) and say so.

Output: `content.md` — the argument in prose, every claim with its
source, ordered by the chosen framework. This is not slides yet.

All prose is written through the `typography` skill from the first draft:
non-breaking spaces, correct glyphs, no em-dash rhetoric, no "not A but B".
Reference: https://github.com/sinaida-space/tardis_type (local: the
`typography` skill). Verify with
`python3 ~/.claude/skills/typography/scripts/typocheck.py content.md`.

## Stage 2 — Structure

Read `references/stage-2-structure.md`.

Turn `content.md` into a spine: one row per slide, each with an assertion
headline (a full sentence that states the takeaway, not a label), the
single idea it carries, the evidence on it, and its role in the arc. Split
any slide that carries two ideas. Mark the data slides and the one CTA
slide.

Output: `spine.md` — the ordered list. Show it to the user and get it
approved before any design work. Changing the spine after Stage 3 means
re-rendering; changing it now costs nothing.

## Stage 3 — Design system

Read `references/stage-3-design-system.md` and `references/muller-brockmann.md`.

First question, always: **is there a design system to work inside?**

- **Yes, the user has one** (locally, that is the `sinaida-grid-style`
  skill and its `reference/grid-law.md`). Ingest its type faces, colours
  and spacing unit. Do not invent a second red or a second face.
- **No / this is for a public or client audience.** Construct one from
  `references/muller-brockmann.md`: type area from the canvas and margin
  proportions, columns from type size, baseline from leading, fields from
  content density.

Either way the grid, the type scale and the spacing are derived by
Müller-Brockmann's maths, not chosen by eye. That book is the bible here;
if a number is not derivable from it, it does not go in.

```bash
python3 scripts/grid.py --canvas 16:9 --body 22 --fields 8 --out system/
```

`grid.py` writes `system/tokens.json` (canvas, margins, type area, column
count and width, gutter, baseline unit, field arrangement, type scale,
colour roles) and `system/theme.css` (a Marp theme built from those
tokens). Feed it the ingested values with `--from system.json` when the
user has a design system.

Output: `system/tokens.json` + `system/theme.css`.

## Stage 4 — Build

Read `references/stage-4-build.md`.

Ask which format with `AskUserQuestion` (the answer can be more than one):

| Format | Route | Use when |
|---|---|---|
| **Marp HTML** | `deck.md` + `theme.css` → `marp` | web-first, version control, live edit, self-export to PDF |
| **PDF** | Marp `--pdf`, or Typst for print-grade grid control | sending a fixed artefact, print |
| **PPTX** | Marp `--pptx` for layout, or the `pptx` skill when the audience will edit | the recipient needs an editable file |

Assemble `deck.md` from `spine.md`: one Marp slide per spine row,
assertion headline as the slide title, body inside the grid the theme
defines. Then render, then **verify** — open the output, read every slide,
check the headline reads as a sentence, check nothing overflows the type
area, check the data slides carry their takeaway. Screenshot the built
deck and send it to the user. Never hand over a deck you have not looked
at.

## Files

```
references/
  muller-brockmann.md        the construction method and every number it yields
  stage-1-content.md         cleaning, sourcing, framework routing
  stage-2-structure.md       the spine: one idea per slide, assertion headlines
  stage-3-design-system.md   ingest-or-construct, then Müller-Brockmann maths
  stage-4-build.md           Marp / Typst / PPTX render and verification
  frameworks/
    mckinsey-7-step.md       define → structure → prioritise → plan → analyse → synthesise → recommend
    project-intro.md         12-point project / product introduction
    scqa-talk.md             situation · complication · question · answer
scripts/
  grid.py                    Müller-Brockmann grid calculator → tokens.json + theme.css
```

## Never

- Never design before the spine is approved.
- Never write a slide title as a label ("Q3 Revenue"). It is a sentence
  that states the point ("Revenue grew in every region").
- Never put two ideas on one slide. Split it.
- Never introduce a second red, a second body face, or a spacing value
  that is not a whole number of baseline units.
- Never let "Thank you" be the last slide. The last slide is the ask.
- Never ship a deck without reading the rendered output yourself.
- Never print the user's email address into a deck, a template or a
  suggestion. Leave a placeholder.
