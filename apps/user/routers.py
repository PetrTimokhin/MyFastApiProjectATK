from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends
from starlette import status
from starlette.requests import Request

from apps.auth.service_current_user import get_current_user_data
from apps.user.schemas import UserCreate, UserResponse, UserUpdate
from apps.user.services import create_new_user, get_user, get_all_users, \
    get_multiple_users, update_user_data, delete_user_data

user_router = APIRouter(prefix="/users", tags=["User"])


# 1. Создать одного пользователя
@user_router.post("/",
                  response_model=UserResponse,
                  status_code=status.HTTP_201_CREATED,
                  summary="Создать одного пользователя")
def create_user(user_in: UserCreate):
    """Создать нового пользователя"""
    new_user = create_new_user(user_in)
    return new_user


# 4. Создать нескольких пользователей (Bulk Create)
@user_router.post("/bulk",
                  response_model=List[UserResponse],
                  status_code=status.HTTP_201_CREATED,
                  summary="Создать нескольких пользователей из списка"
                  )
def create_multiple_users(users_in: List[UserCreate]):
    """Создать список пользователей"""
    created_users = []
    for user_in in users_in:
        # В реальном приложении лучше использовать транзакции
        try:
            user = create_new_user(user_in)
            created_users.append(user)
        except HTTPException as e:
            # Обработка ошибок при создании, например, уникальность email
            print(f"Ошибка при создании {user_in.name}: {e.detail}")
            pass  # пропустить, если ошибка (или вернуть полный список ошибок)

    return created_users


# 3. Получить всех пользователей
@user_router.get("/",
                 response_model=List[UserResponse],
                 summary="Получить всех пользователей"
                 )
def read_all_users():
    """Получить всех пользователей в БД"""
    return get_all_users()


# 4. Получить данные текущего пользователя
@user_router.get("/me",
                 response_model=UserResponse,
                 summary="Получить данные текущего пользователя"
                 )
def read_users_me(current_user_data: dict = Depends(get_current_user_data)):
    """Получить данные текущего аутентифицированного пользователя"""

    user_id = current_user_data['user_id']

    # Здесь вызов сервиса пользователя для получения данных по ID
    user = get_user(user_id)
    return user


# 5. Получить нескольких пользователей по списку id
@user_router.get("/list",
                 response_model=List[UserResponse],
                 summary="Получить нескольких пользователей по списку id"
                 )
def read_users_by_ids(ids: List[int] = Query(...)):
    """Получить список пользователей по их ID"""
    return get_multiple_users(ids)


# 2. Получить одного пользователя
@user_router.get("/{user_id}",
                 response_model=UserResponse,
                 summary="Получить одного пользователя по id"
                 )
def read_user(user_id: int):
    """Получить пользователя по ID"""
    user = get_user(user_id)
    print(f'Получен пользователь {user['name']}')
    return user


# 6. Обновить данные пользователя
@user_router.put("/{user_id}",
                 response_model=UserResponse,
                 summary="Обновление данных пользователя"
                 )
def update_user(user_id: int, user_in: UserUpdate):
    """Обновить данные пользователя"""
    updated_user = update_user_data(user_id, user_in)
    return updated_user


# 7. Удалить пользователя
@user_router.delete("/{user_id}",
                    response_model=UserResponse,
                    summary="Удалить пользователя"
                    )
def delete_user(user_id: int):
    """Удалить пользователя и вернуть его данные"""
    deleted_user = delete_user_data(user_id)
    return deleted_user


# НОВЫЙ РОУТ: Получить данные пользователя через Middleware state
@user_router.get("/profile_via_middleware", response_model=UserResponse)
def read_profile_via_middleware(request: Request):
    """
    Получает user_id и email, установленные в AuthMiddleware.
    Роут защищен MiddleWare, а не Dependency.
    """

    user_id = request.state.user_id
    email = request.state.email

    if not user_id:
        # Этого не должно случиться, если Middleware не пропустил запрос
        raise HTTPException(status_code=500,
                            detail="User ID not found in request state")

    # Используем user_id для получения полных данных из User Service
    user = get_user(user_id)
    print(
        f"Middleware Auth: Пользователь ID {user_id} ({email}) запросил профиль.")
    return user

