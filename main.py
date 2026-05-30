from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth_routes import router as auth_router
from app.core.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from app.routes import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    yield
    print("Приложение завершает работу...")


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(student_router)


@app.get("/")
async def root():
    return {"message": "Student Grade API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )