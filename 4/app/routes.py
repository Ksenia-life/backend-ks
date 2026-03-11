from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import StudentRepository

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE_PATH = BASE_DIR / "students.csv"


@router.get("/status")
async def status():
    return {"status": "ok"}


@router.post("/import")
async def import_students(db: AsyncSession = Depends(get_db)):
    repository = StudentRepository(db)
    return await repository.import_from_csv(str(CSV_FILE_PATH))


@router.get("/students")
async def get_all_students(db: AsyncSession = Depends(get_db)):
    repository = StudentRepository(db)
    students = await repository.get_all_students()

    return [
        {
            "id": student.id,
            "last_name": student.last_name,
            "first_name": student.first_name,
            "faculty": student.faculty,
            "course": student.course,
            "grade": student.grade,
        }
        for student in students
    ]


@router.get("/students/faculty/{faculty_name}")
async def get_students_by_faculty(
    faculty_name: str,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)
    return await repository.get_students_by_faculty(faculty_name)


@router.get("/courses")
async def get_unique_courses(db: AsyncSession = Depends(get_db)):
    repository = StudentRepository(db)
    return await repository.get_unique_courses()


@router.get("/students/course/{course_name}/low-grades")
async def get_students_by_course_with_low_grades(
    course_name: str,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)
    return await repository.get_students_by_course_with_low_grades(course_name)


@router.get("/faculties/{faculty_name}/average-grade")
async def get_average_grade_by_faculty(
    faculty_name: str,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)
    return await repository.get_average_grade_by_faculty(faculty_name)