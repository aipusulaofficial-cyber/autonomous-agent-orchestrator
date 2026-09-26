import sqlite3
from pathlib import Path
from threading import RLock


class DurableJobStore:
    """Crash-safe job state store using SQLite WAL transactions."""

    def __init__(self, path: str = "jobs.db") -> None:
        self.path = str(Path(path))
        self._lock = RLock()
        with self._connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS jobs ("
                "id TEXT PRIMARY KEY, state TEXT NOT NULL, payload TEXT NOT NULL, "
                "updated_at TEXT NOT NULL)"
            )

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level="IMMEDIATE")
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=10000")
        return db

    def put(self, job_id: str, state: str, payload: str, updated_at: str) -> None:
        with self._lock, self._connect() as db:
            db.execute(
                "INSERT INTO jobs VALUES(?,?,?,?) "
                "ON CONFLICT(id) DO UPDATE SET state=excluded.state, "
                "payload=excluded.payload, updated_at=excluded.updated_at",
                (job_id, state, payload, updated_at),
            )

    def get(self, job_id: str):
        with self._connect() as db:
            return db.execute(
                "SELECT id,state,payload,updated_at FROM jobs WHERE id=?", (job_id,)
            ).fetchone()
