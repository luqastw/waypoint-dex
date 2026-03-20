from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.user import User
from app.api.projects.repository import ProjectRepository
from app.api.projects.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.api.projects.service import ProjectService
from app.core.database import get_session
from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=list[ProjectResponse])
async def list_all(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = ProjectRepository(session)
    service = ProjectService(repository)
    return await service.get_all(current_user)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_by_id(
    project_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = ProjectRepository(session)
    service = ProjectService(repository)
    return await service.get_by_id(current_user, project_id)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create(
    data: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = ProjectRepository(session)
    service = ProjectService(repository)
    return await service.create(data, current_user)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update(
    data: ProjectUpdate,
    project_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = ProjectRepository(session)
    service = ProjectService(repository)
    return await service.update(data, current_user, project_id)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    project_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = ProjectRepository(session)
    service = ProjectService(repository)
    return await service.delete(project_id, current_user)
