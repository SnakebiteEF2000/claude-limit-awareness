# Claude Limit Awareness

Check your Claude plan usage from the Claude Code terminal. See how much of your **five-hour** and **all-models weekly** allowances you’ve used, and when each resets. Claude Code supplies the usage data through your existing sign-in. No separate login or API key is needed.

| What you type in Claude Code | What happens |
| --- | --- |
| `usage limits` or `usage limits please` | The hook displays the snapshot locally without sending a prompt to Claude. |
| `/claude-usage-limits` | Claude reads the snapshot through the skill and explains the numbers. |
| “How much Claude quota do I have left?” | Claude can invoke the skill. It can also use the skill when quota matters for planning. |
| `/usage` | Claude Code opens its native usage view, including the Fable weekly limit when available on your plan. |

## Quick install

You’ll need the Claude Code CLI, Python 3.8 or newer, Node.js with npm, and Git on macOS or Linux. Sign in to Claude Code before checking usage.

```sh
git clone git@github.com:SnakebiteEF2000/claude-limit-awareness.git
cd claude-limit-awareness
python3 install.py
```

If you already have the repo, run `python3 install.py` from its directory. The installer configures regular Claude Code launches with a compact [ccstatusline](https://github.com/sirmalloc/ccstatusline) row showing the model, Git branch, and context bar. It replaces the status-line command, backs up your previous settings, and preserves your existing hooks while adding the usage shortcut.

Start a new Claude Code session as usual. Send a normal prompt, then type `usage limits` for the local snapshot or run `/claude-usage-limits` to have Claude explain it.

To customize the bar, open its editor with the installed executable and config:

```sh
~/.claude/claude-limit-awareness/node_modules/.bin/ccstatusline --config ~/.claude/claude-limit-awareness/ccstatusline.json
```

Save your layout in the editor. The installer already wires the status-line command to the usage collector.

## Troubleshooting

- **A limit says unavailable.** The hook shows the current session’s latest snapshot. Usage may be missing before the first response, after a reset, or on plans that don’t expose that window. Open `/usage` to check directly.
- **You need the Fable limit.** Use `/usage`. Claude Code’s documented status-line data exposes the five-hour and all-models weekly windows. Fable availability depends on your plan. [Status-line data](https://code.claude.com/docs/en/statusline) · [Fable plan eligibility](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan)
- **Claude answered the trigger as a normal message.** Try `usage limits` or `usage limits please` exactly. Other phrasing can be handled by the agent through the skill. If the exact trigger still goes to Claude, start a new session and check that hooks are enabled.
- **The skill is missing.** Start a new Claude Code session and check that the file exists at `~/.claude/skills/claude-usage-limits/SKILL.md`. [Claude Code skills](https://code.claude.com/docs/en/skills)

The tool stores only the supported usage numbers, reset times, and snapshot time in a per-session cache under `~/.cache/claude-limit-awareness/`. You can delete that directory to clear the snapshots.

## Development

Run `python3 -m unittest discover -s tests` from the repo directory.
