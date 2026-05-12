import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from apps.user.models import User


pytestmark = pytest.mark.database


@pytest.mark.asyncio
async def test_create_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        password="hashedpassword",
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id(db_session):
    user = User(
        username="getuser",
        email="get@example.com",
        password="hashedpassword",
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    result = await db_session.get(User, user.id)

    assert result is not None
    assert result.id == user.id
    assert result.username == "getuser"
