import os
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id     INTEGER NOT NULL,
    email         TEXT NOT NULL,
    display_name  TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'member',
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (tenant_id, email)
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(os.environ.get("APP_DB_PATH", "app.db"))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
