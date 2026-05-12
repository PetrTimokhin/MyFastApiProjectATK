# tests/conftest.py
import pytest
import sys


# from asgi_lifespan import LifespanManager
# from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from main import app
from DATABASES.db_postgres.base import Base
from DATABASES.db_postgres.connect_to_db import get_session
from settings.settings import settings

print(sys.path)
# -------------------------
# Enable TESTING mode
# -------------------------
@pytest.fixture(scope="session", autouse=True)
def enable_testing_mode():
    settings.TESTING = True

# -------------------------
# Async engine (TEST DB)
# -------------------------
@pytest.fixture
async def test_engine():
    engine = create_async_engine(
        settings.db_address,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

# -------------------------
# DB SESSION (pytest fixture!)
# -------------------------
@pytest.fixture
async def db_session(test_engine):
    async with AsyncSession(
        bind=test_engine,
        expire_on_commit=False,
    ) as session:
        yield session
        await session.rollback()

# -------------------------
# Dependency override (FastAPI)
# -------------------------
@pytest.fixture
def override_get_async_session(test_engine):
    async def _override():
        async with AsyncSession(
            bind=test_engine,
            expire_on_commit=False,
        ) as session:
            yield session

    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()

# -------------------------
# HTTP CLIENT
# -------------------------
# @pytest.fixture
# async def async_client():
#     transport = ASGITransport(app=app)
#
#     async with LifespanManager(app):
#         async with AsyncClient(
#             transport=transport,
#             base_url="http://test",
#         ) as client:
#             yield client
