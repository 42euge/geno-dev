# Workflows

Practical examples showing how geno-dev skills work together in real development scenarios. Each workflow is self-contained.

## Issue to PR

The complete lifecycle from GitHub issue to shipped pull request.

### 1. Create a workspace from the issue

```
/geno-dev-workspaces-init https://github.com/42euge/geno-dev/issues/42
```

The skill fetches the issue, clones the repo, and creates a workspace:

```
~/code-purp/GH-geno-dev-42-fix-auth-token-ws/
  .geno/workspace.yaml
  CLAUDE.local.md
  geno-dev/
```

### 2. Set up task tracking

```
cd ~/code-purp/GH-geno-dev-42-fix-auth-token-ws/geno-dev/
```

```
geno-notes init --project
geno-notes add "Fix auth token expiry bug from issue #42"
```

### 3. Create a feature worktree

```
/geno-dev-worktrees-manage create feature/fix-auth-token
```

This creates a worktree at `.geno/worktrees/geno-dev/feature/fix-auth-token/` and prints the path.

### 4. Start the task

```
/geno-dev-tasks-start fix auth token
```

The skill finds the matching task, assesses scope, plans if needed, and executes. Milestones are logged to the journal as work progresses.

### 5. Rewrite commits

After the work is done, clean up the history:

```
/geno-dev-commits-rewrite
```

The skill analyzes the messy commits, proposes a clean narrative (e.g., 4 commits: add test → fix token refresh → update config → add docs), and asks for approval before rewriting.

### 6. Push and open a PR

```bash
git push -u origin feature/fix-auth-token
gh pr create --title "Fix auth token expiry" --body "Closes #42"
```

---

## Multi-repo Workspace

Working on a feature that spans multiple repositories.

### 1. Create workspace from an idea

```
/geno-dev-workspaces-init add worktree awareness to geno-dev and geno-tools
```

The skill scans known repos, suggests relevant ones, and lets you pick:

```
~/code-red/worktree-awareness-ws/
  geno-dev/
  geno-tools/
```

### 2. Create worktrees in each repo

```
cd ~/code-red/worktree-awareness-ws/geno-dev/
```

```
/geno-dev-worktrees-manage create feature/worktree-awareness
```

Then switch to the other repo and do the same:

```
cd ~/code-red/worktree-awareness-ws/geno-tools/
```

```
/geno-dev-worktrees-manage create feature/worktree-awareness
```

Both worktrees live under the workspace's `.geno/worktrees/`, grouped by repo:

```
.geno/worktrees/
  geno-dev/feature/worktree-awareness/
  geno-tools/feature/worktree-awareness/
```

### 3. Work and ship each repo separately

Each repo gets its own commits, rewrite, and PR. The workspace just keeps them together on disk.

---

## Session Handoff

Continuing interrupted work in a fresh Claude Code session.

### 1. Fork the session

```
/geno-dev-sessions-fork
```

The skill lists recent sessions with timestamps and working directories. Pick the one to fork.

### 2. Context document is produced

The output includes everything a new session needs:

```markdown
## Environment
- Working directory: ~/code-red/geno-dev-ws/geno-dev
- Branch: feature/fix-auth-token
- Model: claude-sonnet-4-6

## Files Modified
- src/auth/token.ts
- tests/auth/token.test.ts

## Commands Run (last 30)
- npm test
- git diff
...

## Conversation History
...
```

### 3. Continue in a new session

Start a new Claude Code session in the same directory and paste the context document. The new session picks up where the old one left off — same files, same branch, same decisions.

---

## Worktree Cleanup

Periodic maintenance after multiple features have shipped.

### 1. List all worktrees

```
/geno-dev-worktrees-manage list
```

Shows a table with path, branch, status (clean/dirty), and category (`[user]`, `[claude-code]`, `[geno-tools]`).

### 2. Prune merged and stale branches

```
/geno-dev-worktrees-manage prune
```

The skill identifies worktrees whose branches have been merged or deleted from the remote. It presents candidates and asks for confirmation before removing anything.

Claude Code and geno-tools worktrees are never included in prune candidates.

### 3. Dry run first

Not sure what will be removed? Use `--dry-run`:

```
/geno-dev-worktrees-manage prune --dry-run
```

---

## Tips

!!! tip "You don't need a workspace"
    Worktrees, tasks, and commit rewriting all work without a workspace. Workspaces add value when you're juggling multiple repos for one feature or want clean isolation from your main checkout.

!!! tip "Set up geno-notes early"
    If you plan to use `/geno-dev-tasks-start`, run `geno-notes init --project` in your repo before starting. The skill will prompt you if it's missing, but it's smoother to have it ready.

!!! tip "Backup branches are your safety net"
    `/geno-dev-commits-rewrite` always creates `backup-before-rewrite` before touching history. If something goes wrong, `git reset --hard backup-before-rewrite` gets you back to where you started.
