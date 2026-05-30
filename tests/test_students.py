from uuid import uuid4


def test_create_student(client, auth_headers, student_data):
    response = client.post(
        "/students",
        json=student_data,
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["last_name"] == student_data["last_name"]
    assert response.json()["first_name"] == student_data["first_name"]
    assert response.json()["grade"] == student_data["grade"]
    assert "id" in response.json()


def test_get_all_students(client, auth_headers, student_data):
    client.post("/students", json=student_data, headers=auth_headers)

    response = client.get("/students", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student_by_id(client, auth_headers, student_data):
    create_response = client.post(
        "/students",
        json=student_data,
        headers=auth_headers,
    )
    student_id = create_response.json()["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == student_id


def test_update_student(client, auth_headers, student_data):
    create_response = client.post(
        "/students",
        json=student_data,
        headers=auth_headers,
    )
    student_id = create_response.json()["id"]

    updated_data = {
        "last_name": "Петрова",
        "first_name": "Анна",
        "faculty": student_data["faculty"],
        "course": student_data["course"],
        "grade": 88,
    }

    response = client.put(
        f"/students/{student_id}",
        json=updated_data,
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["last_name"] == "Петрова"
    assert response.json()["grade"] == 88


def test_delete_student(client, auth_headers, student_data):
    create_response = client.post(
        "/students",
        json=student_data,
        headers=auth_headers,
    )
    student_id = create_response.json()["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Student deleted successfully"


def test_get_missing_student(client, auth_headers):
    response = client.get("/students/999999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_get_students_by_faculty(client, auth_headers):
    suffix = uuid4().hex[:8]
    faculty = f"Факультет_{suffix}"

    student = {
        "last_name": "Сидорова",
        "first_name": "Мария",
        "faculty": faculty,
        "course": "FastAPI",
        "grade": 77,
    }

    client.post("/students", json=student, headers=auth_headers)

    response = client.get(
        f"/students/faculty/{faculty}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["faculty"] == faculty


def test_get_courses(client, auth_headers):
    suffix = uuid4().hex[:8]
    course = f"Курс_{suffix}"

    student = {
        "last_name": "Ким",
        "first_name": "Олег",
        "faculty": "Backend",
        "course": course,
        "grade": 90,
    }

    client.post("/students", json=student, headers=auth_headers)

    response = client.get("/courses", headers=auth_headers)

    assert response.status_code == 200
    assert course in response.json()


def test_get_low_grades(client, auth_headers):
    suffix = uuid4().hex[:8]
    course = f"Курс_{suffix}"

    student = {
        "last_name": "Ли",
        "first_name": "Иван",
        "faculty": "Backend",
        "course": course,
        "grade": 20,
    }

    client.post("/students", json=student, headers=auth_headers)

    response = client.get(
        f"/students/course/{course}/low-grades",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["grade"] < 30


def test_get_average_grade_by_faculty(client, auth_headers):
    suffix = uuid4().hex[:8]
    faculty = f"Факультет_{suffix}"

    first_student = {
        "last_name": "Иванова",
        "first_name": "Ксения",
        "faculty": faculty,
        "course": "FastAPI",
        "grade": 80,
    }

    second_student = {
        "last_name": "Петрова",
        "first_name": "Анна",
        "faculty": faculty,
        "course": "SQLAlchemy",
        "grade": 60,
    }

    client.post("/students", json=first_student, headers=auth_headers)
    client.post("/students", json=second_student, headers=auth_headers)

    response = client.get(
        f"/faculties/{faculty}/average-grade",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["faculty"] == faculty
    assert response.json()["average_grade"] == 70.0