def test_get_user_returns_user_without_password(client):
    r = client.get("/tenants/1/users/1")
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "alice@example.com"
    assert "password_hash" not in body
    assert "password" not in body


def test_get_user_unknown_id_is_404(client):
    assert client.get("/tenants/1/users/999").status_code == 404


def test_get_user_wrong_tenant_is_404(client):
    assert client.get("/tenants/2/users/1").status_code == 404


def test_get_user_non_numeric_id_is_422(client):
    assert client.get("/tenants/1/users/abc").status_code == 422
