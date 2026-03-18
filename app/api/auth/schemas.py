from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str


class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
