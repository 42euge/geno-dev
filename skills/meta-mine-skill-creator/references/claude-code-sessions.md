# Claude Code session adapter

This adapter handles in-scope sessions produced by Claude Code.

## Discovery

Start with a user-supplied location. Otherwise inspect the local Claude configuration area and look for project-scoped JSONL transcripts, commonly under `~/.claude/projects/`. Treat that location as a discoverable default, not a permanent contract.

Inventory files before reading content. Use file modification time, size, and session or project metadata to enforce the requested scope. A project directory name may encode a path; do not expose that encoded value in the report.

## Record normalization

Validate a sample from each distinct record shape. Current transcripts may include:

- top-level `type: user` with a user message;
- top-level `type: assistant` with an assistant message;
- system, mode, permission, title, attachment, snapshot, and other metadata records;
- sidechain or subagent records marked by fields such as `isSidechain` or agent metadata.

For mining conversation turns:

1. Keep user and assistant message records.
2. Extract text blocks from message content while retaining timestamps, session IDs, working directory, and sidechain status as metadata.
3. Keep tool calls and tool results only when they prove an outcome or explain a correction; summarize large results.
4. Exclude system metadata, snapshots, token or usage data, and binary attachments.
5. Label sidechains and subagents. Do not count a parent session and its copied sidechain as independent recurrence.

Content can be a string or a heterogeneous block list. Unsupported blocks should be counted and reported, not coerced into text.

## Correction windows

For a possible correction, capture the smallest coherent window: the agent action or claim, the user's correction, and the next outcome when present. Keyword matches such as “no” or “actually” are leads, not proof; verify that the user materially changed behavior, scope, authorization, or reasoning.

## Safety

- Do not modify, compact, archive, or delete Claude session files.
- Do not read credential files from the Claude configuration directory.
- Avoid actively changing transcripts; defer them or snapshot their file size and read only up to that boundary.
