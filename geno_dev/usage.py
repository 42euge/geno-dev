"""Privacy-minimal local skill invocation storage."""

from __future__ import annotations

from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3
from typing import Any


DEFAULT_DATABASE = Path.home() / ".geno" / "skill-usage.sqlite3"
TRIGGERS = ("explicit", "implicit", "unknown")
SCHEMA_VERSION = 1


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def _connect(database: Path) -> sqlite3.Connection:
    database = database.expanduser()
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 5000")
    current_version = connection.execute("PRAGMA user_version").fetchone()[0]
    if current_version not in (0, SCHEMA_VERSION):
        connection.close()
        raise RuntimeError(
            f"unsupported skill usage database version: {current_version}"
        )
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS skill_invocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL CHECK (length(trim(skill_name)) > 0),
            invoked_at TEXT NOT NULL,
            trigger TEXT NOT NULL
                CHECK (trigger IN ('explicit', 'implicit', 'unknown'))
        );

        CREATE INDEX IF NOT EXISTS idx_skill_invocations_skill_time
            ON skill_invocations (skill_name, invoked_at);
        """
    )
    if current_version == 0:
        connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    connection.commit()
    database.chmod(0o600)
    return connection


def record_invocation(
    database: Path,
    *,
    skill_name: str,
    trigger: str = "unknown",
    invoked_at: datetime | None = None,
) -> int:
    """Record one invocation and return its database identifier."""
    if not skill_name.strip():
        raise ValueError("skill name must not be empty")
    if trigger not in TRIGGERS:
        raise ValueError(f"unsupported trigger: {trigger}")
    timestamp = _format_timestamp(invoked_at or _utc_now())
    with closing(_connect(database)) as connection:
        cursor = connection.execute(
            """
            INSERT INTO skill_invocations (skill_name, invoked_at, trigger)
            VALUES (?, ?, ?)
            """,
            (skill_name, timestamp, trigger),
        )
        connection.commit()
        return int(cursor.lastrowid)


def summarize_invocations(
    database: Path,
    *,
    skill_name: str,
    days: int = 30,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return all-time and rolling-window invocation counts."""
    if not skill_name.strip():
        raise ValueError("skill name must not be empty")
    if days <= 0:
        raise ValueError("days must be positive")
    current_time = now or _utc_now()
    cutoff = _format_timestamp(current_time - timedelta(days=days))
    with closing(_connect(database)) as connection:
        all_time = connection.execute(
            "SELECT COUNT(*) FROM skill_invocations WHERE skill_name = ?",
            (skill_name,),
        ).fetchone()[0]
        period = connection.execute(
            """
            SELECT COUNT(*)
            FROM skill_invocations
            WHERE skill_name = ? AND invoked_at >= ?
            """,
            (skill_name, cutoff),
        ).fetchone()[0]
        active_days = connection.execute(
            """
            SELECT COUNT(DISTINCT substr(invoked_at, 1, 10))
            FROM skill_invocations
            WHERE skill_name = ? AND invoked_at >= ?
            """,
            (skill_name, cutoff),
        ).fetchone()[0]
        trigger_rows = connection.execute(
            """
            SELECT trigger, COUNT(*) AS count
            FROM skill_invocations
            WHERE skill_name = ? AND invoked_at >= ?
            GROUP BY trigger
            ORDER BY trigger
            """,
            (skill_name, cutoff),
        ).fetchall()
        daily_rows = connection.execute(
            """
            SELECT substr(invoked_at, 1, 10) AS day, COUNT(*) AS count
            FROM skill_invocations
            WHERE skill_name = ? AND invoked_at >= ?
            GROUP BY day
            ORDER BY day
            """,
            (skill_name, cutoff),
        ).fetchall()
        bounds = connection.execute(
            """
            SELECT MIN(invoked_at) AS first_invoked_at,
                   MAX(invoked_at) AS last_invoked_at
            FROM skill_invocations
            WHERE skill_name = ?
            """,
            (skill_name,),
        ).fetchone()

    trigger_counts = {trigger: 0 for trigger in TRIGGERS}
    trigger_counts.update({row["trigger"]: row["count"] for row in trigger_rows})
    return {
        "skill": skill_name,
        "days": days,
        "period_count": period,
        "all_time_count": all_time,
        "active_days": active_days,
        "trigger_counts": trigger_counts,
        "daily_counts": {row["day"]: row["count"] for row in daily_rows},
        "first_invoked_at": bounds["first_invoked_at"],
        "last_invoked_at": bounds["last_invoked_at"],
        "database": str(database.expanduser()),
    }
