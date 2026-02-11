from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from apps.auth.repository_token import decode_token
from apps.auth.routers import oauth2_scheme


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

