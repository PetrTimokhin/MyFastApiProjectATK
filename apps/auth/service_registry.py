from typing import Dict, Any, Optional

from apps.auth.repository_hash import get_password_hash
from apps.auth.schemas import UserRegister

from apps.auth.repository_db import get_user_by_email_from_db, \
    create_user_in_db


def is_user_exist(email: str) -> Optional[Dict[str, Any]]:
    return get_user_by_email_from_db(email)


def register_new_user(user_in: UserRegister) -> Dict[str, Any]:
    """Хеширует пароль и регистрирует пользователя"""
    hashed_password = get_password_hash(user_in.password)
    user_data_in_dict = user_in.model_dump()
    user_data_in_dict['password'] = hashed_password

    # создание записи в DB c захешированным паролем
    new_user_data = create_user_in_db(user_data_in_dict)

    return {
        "id": new_user_data['id'],
        "username": new_user_data['username'],
        "email": new_user_data['email']
            }
