# Stage 1 — Content

Goal: turn whatever the user hands over (notes, a doc, a transcript, a
brain-dump, links) into a **sourced argument shaped by one framework**.
Not slides. Prose.

## Readiness gate

Before doing anything, confirm the content is an argument, not a subject.
The user should be able to answer, in their own words:

- What does this deck claim? (one sentence)
- Who is in the room?
- What do you want them to do when it ends?

If any answer is "I don't know yet" or "it's about X" with no position,
stop and hand off to `for-tee-too`. Coming back with its scoping notes is
faster than trying to invent the argument here.

## 1. Clean the raw material

- Pull every factual claim into a list. Mark each: **sourced**,
  **needs a source**, or **opinion**. A deck that makes claims it cannot
  attribute loses the room the first time someone asks.
- Cut anything that is not load-bearing for the claim or the ask.
  "Curate ruthlessly — slides support a speaker, they don't replace one."
- Collapse repetition. If two notes make the same point, keep the
  sharper one.
- Flag the numbers that will become charts. Note, for each, the single
  comparison it exists to show.

## 2. Pick the framework

From what the deck is *for*:

| For | Framework | File |
|---|---|---|
| diagnose a problem, recommend action (internal, exec, consulting) | McKinsey 7-step | `frameworks/mckinsey-7-step.md` |
| introduce a project / product / initiative and get buy-in or funding | Project / product intro, 12-point | `frameworks/project-intro.md` |
| a talk, lecture, conference or portfolio pitch — not a business case | SCQA narrative | `frameworks/scqa-talk.md` |

Load only the file you pick. Ask the user with `AskUserQuestion` if two
plausibly fit. If none fit, build from the primitives every framework
shares — **claim → evidence → implication → ask** — and note in
`content.md` that the outline is bespoke.

## 3. Write `content.md`

Structure it by the framework's sections. Under each section:

- the point of that section, in one sentence;
- the evidence, each line ending with its source in brackets;
- open questions still to resolve, marked `TODO`.

Keep it in prose and lists. Do not pre-format it as slides — Stage 2 does
that, and doing it now locks choices you have not made yet.

Length target: shorter than you think. If `content.md` runs past ~2
pages for a 15-slide deck, there is still cutting to do.

## 4. Typography pass

Every line of prose goes through the `typography` skill as you write it,
not at the end:

- non-breaking spaces after short prepositions, conjunctions, articles,
  initials, titles; between number and unit;
- «ёлочки» in Russian, curly quotes in English, real ellipsis, `–` for
  ranges, `×` for dimensions;
- no em-dash standing in for syntax; no "not A, but B" / «не просто X, а Y».

Verify:

```bash
python3 ~/.claude/skills/typography/scripts/typocheck.py content.md
```

Reference: https://github.com/sinaida-space/tardis_type (local: the
`typography` skill).

## Output

`content.md` — the argument, sourced, framework-shaped. Hand it to the
user and confirm the claim and the ask are right before Stage 2.
