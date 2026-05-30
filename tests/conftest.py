from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def user_data():
    suffix = uuid4().hex[:8]

    return {
        "username": f"test_user_{suffix}",
        "password": "123456",
    }


@pytest.fixture()
def auth_headers(client, user_data):
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", json=user_data)

    user_id = response.json()["user_id"]

    return {"X-User-Id": str(user_id)}


@pytest.fixture()
def student_data():
    suffix = uuid4().hex[:8]

    return {
        "last_name": "Иванова",
        "first_name": "Ксения",
        "faculty": f"Факультет_{suffix}",
        "course": f"Курс_{suffix}",
        "grade": 95,
    }