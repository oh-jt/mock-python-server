from app.user_creation_helpers import (
    _build_insert_sql,
    _collect_values,
    _extract_email,
    _insert_columns,
    _is_valid_email,
    _protect_password,
    _to_response_dict,
)


def test_extract_email():
    assert _extract_email({"email": "bob@example.com"}) == "bob@example.com"


def test_is_valid_email():
    assert _is_valid_email("bob@example.com")


def test_protect_password_returns_value():
    assert _protect_password("secret") == "secret"


def test_build_insert_sql_contains_table():
    sql = _build_insert_sql(_insert_columns(), ["1", "a@b.c", "A", "pw", "member", "now"])
    assert "INSERT INTO users" in sql


def test_to_response_dict_maps_columns():
    row = (1, 1, "a@b.c", "A", "pw", "member", "now")
    assert _to_response_dict(row)["email"] == "a@b.c"


def test_collect_values_order():
    ctx = {"tenant_id": 1, "email": "e", "display_name": "d", "password": "p",
           "role": "r", "created_at": "t"}
    assert _collect_values(ctx)[1] == "e"


def test_create_user_happy_path(client):
    r = client.post("/users", json={"email": "bob@example.com", "display_name": "Bob",
                                    "password": "hunter2-hunter2"})
    assert r.status_code == 200
    assert r.json()["email"] == "bob@example.com"
