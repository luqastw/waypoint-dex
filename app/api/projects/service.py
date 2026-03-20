from uuid import UUID
from fastapi import HTTPException, status

from app.api.projects.repository import ProjectRepository
from app.api.projects.schemas import ProjectCreate, ProjectUpdate
from app.models.user import User
from app.models.project import Project


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    async def get_all(self, user: User) -> list[Project]:
        return await self.repository.get_all(user.id)

    async def get_by_id(self, user: User, project_id: UUID) -> Project:
        project = await self.repository.get_by_id(project_id, user.id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        return project

    async def create(self, data: ProjectCreate, user: User) -> Project:
        return await self.repository.create(data, user.id)

    async def update(
        self, data: ProjectUpdate, user: User, project_id: UUID
    ) -> Project:
        await self.get_by_id(user, project_id)
        return await self.repository.update(data, project_id, user.id)

    async def delete(self, project_id: UUID, user: User) -> None:
        await self.get_by_id(user, project_id)
        return await self.repository.delete(project_id, user.id)
