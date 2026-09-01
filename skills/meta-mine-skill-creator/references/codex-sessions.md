# Codex session adapter

This adapter handles in-scope sessions produced by Codex.

## Supported product behavior

Official OpenAI documentation describes saved local chats and the `codex resume`, `codex archive`, `codex unarchive`, and `codex delete` commands. It does not guarantee a stable JSONL schema, so validate local records at runtime rather than treating the field layout below as an API.

Reference: [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-resume).

## Discovery

Start with a user-supplied location. Otherwise inspect saved sessions commonly found under `~/.codex/sessions/`; include `~/.codex/archived_sessions/` only when the user includes archived history. Use session metadata or `codex resume --all` to understand available scope without changing sessions.

Do not invoke `codex delete`, archive, or unarchive while mining.

## Record normalization

Current JSONL transcripts can contain top-level `timestamp`, `type`, and `payload` fields. Relevant shapes may include:

- `session_meta` for session identity and working directory;
- `response_item` with `payload.type: message` and a user or assistant role;
- `event_msg` projections such as user or agent messages;
- turn context, reasoning, tool calls, tool outputs, token counts, and lifecycle events.

For mining conversation turns:

1. Prefer `response_item` message records as the canonical user and assistant stream when present.
2. Use user and agent `event_msg` records only as a fallback or outcome signal; deduplicate them against canonical messages.
3. Exclude developer messages from user-preference evidence. They are instructions supplied to the session, not corrections made by the user.
4. Do not extract hidden reasoning. Summarize tool calls and outputs only when they establish a verified result or the context for a correction.
5. Deduplicate by session, turn order, role, and normalized content. Forked or resumed copies do not count as independent recurrence without a distinct later interaction.

If the local schema differs, report the unknown type counts and adapt only after confirming which records represent visible user and assistant turns.

## Correction windows

Capture the agent behavior immediately before the user's correction and the observable result immediately after it. Distinguish corrections to the model's work from ordinary requirement additions that were not knowable earlier.

## Safety

- Do not modify session, archive, rollout, state database, or configuration files.
- Do not inspect authentication stores or include tokens and account metadata in mining output.
- Avoid actively changing transcripts; defer them or snapshot their file size and read only up to that boundary.
