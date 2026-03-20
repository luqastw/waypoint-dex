from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.api.projects.schemas import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, owner_id: UUID) -> list[Project]:
        stmt = select(Project).where(Project.owner_id == owner_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, id: UUID, owner_id: UUID) -> Project | None:
        stmt = select(Project).where(Project.id == id, Project.owner_id == owner_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: ProjectCreate, owner_id: UUID) -> Project:
        project = Project(
            owner_id=owner_id,
            name=data.name,
            description=data.description,
            status=data.status,
            stack=data.stack,
            github_url=str(data.github_url) if data.github_url else None,
            started_at=data.started_at,
        )

        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update(
        self, data: ProjectUpdate, id: UUID, owner_id: UUID
    ) -> Project | None:
        project = await self.get_by_id(id, owner_id)

        if project is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, id: UUID, owner_id: UUID) -> bool:
        project = await self.get_by_id(id, owner_id)

        if project is None:
            return False

        await self.session.delete(project)
        await self.session.commit()
        return True
