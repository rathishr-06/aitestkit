import sqlite3
import json
from pathlib import Path
from datetime import datetime

class TestHistoryDB:
    """SQLite Database wrapper for persistent historical run tracking."""

    def __init__(self, db_path: str = "reports/aitestkit_history.db"):
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path))
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS test_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    test_type TEXT,
                    metrics_json TEXT
                )
            """)

    def record_run(self, test_type: str, metrics: dict):
        with self.conn:
            self.conn.execute(
                "INSERT INTO test_runs (timestamp, test_type, metrics_json) VALUES (?, ?, ?)",
                (datetime.now().isoformat(), test_type, json.dumps(metrics))
            )

    def fetch_all_runs(self) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, timestamp, test_type, metrics_json FROM test_runs ORDER BY id DESC")
        rows = cursor.fetchall()
        return [
            {"id": r[0], "timestamp": r[1], "test_type": r[2], "metrics": json.loads(r[3])}
            for r in rows
        ]