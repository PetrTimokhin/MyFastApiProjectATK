from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.user.models import User
from apps.user.schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_in_db(self, email: str, password: str) -> User:
        """
        INSERT INTO users (email) VALUES (:email);
        """
        user = User(email=email, password=password)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        # return User(email=email)  # поменял для тестов
        return user  # поменял для тестов

    async def get_user_by_id_from_db(self, user_id: int) -> User | None:
        """
        SELECT * FROM users WHERE id = :user_id;
        """
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email_from_db(self, email: str) -> dict | None:
        """
        SELECT * FROM users WHERE email = :email;
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user_orm_object = result.scalar_one_or_none()

        if user_orm_object:
            return {
                "id": user_orm_object.id,
                "email": user_orm_object.email,
                "username": user_orm_object.username,
                "password": user_orm_object.password
            }
        else:
            return None



# from sqlalchemy import select, delete, update
# from sqlalchemy.ext.asyncio import AsyncSession
# from apps.user.models import User
# from utils.exceptions import NotFoundException
#
#
# class UserRepository:
#
#     async def get_by_id(self, db: AsyncSession, user_id: int):
#         """
#         SELECT * FROM users WHERE id = :user_id;
#         """
#         result = await db.execute(select(User).where(User.id == user_id))
#         user = result.scalar_one_or_none()
#         if not user:
#             raise NotFoundException()
#         return user
#
#     async def get_by_email(self, db: AsyncSession, email: str):
#         """
#         SELECT * FROM users WHERE email = :email;
#         """
#         result = await db.execute(select(User).where(User.email == email))
#         return result.scalar_one_or_none()
#
#     async def get_all(self, db: AsyncSession):
#         """
#         SELECT * FROM users;
#         """
#         result = await db.execute(select(User))
#         return result.scalars().all()
#
#     async def create(self, db: AsyncSession, data):
#         """
#         INSERT INTO users (email, name) VALUES (:email, :name) RETURNING *;
#         """
#         user = User(**data.dict())
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)
#         return user
#
#     async def delete(self, db: AsyncSession, user_id: int):
#         """
#         DELETE FROM users WHERE id = :user_id RETURNING *;
#         """
#         user = await self.get_by_id(db, user_id)
#         await db.delete(user)
#         await db.commit()
#         return user