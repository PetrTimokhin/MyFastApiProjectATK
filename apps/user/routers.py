from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DATABASES.db_postgres.connect_to_db import get_session
from .repository import UserRepository
from .services import UserService
from .schemas import UserCreate, UserResponse

# router = APIRouter(prefix="/users", tags=["Users"])
user_router = APIRouter(prefix="/users", tags=["User"])


async def get_service(session: AsyncSession = Depends(get_session)):
    return UserService(UserRepository(session))


@user_router.post("/", response_model=UserResponse)
async def create_user(data: UserCreate, service: UserService = Depends(get_service)):
    return await service.create_user(data.email, data.password)


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends(get_service)):
    return await service.get_user_by_id(user_id)
