from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import uvicorn
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from DATABASES.db_postgres.connect_to_db import create_tables, get_session
from routers.api_v1_router import api_router
from apps.auth.middleware import jwt_authentication_middleware

from fastapi import Request
from fastapi.responses import JSONResponse

from utils.exceptions import NotFoundException, DatabaseException

# Этот декоратор @asynccontextmanager в сочетании с асинхронной функцией
# lifespan используется в FastAPI для управления жизненным циклом приложения.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    # await drop_tables()  # можно применить

app = FastAPI(lifespan=lifespan)

# ИСПРАВИТЬ!!! разобраться с middleware, как их добавлять! github Славы
app.middleware("http")(jwt_authentication_middleware)

# еще одна версия middleware, она закоммичена в том же файле
# app.add_middleware(AuthMiddleware)

app.include_router(api_router)


# просто корневая страничка с надписью
@app.get("/", tags=["Root"], summary="Корневая страница")
def read_root():
    return "Hello FastAPI World"


@app.get("/healthcheck", tags=["Healthcheck"], summary="Проверка БД")
async def health_check():
    return {"status": "healthy"}


# healthcheck для проверки БД при загрузке YAML файла
@app.get("/db-check", tags=["Healthcheck"], summary="Проверка БД")
async def db_check(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(text("SELECT version();"))
        version = result.scalar()

        return {
            "status": "ok",
            "database": "postgresql",
            "version": version,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(exc)}"
        )

# глобальная обработка ошибок
@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DatabaseException)
async def db_handler(request: Request, exc: DatabaseException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# запуск через python main.py
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # host="0.0.0.0" для продакшена
        port=8000,
        reload=True,
    )
