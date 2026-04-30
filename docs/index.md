# geno-dev

Developer and infrastructure skills for AI coding agents. Task execution from lab notes, git commit history rewriting, worktree management, workspace creation, and session forking.

Part of the [geno-tools](https://42euge.github.io/geno-tools) ecosystem.

## Install

```bash
geno-tools install geno-dev
```

Or from within an agent session:

```
/geno-tools install geno-dev
```

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees -- list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |
| `/geno-dev-sessions-fork [session]` | Fork an agent session — extract context to continue in a new session |

## Next steps

- [Getting Started](getting-started.md) -- install, prerequisites, first use
- [Concepts](concepts.md) -- how workspaces, worktrees, and tasks connect
- [Workflows](workflows.md) -- end-to-end examples
- [Commands](commands.md) -- detailed reference for each slash command
