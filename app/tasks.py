from app.database import AsyncSessionLocal
from app.repositories import StudentRepository
from app.cache import clear_cache

async def import_students_task(file_path: str):
    async with AsyncSessionLocal() as db:
        repository = StudentRepository(db)
        await repository.import_from_csv(file_path)
        await clear_cache()

async def delete_students_task(student_ids: list[int]):
    async with AsyncSessionLocal() as db:
        repository = StudentRepository(db)
        await repository.delete_students_by_ids(student_ids)
        await clear_cache()