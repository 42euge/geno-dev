---
name: geno-dev-loops-nos
description: >-
  Burst parallel sprint that identifies independent work items and spawns 2–5 Agent subagents simultaneously.
  Use when user says /geno-dev-loops-nos.
argument-hint: "[task] [--batch <file>] [--n <count>]"
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# NOS Loop (Burst Parallel Sprint)

Burst parallel sprint that identifies independent work items and spawns multiple Agent subagents simultaneously. The orchestrator (you) merges results. This loop is optimized for maximum throughput on embarrassingly parallel tasks where items do not depend on each other.

## Input

Parse `$ARGUMENTS` for:

- **Task pattern** — fuzzy-matches against geno-notes tasks (optional)
- **`--batch <file>`** — path to a file containing a list of independent items (one per line or numbered)
- **`--n <count>`** — number of parallel agents to spawn (default: 3, max: 5)

Batch discovery order if `--batch` is not provided:

1. Check `geno-notes plans/<task-slug>.md` for a list of items
2. Check `.geno/loops/nos/` for a recent session with remaining items
3. If nothing found, use `AskUserQuestion` to ask the user for one of:
   - A batch file path
   - A list of independent items (freeform text — write to `.geno/loops/nos/<session>/batch.md`)
   - "Identify them" — analyze the current task and generate a list of independent sub-tasks

## When to Use

- You have a **list of independent items** that can be worked on in any order
- Items have **zero overlap** in the files they modify (or overlap is minimal and mergeable)
- Generating documentation for multiple modules
- Writing unit tests for multiple independent functions
- Creating configuration files for different environments
- Applying a repetitive fix across multiple files

Do **not** use when steps are sequential (use Cruise), when work needs frequent re-planning (use Overdrive), or when the goal is exploratory (use Drift).

## Workflow

### 1. Load context

- Check for geno-notes project scope: `geno-notes list --project --status active --json`
- If a task pattern was provided, activate it: `geno-notes start <pattern> --project`
- Read the batch file and parse items
- Create session directory:
  ```
  .geno/loops/nos/<YYYYMMDD-HHMM>/
  ├── session.md
  ├── batch.md          (copy of the batch list)
  └── results/
  ```
- Write `session.md` header:
  ```markdown
  # NOS Session — <YYYY-MM-DD HH:MM>
  ## Config
  - Task: <id>
  - Batch: <path>
  - Parallelism (N): <count>
  - Items: <total count>

  ## Queue
  - [ ] Item 1: <desc>
  - [ ] Item 2: <desc>
  ...

  ## Log
  ```

### 2. Batching

Group items into waves of size `N`. Items in a wave will run in parallel.

### 3. Execute Wave

For each item in the current wave, spawn an **Agent subagent** in parallel (without `wait_for_previous: true`).

Each agent prompt includes:
- The item description
- Instructions to perform the work
- Requirement to report results to `<session-dir>/results/item_<id>.md`

Prompt structure:
```
You are executing an independent task as part of a parallel burst (NOS loop).

## Your task
<item description>

## Context
This task is independent. You have full control over your assigned scope.

## When done
Write a result summary to: <session-dir>/results/item_<id>.md

Result format:
  # Item <id> Result
  ## Status
  <Success/Failure>
  ## Summary
  <what was done>
  ## Files modified
  <list>
```

### 4. Merge + Log

Wait for all agents in the wave to finish.

- Read result files from `results/`
- Check for merge conflicts if multiple agents modified the same files (rare for NOS)
- If conflicts exist, resolve them or ask the user
- Update `session.md`: mark items `[x]`, log results:
  ```markdown
  ### Wave <n> — <timestamp>
  - Item <id>: <Status> - <Summary>
  ```
- Log to geno-notes:
  ```bash
  geno-notes note "NOS wave <n> complete: <count> items done" --task <id> --kind milestone --project
  ```

### 5. Next Wave

If items remain in the queue, proceed to the next wave (step 3).

### 6. Completion

1. Write final summary to `session.md`:
   ```markdown
   ## Summary
   - Total items: <total>
   - Success: <s_count>
   - Failure: <f_count>
   - Duration: <start to end>
   ```
2. Log completion: `geno-notes note "NOS complete: <total> items processed" --task <id> --kind milestone --project`
3. If the task is fully done: `geno-notes done <id> --project`
4. Report results to the user.

## Error Recovery

- If an agent fails, log the failure and continue with other items.
- If a wave results in significant errors, stop the loop and ask the user.
- If parallelism causes system load issues (timeouts), reduce `N` for the next wave.

## What NOT to Do

- **Don't run dependent tasks in parallel.** If Item B needs Item A, use Cruise.
- **Don't exceed N=5.** High parallelism can lead to context exhaustion or rate limits.
- **Don't ignore failures.** Log them clearly for the user to review.

## Runtime

Pure markdown workflow. Uses Agent subagents for parallel execution.
