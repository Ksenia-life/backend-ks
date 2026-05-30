# Student Grade API

Это backend-проект для работы со студентами, курсами, факультетами и оценками.

Итоговое задание по «Разработке веб-сервисов и приложений».

Основной фреймворк - FastAPI.

## Что реализовано

В проекте есть:

- регистрация, вход и выход пользователя;
- защита эндпоинтов через заголовок `X-User-Id`;
- CRUD для студентов;
- поиск студентов по факультету;
- список уникальных курсов;
- поиск студентов с низкими оценками по курсу;
- средний балл по факультету;
- импорт студентов из CSV;
- фоновое удаление студентов
- кеширование через Redis;
- миграции Alembic;
- запуск через Docker Compose;
- автотесты на Pytest.

## Стек

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Pytest
- Docker
- Docker Compose
- Uvicorn

## Запуск через Docker

```bash
docker compose up --build
```

После запуска Swagger будет доступен по адресу:

```text
http://127.0.0.1:8000/docs
```

Остановить контейнеры:

```bash
docker compose down
```

## Авторизация

Сначала нужно зарегистрировать пользователя:

```text
POST /auth/register
```

Потом выполнить вход:

```text
POST /auth/login
```

После входа в ответе вернётся `user_id`.

Этот `user_id` нужно передавать в защищённые эндпоинты через заголовок:

```text
X-User-Id: 1
```

## Основные эндпоинты

```text
GET    /

POST   /auth/register
POST   /auth/login
POST   /auth/logout

GET    /status

POST   /students
GET    /students
GET    /students/{student_id}
PUT    /students/{student_id}
DELETE /students/{student_id}

GET    /students/faculty/{faculty_name}
GET    /courses
GET    /students/course/{course_name}/low-grades
GET    /faculties/{faculty_name}/average-grade

POST   /import
POST   /import/background
DELETE /students/background/delete
```

## Тесты

Локально:

```bash
python -m pytest -q
```

В Docker:

```bash
docker compose exec app python -m pytest -q
```