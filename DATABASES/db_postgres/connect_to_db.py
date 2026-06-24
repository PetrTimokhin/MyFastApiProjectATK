from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)
from settings.settings import settings
from DATABASES.db_postgres.base import Base
import DATABASES.db_postgres.models   # важно для Base.metadata.create_all!!!

async_engine = create_async_engine(settings.db_address,
                                   echo=True)

async_session = async_sessionmaker(async_engine,
                                   expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# функция используется в main.py в async def lifespan
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# если нужно удалить все таблицы например после остановки приложения
async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)













# from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, \
#     create_async_engine
# from sqlalchemy.orm import sessionmaker
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mydb"
#
# # создаём асинхронный engine
# engine: AsyncEngine = create_async_engine(DATABASE_URL,
#                                           # вывод SQL в консоль для отладки
#                                           echo=True)
#
#
# # фабрика сессий
# # AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# AsyncSessionLocal = sessionmaker(class_=AsyncSession, expire_on_commit=False)
#
#
# # dependency, который выдаёт сессию на один запрос
# async def get_session() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         yield session
