import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./students.db",
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

APP_TITLE = "Student Grade API"
APP_DESCRIPTION = "Backend service for students, faculties, courses and grades"
APP_VERSION = "1.0.0"