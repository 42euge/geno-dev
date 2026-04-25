# Commands

## Start Task

**`/gt-dev-tasks-start [description]`**

Pick up a task from the project's `geno-tools/labnotes/tasks.md` and start working on it.

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
    If `geno-tools/labnotes/` doesn't exist, the skill will prompt you to run `/gt-lab-notes create` first.

---

## Rewrite Commit History

**`/gt-dev-commits-rewrite [branch] [--onto <base>]`**

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

**`/gt-dev-worktrees-manage [list|create|switch|prune] [args...]`**

Manage git worktrees for the current repository. Workspace-aware — if you're inside a workspace created by `/gt-dev-workspaces-init`, worktrees are placed at `<workspace>/.geno/worktrees/<repo>/<branch>/`. Otherwise, inline at `<repo>/.geno/worktrees/<branch>/`.

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

## Create Workspace

**`/gt-dev-workspaces-init [config|list|<freeform text>]`**

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
    Workspaces and worktrees work together: create a workspace with `/gt-dev-workspaces-init`, then use `/gt-dev-worktrees-manage` inside it for branch-level isolation.
