from datetime import datetime, timedelta
from typing import Dict, Any
from jose import jwt
from settings.settings import settings


# --- 2. JWT Функции ---
def create_access_token(data: Dict[str, Any],
                        expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    expire = datetime.now() + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    encoded_jwt = encode_token(to_encode)
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
