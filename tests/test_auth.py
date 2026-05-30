def test_register_user(client, user_data):
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert response.json()["is_logged_in"] is False


def test_register_existing_user(client, user_data):
    client.post("/auth/register", json=user_data)

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_login_user(client, user_data):
    client.post("/auth/register", json=user_data)

    response = client.post("/auth/login", json=user_data)

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "user_id" in response.json()


def test_login_with_wrong_password(client, user_data):
    client.post("/auth/register", json=user_data)

    response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_logout_user(client, auth_headers):
    response = client.post("/auth/logout", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"


def test_status_without_auth(client):
    response = client.get("/status")

    assert response.status_code == 401