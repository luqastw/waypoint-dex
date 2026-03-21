from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

ADRStatus = Literal["proposed", "accepted", "deprecated"]


class ADRCreate(BaseModel):
    title: str
    context: str
    decision: str
    consequences: str


class ADRUpdate(BaseModel):
    title: str | None = None
    context: str | None = None
    decision: str | None = None
    consequences: str | None = None
    status: ADRStatus | None = None


class ADRResponse(BaseModel):
    id: UUID
    title: str
    context: str
    decision: str
    consequences: str
    status: str
    version: int
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
