from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only, selectinload

from utils.exceptions import NotFoundException, DatabaseException
from .models import Project
from .schemas import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get_by_id(self, project_id: int) -> Project:
    #
    #     # SELECT * FROM projects WHERE id = :project_id;
    #     """
    #     SELECT id FROM projects WHERE id = :project_id
    #     """
    #     result = await self.session.execute(
    #         select(Project).where(Project.id == project_id)
    #     )
    #     project = result.scalar_one_or_none()
    #
    #     if not project:
    #         raise NotFoundException("Проект не найден")
    #
    #     return project

    async def get_by_id(self, project_id: int) -> Project:
        """
        SELECT id FROM projects
        SELECT * FROM users WHERE id IN (...)
        """
        result = await self.session.execute(
            select(Project)
            .options(load_only(Project.id), selectinload(Project.person))
            .where(Project.id == project_id)
        )

        project = result.scalar_one_or_none()

        if not project:
            raise NotFoundException("Проект не найден")

        return project

    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        status: str | None = None,
        person_id: int | None = None,
        order_by: str = "create_time",
    ):
        """
        SELECT * FROM projects
        WHERE ...
        ORDER BY ...
        LIMIT :limit OFFSET :offset;
        """

        query = select(Project)

        if status:
            query = query.where(Project.status == status)

        if person_id:
            query = query.where(Project.person_id == person_id)

        # сортировка
        if order_by == "start_time":
            query = query.order_by(Project.start_time)
        elif order_by == "complete_time":
            query = query.order_by(Project.complete_time)
        else:
            query = query.order_by(Project.create_time)

        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        items = result.scalars().all()

        # total count
        count_query = select(func.count(Project.id))
        total = await self.session.scalar(count_query)

        return {
            "items": items,
            "total_count": total,
            "has_next": total > page * limit,
            "has_prev": page > 1,
        }

    async def create(self, data: ProjectCreate) -> Project:
        """
        INSERT INTO projects (...) VALUES (...);
        """
        project = Project(**data.dict())

        self.session.add(project)

        try:
            await self.session.commit()
            await self.session.refresh(project)
        except IntegrityError:
            await self.session.rollback()
            raise DatabaseException("Ошибка создания проекта")

        return project

    async def create_many(self, data: list[ProjectCreate]):
        """
        INSERT INTO projects (...) VALUES (...), (...);
        """
        projects = [Project(**item.dict()) for item in data]

        self.session.add_all(projects)

        try:
            await self.session.commit()
            for p in projects:
                await self.session.refresh(p)
        except Exception:
            await self.session.rollback()
            raise DatabaseException("Ошибка массового создания")

        return projects

# старый вариант update
    # async def update(self, project_id: int, data: ProjectUpdate):
    #     """
    #     UPDATE projects SET ... WHERE id = :project_id;
    #     """
    #     project = await self.get_by_id(project_id)
    #
    #     for field, value in data.dict(exclude_unset=True).items():
    #         if field == "create_time":
    #             continue
    #         setattr(project, field, value)
    #
    #     try:
    #         await self.session.commit()
    #         await self.session.refresh(project)
    #     except Exception:
    #         await self.session.rollback()
    #         raise DatabaseException("Ошибка обновления")
    #
    #     return project

    async def update(self, project_id: int, data: ProjectUpdate) -> Project:
        """
        UPDATE projects SET ... WHERE id = :project_id;
        """
        update_data = data.dict(exclude_unset=True)
        # запрещаем обновление create_time
        update_data.pop("create_time", None)

        try:
            async with self.session as session:
                async with session.begin():
                    stmt = (
                        update(Project)
                        .where(Project.id == project_id)
                        .values(**update_data)
                        .returning(Project)
                    )

                    result = await session.execute(stmt)

                    project = result.scalar_one_or_none()

                    if not project:
                        raise NotFoundException("Проект не найден")

                return project
        except NotFoundException:
            raise

        except Exception:
            raise DatabaseException("Ошибка обновления")

# старый вариант delete
    # async def delete(self, project_id: int):
    #     """
    #     DELETE FROM projects WHERE id = :project_id;
    #     """
    #     project = await self.get_by_id(project_id)
    #
    #     await self.session.delete(project)
    #
    #     try:
    #         await self.session.commit()
    #     except Exception:
    #         await self.session.rollback()
    #         raise DatabaseException("Ошибка удаления")
    #
    #     return project

    async def delete(self, project_id: int) -> Project:
        """
        DELETE FROM projects
        WHERE id = :project_id
        RETURNING *;
        """

        try:
            async with self.session as session:
                async with session.begin():

                    stmt = (
                        delete(Project)
                        .where(Project.id == project_id)
                        .returning(Project)
                    )

                    result = await session.execute(stmt)

                    deleted_project = result.scalar_one_or_none()

                    if not deleted_project:
                        raise NotFoundException("Проект не найден")

                # commit автоматически

                return deleted_project

        except NotFoundException:
            raise

        except Exception:
            raise DatabaseException("Ошибка удаления")
