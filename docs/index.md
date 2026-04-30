# geno-dev

Developer and infrastructure skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Task execution from lab notes, git commit history rewriting, worktree management, workspace creation, and session forking.

Part of the [geno-tools](https://42euge.github.io/geno-tools) ecosystem.

## What's included

- **Task execution** -- pick up tasks from lab notes, assess scope, plan if needed, execute, and mark done
- **Commit rewriting** -- rewrite messy git history into a clean narrative with backup and verification
- **Worktree management** -- create, list, switch, and prune git worktrees with workspace awareness
- **Workspace creation** -- create isolated dev workspaces from GitHub issues, JIRA tickets, repos, or ideas
- **Session forking** -- extract full context from a Claude Code session to continue in a new one

## Install

```bash
npx skills add 42euge/geno-dev
```

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees -- list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |
| `/geno-dev-sessions-fork [session]` | Fork a Claude Code session to continue in a new session |

## Next steps

- [Getting Started](getting-started.md) -- install, prerequisites, first use
- [Concepts](concepts.md) -- how workspaces, worktrees, and tasks connect
- [Workflows](workflows.md) -- end-to-end examples
- [Commands](commands.md) -- detailed reference for each slash command
