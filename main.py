import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.auth.middleware import jwt_authentication_middleware
from routers.api_v1_router import api_router


app = FastAPI()


@app.get("/", tags=["Root"], summary="Корневая страница")
def read_root():
    return "Hello FastAPI World"


app.middleware("http")(jwt_authentication_middleware)
# app.add_middleware(AuthMiddleware)


app.include_router(api_router)
# app.include_router(auth_router)
# app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
