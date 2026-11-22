#!/usr/bin/env python3
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


WINDOWS = {"five_hour": "Five-hour session", "seven_day": "Weekly, all models"}


def read_object(stream):
    try:
        data = json.load(stream)
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def valid_windows(data, now):
    windows = {}
    if isinstance(data, dict):
        for key in WINDOWS:
            window = data.get(key)
            if not isinstance(window, dict):
                continue
            used = window.get("used_percentage")
            reset = window.get("resets_at")
            if (type(used) in (int, float) and 0 <= used <= 100
                    and type(reset) is int and now < reset < 253402214400):
                windows[key] = {"used_percentage": used, "resets_at": reset}
    return windows


def collect(path, data, now):
    snapshot = {"captured_at": now, "rate_limits": valid_windows(data.get("rate_limits"), now)}
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    stream = tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False)
    temporary = Path(stream.name)
    try:
        with stream:
            json.dump(snapshot, stream)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def local_time(timestamp):
    return datetime.fromtimestamp(timestamp).astimezone().strftime("%Y-%m-%d %H:%M %Z")


def report(path, now):
    snapshot = {}
    if path is not None:
        try:
            with path.open() as stream:
                snapshot = read_object(stream)
        except OSError:
            pass

    windows = valid_windows(snapshot.get("rate_limits"), now)
    lines = []
    captured = snapshot.get("captured_at")
    if windows and type(captured) is int and 0 < captured <= now:
        lines.append(f"Last snapshot {local_time(captured)}")
    for key, label in WINDOWS.items():
        window = windows.get(key)
        detail = "unavailable · see /usage"
        if window:
            used = window["used_percentage"]
            reset = local_time(window["resets_at"])
            detail = f"{used:g}% used · resets {reset}"
        lines.append(f"{label}: {detail}")
    lines.append("Fable weekly: see /usage")
    return "\n".join(lines)


def snapshot_path(session_id):
    if isinstance(session_id, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,128}", session_id):
        cache = Path.home() / ".cache" / "claude-limit-awareness"
        return cache / f"{session_id}.json"


def main(mode):
    data = read_object(sys.stdin)
    prompt = data.get("prompt")
    if mode == "show" and (
        not isinstance(prompt, str) or prompt.strip() not in ("usage limits", "usage limits please")
    ):
        return

    path = snapshot_path(data.get("session_id"))
    now = int(time.time())
    if mode == "collect":
        if path is not None:
            try:
                collect(path, data, now)
            except OSError as error:
                print(f"Usage snapshot could not be saved: {error}", file=sys.stderr)
    else:
        print(json.dumps({"decision": "block", "reason": report(path, now)}))


if __name__ == "__main__":
    if sys.argv[1:] in (["collect"], ["show"]):
        main(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "report":
        print(report(snapshot_path(sys.argv[2]), int(time.time())))
    else:
        sys.exit("Usage: python3 usage_limits.py {collect|show|report SESSION_ID}")
