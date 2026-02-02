from typing import Dict, Any, Optional

from apps.auth.repository_db import get_user_by_email_from_db
from apps.auth.repository_hash import verify_hashed_password
from apps.auth.repository_token import create_access_token, \
    create_refresh_token


def authenticate_user(email: str,
                      password: str) -> Optional[Dict[str, Any]]:
    """Проверяет email и пароль для авторизации.
     Возвращает payload для JWT или None."""
    try:
        # 1. Получаем пользователя с hashed_password)
        user_by_email = get_user_by_email_from_db(email=email)

        if not user_by_email:
            return None

        # 2. Проверяем пароль
        if not verify_hashed_password(password,
                                      user_by_email['password']):
            return None

        # 3. Возвращаем данные для JWT payload
        return {
            "user_id": user_by_email['id'],
            "username": user_by_email['username'],
            "email": user_by_email['email']
        }

    except Exception as e:
        print(e, 'ошибка в функции verify_user_credentials auth/service_login')
        return None


def create_tokens(user_payload: Dict[str, Any]) -> Dict[str, str]:
    """Создание токенов access и refresh"""
    access_token = create_access_token(user_payload)
    refresh_token = create_refresh_token(user_payload)

    return {"access_token": access_token, "refresh_token": refresh_token}





