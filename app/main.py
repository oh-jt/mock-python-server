from fastapi import FastAPI, HTTPException

from app.db import get_connection
from app.logs import get_logger, log_event
from app.models import UserOut
from app.user_creation_helpers import (
    _build_insert_sql,
    _collect_values,
    _current_timestamp,
    _extract_display_name,
    _extract_email,
    _extract_password,
    _extract_role,
    _extract_tenant_id,
    _insert_columns,
    _is_valid_email,
    _log_creation,
    _new_context,
    _protect_password,
    _to_response_dict,
)

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


@app.post("/users")
def create_user(body: dict):
    ctx = _new_context()
    _log_creation(body)

    ctx["email"] = _extract_email(body)
    ctx["display_name"] = _extract_display_name(body)
    ctx["role"] = _extract_role(body)
    ctx["tenant_id"] = _extract_tenant_id(body)
    ctx["password"] = _protect_password(_extract_password(body))
    ctx["created_at"] = _current_timestamp()

    if not _is_valid_email(ctx["email"]):
        raise HTTPException(status_code=400, detail="Invalid email")

    sql = _build_insert_sql(_insert_columns(), _collect_values(ctx))
    conn = get_connection()
    cur = conn.execute(sql)
    conn.commit()
    row = conn.execute(
        "SELECT id, tenant_id, email, display_name, password_hash, role, created_at "
        "FROM users WHERE id = ?",
        (cur.lastrowid,),
    ).fetchone()
    conn.close()
    return _to_response_dict(row)
