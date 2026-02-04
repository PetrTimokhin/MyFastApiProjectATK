from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt import PyJWTError
from jose import jwt, JWTError

from apps.auth.repository_token import decode_token, create_access_token, \
    create_refresh_token
from apps.auth.schemas import UserRegister, UserLogin, Token, UserAfterRegister
from apps.auth.service_login import create_tokens, authenticate_user
from apps.auth.service_registry import is_user_exist, register_new_user


# Настройка OAuth2 для Dependency.
# Создает экземпляр схемы OAuth2, указывая, что точка, где пользователи могут
# получить токен (через логин), будет иметь путь /auth/login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# 1. Регистрация
@auth_router.post("/register",
                  response_model=UserAfterRegister,
                  status_code=status.HTTP_201_CREATED,
                  summary="Регистрация пользователя")
def register_user(user_in: UserRegister):
    # 1.1 Проверка существования email в БД
    if is_user_exist(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered")


    # 1.2 Регистрация нового пользователя
    created_user = register_new_user(user_in)

    return created_user


# 2. Вход Авторизация login
@auth_router.post("/login",
                  response_model=Token,
                  summary="Авторизация пользователя")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print('username', form_data.username, 'password', form_data.password)
    user_payload = authenticate_user(form_data.username, form_data.password)
    # возвращаем id, username, email (?)

    if not user_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = create_tokens(user_payload)
    return tokens

# 3. Обновляет Access Token, используя валидный Refresh Token


# Новая Dependency для извлечения Refresh Token из тела запроса
def get_current_refresh_token(refresh_token: str = Body(...)):
    """Извлекает refresh_token из тела запроса."""
    # Валидация уже происходит внутри decode_token при вызове
    return refresh_token


@auth_router.post("/token/refresh",
                  response_model=Token,
                  summary="Обновляем Access Token")
def refresh_token_endpoint(refresh_token_str: str
                           = Depends(get_current_refresh_token)):
    """Обновляет Access Token, используя валидный Refresh Token."""

    try:
        # 1. Валидация Refresh Token
        payload = decode_token(refresh_token_str)

        # 2. Проверяем, что необходимые данные присутствуют в payload
        user_id = payload.get("user_id")
        email = payload.get("email")

        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid payload in refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Создаем новый Access Token и Refresh Token
        new_access_token = create_access_token(
                              {"user_id": user_id, "email": email}
                                              )

        # Опционально: Создаем новый Refresh Token (для ротации токенов)
        new_refresh_token = create_refresh_token(
                                 {"user_id": user_id, "email": email}
                                                )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
