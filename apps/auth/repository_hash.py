"""Хеширование Паролей"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# проверка соответствия хешированного и нехешированного пароля
def verify_hashed_password(plain_password: str,
                           hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# получение хеша пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


