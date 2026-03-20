from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "active"
    stack: list[str]


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    stack: list[str] | None = None
    github_url: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    status: str
    stack: list[str]
    github_url: str | None = None
    owner_id: UUID
    started_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
