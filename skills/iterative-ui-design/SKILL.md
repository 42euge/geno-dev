---
name: iterative-ui-design
description: >-
  Use when the user will recognize the right UI when shown alternatives and
  wants multiple browser-reviewable options at each refinement round before
  explicit convergence. Do not use when the design is already settled and the
  user only wants it implemented.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# Converge on a UI through reviewable variants

Turn uncertain taste into an explicit design by repeatedly showing concrete
alternatives, carrying the user's selections forward, and narrowing one design
decision at a time. The deliverable is a chosen prototype and a decision
summary suitable for implementation—not production code disguised as a
mockup.

## Establish the design contract

Before the first round, infer from the request and existing application:

- the surface and representative user state being designed;
- fixed constraints and behavior that must remain;
- the first decision axis, such as layout, navigation, density, or interaction;
- the fastest review medium that lets the user judge that axis.

Do not turn this into a questionnaire when the repository or prompt already
answers it. When the user says they will know the design when they see it,
prefer an early artifact over more speculative questions.

For GUI work, make the review artifact renderable in a browser or the
application's native preview. Do not substitute ASCII, prose wireframes, or a
list of ideas unless the user requests that medium.

## Isolate the prototypes

Follow the repository's prototype convention when one exists. Otherwise use a
clearly named local prototype or `mockups/` location and tell the user how to
open it. Keep prototype code separate from production paths and do not commit
it unless requested.

Use representative content, realistic density, and the application's existing
visual context where practical. Stub mutations and external effects; a design
prototype must not write production data or call live services merely to look
realistic.

## Run the refinement loop

### 1. Generate a contrasting round

Default to three variants; add a fourth only when it represents another
genuinely different thesis. Give each a stable label and a one-sentence design
thesis. The variants should disagree about structure, hierarchy, or primary
interaction—not just color, copy, or decoration.

**Branching invariant:** while exploration is active, every presented round
contains multiple options. A selected variant is the seed for another branch
set, not permission to collapse the workflow into one refined artifact.

Make comparison cheap: provide one launcher, route switcher, or compact set of
links so the user can move among every option without rebuilding the project.

### 2. Convert feedback into state

After each response, maintain a compact internal ledger:

- **Locked:** decisions and elements that carry forward;
- **Rejected:** approaches that should not quietly return;
- **Active axis:** the one question the next round will vary;
- **Fidelity gaps:** interactions or real-world behavior the current mockup
  cannot yet answer;
- **Round state:** `exploring` until the user explicitly converges.

Treat partial choices as useful signal. “B with A's navigation” locks B's base,
adds A's navigation, and rejects the remaining differences. “None, but C is
closest” keeps only the stated parts of C. Do not average every option into an
undirected compromise.

When the user points at a screenshot or a specific element, restate the exact
referent and requested delta before changing the prototype. Ask one focused
question only if that delta is materially ambiguous.

### 3. Re-diverge from the selected seed

Generate the next round from the locked state, varying the active axis while
preserving prior decisions. Later variants should be closer together than the
first round because the design space is narrowing.

Treat the user's requested changes as the shared baseline for the next branch
set. Apply them to every new option, then vary another consequential dimension
related to the feedback. The user does not need to repeat “show me options” or
“continue exploring” after each selection. A selection plus a list of concrete
deltas is still an exploration turn.

If the next axis is not stated, infer one from the unresolved design space and
name it when presenting the round. Do not refine one artifact and ask for
approval merely because the requested deltas were precise.

Collapse to a single revision only when the user explicitly opts out of more
branches, for example “make only this correction,” “no more options,” or
“finalize this one.” A mechanical clarification can be applied across the next
branch set without ending exploration.

### 4. Raise fidelity only to unlock feedback

Start with the cheapest artifact that exposes the current decision, then add
behavior when the user can no longer judge from a static view. Typical levels
are:

1. representative layout and content;
2. working navigation, disclosure, and view switching;
3. editable or stateful interactions with in-memory data;
4. realistic edge states needed to validate the chosen interaction.

State which controls are real and which are placeholders. Do not build a
backend, persistence, exhaustive error handling, or production abstractions to
increase the appearance of fidelity.

## Converge and hand off

Stop the loop only when the user explicitly approves or finalizes a direction,
says it is good enough to implement, or explicitly asks to stop seeing
alternatives. Selecting a favorite, giving detailed deltas, or omitting the
word “options” does not establish convergence. Record:

- the chosen variant and why it won;
- locked elements gathered from other variants;
- rejected directions that should stay out;
- interactions actually exercised;
- unresolved behavior or prototype shortcuts.

Before implementation, compare the winning prototype with the relevant real
schema, data, permissions, and existing behavior. Resolve or expose mismatches
instead of allowing prototype assumptions to become requirements accidentally.

Design approval authorizes the design deliverable, not unrelated production
edits, commits, or deployment. If the user also asks to implement it, end this
workflow and hand the decision summary to the repository's normal planning and
implementation process.

## Failure conditions

Correct course when:

- the artifact cannot be reviewed in the medium the user requested;
- options are cosmetic siblings rather than distinct design theses;
- a locked or rejected decision reappears without new evidence;
- one refined artifact replaces a branch set before explicit convergence;
- a round varies several uncoupled axes and makes feedback uninterpretable;
- static placeholders are presented as working interactions;
- prototype code starts accumulating production obligations;
- the loop continues after the user has converged.
