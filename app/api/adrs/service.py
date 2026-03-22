from uuid import UUID
from fastapi import HTTPException, status

from app.api.adrs.repository import ADRRepository
from app.api.adrs.schemas import ADRCreate, ADRUpdate
from app.api.projects.repository import ProjectRepository
from app.models.adr import ADR
from app.models.user import User


class ADRService:
    def __init__(
        self, adr_repository: ADRRepository, project_repository: ProjectRepository
    ) -> None:
        self.adr_repository = adr_repository
        self.project_repository = project_repository

    async def _get_project_or_404(self, project_id: UUID, user: User):
        project = await self.project_repository.get_by_id(project_id, user.id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found."
            )
        return project

    async def _get_adr_or_404(self, adr_id: UUID, project_id: UUID) -> ADR:
        adr = await self.adr_repository.get_by_id(adr_id, project_id)
        if adr is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="ADR not found."
            )
        return adr

    async def get_all(self, project_id: UUID, user: User) -> list[ADR]:
        await self._get_project_or_404(project_id, user)
        return await self.adr_repository.get_all(project_id)

    async def get_by_id(self, project_id: UUID, adr_id: UUID, user: User) -> ADR:
        await self._get_project_or_404(project_id, user)
        return await self._get_adr_or_404(adr_id, project_id)

    async def create(self, data: ADRCreate, project_id: UUID, user: User) -> ADR:
        await self._get_project_or_404(project_id, user)
        return await self.adr_repository.create(data, project_id)

    async def update(
        self, data: ADRUpdate, adr_id: UUID, project_id: UUID, user: User
    ) -> ADR:
        await self._get_project_or_404(project_id, user)
        await self._get_adr_or_404(adr_id, project_id)
        adr = await self.adr_repository.update(data, adr_id, project_id)
        return adr

    async def delete(self, adr_id: UUID, project_id: UUID, user: User) -> None:
        await self._get_project_or_404(project_id, user)
        await self._get_adr_or_404(adr_id, project_id)
        await self.adr_repository.delete(adr_id, project_id)
        return None
