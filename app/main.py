from fastapi import FastAPI, HTTPException

from app.db import get_connection
from app.logs import get_logger, log_event
from app.models import UserOut

app = FastAPI(title="mock-python-server")
logger = get_logger(__name__)


@app.get("/tenants/{tenant_id}/users/{user_id}", response_model=UserOut)
def get_user(tenant_id: int, user_id: int) -> UserOut:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, tenant_id, email, display_name, role, created_at "
            "FROM users WHERE id = ? AND tenant_id = ?",
            (user_id, tenant_id),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        # Same answer for "no such user" and "user in another tenant": do not leak existence.
        raise HTTPException(status_code=404, detail="User not found")

    log_event(logger, "user_fetched", tenant_id=tenant_id, user_id=user_id)
    return UserOut(**dict(row))
