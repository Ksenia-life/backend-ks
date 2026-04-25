import csv

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Student, User


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_student(
        self,
        last_name: str,
        first_name: str,
        faculty: str,
        course: str,
        grade: int,
    ) -> Student:
        student = Student(
            last_name=last_name,
            first_name=first_name,
            faculty=faculty,
            course=course,
            grade=grade,
        )
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def get_all_students(self) -> list[Student]:
        result = await self.db.execute(select(Student))
        return list(result.scalars().all())

    async def get_student_by_id(self, student_id: int) -> Student | None:
        student = await self.db.get(Student, student_id)
        return student

    async def update_student(
        self,
        student_id: int,
        last_name: str,
        first_name: str,
        faculty: str,
        course: str,
        grade: int,
    ) -> Student | None:
        student = await self.db.get(Student, student_id)

        if student is None:
            return None

        student.last_name = last_name
        student.first_name = first_name
        student.faculty = faculty
        student.course = course
        student.grade = grade

        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def delete_student(self, student_id: int) -> bool:
        student = await self.db.get(Student, student_id)

        if student is None:
            return False

        await self.db.delete(student)
        await self.db.commit()
        return True
    
    async def delete_students_by_ids(self, student_ids: list[int]) -> dict:
        deleted_count = 0

        for student_id in student_ids:
            student = await self.db.get(Student, student_id)

            if student is None:
                continue

            await self.db.delete(student)
            deleted_count += 1

        await self.db.commit()

        return {
            "message": "Students deleted successfully",
            "deleted_count": deleted_count,
        }

    async def import_from_csv(self, file_path: str) -> dict:
        rows_processed = 0

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                last_name = row.get("Фамилия", "").strip()
                first_name = row.get("Имя", "").strip()
                faculty = row.get("Факультет", "").strip()
                course = row.get("Курс", "").strip()
                grade_value = row.get("Оценка", "").strip()

                if not all([last_name, first_name, faculty, course, grade_value]):
                    continue

                student = Student(
                    last_name=last_name,
                    first_name=first_name,
                    faculty=faculty,
                    course=course,
                    grade=int(grade_value),
                )

                self.db.add(student)
                rows_processed += 1

        await self.db.commit()

        return {
            "message": "CSV file imported successfully",
            "rows_processed": rows_processed,
        }

    async def get_students_by_faculty(self, faculty_name: str) -> list[dict]:
        stmt = (
            select(Student)
            .where(Student.faculty == faculty_name)
            .order_by(Student.last_name, Student.first_name)
        )

        result = await self.db.execute(stmt)
        students = result.scalars().all()

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

    async def get_unique_courses(self) -> list[str]:
        stmt = select(distinct(Student.course)).order_by(Student.course)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_students_by_course_with_low_grades(self, course_name: str) -> list[dict]:
        stmt = (
            select(Student)
            .where(Student.course == course_name, Student.grade < 30)
            .order_by(Student.grade, Student.last_name, Student.first_name)
        )

        result = await self.db.execute(stmt)
        students = result.scalars().all()

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

    async def get_average_grade_by_faculty(self, faculty_name: str) -> dict:
        stmt = select(func.avg(Student.grade)).where(Student.faculty == faculty_name)

        result = await self.db.execute(stmt)
        average_grade = result.scalar()

        return {
            "faculty": faculty_name,
            "average_grade": round(float(average_grade), 2) if average_grade is not None else None,
        }


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str, hashed_password: str) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            is_logged_in=False,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.db.get(User, user_id)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def login_user(self, user: User) -> User:
        user.is_logged_in = True
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def logout_user(self, user: User) -> User:
        user.is_logged_in = False
        await self.db.commit()
        await self.db.refresh(user)
        return user