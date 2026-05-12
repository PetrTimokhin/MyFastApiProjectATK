# tests/services/test_user_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock

from apps.user.services import UserService
from apps.user.models import User
from apps.user.schemas import UserCreate

# pytestmark = pytest.mark.services


@pytest.mark.services
@pytest.mark.asyncio
async def test_create_user():
    # фейковый репозиторий подменяет работу с БД
    fake_repo = AsyncMock()

    data = UserCreate(
        username="testuser",
        email="test@mail.com",
        password="123456",
    )

    fake_user = User(
        username=data.username,
        email=data.email,
        password="hashed",
    )

    # Когда вызовут repo.create(...), верни fake_user
    # create_user_in_db из слоя репозитория
    fake_repo.create_user_in_db.return_value = fake_user
    # Создаём сервис и подставляем mock-репозиторий вместо настоящего.
    # Это называется Dependency Injection.
    service = UserService(repo=fake_repo)
    result = await service.create_user(data.password, data.email)

    fake_repo.create_user_in_db.assert_called_once()
    assert result == fake_user


# @pytest.mark.services
# @pytest.mark.asyncio
# async def test_get_user_by_id_found():
#     repo = AsyncMock()
#
#     fake_user = User(
#         user_id=1,
#         name="User",
#         username="user1",
#         hashed_password="hashed",
#     )
#
#     repo.get_by_id.return_value = fake_user
#
#     service = UserService(repository=repo)
#     result = await service.get_by_id(repo, 1)
#
#     repo.get_by_id.assert_called_once_with(repo, 1)
#     assert result == fake_user
#
#
#
# @pytest.mark.services
# @pytest.mark.asyncio
# async def test_get_user_by_id_not_found():
#     repo = AsyncMock()
#     repo.get_by_id.return_value = None
#
#     service = UserService(repository=repo)
#     result = await service.get_by_id(repo, 999)
#
#     assert result is None