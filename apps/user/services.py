from typing import Optional, List

from fastapi import HTTPException
from starlette import status

from apps.user.repository import (get_all_users_from_db,
                                  get_user_by_id_from_db,
                                  get_users_by_ids_from_db,
                                  update_user_in_db, delete_user_from_db,
                                  create_user_in_db)
from apps.user.schemas import UserCreate, UserUpdate
from apps.database.repository_db import get_user_by_email_from_db


def check_if_user_exists_by_email(email_value: str,
                                  current_id: Optional[int] = None) -> bool:
    """Проверяет, существует ли пользователь с таким email (кроме себя при обновлении)"""
    for user in get_all_users_from_db():
        if user['email'] == email_value and user.get('id') != current_id:
            return True
    return False


def create_new_user(user_in: UserCreate) -> dict:
    if check_if_user_exists_by_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_in.email} already exists")

    # Конвертируем Pydantic модель в словарь для репозитория
    user_data = user_in.model_dump()
    created_user = create_user_in_db(user_data)
    return created_user


def get_user(user_id: int) -> dict:
    user = get_user_by_id_from_db(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user


def get_user_by_email(email: str) -> dict:
    user = get_user_by_email_from_db(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user

def get_multiple_users(user_ids: List[int]) -> List[dict]:
    return get_users_by_ids_from_db(user_ids)


def get_all_users() -> List[dict]:
    return get_all_users_from_db()


def update_user_data(user_id: int, user_in: UserUpdate) -> dict:
    if not get_user_by_id_from_db(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    update_data = user_in.dict(exclude_unset=True)

    if 'email' in update_data and check_if_user_exists_by_email(
            update_data['email'], user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с {update_data['email']} уже существует!"
        )

    updated_user = update_user_in_db(user_id, update_data)
    return updated_user


def delete_user_data(user_id: int) -> dict:
    deleted_user = delete_user_from_db(user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return deleted_user
