---
name: geno-dev-loops-control-tower
description: >-
  Meta loop that routes work to the right execution loop, supervises it,
  and intervenes when progress drifts. Use when user says
  /geno-dev-loops-control-tower.
argument-hint: "[task] [--brief <file>] [--for <duration>] [--max <n>] [--prefer <loop>]"
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# Control Tower Loop

Meta orchestration loop for the geno ecosystem. Control Tower does not try to solve every task itself. It classifies the work, chooses the best execution loop, supervises progress, intervenes when the run starts drifting, and escalates to supporting skills when the current lane lacks information, specs, or execution shape.

## Input

Parse `$ARGUMENTS` for:

- **Task pattern** - fuzzy-matches against geno-notes tasks (optional)
- **`--brief <file>`** - optional issue brief, notes file, or plan/spec seed
- **`--for <duration>`** - target orchestration window (default: `4h`)
- **`--max <n>`** - maximum supervision cycles (default derived from duration, usually 8-16)
- **`--prefer <loop>`** - optional preferred starting loop (`turbocharge`, `cruise`, `ignition`, `drift`, `nos`, `overdrive`, `autopilot`, `boost`)

If neither a task pattern nor a brief is provided, use `AskUserQuestion` to ask the user for one of:
1. A high-level goal
2. A brief file path
3. "Start from current issue/task"

## When to Use

- The task is ambiguous and may need to change strategy as understanding improves
- You want the agent to pick between multiple loop styles instead of committing up front
- The work may need research, spec generation, parallel help, supervision, and journaling in one run
- You want an orchestration layer above the loop family rather than another single-purpose loop

Do **not** use when you already know the exact right loop and just want to run it directly. Control Tower is for orchestration overhead when the choice itself matters.

## Capability Model

Control Tower should treat every helper as optional until proven available.

### Loop family

Check which execution loops are actually installed in `skills/`:

- `geno-dev-loops-turbocharge`
- `geno-dev-loops-cruise`
- `geno-dev-loops-ignition`
- `geno-dev-loops-drift`
- `geno-dev-loops-nos`
- `geno-dev-loops-overdrive`
- `geno-dev-loops-autopilot`
- `geno-dev-loops-boost`

### Supervisory helpers

Check whether these helpers are available before depending on them:

- `geno-mon`
- `geno-msg`
- `geno-research`
- `geno-specs`
- `geno-agents`
- `geno-notes`

Record the result in `capabilities.md` as `available`, `missing`, or `degraded`.

## Storage

Create a session directory:

```
.geno/loops/control-tower/<YYYYMMDD-HHMM>/
├── session.md
├── brief.md
├── capabilities.md
├── route.md
├── telemetry/
│   ├── cycle_01.md
│   └── ...
├── interventions/
│   ├── intervention_01.md
│   └── ...
├── artifacts/
│   ├── research.md
│   ├── spec.md
│   └── agent-roster.md
└── checkpoints/
    └── active-lane.md
```

Use this directory as the source of truth when external helpers are missing.

## Routing Rubric

Route based on the strongest evidence, not preference alone.

| Loop | Choose when | Fallback if unavailable |
|---|---|---|
| `turbocharge` | A testable spec, acceptance criteria, or contract already exists | `cruise`, then `ignition` |
| `cruise` | There is a clear numbered plan or checklist | `overdrive`, then `ignition` |
| `ignition` | Cold-start bootstrap: goal exists but structure/spec does not | `overdrive`, then `cruise` |
| `drift` | The task is question-heavy and understanding is the bottleneck | `boost`, then local research notes |
| `nos` | The work decomposes into independent parallel items with disjoint write scopes | `overdrive`, then `cruise` |
| `overdrive` | Long-horizon active implementation with periodic re-planning is needed | `cruise`, then `ignition` |
| `autopilot` | The job has become monitoring, maintenance, or regression watching | `boost`, then manual periodic checks |
| `boost` | Time-boxed focus/reflection is more important than route sophistication | `drift`, then manual note cadence |

If `--prefer <loop>` is provided, honor it only when it does not contradict the evidence. If it does contradict the evidence, log the mismatch and choose the evidence-backed route.

## Workflow

### 1. Load context

- Check for geno-notes project scope: `geno-notes list --project --status active --json`
- If a task pattern was provided, activate it: `geno-notes start <pattern> --project`
- If no active task matches and the user gave a goal, create one: `geno-notes add "<goal>" --project`
- Read the brief file if provided; otherwise summarize the issue, task, or goal into `brief.md`
- Detect repo, current branch, default branch, working tree status, and whether a PR already exists
- Write `session.md` header:
  ```markdown
  # Control Tower Session - <YYYY-MM-DD HH:MM>
  ## Config
  - Task: <geno-notes task id or "none">
  - Brief: <brief file path or generated>
  - Duration: <requested duration>
  - Max cycles: <n>
  - Branch: <current branch>

  ## Log
  ```

### 2. Detect capabilities

Build `capabilities.md` with:

- installed loop skills
- installed supervisory helpers
- degraded substitutes

Examples:

- If `geno-mon` is available, supervision can use telemetry and tail output
- If `geno-msg` is missing, intervention must happen by stopping/re-routing rather than messaging a live lane
- If `geno-specs` is missing, write a local `artifacts/spec.md` instead
- If `geno-research` is missing, use a local Drift-style question list in `artifacts/research.md`

Log the capability snapshot to `session.md` and, if `geno-notes` is available:
```bash
geno-notes note "Control Tower started: capability snapshot recorded" --task <id> --kind note --project
```

### 3. Score the task

Classify the work along these dimensions:

- **Spec strength** - how explicit and testable is the target?
- **Plan strength** - is there an ordered runbook already?
- **Question load** - how much of the task is unanswered understanding?
- **Parallelism potential** - are there independent work items?
- **Monitoring intensity** - is the main job active building or passive watching?
- **Route volatility** - how likely is it that the current strategy becomes wrong mid-run?

Write the assessment to `route.md` and choose the initial loop from the rubric.

### 4. Establish the active lane

Create `checkpoints/active-lane.md` with:

```markdown
# Active Lane
## Selected loop
<loop name>
## Why this route won
<reasoning from rubric>
## Success signal
<what would justify staying on this route>
## Stop / switch triggers
<what would force intervention>
## Fallback route
<what to try next if this lane fails>
```

Then start the selected lane:

- If the selected loop skill is installed, open its `SKILL.md` and follow it as the execution contract
- If the loop is not installed, use the fallback route immediately and log degraded mode
- Keep write ownership simple: Control Tower supervises, the active lane executes. Do not let both edit the same tracked files concurrently

### 5. Supervise the lane

At each supervision cycle, collect evidence from as many sources as are available:

1. **Telemetry**
   - If `geno-mon` is available, inspect the active session with:
     - `geno-mon --latest`
     - `geno-mon tail --json`
     - or a specific session id if the lane runs elsewhere
   - Watch for thrashing, repeated recovery, hot files, or stalled progress
2. **Repo state**
   - `git status`
   - changed files and diff size
   - whether checks are running or passing
3. **Lane artifacts**
   - loop session logs
   - checkpoint files
   - claimed milestones vs. actual repo state

Write a telemetry snapshot to `telemetry/cycle_<n>.md` and append a summary to `session.md`.

### 6. Classify the lane state

After each supervision cycle, classify the active lane as one of:

- **healthy** - making bounded progress with verification
- **under-informed** - blocked by missing context or unanswered questions
- **under-specified** - building without a stable target or acceptance criteria
- **thrashing** - repeated edits, repeated errors, or file churn without progress
- **over-parallelized** - conflicts or coordination cost now exceed throughput
- **passive** - active implementation is mostly done and the job has become watching
- **complete** - the current goal is satisfied

Use these signals:

- `geno-mon` thrashing score > `0.3`
- repeated failures on the same check or same files for 2+ cycles
- no new milestone, checkpoint, or verification progress for 2+ cycles
- scope growth without corresponding verification
- manual review shows the loop is solving the wrong problem

### 7. Intervene

Intervene only when the evidence supports it.

#### If the lane is under-informed

- If `geno-research` is available, launch research and save the output to `artifacts/research.md`
- Otherwise create a local research note:
  - key unanswered questions
  - sources or files to inspect
  - findings that affect routing
- After research, usually route to `drift`, `ignition`, or back to the previous lane with the new context

#### If the lane is under-specified

- If `geno-specs` is available, use it to create explicit acceptance criteria or a contract
- Otherwise write `artifacts/spec.md` locally with:
  - target behavior
  - non-goals
  - acceptance criteria
  - verification method
- Then route toward `turbocharge` or `cruise`

#### If the lane is thrashing or off the rails

- If `geno-msg` is available, send a short corrective message that:
  - names the observed drift
  - restates the target
  - narrows the next step
- If `geno-msg` is missing, stop the lane at the next safe checkpoint and re-route directly
- Write an intervention record to `interventions/intervention_<n>.md`

#### If recurring pain suggests specialization

- If `geno-agents` is available, spawn or register specialist help for bounded sidecar work such as:
  - research scout
  - spec author
  - verifier
  - merge coordinator
  - telemetry watcher
- Record agent roles, ownership, and outputs in `artifacts/agent-roster.md`
- If `geno-agents` is missing, keep the specialist roles as explicit checklist sections in `session.md` instead

#### If the lane has become passive

- Route to `autopilot` when available
- Otherwise switch to manual periodic checks and note the degraded mode

### 8. Switch routes when needed

A route switch is justified when:

- the chosen loop is solving the wrong shape of problem
- new research changes the nature of the task
- specs become explicit enough to move from exploration to convergence
- parallel work has converged and now needs sequential integration
- active implementation is done and only monitoring remains

On every switch:

1. Update `route.md`
2. Update `checkpoints/active-lane.md`
3. Log the reason in `session.md`
4. Write a geno-notes entry if available:
   ```bash
   geno-notes note "Control Tower switched route: <from> -> <to> because <reason>" --task <id> --kind decision --project
   ```

### 9. Log to geno-notes throughout

When `geno-notes` is available, log:

- route selection
- route switches
- research findings
- spec creation
- intervention decisions
- specialist agent launches
- milestones
- blockers
- completion summary

Suggested entry patterns:

```bash
geno-notes note "Control Tower route selected: <loop> - <reason>" --task <id> --kind decision --project
geno-notes note "Control Tower intervention: <summary>" --task <id> --kind note --project
geno-notes note "Control Tower milestone: <summary>" --task <id> --kind milestone --project
geno-notes note "Control Tower blocker: <summary>" --task <id> --kind bug --project
```

If `geno-notes` is unavailable, `session.md` becomes the authoritative log.

### 10. Complete or stop

**If the goal is complete:**
1. Write a final summary to `session.md`
2. Capture the winning route history and interventions that mattered
3. Log completion:
   ```bash
   geno-notes note "Control Tower complete: <summary>" --task <id> --kind milestone --project
   ```
4. If the task is fully done: `geno-notes done <id> --project`
5. Stop the loop

**If blocked on the user:**
1. Write a partial summary
2. State the blocker clearly
3. Stop until the user responds

**If duration or max cycles are reached:**
1. Write the best-known state, active route, and next recommended route
2. Log the stop reason
3. Stop cleanly instead of pretending the orchestration should run forever

## Error Recovery

- If the preferred loop is missing, choose the next fallback from the rubric and log degraded mode.
- If `geno-mon` is unavailable, supervise using checkpoint files, git state, and direct inspection instead of telemetry.
- If `geno-msg` is unavailable, intervene by stopping and re-routing rather than by messaging a live lane.
- If `geno-research` is unavailable, create a local research artifact and run a Drift-style question queue manually.
- If `geno-specs` is unavailable, write the missing spec locally and treat it as the handoff artifact.
- If `geno-agents` is unavailable, keep specialist roles sequential and explicit in the session log.
- If `geno-notes` fails, continue working and preserve the full trail in `session.md`.
- If Control Tower switches routes more than twice without net progress, stop and ask the user rather than churning forever.

## What NOT to Do

- **Don't supervise for the sake of supervision.** If the right loop is obvious, use it directly.
- **Don't switch routes every cycle.** Route changes need evidence, not impatience.
- **Don't invoke every ecosystem tool just because it exists.** Use research, specs, agents, and interventions only when the lane truly needs them.
- **Don't let Control Tower and the active lane both modify the same tracked files.** Keep orchestration and execution responsibilities separate.
- **Don't hide degraded mode.** If a dependency is missing, say so in the session artifacts and adapt explicitly.
- **Don't keep a bad lane alive out of sunk-cost bias.** Re-route when the evidence says the current loop is wrong.

## Runtime

No venv or scripts - pure markdown workflow. Uses installed geno ecosystem skills opportunistically, with explicit fallback behavior when they are missing.
