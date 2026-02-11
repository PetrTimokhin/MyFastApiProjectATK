from typing import Dict, Any, Optional

from apps.database.repository_db import get_user_by_email_from_db
from apps.auth.repository_hash import verify_hashed_password, get_password_hash
from apps.auth.repository_token import create_access_token, \
    create_refresh_token


def authenticate_user(email: str,
                      password: str) -> Optional[Dict[str, Any]]:
    """Проверяет email и пароль для авторизации.
     Возвращает payload для JWT или None."""
    try:
        # 1. Получаем пользователя с hashed_password)
        user_by_email = get_user_by_email_from_db(email=email)
        # возвращает словарь с (id, username, email, password) или None

        if not user_by_email:
            print('Пользователь с данным email не найден!')
            return None

        # 2. Проверяем пароль
        print("Сверка паролей:", verify_hashed_password(password,
                                      user_by_email['password']))
        if not verify_hashed_password(password,
                                      user_by_email['password']):
            print('Присланный пароль:', password)
            print('Пароль из базы:', user_by_email['password'])
            print('Проверка хеширования пароля:', get_password_hash(password))
            return None


        print('Присланный пароль:', password)
        print('Пароль из базы:', user_by_email['password'])
        print(f'Проверка хеширования пароля:{password} = {get_password_hash(password)}')
        print(f'Проверка хеширования пароля:{password} = {get_password_hash(password)}')

        jwt_payload_data = {
            "user_id": user_by_email['id'],
            "email": user_by_email['email']
        }
        print('Возвращаем для payload', jwt_payload_data)

        # 3. Возвращаем данные для JWT payload
        return jwt_payload_data

    except Exception as e:
        print(e, 'ошибка в функции verify_user_credentials auth/service_login')
        return None


def create_tokens(user_payload: Dict[str, Any]) -> Dict[str, str]:
    """Создание токенов access и refresh"""
    access_token = create_access_token(user_payload)
    refresh_token = create_refresh_token(user_payload)

    return {"access_token": access_token, "refresh_token": refresh_token}





