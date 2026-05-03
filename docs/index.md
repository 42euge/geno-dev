# geno-dev

Developer and infrastructure skills for AI coding agents. Task execution from lab notes, git commit history rewriting, worktree management, workspace creation, session forking, end-to-end feature shipping, issue-driven development, agentic loops, background monitoring, PR checking and branch auditing, scheduled snoozing, and skill retrospectives.

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
| `/geno-dev-feature-ship [description\|issue URL]` | End-to-end: scope, issue, branch, implement, and PR |
| `/geno-dev-issue-work [number\|query\|URL]` | Pick a GitHub issue or JIRA ticket and work on it (normal or loop mode) |
| `/geno-dev-loops-turbocharge [task] [--spec <file>]` | Spec-driven convergence loop — iterate until all acceptance criteria pass |
| `/geno-dev-loops-cruise [task] [--plan <file>]` | Plan-driven sequential loop — execute a plan one step at a time |
| `/geno-dev-loops-autopilot [task] [--watch <tests\|ci\|lint\|git\|all>]` | Background monitoring loop — watch CI, tests, lint, and git state |
| `/geno-dev-loops-boost [task]` | Pomodoro focus loop — time-boxed work blocks with reflection |
| `/geno-dev-loops-ignition [goal] [--blueprint <file>]` | Cold-start bootstrap loop — turn a high-level goal into a blueprint and verified first slice |
| `/geno-dev-prs-check [repo\|--all]` | Check open PRs and flag ones that may need closing |
| `/geno-dev-branches-audit [repo\|--all]` | Audit all branches — find ones needing PRs, ready to merge, or stale |
| `/geno-dev-scheduling-snooze <time> [prompt]` | Snooze session until a specified time, then execute a prompt |
| `/geno-dev-skills-retro [session] [--skill <name>]` | Meta-harness: analyze a failed session and patch the responsible skill |

## Next steps

- [Getting Started](getting-started.md) -- install, prerequisites, first use
- [Concepts](concepts.md) -- how workspaces, worktrees, and tasks connect
- [Workflows](workflows.md) -- end-to-end examples
- [Commands](commands.md) -- detailed reference for each slash command
