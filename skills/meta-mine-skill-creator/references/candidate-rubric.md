# Candidate rubric

Use this rubric after evidence windows have been clustered.

## Destination test

Choose exactly one primary destination for each cluster:

| Destination | Use when |
|---|---|
| New `geno-dev` skill | A repeatable developer workflow has a clear trigger, observable outcome, and non-obvious decisions worth hiding behind one interface. |
| Existing skill patch | The right skill already exists, but its instructions caused or failed to prevent the observed correction. |
| Repository guidance | The behavior is specific to one codebase, team, or checked-in convention. |
| Global agent rule | The correction applies across unrelated work but is a general interaction rule rather than a workflow. |
| Product or tool feedback | The issue belongs to Claude Code, Codex, a tool, or its configuration and cannot honestly be fixed by a skill. |
| Discard | The signal is one-off, obvious to a capable agent, contradictory, obsolete, or unsupported by enough evidence. |

Do not create a skill merely to remember a preference, wrap one shell command, or restate generic competence.

## Score

Score each recommended or watchlisted cluster from 0–3 on four positive dimensions, then subtract 0–3 for risk.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Recurrence | One ambiguous event | One explicit event | Two independent sessions | Three or more sessions or both providers |
| Leverage | Little behavior hidden | Saves a reminder | Reuses meaningful decisions | Prevents repeated expensive failure or coordination |
| Scope fit | Wrong owner | Weakly related | Clearly developer workflow | Central to this skillset's purpose |
| Specificity | Vague preference | Partial trigger or outcome | Clear trigger and outcome | Clear trigger, outcome, constraints, and failure modes |
| Risk penalty | No meaningful risk | Could over-trigger | Handles sensitive or destructive work | Would broaden authority or encode uncertain behavior |

`score = recurrence + leverage + scope fit + specificity - risk penalty`

- 8 or more: recommend creating or patching.
- 5–7: watchlist unless the user explicitly prioritizes it.
- 4 or less: redirect or discard.

The threshold is decision support, not a substitute for judgment. A severe single correction may justify a global rule or product report without justifying a new skill.

## Candidate dossier

Use this compact shape:

```markdown
### <candidate name>

- Destination: <new skill | patch | repository | global | product | discard>
- Recommendation: <create | patch | watch | redirect | discard>
- Score: <total> (recurrence N, leverage N, fit N, specificity N, risk -N)
- Trigger: <one sentence>
- Outcome: <observable result>
- Hidden decisions: <what a capable agent still benefits from being told>
- Evidence: <provider/session/date/project references and short redacted excerpts>
- Counterevidence: <conflicts, false positives, or missing validation>
- Proposed interface: <inputs, authorization constraints, failure modes>
```

## Correction ledger

Also report corrections that do not become skill candidates:

| Correction | Evidence | Destination | Reason |
|---|---|---|---|

This keeps system-level and repo-level improvements visible instead of forcing every useful lesson into a skill.
