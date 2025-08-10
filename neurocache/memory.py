import sqlite3
import json
import time
from pathlib import Path

class MemoryModule:
    """
    A lightweight, plug-and-play local memory module for LLM agents.
    Uses SQLite for persistent, local-first storage.
    """

    def __init__(self, db_path="neurocache.db"):
        """Initializes the memory module and sets up the database connection."""
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        """Creates the 'memories' table if it doesn't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                metadata TEXT,
                timestamp REAL NOT NULL
            )
        """)
        self.conn.commit()

    def remember(self, key: str, value: str, metadata: dict = None):
        """Saves a key-value pair to the memory."""
        try:
            ts = time.time()
            metadata_json = json.dumps(metadata or {})
            self.cursor.execute("""
                INSERT OR REPLACE INTO memories (key, value, metadata, timestamp)
                VALUES (?, ?, ?, ?)
            """, (key, value, metadata_json, ts))
            self.conn.commit()
        except Exception as e:
            print(f"[MemoryModule] Error remembering key '{key}': {e}")

    def recall(self, key: str) -> str or None:
        """Retrieves a value from memory based on its key."""
        try:
            self.cursor.execute("SELECT value FROM memories WHERE key = ?", (key,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"[MemoryModule] Error recalling key '{key}': {e}")
            return None

    def clear(self):
        """Deletes all memories from the database."""
        try:
            self.cursor.execute("DELETE FROM memories")
            self.conn.commit()
        except Exception as e:
            print(f"[MemoryModule] Error clearing memory: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Support context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure DB is closed when exiting context."""
        self.close()
