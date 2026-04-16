from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from DATABASES.db_postgres.connect_to_db import get_session
from apps.auth.repository_hash import get_password_hash
from apps.auth.repository_token import decode_token
from apps.auth.routers import oauth2_scheme
from apps.auth.schemas import UserForRegister
from apps.user.repository import UserRepository
# from apps.auth.service_registry import is_user_exist, register_new_user


# для работы с методами UserRepository
user_repo = UserRepository(get_session())


async def is_user_exist(email: str) -> Optional[dict]:
    user = await user_repo.get_user_by_email_from_db(email)
    if user:
        return user
    else:
        return None


async def register_new_user(user_in: UserForRegister) -> Dict[str, Any]:
    """Хеширует пароль и регистрирует пользователя"""
    hashed_password = get_password_hash(user_in.password)
    user_data_in_dict = user_in.model_dump()
    user_data_in_dict['password'] = hashed_password

    # создание записи в DB c захешированным паролем
    new_user_data = await user_repo.create_user_in_db(**user_data_in_dict)

    return {
        "id": new_user_data.id,
        "email": new_user_data.email
            }


def get_current_user_data(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Извлекает данные user_id и email из валидного токена.
    Выбрасывает 401, если токен просрочен или недействителен.
    """
    try:
        payload = decode_token(token)
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            print('Функция get_current_user_data не нашла id или email!')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token payload")
        return {"user_id": user_id, "email": email}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

## из конспекта
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Не удалось проверить учетные данные",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username)
#     if user is None:
#         raise credentials_exception
#     return user

