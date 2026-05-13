---
name: geno-dev-sessions-remote
description: >-
  Start a Claude Code session with remote access in a workspace directory.
  Opens a new Terminal window with claude --remote-control.
  Use when user says /geno-dev-sessions-remote.
argument-hint: "[workspace-path] [--name <session-name>]"
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# Start Remote Session

Launch a Claude Code session with remote access enabled in a target workspace. Opens a new Terminal window running `claude --remote-control`, which provides a URL for connecting from any browser or device.

## Usage

```
/geno-dev-sessions-remote <workspace-path> [--name <session-name>]
/geno-dev-sessions-remote                   # uses current directory
```

## Arguments

- `$ARGUMENTS` — path to the workspace directory. If omitted, uses the current working directory.
- `--name <name>` — optional session name for the remote control session. Defaults to the directory basename.

## Workflow

1. **Resolve path** — if `$ARGUMENTS` contains a path, resolve it. If it's a workspace name, look it up under the user's code directories (`~/code-red/*/`). If empty, use `$PWD`.

2. **Validate** — confirm the directory exists. Check if it's a git repo or contains a `CLAUDE.md`.

3. **Derive session name** — use `--name` if provided, otherwise use the directory basename.

4. **Launch** — open a new Terminal window with:
   ```bash
   osascript -e '
   tell application "Terminal"
       activate
       do script "cd <resolved-path> && claude --remote-control <session-name>"
   end tell'
   ```

5. **Confirm** — tell the user the session is starting and to check the new Terminal window for the remote access URL.

## Examples

```
/geno-dev-sessions-remote /Users/euge/code-red/comfy-geno-ws/comfyGeno
/geno-dev-sessions-remote comfyGeno --name comfy
/geno-dev-sessions-remote   # current directory
```

## Notes

- The remote control session runs in a separate Terminal window because it requires an interactive TTY.
- The session name is passed to `--remote-control` and used to identify the session in the remote control UI.
- Remote sessions can be accessed from any device via the URL printed in the Terminal.
- To stop the session, close the Terminal window or press Ctrl+C.
