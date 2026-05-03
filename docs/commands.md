# Commands

Detailed reference for each geno-dev slash command. For conceptual background see [Concepts](concepts.md); for end-to-end examples see [Workflows](workflows.md).

## Start Task

**`/geno-dev-tasks-start [description]`**

Pick up a task from geno-notes and start working on it.

### Input

The user optionally provides a task description or number. If empty, shows the task list and asks which one to start.

### Workflow

1. **Load context** — reads `tasks.md`, `notes.md`, existing plans, and project instructions
2. **Select the task** — fuzzy-match from arguments or interactive selection from Active/Backlog
3. **Assess scope** — small tasks skip planning; medium/large tasks enter plan mode
4. **Plan** (if needed) — enters plan mode, explores codebase, saves plan to `plans/<task-slug>.md`
5. **Execute** — works through the task, logging milestones to `notes.md`
6. **Complete** — marks done in `tasks.md`, summarizes work, suggests next task

!!! tip
    If no geno-notes scope exists, the skill will prompt you to run `geno-notes init --project` first.

**See also:** [Tasks concept](concepts.md#tasks) · [Issue to PR workflow](workflows.md#issue-to-pr)

---

## Rewrite Commit History

**`/geno-dev-commits-rewrite [branch] [--onto <base>]`**

Rewrite git commit history so it tells a clear, logical narrative — as if the work was done in clean, intentional steps from the start.

### Input

- A branch name (default: current branch)
- `--onto <base>` to specify the base branch (default: auto-detect merge-base with main/master)

### Workflow

1. **Analyze** — inspects commit log, status, and diffs
2. **Understand** — reads diffs and lab notes to identify the logical narrative
3. **Plan** — presents proposed commits to the user for approval
4. **Execute** — creates backup branch, soft resets, restages files into clean commits
5. **Verify** — confirms no content lost (`git diff backup-before-rewrite` should be empty)
6. **Clean up** — optionally deletes backup branch

!!! warning
    Always creates a `backup-before-rewrite` branch before modifying history. Force push with `--force-with-lease` only after user confirmation.

### Guidelines for good narrative commits

- Each commit should be a single logical unit that makes sense on its own
- Build on each other in natural progression: scaffold → core → implementation → polish
- 3–8 commits is usually the sweet spot
- Explain the "why", not just the "what"

**See also:** [Commits as Narrative](concepts.md#commits-as-narrative) · [Issue to PR workflow](workflows.md#issue-to-pr)

---

## Manage Worktrees

**`/geno-dev-worktrees-manage [list|create|switch|prune] [args...]`**

Manage git worktrees for the current repository. Workspace-aware — if you're inside a workspace created by `/geno-dev-workspaces-init`, worktrees are placed at `<workspace>/.geno/worktrees/<repo>/<branch>/`. Otherwise, inline at `<repo>/.geno/worktrees/<branch>/`.

### Subcommands

- **list** (default) — show all worktrees with branch, status, and category tags
- **create `<branch>` `[--from <base>]`** — create a new worktree (uses workspace if available, otherwise inline)
- **switch `<name>`** — find a worktree and print navigation instructions
- **prune `[--dry-run]`** — remove stale/merged worktrees with interactive confirmation

### Safety

The skill automatically detects and protects:

- **Claude Code worktrees** (`.claude/worktrees/`) — never modified or removed
- **geno-tools meta-harness worktrees** (`~/.geno/`) — warned before any action

This skill never edits a project's `.gitignore`, `CLAUDE.md`, or any tracked files.

**See also:** [Worktrees concept](concepts.md#worktrees) · [Multi-repo workspace workflow](workflows.md#multi-repo-workspace) · [Worktree cleanup workflow](workflows.md#worktree-cleanup)

---

## Fork Session

**`/geno-dev-sessions-fork [session] [--output <file>] [--max-messages <N>]`**

Fork an agent session — extract the full context (environment, files touched, conversation history) and produce a structured markdown document for continuing work in a new session.

### Prerequisites

- `geno-mon` must be installed and available on `$PATH`

### Workflow

1. **Discover** — runs `geno-mon list` to show recent sessions
2. **Select** — uses the user's argument or asks them to pick
3. **Extract** — runs `geno-mon fork <session>` to produce the context document
4. **Deliver** — writes to file or displays, with instructions on how to use it

### Options

| Flag | Description |
|---|---|
| `<session>` | Session number, partial ID, or JSONL path (default: latest) |
| `-o <file>` | Write output to a file instead of stdout |
| `-m <N>` | Maximum user messages to include (default: 50) |

!!! tip
    The fork output includes environment, files modified/read, commands run, and full conversation history — everything a new session needs to continue where the original left off.

**See also:** [Sessions concept](concepts.md#sessions) · [Session handoff workflow](workflows.md#session-handoff)

---

## Create Workspace

**`/geno-dev-workspaces-init [config|list|<freeform text>]`**

Create isolated development workspaces by cloning repos into color-coded folders. Accepts freeform text — the skill infers whether it's a GitHub issue, JIRA ticket, repo names, or a feature idea.

### Input modes (inferred from freeform text)

- **GitHub issue** — input contains a `github.com` URL → fetches issue, clones the repo
- **JIRA ticket** — input matches `[A-Z]+-\d+` → uses as naming label, prompts for repos
- **Repos** — input looks like repo names or URLs → clones them
- **Idea** — anything else → AI scans `.geno-agents` files and suggests relevant repos

### Naming

| Source | Format | Example |
|---|---|---|
| GitHub issue | `GH-{repo}-{n}-{slug}-ws` | `GH-geno-dev-42-fix-auth-token-ws` |
| JIRA ticket | `{PROJ-N}-{slug}-ws` | `PROJ-1234-migrate-db-schema-ws` |
| Repos / Idea | `{slug}-ws` | `voice-coding-assist-ws` |

### Config

Workspace settings at `~/.geno/config.yaml` (auto-created on first use):

- `config` — view current settings
- `config default <color>` — set default color folder
- `config add <color>` — add a color folder

### Listing

`list` scans all configured color folders for workspaces. Shows metadata from `.geno/workspace.yaml`, tags legacy `*-WS/` dirs and unmanaged `*-ws/` dirs.

!!! tip
    Workspaces and worktrees work together: create a workspace with `/geno-dev-workspaces-init`, then use `/geno-dev-worktrees-manage` inside it for branch-level isolation.

**See also:** [Workspaces concept](concepts.md#workspaces) · [Structuring code folders](concepts.md#structuring-code-folders) · [Issue to PR workflow](workflows.md#issue-to-pr)

---

## Drift Loop

**`/geno-dev-loops-drift [question] [--max <n>]`**

Question-driven exploration loop. Ideal for codebase archaeology, debugging complex issues, or understanding unfamiliar systems.

### Input

- **Starting question** — the initial inquiry to kick off exploration (optional)
- **`--max <n>`** — maximum cycles (default: 10)

If no starting question is provided, the skill asks what you want to explore.

### Workflow

1. **Load context** — finds active geno-notes task (if any), creates session directory at `.geno/loops/drift/<timestamp>/`
2. **Initialize queue** — writes the starting question to a prioritized `questions.md` queue
3. **Pick next question** — selects the highest priority open question from the queue
4. **Explore and answer** — investigates the codebase to answer the question. Documents findings in `session.md`
5. **Finalize answer** — marks the question as done, logs milestones to geno-notes
6. **Loop or complete** — if more questions in queue and cycles < max, schedules next cycle (180–270s). Stops when all questions answered or max cycles reached

!!! tip
    Drift is a "journal-entry factory." Its primary value is the trail of findings, decisions, and bugs it leaves in your lab notes while following an exploratory thread.

---

## Ship Feature

**`/geno-dev-feature-ship [description|issue URL]`**

Take a feature idea from scoping through implementation to a pull request.

### Input

- A freeform feature description
- An existing GitHub issue URL

If no argument is provided, the skill asks what the user wants to build.

### Workflow

1. **Scope the feature** — clarify requirements with the user, or fetch the linked GitHub issue
2. **Create the issue** — draft and create a GitHub issue when starting from a freeform idea
3. **Create the branch** — branch from the default branch with a descriptive name
4. **Implement** — explore, plan if needed, code, document, and verify
5. **Open the PR** — create a pull request that links back to the issue
6. **Wrap up** — summarize what shipped and note any follow-up scope

!!! tip
    Use this when the work starts as an idea. If the issue already exists and you want to execute it directly, use `/geno-dev-issue-work`.

**See also:** [Issue to PR workflow](workflows.md#issue-to-pr)

---

## Work on Issue

**`/geno-dev-issue-work [number|query|URL]`**

Pick a GitHub issue or JIRA ticket and execute it with either interactive or autonomous flow.

### Input

- A GitHub issue number
- A JIRA key like `PROJ-1234`
- A GitHub or JIRA URL
- A search query for finding the issue

### Workflow

1. **Detect source** — determine GitHub vs. JIRA from the argument
2. **Select the issue** — fetch directly or search and let the user choose
3. **Read context** — summarize the issue body, constraints, and comments
4. **Choose execution mode** — normal interactive mode or autonomous loop mode
5. **Choose workspace strategy** — worktree or in-place
6. **Create the branch** — branch from the default branch using the issue number or ticket key
7. **Implement and ship** — do the work, verify it, and open the PR

### Modes

- **Normal mode** — interactive back-and-forth, best for ambiguous work
- **Loop mode** — autonomous execution with periodic check-ins, best for well-defined work

!!! tip
    Prefer a separate worktree when your current checkout is dirty or you want parallel issue work without disturbing the main clone.

**See also:** [Issue to PR workflow](workflows.md#issue-to-pr) · [Manage Worktrees](#manage-worktrees)

---

## Turbocharge Loop

**`/geno-dev-loops-turbocharge [task] [--spec <file>] [--max <n>]`**

Spec-driven convergence loop. Takes a testable specification (test suite, acceptance criteria, type contract) and iterates until every criterion passes.

### Input

- A task pattern to fuzzy-match against geno-notes tasks (optional)
- `--spec <file>` — path to the spec file (test suite, criteria list, type definitions)
- `--max <n>` — maximum iterations (default: 8)

If no spec is provided, the skill asks for a test file, acceptance criteria, or API contract.

### Workflow

1. **Load context** — finds geno-notes task, reads spec, creates session directory at `.geno/loops/turbocharge/<timestamp>/`
2. **Validate spec (baseline)** — runs spec check, records which criteria pass and fail
3. **Identify gaps** — prioritizes: quick wins, blockers, isolated fixes, then hard items
4. **Implement fixes** — makes targeted changes for the top gaps. Small and focused per iteration
5. **Re-validate** — runs spec check again, logs newly-passing criteria as geno-notes milestones
6. **Loop or complete** — if all pass, done. If not, schedules next iteration (60–120s). Stops at max iterations

### Spec types supported

| Spec type | Validation |
|---|---|
| Test file (`.test.*`) | Test runner (`npm test`, `pytest`, etc.) |
| Type definitions (`.d.ts`, `.pyi`) | Type checker (`tsc`, `mypy`, etc.) |
| Acceptance criteria (`.md`) | Manual criterion-by-criterion check |
| API contract (OpenAPI, protobuf) | Contract validation or diff |

!!! tip
    Best for TDD workflows: write your tests first, then run `/geno-dev-loops-turbocharge --spec tests/my-feature.test.ts` and let it grind until green.

---

## Cruise Loop

**`/geno-dev-loops-cruise [task] [--plan <file>]`**

Plan-driven sequential execution. Takes a plan with numbered steps and executes them one at a time, each in a fresh agent with checkpoint handoff.

### Input

- A task pattern to fuzzy-match against geno-notes tasks (optional)
- `--plan <file>` — path to a plan file with numbered steps

If no plan is provided, checks `geno-notes plans/` for the task's plan, then asks the user.

### Workflow

1. **Load context** — finds geno-notes task, reads plan, creates session directory at `.geno/loops/cruise/<timestamp>/`
2. **Parse plan** — extracts numbered steps, creates a checklist, identifies dependencies
3. **Pick next step** — selects the first uncompleted step, reads previous checkpoint
4. **Execute step** — spawns an agent with the step description + previous checkpoint. Agent writes result to `checkpoints/step_<n>.md`
5. **Verify + log** — reads checkpoint, spot-checks changes, logs geno-notes milestone
6. **Loop or complete** — if more steps, repeat. If all done, write summary. If a step fails twice, stop and ask user

!!! tip
    Pairs well with plan mode: use `/geno-dev-tasks-start` to plan a complex task, then run `/geno-dev-loops-cruise --plan geno/geno-notes/plans/<task>.md` to execute it.

---

## Overdrive Loop

**`/geno-dev-loops-overdrive [task] [--brief <file>] [--for <duration>] [--max <n>]`**

Long-horizon adaptive execution. Rotates through Planner, Implementer, and Reviewer roles in fresh agents, using checkpoint handoffs to sustain multi-hour work without silent context drift.

### Input

- A task pattern to fuzzy-match against geno-notes tasks (optional)
- `--brief <file>` — seed the loop from an issue brief, plan, spec, or notes file
- `--for <duration>` — target run length; defaults to `4h` and typically ranges from `2h` to `12h`
- `--max <n>` — maximum cycles; overrides the duration-derived default

### Workflow

1. **Load context** — activate the task, summarize or copy the brief, detect repo state, and create `.geno/loops/overdrive/<timestamp>/`
2. **Capture baseline** — record current constraints, branch state, and verification targets
3. **Planner cycle** — choose the next bounded sprint slice and define what success looks like
4. **Implementer cycle** — make focused progress on that slice and log milestones
5. **Reviewer cycle** — verify the actual changes, record findings, and decide whether to continue, stop, or re-plan
6. **Repeat rotation** — continue Planner -> Implementer -> Reviewer until complete, blocked, or at max cycles

### Role rotation

- **Planner** — reads the active task and previous checkpoint, then picks the next 1-3 concrete slices
- **Implementer** — executes the highest-priority slice and records what changed
- **Reviewer** — validates the work, looks for regressions or scope drift, and drives the next handoff

### Duration mapping

| Duration | Default cycles |
|---|---|
| `2h` | 4 |
| `4h` | 8 |
| `8h` | 16 |
| `12h` | 24 |

!!! tip
    Use Overdrive when the work is too long or dynamic for Cruise, but still goal-oriented enough that each cycle should end with a concrete decision or verification result.

---

## Autopilot Loop

**`/geno-dev-loops-autopilot [task] [--watch <tests|ci|lint|git|all>] [--every <15m|30m>] [--for <duration>]`**

Background monitoring loop. Watches a branch or PR over a long window and reacts to regressions or maintenance opportunities.

### Input

- A task pattern to match against geno-notes (optional)
- `--watch <tests|ci|lint|git|all>` — which signals to monitor
- `--every <15m|30m>` — how often to wake up
- `--for <duration>` — total monitoring window, up to the `CronCreate` 7-day limit

### Workflow

1. **Load context** — detect repo, branch, PR context, active task, and create `.geno/loops/autopilot/<timestamp>/`
2. **Capture baseline** — record current test, lint, CI, and git state for the chosen watch set
3. **Schedule monitoring** — use `CronCreate` for 15–30 minute recurring checks
4. **React on each cycle** — re-check signals, retry transient failures once, apply safe deterministic fixes, or escalate
5. **Journal outcomes** — log cycles to `session.md` and write bug notes, milestones, or follow-up tasks via geno-notes
6. **Stop cleanly** — finish when the duration expires, the PR merges, or a human decision is needed

### Safe auto-fixes

- Formatter or lint autofix commands with immediate verification
- Deterministic generated-file refreshes for repos that already track generated outputs
- A single retry for likely transient CI or test failures

!!! tip
    Autopilot is for low-intensity background maintenance. If the work turns into active implementation, switch to Turbocharge or Cruise.

---

## Boost Loop

**`/geno-dev-loops-boost [task] [--work <min>] [--reflect <min>]`**

Time-boxed focus sessions (Pomodoro). Works for 25 minutes, then stops for 5 minutes of reflection and journal logging.

### Input

- A task pattern to fuzzy-match against geno-notes tasks (optional)
- `--work <min>` — duration of the work phase in minutes (default: 25)
- `--reflect <min>` — duration of the reflection phase in minutes (default: 5)

### Workflow

1. **Load context** — finds geno-notes task, creates session directory at `.geno/loops/boost/<timestamp>/`
2. **Start Work Phase** — calls `ScheduleWakeup` for the work duration and starts autonomous work on the task
3. **Reflect Phase** — triggered by wakeup. The agent summarizes accomplishments, identifies findings/decisions, and writes a reflection note to `geno-notes`
4. **Continue or Finish** — updates the session log and asks the user whether to start another block, finish the session, or change tasks

!!! tip
    Perfect for open-ended exploration, debugging, or complex investigations where you want to ensure you don't lose track of progress and maintain a steady journal.

---

## Ignition Loop

**`/geno-dev-loops-ignition [goal] [--blueprint <file>] [--max <n>]`**

Cold-start bootstrap loop. Takes a high-level goal, generates or loads a blueprint, then bootstraps the work in layers: structure, implementation, and verification.

### Input

- A high-level goal to bootstrap
- An optional task pattern to fuzzy-match against geno-notes tasks
- `--blueprint <file>` — start from an existing blueprint instead of generating one
- `--max <n>` — maximum layers or iterations (default: 6)

If no goal or blueprint is provided, the skill asks the user for one.

### Workflow

1. **Load or create task context** — finds or creates a geno-notes task, starts it, and creates a session directory at `.geno/loops/ignition/<timestamp>/`
2. **Generate blueprint** — inspects the issue, repo, and constraints, then writes a living blueprint with deliverables, structure, layers, and verification plan
3. **Pick next layer** — chooses the thinnest meaningful layer to bootstrap next, avoiding broad over-scaffolding
4. **Scaffold** — a Scaffolder role creates the minimum structure and writes a checkpoint
5. **Build** — a Builder role fills in the scaffold with a coherent first implementation and writes a checkpoint
6. **Verify** — a Verifier role runs the lightest meaningful validation, records evidence, and recommends the next layer
7. **Evolve blueprint** — updates the blueprint and session log with what became concrete during the layer
8. **Loop or complete** — continues until there is a verified first slice or the max layer count is reached

### Best Fit

Use Ignition when you're starting from a rough goal and need the first working slice to take shape. If you already have a numbered plan, use Cruise. If you already have a testable spec, use Turbocharge.

!!! tip
    A good Ignition prompt is short and outcome-oriented: `/geno-dev-loops-ignition bootstrap a new skill for parsing deployment logs` is enough to start with blueprint generation.

---

## Check PRs

**`/geno-dev-prs-check [repo|--all]`**

Check open pull requests for repos in the current session. Produces a table highlighting PRs that may need to be closed — stale branches, drafts, or PRs with deleted head branches.

### Input

- Empty — checks the current repo (from `git remote -v`)
- A repo name or `owner/repo` — checks that specific repo
- `--all` — if inside a workspace, checks all repos in `.geno/workspace.yaml`

### Status Tags

Each PR is classified with a status tag:

| Tag | Meaning |
|-----|---------|
| `CLOSEABLE` | Head branch deleted or already merged — PR is stale |
| `STALE` | No updates in 30+ days |
| `BLOCKED` | Changes requested or merge conflicts |
| `DRAFT` | Marked as draft |
| `APPROVED` | Approved and ready to merge |
| `OPEN` | Normal open PR |

### Output

A markdown table sorted by priority (closeable first), always including a link:

```
| # | Title | Author | Branch | Age | Status | Link |
|---|-------|--------|--------|-----|--------|------|
| 47 | Remove legacy auth middleware | 42euge | fix/auth → main | 45d | CLOSEABLE | https://... |
| 52 | Add worktree safety checks | 42euge | feature/wt → main | 12d | APPROVED | https://... |
```

Followed by a summary line with counts per status and a hint for closing stale PRs.

---

## Audit Branches

**`/geno-dev-branches-audit [repo|--all]`**

Audit all branches across a workspace or repo. For each branch, determines whether a PR exists, what state it's in, and what action is needed.

### Input

- Empty — audits the current repo
- A repo name or `owner/repo` — audits that specific repo
- `--all` — if inside a workspace, audits all repos in `.geno/workspace.yaml`

### Status Tags

| Tag | Meaning |
|-----|---------|
| `PR MERGED` | PR was merged but branch still exists (cleanup candidate) |
| `PR CLOSED` | PR was closed without merge, branch still exists |
| `PR APPROVED` | PR approved, ready to merge |
| `PR BLOCKED` | Changes requested or merge conflicts |
| `PR DRAFT` | PR is a draft |
| `PR OPEN` | Normal open PR |
| `NEEDS PR` | Has commits ahead of default, no PR exists |
| `STALE` | No PR, no updates in 30+ days |
| `NO CHANGES` | Branch has zero commits ahead of default (delete candidate) |

### Output

A table per repo showing branch name, commits ahead, age, worktree path, PR link, and status tag. Followed by grouped suggested actions with copy-pasteable commands.

!!! tip
    Complements `/geno-dev-prs-check` which only looks at open PRs. This skill finds branches that *don't* have PRs yet, and branches whose PRs have already been merged or closed.

---

## Snooze

**`/geno-dev-scheduling-snooze <time> [prompt]`**

Delay the current session's work until a specified time. Parses natural language time expressions and schedules a wakeup via `ScheduleWakeup`.

### Input

A time expression followed by an optional prompt describing what to do on wakeup.

| Format | Examples |
|---|---|
| Absolute clock time | `3:30 AM`, `15:30`, `3:30am` |
| Relative duration | `in 2 hours`, `45m`, `2h` |
| Named time | `tomorrow at 9am`, `tonight at midnight` |

### Workflow

1. **Parse time** — extracts time expression, resolves to seconds from now
2. **Resolve prompt** — uses provided prompt or asks the user
3. **Chain if needed** — if delay exceeds 3600s (ScheduleWakeup max), chains hourly wakeups that re-snooze until the target
4. **Schedule** — calls ScheduleWakeup with computed delay and prompt
5. **Confirm** — reports target time, delay, chain count, and wakeup action

### Examples

```
/geno-dev-scheduling-snooze 3:30 AM start working on the auth refactor
→ Snoozing until 3:30 AM PDT (in 3h 19m). On wake: "start working on the auth refactor"

/geno-dev-scheduling-snooze 45m run the benchmark suite
→ Snoozing for 45 minutes. On wake: "run the benchmark suite"

/geno-dev-scheduling-snooze in 10 minutes
→ (asks what to do on wakeup, then schedules)
```

!!! tip
    For delays longer than 1 hour, the skill automatically chains hourly wakeups. Each hop re-checks the clock and re-snoozes until the target time is reached.
