from datetime import datetime, timedelta
from typing import Dict, Any
# import jwt
# from jwt import PyJWTError
from jose import jwt
from settings.settings import settings


# --- 2. JWT Функции ---
def create_access_token(data: Dict[str, Any],
                        expires_delta: timedelta = None) -> str:
    print("Формирование access токена")
    to_encode = data.copy()
    print('Копия payload_data для токена', to_encode)
    print('expires_delta', expires_delta)
    print('datetime.utcnow()', datetime.utcnow())
    print('timedelta', timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    expire = datetime.utcnow() + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    print("expire", expire)
    to_encode.update({"exp": expire})
    print('to_encode', to_encode)

    encoded_jwt = encode_token(to_encode)
    print('jwt', encoded_jwt)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any],
                         expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = encode_token(to_encode)

    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Декодирует токен, выбрасывая исключения при ошибке."""
    return jwt.decode(token,
                      settings.SECRET_KEY,
                      settings.ALGORITHM
                      )


def encode_token(data: dict) -> str:
    """Кодирует токен, выбрасывая исключения при ошибке."""
    return jwt.encode(data,
                      settings.SECRET_KEY,
                      settings.ALGORITHM)
