<img width="3072" height="384" alt="image" src="https://github.com/user-attachments/assets/c45d1024-89ce-40cd-93e9-594536e3774f" />


# walk-on-a-slide-side

The ultimate slide-deck maker, as a Claude&nbsp;Code skill. It builds a deck
in four stages, in order: clean the content, structure the argument,
construct a Müller-Brockmann design system, render the slides.

## Why this exists

Most decks are built back to front. Someone opens a template, picks a
theme, and starts typing headings like “Overview” and “Next Steps” onto
slides that each carry three half-thoughts. The design is chosen before
anyone has decided what the deck argues, so the design cannot help. The
result reads like filler, and the room stops listening on slide&nbsp;four.

This skill refuses that order. It will not touch layout until the
argument exists and the spine is approved. Then it builds the grid the
way Josef Müller-Brockmann builds a grid: the type area from the canvas
and its margins, the columns from the type size, the baseline from the
leading, the field count from how much the deck has to hold. Nothing is
chosen by eye. The book is the design bible, and if a number cannot be
derived from it, it does not go in.

What you get is a deck that reads as one object, page to page, where the
headlines alone carry the argument and every slide holds exactly one
idea.

## What it gives you

- **`content.md`.** Your raw material cleaned into a sourced argument,
  shaped by the framework that fits what the deck is for.
- **`spine.md`.** One row per slide: an assertion headline that states
  the point, the single idea it carries, the evidence, its place in the
  arc.
- **`system/tokens.json` and `system/theme.css`.** A design system
  derived by Müller-Brockmann’s maths: margins, type area, columns,
  gutter, baseline unit, field arrangement, type scale, colour roles,
  and a Marp theme bound to all of it.
- **`deck.html` / `deck.pdf` / `deck.pptx`.** The rendered deck, in the
  format you ask for, checked slide by slide before it reaches you.

## How to use it

Install as a git checkout under `~/.claude/skills/`:

```bash
git clone https://github.com/sinaida-space/walk-on-a-slide-side.git \
  ~/.claude/skills/walk-on-a-slide-side
```

`scripts/grid.py` needs only Python&nbsp;3. Rendering needs the Marp CLI:

```bash
npm i -g @marp-team/marp-cli
```

Then, in Claude&nbsp;Code, ask for a deck (“make a deck from these notes”,
“build a pitch deck for …”) or run `/walk-on-a-slide-side`. The skill
announces the four stages and runs them in order.

### Stage 1: Content

It checks first that you can state what the deck argues and what you want
the audience to do. If you can only name a topic, it sends you to
[`for-tee-too`](https://github.com/sinaida-space/for-tee-too)
to scope the problem, audience and goal, and you come back with those
notes. Then it cleans the raw material: every claim tagged with its
source, everything that is not load-bearing cut, the numbers that will
become charts flagged with the one comparison each exists to show. It
picks a narrative framework from what the deck is for:

| The deck is for… | Framework |
|---|---|
| diagnosing a problem and recommending action | McKinsey 7-step problem solving |
| introducing a project or product for buy-in | Project / product intro, 12-point |
| a talk, lecture or pitch that is not a business case | SCQA narrative |

The project-intro framework is Sinaida’s own, built from running IT and
process projects at General&nbsp;Electric and from the years in creative
direction that followed. Its rule: avoid the “just an idea” stage. The
world has enough ideas and lacks the resources to make them work.

### Stage 2: Structure

The argument becomes a spine. One idea per slide. Assertion headlines: a
title is a full sentence that states the takeaway (“Revenue grew in every
region”), never a label (“Q3 Revenue”). Read the headlines top to bottom
and they form the argument by themselves. Data slides state their
takeaway in the chart title. There is one call-to-action slide and it is
last; “Thank you” is not a slide. You approve the spine before any design
work, because changing it later means re-rendering and changing it now
costs nothing.

### Stage 3: Design system

It asks whether you already have a design system.

- **If you do**, supply a tokens file or a brand spec and it ingests your
  faces, your accent, your grey steps and your baseline unit, and adds
  nothing of its own.
- **If you do not** (anything shared publicly, or client work that needs
  its own identity), it constructs one from
  [`references/muller-brockmann.md`](references/muller-brockmann.md). The
  default accent is pure red `#FF0000`, used only to mark the
  grid.

Either way the grid, the type scale and the spacing come from the maths,
not from taste. `grid.py` does the derivation:

```bash
python3 scripts/grid.py --canvas 16:9 --body 16 --fields 8 --advance 0.50 --out system/
```

### Stage 4: Build

It asks which format you want, and you can pick more than one:

| Format | Route |
|---|---|
| **Marp HTML** | web-first, in version control, exports its own PDF |
| **PDF** | Marp for most work, Typst when the grid needs print-grade control |
| **PPTX** | Marp for layout, the `pptx` skill when the recipient will edit the content |

It assembles `deck.md` from the spine, renders, then reads every slide:
headlines that argue the thesis, nothing overflowing the type area, one
idea per slide, data slides carrying their takeaway, the ask last, the
grid holding. It sends you a screenshot of the built deck. It never hands
over a deck it has not looked at.

## Typography

Every line of prose in the deck goes through
[Tardis&nbsp;Type](https://github.com/sinaida-space/tardis_type), the
typography skill: non-breaking spaces, correct glyphs, no em-dash
standing in for syntax, no “not A, but B”. Verify with:

```bash
python3 ~/.claude/skills/typography/scripts/typocheck.py deck.md
```

## Author

Sinaida Krivchenko is a new media artist based in Prague, working in
interactive projection, GLSL shaders, generative art and web
applications. Background in biomedical engineering and IT project
management, including General&nbsp;Electric’s IT Leadership Program.

[sinaida.eu](https://sinaida.eu)

## License

Source code under the Apache License&nbsp;2.0 ([`LICENSE`](LICENSE)). The
banner imagery is separate ([`LICENSE-ARTWORK`](LICENSE-ARTWORK)). The
Müller-Brockmann book is referenced, not reproduced; obtain it to read
the method at source. See [`NOTICE`](NOTICE).

<img width="3072" height="384" alt="image" src="https://github.com/user-attachments/assets/edadb9be-0def-4b24-aa6b-8777dbc1b3ca" />

