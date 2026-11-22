import json
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent
    claude = Path.home() / ".claude"
    install = claude / "claude-limit-awareness"
    settings = claude / "settings.json"
    original = settings.read_text() if settings.exists() else None
    data = json.loads(original) if original is not None else {}
    hooks = data.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    helper = "python3 " + shlex.quote(str(install / "usage_limits.py"))
    hook = {"type": "command", "command": helper + " show"}
    if not any(hook in group["hooks"] for group in hooks):
        hooks.append({"hooks": [hook]})

    install.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["npm", "install", "--prefix", str(install), "--no-audit", "--no-fund", "--save-exact", "ccstatusline@2.2.34"],
        check=True,
    )
    renderer = install / "node_modules" / ".bin" / "ccstatusline"
    config = install / "ccstatusline.json"
    if not config.exists():
        config.write_text(json.dumps({
            "version": 4,
            "lines": [[
                {"id": "model", "type": "model"},
                {"id": "model-divider", "type": "separator"},
                {"id": "branch", "type": "git-branch", "metadata": {"hide": "no-git"}},
                {"id": "context-divider", "type": "separator"},
                {"id": "context", "type": "context-bar"},
            ], [], []],
        }, indent=2) + "\n")
    shutil.copy2(source / "usage_limits.py", install)
    skill = claude / "skills" / "claude-usage-limits"
    skill.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / "skills" / skill.name / "SKILL.md", skill)

    render = shlex.join([str(renderer), "--config", str(config)])
    script = (
        'input=$(cat)\n'
        f'printf \'%s\' "$input" | {helper} collect\n'
        f'printf \'%s\' "$input" | {render}'
    )
    data.setdefault("statusLine", {}).update(type="command", command="sh -c " + shlex.quote(script))
    updated = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    current = settings.read_text() if settings.exists() else None
    if current != original:
        raise SystemExit("Claude Code settings changed during installation. Run the installer again.")
    if original == updated:
        return
    if settings.exists():
        with tempfile.NamedTemporaryFile(prefix="settings.backup-", suffix=".json", dir=install, delete=False) as backup:
            shutil.copy2(settings, backup.name)
        print(f"Previous settings saved to {backup.name}")
    with tempfile.NamedTemporaryFile(mode="w", dir=claude, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(updated)
    try:
        if settings.exists():
            shutil.copymode(settings, temporary)
        temporary.replace(settings)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
