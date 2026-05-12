from utils.exceptions import NotFoundException
from .repository import ProjectRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def get_project(self, project_id: int):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project not found")
        return project

    async def get_projects(self, **kwargs):
        return await self.repo.get_all(**kwargs)

    async def create_project(self, data):
        return await self.repo.create(data)

    async def create_many(self, data):
        return await self.repo.create_many(data)

    async def update_project(self, project_id, data):
        return await self.repo.update(project_id, data)

    async def delete_project(self, project_id):
        return await self.repo.delete(project_id)
