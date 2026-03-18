from fastapi import HTTPException, status

from app.core.security import hash_password, create_access_token, verify_password
from app.api.auth.repository import UserRepository
from app.api.auth.schemas import UserCreate, UserRegister
from app.models.user import User


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register(self, user_data: UserRegister) -> User:
        user_email = await self.repository.get_by_email(user_data.email)
        user_username = await self.repository.get_by_username(user_data.username)

        if user_email is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use."
            )
        if user_username is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use.",
            )

        user_create = UserCreate(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
        )

        user = await self.repository.create(user_create)
        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.repository.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
            )

        return user
