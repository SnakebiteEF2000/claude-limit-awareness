# Claude Limit Awareness

Check your Claude plan usage from the Claude Code terminal. See how much of your **five-hour** and **all-models weekly** allowances you’ve used, and when each resets. Claude Code supplies the usage data through your existing sign-in. No separate login or API key is needed.

| What you type in Claude Code | What happens |
| --- | --- |
| `usage limits` or `usage limits please` | The hook displays the snapshot locally without sending a prompt to Claude. |
| `/claude-usage-limits` | Claude reads the snapshot through the skill and explains the numbers. |
| “How much Claude quota do I have left?” | Claude can invoke the skill. It can also use the skill when quota matters for planning. |
| `/usage` | Claude Code opens its native usage view, including the Fable weekly limit when available on your plan. |

## Quick install

You’ll need the Claude Code CLI, Python 3.8 or newer, and Git. These commands are for macOS and Linux. Sign in to Claude Code as usual before checking usage.

```sh
git clone git@github.com:SnakebiteEF2000/claude-limit-awareness.git
cd claude-limit-awareness

mkdir -p "$HOME/.claude/claude-limit-awareness" "$HOME/.claude/skills/claude-usage-limits"
cp usage_limits.py "$HOME/.claude/claude-limit-awareness/"
cp skills/claude-usage-limits/SKILL.md "$HOME/.claude/skills/claude-usage-limits/"

sed "s|/absolute/path/to/claude-limit-awareness|$HOME/.claude/claude-limit-awareness|g" \
  settings.example.json > "$HOME/.claude/claude-limit-awareness/settings.json"

claude --settings "$HOME/.claude/claude-limit-awareness/settings.json"
```

If you already have the repo, start with the `mkdir` command from the repo directory. The quick install loads the collector as the status line for that launch. It leaves your regular settings file in place.

In the new session, send a normal prompt first so Claude Code has usage data. Then type `usage limits`. Look for a hook message with the two limits and their reset times. To test agent access, ask “How much Claude quota do I have left?”

### Enable it for regular launches

Merge the generated settings into `~/.claude/settings.json`. Add the example `UserPromptSubmit` entry to your existing hook list, and add `statusLine` if you don’t have one. For project-only setup, merge those entries into `.claude/settings.local.json` in that project instead.

If you already have a status-line command you want to keep, configure it to pass a copy of the same JSON stdin to `python3 ~/.claude/claude-limit-awareness/usage_limits.py collect` and continue emitting its usual display output. [Claude Code settings](https://code.claude.com/docs/en/settings) · [Status-line commands](https://code.claude.com/docs/en/statusline)

## Troubleshooting

- **A limit says unavailable.** The hook shows the current session’s latest snapshot. Usage may be missing before the first response, after a reset, or on plans that don’t expose that window. Open `/usage` to check directly.
- **You need the Fable limit.** Use `/usage`. Claude Code’s documented status-line data exposes the five-hour and all-models weekly windows. Fable availability depends on your plan. [Status-line data](https://code.claude.com/docs/en/statusline) · [Fable plan eligibility](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan)
- **Claude answered the trigger as a normal message.** Try `usage limits` or `usage limits please` exactly. Other phrasing can be handled by the agent through the skill. If the exact trigger still goes to Claude, launch with the generated settings file and check that hooks are enabled.
- **The skill is missing.** Start a new Claude Code session and check that the file exists at `~/.claude/skills/claude-usage-limits/SKILL.md`. [Claude Code skills](https://code.claude.com/docs/en/skills)

The tool stores only the supported usage numbers, reset times, and snapshot time in a per-session cache under `~/.cache/claude-limit-awareness/`. You can delete that directory to clear the snapshots.

## Development

Run `python3 -m unittest discover -s tests` from the repo directory.
