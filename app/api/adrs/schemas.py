from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

ADRStatus = Literal["proposed", "accepted", "deprecated"]


class ADRCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    context: str = Field(..., min_length=1, max_length=10000)
    decision: str = Field(..., min_length=1, max_length=10000)
    consequences: str = Field(..., min_length=1, max_length=10000)


class ADRUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    context: str | None = Field(default=None, min_length=1, max_length=10000)
    decision: str | None = Field(default=None, min_length=1, max_length=10000)
    consequences: str | None = Field(default=None, min_length=1, max_length=10000)
    status: ADRStatus | None = None


class ADRResponse(BaseModel):
    id: UUID
    title: str
    context: str
    decision: str
    consequences: str
    status: ADRStatus
    version: int
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
