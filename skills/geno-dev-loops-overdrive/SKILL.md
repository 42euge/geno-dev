---
name: geno-dev-loops-overdrive
description: >-
  Long-horizon adaptive execution loop with Planner -> Implementer ->
  Reviewer rotation and checkpoint handoffs. Use when user says
  /geno-dev-loops-overdrive.
argument-hint: "[task] [--brief <file>] [--for <duration>] [--max <n>]"
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# Overdrive Loop

Long-horizon adaptive execution loop. It rotates through three roles — Planner, Implementer, and Reviewer — with a fresh Agent each cycle and a checkpoint handoff between them. Overdrive is the generalized version of Supercharge: built for sustained autonomous work in normal repos, not tied to Kaggle or benchmark harnesses.

## Input

Parse `$ARGUMENTS` for:

- **Task pattern** — fuzzy-matches against geno-notes tasks (optional)
- **`--brief <file>`** — optional issue brief, plan, spec, or notes file to seed the loop
- **`--for <duration>`** — target run length (default: `4h`, typical range: `2h` to `12h`)
- **`--max <n>`** — maximum cycles; overrides duration-derived default

If neither a task pattern nor a brief is provided, use `AskUserQuestion` to ask the user for one of:
1. A high-level goal
2. A brief file path
3. "Start from current issue/task"

## Duration Dial

Each cycle should target roughly 20-30 minutes of focused work before handing off:

| Duration | Default cycles | Typical use |
|---|---|---|
| `2h` | 4 | Focused push on one feature slice |
| `4h` | 8 | Medium feature or refactor |
| `8h` | 16 | Large feature across multiple subsystems |
| `12h` | 24 | Maximum deep autonomous run |

If `--max` is provided, it takes precedence over the duration mapping.

## When to Use

- Large features, migrations, or sustained implementation work that will evolve as you learn
- Work that needs periodic re-planning, not just blind execution
- Branches where you want explicit verification and critique between implementation bursts
- Issue-driven or task-driven work where the agent should keep moving for hours without drifting

Do **not** use when the work already has a fixed ordered plan (use Cruise), when it has a tight pass/fail spec (use Turbocharge), or when the main job is passive monitoring rather than active implementation.

## Storage

Create a session directory:

```
.geno/loops/overdrive/<YYYYMMDD-HHMM>/
├── session.md
├── brief.md
├── checkpoints/
│   ├── cycle_01_planner.md
│   ├── cycle_02_implementer.md
│   ├── cycle_03_reviewer.md
│   └── ...
└── artifacts/
```

Use it as the durable handoff surface across fresh-agent cycles.

## Workflow

### 1. Load context

- Check for geno-notes project scope: `geno-notes list --project --status active --json`
- If a task pattern was provided, activate it: `geno-notes start <pattern> --project`
- If no active task matches and the user gave a goal, create one: `geno-notes add "<goal>" --project`
- Read the brief file if one was provided; otherwise summarize the issue, task, or user goal into `brief.md`
- Detect repo, current branch, default branch, working tree status, and any existing open PR
- Write `session.md` header:
  ```markdown
  # Overdrive Session — <YYYY-MM-DD HH:MM>
  ## Config
  - Task: <geno-notes task id or "none">
  - Brief: <brief file path or generated>
  - Duration: <requested duration>
  - Max cycles: <n>
  - Branch: <current branch>

  ## Log
  ```

### 2. Establish baseline

Capture the starting state before the first role runs:

- Active geno-notes tasks and any task already in progress
- Repo status and ahead/behind state
- Key constraints from the brief
- Known verification targets (tests, docs, commands, manual checks)

Append a baseline note to `session.md` so later reviews can compare progress against a real starting point.

### 3. Pick the next role

Role rotation is strict unless a blocker forces escalation:

1. **Planner**
2. **Implementer**
3. **Reviewer**
4. Repeat from Planner

Rules:

- If there is no prior checkpoint, start with Planner
- If the last Reviewer checkpoint says "complete", stop
- If the last checkpoint says "blocked on user decision", stop and ask the user
- If the last Reviewer checkpoint found regressions or scope drift, the next cycle must be Planner, not another Implementer pass

### 4. Planner cycle

Spawn a fresh **Planner** agent with:

- `brief.md`
- `session.md`
- The latest checkpoint (if any)
- Current repo status and active task list

Planner responsibilities:

- Re-read the task and decide the next 1-3 concrete slices
- Prioritize based on impact, risk, and what was learned in the previous review
- Define explicit verification targets for the next implementation cycle
- Keep scope bounded: the plan should fit one implementer burst, not the whole project

Planner writes `checkpoints/cycle_<n>_planner.md`:

```markdown
# Overdrive Planner Checkpoint — Cycle <n>
## Objective
<what this sprint is trying to achieve>
## Priority slices
1. <slice>
2. <slice>
## Files / areas
<likely files or subsystems>
## Verification target
<tests, commands, docs, manual checks>
## Risks / assumptions
<what could go wrong>
## Handoff to Implementer
<what to do next>
```

### 5. Implementer cycle

Spawn a fresh **Implementer** agent with:

- `brief.md`
- The latest Planner checkpoint
- Relevant local files

Implementer responsibilities:

- Execute the highest-priority slice from the plan
- Make bounded, coherent changes rather than sprawling edits
- Run the lightest useful self-checks before handing off
- Log a milestone to geno-notes when meaningful progress is made:
  ```bash
  geno-notes note "Overdrive implementer cycle <n>: <summary>" --task <id> --kind milestone --project
  ```

Implementer writes `checkpoints/cycle_<n>_implementer.md`:

```markdown
# Overdrive Implementer Checkpoint — Cycle <n>
## What changed
<summary>
## Files modified
<list>
## Checks run
<commands and outcomes>
## Remaining gaps
<what is still incomplete>
## Handoff to Reviewer
<what needs verification>
```

### 6. Reviewer cycle

Spawn a fresh **Reviewer** agent with:

- `brief.md`
- The latest Implementer checkpoint
- Access to the modified files and diff

Reviewer responsibilities:

- Verify the implementer's claims against the actual repo state
- Run targeted checks, spot-check docs, and look for regressions or scope drift
- Decide whether the work is:
  - **ready to continue** with a new plan
  - **complete** for the goal
  - **blocked** on a user decision
  - **failing** and needs course correction
- Log findings to geno-notes:
  ```bash
  geno-notes note "Overdrive review cycle <n>: <finding>" --task <id> --kind note --project
  ```
  Use `--kind bug` instead when the review surfaces a concrete regression.

Reviewer writes `checkpoints/cycle_<n>_reviewer.md`:

```markdown
# Overdrive Reviewer Checkpoint — Cycle <n>
## Verdict
<continue | complete | blocked | replan>
## Evidence
<tests, inspection, docs checks>
## Findings
<bugs, risks, design notes, scope issues>
## Recommended next action
<planner should do X next>
## Handoff to Planner
<what the next cycle must consider>
```

### 7. Log the cycle

After each role cycle:

- Append a short entry to `session.md`
  ```markdown
  ### Cycle <n> — <Planner|Implementer|Reviewer> — <timestamp>
  <summary>
  ```
- Save or reconstruct the checkpoint if the agent forgot to write it
- Keep the checkpoint concise but sufficient for a fresh agent to continue without hidden context

### 8. Loop or complete

**If work remains and cycles < max:**
1. Choose the next role from the rotation
2. Use `ScheduleWakeup` to continue the loop inside `/loop`
3. Prefer short delays (60-180s) during active local work and longer delays only when waiting on external validation

**If the Reviewer says complete:**
1. Write final summary to `session.md`
2. Log completion:
   ```bash
   geno-notes note "Overdrive complete: <summary>" --task <id> --kind milestone --project
   ```
3. If the task is fully done: `geno-notes done <id> --project`
4. Stop the loop and report the result

**If blocked on user input:**
1. Write a partial summary to `session.md`
2. Present the blocker clearly to the user
3. Stop until the user responds

## Context Management

- Every cycle uses a **fresh Agent** to avoid context drift
- The checkpoint is the contract between roles
- `session.md` is append-only history, not the main handoff artifact
- Planner should never rely on memory that was not written down

## Error Recovery

- If Planner produces a vague or oversized sprint, rerun planning once with a tighter scope. If it is still vague, ask the user.
- If Implementer makes no meaningful progress for two implementation cycles on the same slice, force a Planner replan.
- If Reviewer finds a regression, do not continue straight into another implementation burst without a fresh Planner checkpoint.
- If a checkpoint file is missing, reconstruct it from the agent output and `git diff`.
- If `geno-notes` fails, continue the loop and write the missing journal information to `session.md`.
- Never do destructive git operations inside Overdrive: no force pushes, hard resets, rebases, or branch deletions.

## What NOT to Do

- **Don't let Planner write a full-project master plan every cycle.** Plan only the next bounded slice.
- **Don't let Implementer wander outside the planned verification target.** Broad rewrites break the loop.
- **Don't let Reviewer rubber-stamp work.** A review must include evidence or an explicit reason evidence was unavailable.
- **Don't skip the checkpoint.** Hidden context is how multi-hour loops degrade.
- **Don't keep looping once the work is clearly blocked on human judgment.** Stop and escalate.

## Runtime

No venv or scripts — pure markdown workflow. Uses Agent subagents for role rotation and `ScheduleWakeup` for self-pacing within `/loop`.
