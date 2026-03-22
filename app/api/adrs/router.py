from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.adrs.repository import ADRRepository
from app.api.adrs.schemas import ADRCreate, ADRResponse, ADRUpdate
from app.api.adrs.service import ADRService
from app.api.projects.repository import ProjectRepository
from app.core.dependencies import get_current_user
from app.core.database import get_session
from app.models.user import User

router = APIRouter()


def get_adr_service(session: AsyncSession = Depends(get_session)) -> ADRService:
    project_repository = ProjectRepository(session)
    adr_repository = ADRRepository(session)
    return ADRService(adr_repository, project_repository)


@router.get("/", response_model=list[ADRResponse])
async def get_all(
    project_id: UUID,
    user: User = Depends(get_current_user),
    service: ADRService = Depends(get_adr_service),
):
    return await service.get_all(project_id, user)


@router.get("/{adr_id}", response_model=ADRResponse)
async def get_by_id(
    project_id: UUID,
    adr_id: UUID,
    user: User = Depends(get_current_user),
    service: ADRService = Depends(get_adr_service),
):
    return await service.get_by_id(project_id, adr_id, user)


@router.post("/", response_model=ADRResponse, status_code=status.HTTP_201_CREATED)
async def create(
    data: ADRCreate,
    project_id: UUID,
    user: User = Depends(get_current_user),
    service: ADRService = Depends(get_adr_service),
):
    return await service.create(data, project_id, user)


@router.patch("/{adr_id}", response_model=ADRResponse)
async def update(
    data: ADRUpdate,
    adr_id: UUID,
    project_id: UUID,
    user: User = Depends(get_current_user),
    service: ADRService = Depends(get_adr_service),
):
    return await service.update(data, adr_id, project_id, user)


@router.delete("/{adr_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    adr_id: UUID,
    project_id: UUID,
    user: User = Depends(get_current_user),
    service: ADRService = Depends(get_adr_service),
):
    return await service.delete(adr_id, project_id, user)
