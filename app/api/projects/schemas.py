from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


ProjectStatus = Literal["active", "inactive", "completed", "archived"]


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus = "active"
    stack: list[str] = Field(..., min_length=1)
    github_url: HttpUrl | None = None
    started_at: datetime | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus | None = None
    stack: list[str] | None = Field(None, min_length=1)
    github_url: HttpUrl | None = None
    started_at: datetime | None = None


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
