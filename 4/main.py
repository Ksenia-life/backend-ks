from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    yield
    print("Приложение завершает работу...")


app = FastAPI(
    title="Homework 4 API",
    description="FastAPI + SQLAlchemy + Alembic",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )