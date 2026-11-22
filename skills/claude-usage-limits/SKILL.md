---
name: claude-usage-limits
description: Check the current Claude Code session's plan usage and reset times. Use when asked about remaining Claude quota, or when remaining quota matters for planning a long task.
---

Current session usage snapshot:

!`python3 "$HOME/.claude/claude-limit-awareness/usage_limits.py" report '${CLAUDE_SESSION_ID}'`

Use the values above when answering or planning. The percentages are amounts used. If a value is unavailable or the snapshot may be stale, direct the user to Claude Code's native `/usage` view. Use `/usage` for the Fable weekly limit.
