from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.adrs.schemas import ADRCreate, ADRUpdate
from app.models.adr import ADR


class ADRRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, project_id: UUID) -> list[ADR]:
        stmt = select(ADR).where(ADR.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, id: UUID, project_id: UUID) -> ADR | None:
        stmt = select(ADR).where(ADR.id == id, ADR.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: ADRCreate, project_id: UUID) -> ADR:
        adr = ADR(
            project_id=project_id,
            title=data.title,
            context=data.context,
            decision=data.decision,
            consequences=data.consequences,
        )

        self.session.add(adr)
        await self.session.commit()
        await self.session.refresh(adr)
        return adr

    async def update(self, data: ADRUpdate, id: UUID, project_id: UUID) -> ADR | None:
        adr = await self.get_by_id(id, project_id)

        if adr is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(adr, field, value)

        await self.session.commit()
        await self.session.refresh(adr)
        return adr

    async def delete(self, id: UUID, project_id: UUID) -> None:
        adr = await self.get_by_id(id, project_id)

        if adr is None:
            return None

        await self.session.delete(adr)
        await self.session.commit()
        return None
