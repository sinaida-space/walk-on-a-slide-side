# Framework: McKinsey 7-step problem solving

For a deck that diagnoses a problem and recommends action: internal
decision decks, executive updates, consulting-style readouts.

The seven steps are the thinking order. The **deck order** can differ.
For an executive audience you lead with the recommendation and support it
backwards. Decide which you need before writing `content.md`.

## The seven steps (thinking order)

1. **Define the problem.** Think impact. What do we actually need to know?
   State the problem as a single question with a clear scope, a decision
   owner and a deadline. One sentence.
2. **Structure the problem.** Break it into a small tree of independent
   sub-questions (issue tree / MECE). State an early hypothesis for each,
   meaning what you expect the answer to be.
3. **Prioritise the issues.** Think speed. Which branches actually move
   the answer? Cut or park the ones that do not. Most branches do not
   matter; say which two do.
4. **Work plan.** Think efficiency. For each live issue: the analysis that
   would resolve it, the data it needs, who does it, by when.
5. **Conduct the analyses.** Think evidence. For each: what are we trying
   to prove or disprove, and what result would change our mind.
6. **Synthesise the findings.** Think “so what”. Each finding gets a
   one-line implication. Group them into the two or three that carry the
   recommendation.
7. **Recommend.** Think solution. What to do, who owns it, what it costs,
   what the risks are, what the first step is.

## Deck sections

**Executive or decision audience, recommendation first:**

| Section | Slides |
|---|---|
| The ask | recommendation as one assertion headline; the decision needed |
| Why | the 2–3 synthesised findings, one slide each, each with its evidence |
| The problem | the defining question, its scale (data slide), why it matters now |
| Risks and mitigations | the real objections, answered |
| Next step | owner, cost, first action, date. The CTA slide |

**Working session, thinking order:**
problem, issue tree, the two issues that matter, evidence per issue,
synthesis, recommendation, next step.

## `content.md` shape

```
## Problem
<one-sentence question, scope, owner, deadline>
Why we say this: <trigger / evidence> [source]

## Structure
- Sub-question A. hypothesis: ...
- Sub-question B. hypothesis: ...
(prioritised: A and B carry the answer; C, D parked because ...)

## Analysis, A
Trying to prove or disprove: ...
Finding: ... [source]  => implication: ...

## Analysis, B
...

## Synthesis
1. <implication>, because <findings>
2. <implication>, ...

## Recommendation
Do: ...  Owner: ...  Cost: ...  First step: ...
Risks: ... => mitigation: ...
```

Each finding needs a source and an explicit implication, or it does not
go on a slide. If a finding has no “so what”, drop it.
