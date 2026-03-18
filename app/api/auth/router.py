from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.repository import UserRepository
from app.api.auth.schemas import TokenResponse, UserRegister, UserResponse
from app.api.auth.service import AuthService
from app.core.database import get_session
from app.core.security import create_access_token

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user with the provided information.",
)
async def register(
    user_data: UserRegister, session: AsyncSession = Depends(get_session)
) -> UserResponse:
    repository = UserRepository(session)
    service = AuthService(repository)
    return await service.register(user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login a existent account.",
    description="Enter in a existent account with the provided information.",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    repository = UserRepository(session)
    service = AuthService(repository)
    user = await service.authenticate(form_data.username, form_data.password)
    token = create_access_token({"sub": user.username})

    return TokenResponse(access_token=token, token_type="bearer")
