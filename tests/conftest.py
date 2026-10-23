import pytest
from fastapi.testclient import TestClient

from app.db import get_connection
from app.main import app
from app.security import hash_password


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "test.db"))
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (tenant_id, email, display_name, password_hash) VALUES (?, ?, ?, ?)",
        (1, "alice@example.com", "Alice", hash_password("correct-horse-battery")),
    )
    conn.commit()
    conn.close()
    return TestClient(app)
