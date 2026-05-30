def test_register_with_short_data(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "ks",
            "password": "123",
        },
    )

    assert response.status_code == 422


def test_create_student_with_bad_grade(client, auth_headers):
    response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "last_name": "Иванова",
            "first_name": "Ксения",
            "faculty": "Backend",
            "course": "FastAPI",
            "grade": 120,
        },
    )

    assert response.status_code == 422


def test_create_student_with_empty_name(client, auth_headers):
    response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "last_name": "",
            "first_name": "Ксения",
            "faculty": "Backend",
            "course": "FastAPI",
            "grade": 90,
        },
    )

    assert response.status_code == 422


def test_update_student_with_bad_grade(client, auth_headers, student_data):
    create_response = client.post(
        "/students",
        headers=auth_headers,
        json=student_data,
    )
    student_id = create_response.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        headers=auth_headers,
        json={
            "last_name": "Иванова",
            "first_name": "Ксения",
            "faculty": "Backend",
            "course": "FastAPI",
            "grade": -1,
        },
    )

    assert response.status_code == 422


def test_delete_missing_student(client, auth_headers):
    response = client.delete(
        "/students/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404