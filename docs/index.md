# geno-dev

Developer and infrastructure skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Task execution from lab notes, git commit history rewriting, worktree management, and workspace creation.

Part of the [geno-tools](https://42euge.github.io/geno-tools) ecosystem.

<div class="feature-grid" markdown>

<div class="feature-card" markdown>
<span class="card-icon">:material-clipboard-check:</span>

### Task execution

Pick up tasks from lab notes, assess scope, plan if needed, execute, and mark done — all from a single slash command.

[See command :material-arrow-right:](commands.md#start-task)
</div>

<div class="feature-card" markdown>
<span class="card-icon">:material-source-branch:</span>

### Commit rewriting

Rewrite messy git history into a clean narrative — backup, soft reset, restage in logical chapters.

[See command :material-arrow-right:](commands.md#rewrite-commit-history)
</div>

<div class="feature-card" markdown>
<span class="card-icon">:material-git:</span>

### Worktree management

Manage git worktrees — create for feature branches, list with status, and prune stale ones. Automatically protects Claude Code and geno-tools worktrees.

[See command :material-arrow-right:](commands.md#manage-worktrees)
</div>

<div class="feature-card" markdown>
<span class="card-icon">:material-folder-multiple:</span>

### Workspace creation

Create isolated development workspaces from GitHub issues, JIRA tickets, or feature ideas. Clone repos into color-coded folders with metadata tracking.

[See command :material-arrow-right:](commands.md#create-workspace)
</div>

</div>

## Install

```bash
npx skills add 42euge/geno-dev
```

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |

## Runtime

No venv, no scripts — pure markdown workflows.
