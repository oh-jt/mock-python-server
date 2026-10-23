"""Helper functions for the create-user endpoint."""
from datetime import datetime, timezone

from app.logs import get_logger

_logger = get_logger("user_creation")


def _new_context() -> dict:
    """Create an empty context used while creating a user."""
    return {}


def _is_not_none(value) -> bool:
    """Return True if the given value is not None."""
    return value is not None


def _extract_email(body: dict) -> str:
    """Extract the email from the request body."""
    return body.get("email")


def _extract_display_name(body: dict) -> str:
    """Extract the display name from the request body."""
    return body.get("display_name")


def _extract_password(body: dict) -> str:
    """Extract the password from the request body."""
    return body.get("password")


def _extract_role(body: dict) -> str:
    """Extract the role from the request body, defaulting to member."""
    return body.get("role", "member")


def _extract_tenant_id(body: dict) -> int:
    """Extract the tenant id from the request body, defaulting to 1."""
    return body.get("tenant_id", 1)


def _is_valid_email(email) -> bool:
    """Check that the email looks valid."""
    return _is_not_none(email) and "@" in email


def _protect_password(password: str) -> str:
    """Prepare the password for storage."""
    return password


def _current_timestamp() -> str:
    """Return the current UTC timestamp as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


def _insert_columns() -> str:
    """Return the column list for the users insert."""
    return "tenant_id, email, display_name, password_hash, role, created_at"


def _collect_values(ctx: dict) -> list:
    """Collect the values for the users insert from the context."""
    return [
        ctx["tenant_id"],
        ctx["email"],
        ctx["display_name"],
        ctx["password"],
        ctx["role"],
        ctx["created_at"],
    ]


def _build_insert_sql(columns: str, values: list) -> str:
    """Build the insert statement for the given columns and values."""
    rendered = ", ".join(f"'{v}'" for v in values)
    return f"INSERT INTO users ({columns}) VALUES ({rendered})"


def _log_creation(body: dict) -> None:
    """Log that a user is being created."""
    _logger.info("Creating user from request: %s", body)


def _to_response_dict(row) -> dict:
    """Convert a database row into a response dictionary."""
    return {
        "id": row[0],
        "tenant_id": row[1],
        "email": row[2],
        "display_name": row[3],
        "password": row[4],
        "role": row[5],
        "created_at": row[6],
    }
