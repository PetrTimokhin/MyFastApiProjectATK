from apps.auth.routers import auth_router
from apps.external.routers import ex_router
from apps.project.routers import project_router
# from apps.user_for_db_dict.routers import user_router
from apps.user.routers import user_router

from fastapi import APIRouter

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(project_router)
api_router.include_router(ex_router)
