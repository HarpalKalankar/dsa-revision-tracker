from conftest import auth_headers


def test_signup_returns_user_without_password(client):
    response = client.post(
        "/auth/signup",
        json={"email": "Asha@Example.com", "name": "Asha", "password": "password123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "asha@example.com"
    assert "password" not in body and "password_hash" not in body


def test_duplicate_email_is_rejected(client):
    user = {"email": "asha@example.com", "name": "Asha", "password": "password123"}
    client.post("/auth/signup", json=user)
    assert client.post("/auth/signup", json=user).status_code == 409


def test_login_and_me(client):
    headers = auth_headers(client)
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Asha"


def test_wrong_password_is_rejected(client):
    auth_headers(client)
    response = client.post(
        "/auth/login", data={"username": "asha@example.com", "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_routes_need_a_token(client):
    assert client.get("/problems").status_code == 401
    assert client.get("/revisions/today").status_code == 401