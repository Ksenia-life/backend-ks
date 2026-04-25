from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.cache import clear_cache, get_cache, set_cache
from app.database import get_db
from app.repositories import StudentRepository
from app.schemas import StudentCreate, StudentDeleteList, StudentResponse, StudentUpdate
from app.tasks import delete_students_task, import_students_task

router = APIRouter(
    tags=["students"],
    dependencies=[Depends(get_current_user)],
)

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE_PATH = BASE_DIR / "students.csv"


@router.get("/status")
async def status():
    cache_key = "status"

    cached_status = await get_cache(cache_key)
    if cached_status is not None:
        return cached_status

    data = {"status": "ok"}
    await set_cache(cache_key, data)

    return data


@router.post("/import")
async def import_students(db: AsyncSession = Depends(get_db)):
    repository = StudentRepository(db)
    result = await repository.import_from_csv(str(CSV_FILE_PATH))
    await clear_cache()
    return result

@router.post("/import/background")
async def import_students_background(
    file_path: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(import_students_task, file_path)

    return {
        "message": "CSV import started in background",
        "file_path": file_path,
    }

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

    await clear_cache()

    return student


@router.get("/students", response_model=list[StudentResponse])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    cache_key = "students:all"

    cached_students = await get_cache(cache_key)
    if cached_students is not None:
        return cached_students

    repository = StudentRepository(db)
    students = await repository.get_all_students()

    students_data = [
        StudentResponse.model_validate(student).model_dump()
        for student in students
    ]

    await set_cache(cache_key, students_data)

    return students_data


@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student_by_id(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"students:{student_id}"

    cached_student = await get_cache(cache_key)
    if cached_student is not None:
        return cached_student

    repository = StudentRepository(db)
    student = await repository.get_student_by_id(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data = StudentResponse.model_validate(student).model_dump()
    await set_cache(cache_key, student_data)

    return student_data


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

    await clear_cache()

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

    await clear_cache()

    return {"message": "Student deleted successfully"}

@router.delete("/students/background/delete")
async def delete_students_background(
    student_data: StudentDeleteList,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(delete_students_task, student_data.student_ids)

    return {
        "message": "Students delete started in background",
        "student_ids": student_data.student_ids,
    }

@router.get("/students/faculty/{faculty_name}")
async def get_students_by_faculty(
    faculty_name: str,
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"students:faculty:{faculty_name}"

    cached_students = await get_cache(cache_key)
    if cached_students is not None:
        return cached_students

    repository = StudentRepository(db)
    students = await repository.get_students_by_faculty(faculty_name)

    await set_cache(cache_key, students)

    return students


@router.get("/courses")
async def get_unique_courses(db: AsyncSession = Depends(get_db)):
    cache_key = "courses:all"

    cached_courses = await get_cache(cache_key)
    if cached_courses is not None:
        return cached_courses

    repository = StudentRepository(db)
    courses = await repository.get_unique_courses()

    await set_cache(cache_key, courses)

    return courses


@router.get("/students/course/{course_name}/low-grades")
async def get_students_by_course_with_low_grades(
    course_name: str,
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"students:course:{course_name}:low-grades"

    cached_students = await get_cache(cache_key)
    if cached_students is not None:
        return cached_students

    repository = StudentRepository(db)
    students = await repository.get_students_by_course_with_low_grades(course_name)

    await set_cache(cache_key, students)

    return students


@router.get("/faculties/{faculty_name}/average-grade")
async def get_average_grade_by_faculty(
    faculty_name: str,
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"faculties:{faculty_name}:average-grade"

    cached_average_grade = await get_cache(cache_key)
    if cached_average_grade is not None:
        return cached_average_grade

    repository = StudentRepository(db)
    average_grade = await repository.get_average_grade_by_faculty(faculty_name)

    await set_cache(cache_key, average_grade)

    return average_grade