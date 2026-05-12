from fastapi import Request
from fastapi.responses import JSONResponse
from utils.exceptions import NotFoundException


async def db_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except NotFoundException:
        return JSONResponse(status_code=404,
                            content={"detail": "Запись не найдена"})
    except Exception:
        return JSONResponse(status_code=500,
                            content={"detail": "Ошибка сервера"})
