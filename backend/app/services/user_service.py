from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.user_schemas import (
    User as UserSchema,
    UserCreate,
    UserUpdate,
    UserUpdatePassword,
)
from app.repositories.user import UserRepository
from app.dependancies.auth import hash_password
from app.exceptions.user_exc import UserAlreadyExists, UserNotFound
from app.exceptions.common import DatabaseIntegrityError


async def get_all_users(db: AsyncSession) -> List[UserSchema]:
    users = await UserRepository.select_all(db)
    return [UserSchema.model_validate(user) for user in users]


async def get_user_by_id(user_id: UUID, db: AsyncSession) -> UserSchema:
    user = await UserRepository.select_by_id(db, user_id)

    if not user:
        raise UserNotFound(f"User with id '{user_id}' not found")

    return UserSchema.model_validate(user)


async def create_user(user_data: UserCreate, db: AsyncSession) -> UserSchema:
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


async def update_user(
    user_id: UUID, user_data: UserUpdate, db: AsyncSession
) -> UserSchema:
    user = await UserRepository.select_by_id(db, user_id)

    if not user:
        raise UserNotFound(f"User with id '{user_id}' not found")

    try:
        update_dict = user_data.model_dump(exclude_unset=True)
        updated_user = await UserRepository.update(db, user, update_dict)
        return UserSchema.model_validate(updated_user)

    except IntegrityError as e:
        original = e.orig
        if isinstance(original, UniqueViolationError):
            raise UserAlreadyExists("User with this email or username already exists")
        else:
            raise DatabaseIntegrityError(str(original))


async def update_user_password(
    user_id: UUID, password_data: UserUpdatePassword, db: AsyncSession
) -> UserSchema:
    user = await UserRepository.select_by_id(db, user_id)

    if not user:
        raise UserNotFound(f"User with id '{user_id}' not found")

    hashed_password = hash_password(password_data.password)
    updated_user = await UserRepository.update(
        db, user, {"hashed_password": hashed_password}
    )
    return UserSchema.model_validate(updated_user)


async def delete_user(user_id: UUID, db: AsyncSession) -> UserSchema:
    user = await UserRepository.delete(db, user_id)

    if not user:
        raise UserNotFound(f"User with id '{user_id}' not found")

    return UserSchema.model_validate(user)
