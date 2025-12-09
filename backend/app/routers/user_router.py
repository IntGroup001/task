from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.user_schemas import User, UserCreate, UserUpdate, UserUpdatePassword
from app.services import user_service
from app.dependancies.auth import require_admin, get_current_active_user
from app.models.user import User as UserModel
from app.exceptions.user_exc import UserAlreadyExists, UserNotFound
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
async def get_current_user(current_user: UserModel = Depends(get_current_active_user)):
    from app.schemas.user_schemas import User as UserSchema

    return UserSchema.model_validate(current_user)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[User],
    dependencies=[Depends(require_admin)],
)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(db)
    return users


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    dependencies=[Depends(require_admin)],
)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await user_service.get_user_by_id(user_id, db)
        return user

    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    dependencies=[Depends(require_admin)],
)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await user_service.create_user(data, db)
        return user

    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    dependencies=[Depends(require_admin)],
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await user_service.update_user(user_id, data, db)
        return user

    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put(
    "/{user_id}/password",
    status_code=status.HTTP_200_OK,
    response_model=User,
    dependencies=[Depends(require_admin)],
)
async def update_user_password(
    user_id: UUID,
    data: UserUpdatePassword,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await user_service.update_user_password(user_id, data, db)
        return user

    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    dependencies=[Depends(require_admin)],
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await user_service.delete_user(user_id, db)
        return user

    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
