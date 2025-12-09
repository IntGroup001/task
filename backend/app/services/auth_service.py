from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.user_schemas import UserCreate, User as UserSchema, Token, UserLogin
from app.repositories.user import UserRepository
from app.dependancies.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.exceptions.user_exc import UserAlreadyExists, InvalidCredentials
from app.exceptions.common import DatabaseIntegrityError


async def register_user(user_data: UserCreate, db: AsyncSession) -> UserSchema:
    existing_user = await UserRepository.select_by_email(db, user_data.email)
    if existing_user:
        raise UserAlreadyExists(f"User with email '{user_data.email}' already exists")

    existing_username = await UserRepository.select_by_username(db, user_data.username)
    if existing_username:
        raise UserAlreadyExists(
            f"User with username '{user_data.username}' already exists"
        )

    try:
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hash_password(user_data.password)

        user = await UserRepository.insert(db, user_dict)
        return UserSchema.model_validate(user)

    except IntegrityError as e:
        original = e.orig
        if isinstance(original, UniqueViolationError):
            raise UserAlreadyExists("User with this email or username already exists")
        else:
            raise DatabaseIntegrityError(str(original))


async def login_user(credentials: UserLogin, db: AsyncSession) -> Token:
    user = await UserRepository.select_by_email(db, credentials.email)

    if not user:
        raise InvalidCredentials("Invalid email or password")

    if not verify_password(credentials.password, user.hashed_password):
        raise InvalidCredentials("Invalid email or password")

    if not user.is_active:
        raise InvalidCredentials("User account is inactive")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return Token(access_token=access_token, refresh_token=refresh_token)


async def refresh_access_token(refresh_token: str, db: AsyncSession) -> Token:
    try:
        user_id = verify_token(refresh_token)
        user = await UserRepository.select_by_id(db, UUID(user_id))

        if not user or not user.is_active:
            raise InvalidCredentials("Invalid refresh token")

        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)

        return Token(access_token=new_access_token, refresh_token=new_refresh_token)
    except Exception:
        raise InvalidCredentials("Invalid refresh token")
