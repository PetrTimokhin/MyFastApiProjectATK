from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from .services import ProjectService
from .repository import ProjectRepository
from DATABASES.db_postgres.connect_to_db import get_session  # твой dependency

project_router = APIRouter(prefix="/projects", tags=["Projects"])


async def get_service(session: AsyncSession = Depends(get_session)):
    repo = ProjectRepository(session)
    return ProjectService(repo)


@project_router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, service: ProjectService = Depends(get_service)):
    return await service.get_project(project_id)


@project_router.get("/")
async def get_projects(
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    person_id: int | None = None,
    order_by: str = "create_time",
    service: ProjectService = Depends(get_service),
):
    return await service.get_projects(
        page=page,
        limit=limit,
        status=status,
        person_id=person_id,
        order_by=order_by,
    )


@project_router.post("/", response_model=ProjectResponse)
async def create_project(data: ProjectCreate, service: ProjectService = Depends(get_service)):
    return await service.create_project(data)


@project_router.post("/bulk")
async def create_many(data: list[ProjectCreate], service: ProjectService = Depends(get_service)):
    return await service.create_many(data)


@project_router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_service),
):
    return await service.update_project(project_id, data)


@project_router.delete("/{project_id}", response_model=ProjectResponse)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_service),
):
    return await service.delete_project(project_id)