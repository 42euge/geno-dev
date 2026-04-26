# Commands

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
