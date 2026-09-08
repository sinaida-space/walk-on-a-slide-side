# Stage 2. Structure

Goal: turn `content.md` into a **spine**, one row per slide, in order,
each carrying exactly one idea under an assertion headline. This is the
document the whole deck is built from. Get it approved before Stage 3.

## The rules

**One idea per slide.** Each slide communicates a single testable
takeaway. If a slide has two, split it into two slides. A slide whose
headline needs an “and” is two slides.

**Assertion headlines.** The title is a full sentence stating the point.
A topic label is not enough.

- label “Q3 revenue” becomes “Revenue grew in every region in Q3”
- label “Competitors” becomes “No competitor covers both segments”
- label “Next steps” becomes “We need sign-off on the budget by Friday”

Read the headlines alone, top to bottom. They should form the argument by
themselves. That is the deck’s skeleton and its handout.

**Self-explaining data slides.** Every chart slide’s headline states what
the chart shows. The chart is simplified to the one comparison that backs
the headline. If a chart needs a spoken sentence to be understood, the
headline is missing.

**One CTA slide, and it is last.** It names the specific next step and who
owns it. “Thank you” is not a slide. A questions slide, if any, comes
before it.

## The arc

Order the spine to an arc. The rows have a shape: setup, turn, evidence,
ask.

- **Business case / consulting.** Recommendation first for executives, or
  problem, structure, evidence, recommendation, ask for a working
  session. Match the framework chosen in Stage 1.
- **Talk / pitch.** Setup, tension, resolution, proof, ask. Rehearse the
  open and the close; they carry the room.
- Put the hardest objection on its own slide and answer it. Hoping no one
  raises it is not a plan.

Section dividers are full-bleed title slides (see `muller-brockmann.md`)
and do not count as content slides.

## Adapt to the audience

The same argument shifts emphasis by who is in the room. Use the framing
answers from launch (audience, the one action, the time slot) to pick the
pattern:

| Audience | Prioritise | Structure | On the slides |
|---|---|---|---|
| Investor / fundraising | credibility, traction, a clear ask | assertion headlines, numeric evidence, problem → solution → evidence → ask | metrics shown visually; no stock imagery |
| Executive / board | decisions, risks, trade-offs | recommendation first, then context → tension → resolution → proof → decision needed | one takeaway per chart, the “so what” at the top |
| Sales / client | relevance to the client’s goals | map each slide to a client priority; answer the likely objections explicitly | before / after visuals, a case, clear ROI, minimal text |
| Technical / engineering review | accuracy, depth, reproducibility | separate the high-level narrative from the detail; put deep dives in an appendix | precise diagrams and labelled charts; define terms once; keep jargon off the narrative slides |
| All-hands / internal | clarity, alignment, morale | plain language, clear signposting; repeat the core message across sections | simple visuals, consistent branding; name the action for each team |
| Conference / public talk | story, memorability, pacing | a clear arc (setup → tension → resolution → proof → close); rehearse the open and the close | one strong visual per slide, large type for a room |

Note the pattern in `spine.md` so Stage 3 and Stage 4 keep to it.

## Write `spine.md`

A table, one row per slide:

```
| # | role | assertion headline | the one idea | evidence on slide | notes |
|---|------|--------------------|--------------|-------------------|-------|
| 1 | title | <deck title> | . | . | full-bleed |
| 2 | context | Manual screening costs the team a day a week | scale of the problem | time-log chart | data slide |
| 3 | ...
```

`role` is one of: `title`, `section`, `context`, `claim`, `evidence`,
`data`, `objection`, `cta`.

## Length

Target one idea per minute of talk time, minus section dividers. A
20-minute talk is about 15 content slides. If the spine is longer, some
rows are really speaker notes. Move them off the deck.

## Output

`spine.md`. Show it to the user. Walk the headlines aloud as a paragraph
and ask whether they argue the thing. Fix it here. Every change after
Stage 3 costs a re-render.
