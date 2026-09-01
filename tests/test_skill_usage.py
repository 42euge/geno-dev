from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from geno_dev.usage import record_invocation, summarize_invocations


class SkillUsageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database = Path(self.temporary_directory.name) / "usage.sqlite3"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_records_only_minimal_invocation_fields(self) -> None:
        record_invocation(
            self.database,
            skill_name="example-skill",
            trigger="explicit",
            invoked_at=datetime(2026, 8, 1, 12, tzinfo=timezone.utc),
        )

        with sqlite3.connect(self.database) as connection:
            connection.row_factory = sqlite3.Row
            columns = [
                row["name"]
                for row in connection.execute("PRAGMA table_info(skill_invocations)")
            ]
            row = connection.execute(
                "SELECT skill_name, invoked_at, trigger FROM skill_invocations"
            ).fetchone()

        self.assertEqual(columns, ["id", "skill_name", "invoked_at", "trigger"])
        self.assertEqual(row["skill_name"], "example-skill")
        self.assertEqual(row["invoked_at"], "2026-08-01T12:00:00Z")
        self.assertEqual(row["trigger"], "explicit")
        self.assertEqual(self.database.stat().st_mode & 0o777, 0o600)

    def test_report_counts_period_triggers_and_active_days(self) -> None:
        for timestamp, trigger in (
            (datetime(2026, 7, 1, tzinfo=timezone.utc), "explicit"),
            (datetime(2026, 8, 20, tzinfo=timezone.utc), "explicit"),
            (datetime(2026, 8, 20, 12, tzinfo=timezone.utc), "implicit"),
            (datetime(2026, 8, 31, tzinfo=timezone.utc), "implicit"),
        ):
            record_invocation(
                self.database,
                skill_name="example-skill",
                trigger=trigger,
                invoked_at=timestamp,
            )

        report = summarize_invocations(
            self.database,
            skill_name="example-skill",
            days=30,
            now=datetime(2026, 9, 1, tzinfo=timezone.utc),
        )

        self.assertEqual(report["all_time_count"], 4)
        self.assertEqual(report["period_count"], 3)
        self.assertEqual(report["active_days"], 2)
        self.assertEqual(report["trigger_counts"]["explicit"], 1)
        self.assertEqual(report["trigger_counts"]["implicit"], 2)
        self.assertEqual(
            report["daily_counts"], {"2026-08-20": 2, "2026-08-31": 1}
        )

    def test_cli_records_and_returns_json_report(self) -> None:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "geno_dev.cli",
                "usage",
                "record",
                "example-skill",
                "--trigger",
                "implicit",
                "--database",
                str(self.database),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "geno_dev.cli",
                "usage",
                "report",
                "example-skill",
                "--days",
                "30",
                "--database",
                str(self.database),
                "--json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        report = json.loads(result.stdout)
        self.assertEqual(report["all_time_count"], 1)
        self.assertEqual(report["trigger_counts"]["implicit"], 1)


if __name__ == "__main__":
    unittest.main()
