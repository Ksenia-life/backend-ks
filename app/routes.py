from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_db
from app.repositories import StudentRepository
from app.schemas import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(
    tags=["students"],
    dependencies=[Depends(get_current_user)],
)

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE_PATH = BASE_DIR / "students.csv"


@router.get("/status")
async def status():
    return {"status": "ok"}


@router.post("/import")
async def import_students(db: AsyncSession = Depends(get_db)):
    repository = StudentRepository(db)
    return await repository.import_from_csv(str(CSV_FILE_PATH))


@router.post("/students", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)

    student = await repository.create_student(
        last_name=student_data.last_name,
        first_name=student_data.first_name,
        faculty=student_data.faculty,
        course=student_data.course,
        grade=student_data.grade,
    )

    return student


@router.get("/students", response_model=list[StudentResponse])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    repository = StudentRepository(db)
    return await repository.get_all_students()


@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student_by_id(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)
    student = await repository.get_student_by_id(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)

    student = await repository.update_student(
        student_id=student_id,
        last_name=student_data.last_name,
        first_name=student_data.first_name,
        faculty=student_data.faculty,
        course=student_data.course,
        grade=student_data.grade,
    )

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    repository = StudentRepository(db)
    deleted = await repository.delete_student(student_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}


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