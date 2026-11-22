import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "usage_limits.py"


class UsageLimitsTest(unittest.TestCase):
    def test_status_line_to_hook(self):
        now = int(time.time())
        with tempfile.TemporaryDirectory() as home:
            def run(mode, **data):
                return subprocess.check_output(
                    [sys.executable, SCRIPT, mode],
                    input=json.dumps(data),
                    text=True,
                    env={**os.environ, "HOME": home},
                )

            def show(session_id="first", prompt=" usage limits "):
                response = json.loads(run("show", session_id=session_id, prompt=prompt))
                self.assertEqual(response["decision"], "block")
                return response["reason"]

            self.assertIn("Five-hour session: unavailable", show())
            self.assertEqual(run("show", session_id="first", prompt="explain usage limits"), "")
            self.assertEqual(run("collect", session_id="first", rate_limits={
                "five_hour": {"used_percentage": 0, "resets_at": now + 3600},
                "seven_day": {"used_percentage": 23.75, "resets_at": now + 86400},
            }), "")
            self.assertIn("Five-hour session: 0% used", show())
            self.assertIn("Weekly, all models: 23.75% used", show())
            self.assertIn("Weekly, all models: 23.75% used", show(prompt="usage limits please"))
            skill_report = subprocess.check_output(
                [sys.executable, SCRIPT, "report", "first"],
                text=True,
                env={**os.environ, "HOME": home},
            )
            self.assertEqual(skill_report.rstrip(), show())
            self.assertIn("Fable weekly: see /usage", show())
            self.assertIn("Five-hour session: unavailable", show("second"))
            run("collect", session_id="first", rate_limits={
                "five_hour": {"used_percentage": 30, "resets_at": now - 1},
            })
            self.assertIn("Five-hour session: unavailable", show())
            self.assertIn("Weekly, all models: unavailable", show())
            self.assertIn("Five-hour session: unavailable", show("../first"))
