from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.schemas.submodel_schemas import Submodel as SubmodelSchema, SubmodelCreate
from app.repositories.submodel import SubmodelRepository
from app.repositories.car_model import CarModelRepository
from app.exceptions.submodel_exc import (
    SubmodelAlreadyExists,
    CarModelNotFound,
    SubmodelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


async def create_submodel(
    submodel_data: SubmodelCreate, db: AsyncSession
) -> SubmodelSchema:
    car_model = await CarModelRepository.select_by_id(db, submodel_data.model_id)
    if not car_model:
        raise CarModelNotFound(
            f"Car model with id '{submodel_data.model_id}' not found"
        )

    try:
        submodel = await SubmodelRepository.insert(db, submodel_data.model_dump())
        return SubmodelSchema.model_validate(submodel)

    except IntegrityError as e:
        original = e.orig

        if isinstance(original, ForeignKeyViolationError):
            raise CarModelNotFound(
                f"Car model with id '{submodel_data.model_id}' not found"
            )

        elif isinstance(original, UniqueViolationError):
            raise SubmodelAlreadyExists(
                f"Submodel with name '{submodel_data.name}' already exists"
            )

        else:
            raise DatabaseIntegrityError(str(original))


async def get_all_submodels(db: AsyncSession) -> List[SubmodelSchema]:
    submodels = await SubmodelRepository.select_all(db)
    return [SubmodelSchema.model_validate(submodel) for submodel in submodels]


async def get_submodel_by_id(submodel_id: UUID, db: AsyncSession) -> SubmodelSchema:
    submodel = await SubmodelRepository.select_by_id(db, submodel_id)

    if not submodel:
        raise SubmodelNotFound(f"Submodel with id '{submodel_id}' not found")

    return SubmodelSchema.model_validate(submodel)


async def get_submodels_by_model_id(
    model_id: UUID, db: AsyncSession
) -> List[SubmodelSchema]:
    car_model = await CarModelRepository.select_by_id(db, model_id)
    if not car_model:
        raise CarModelNotFound(f"Car model with id '{model_id}' not found")

    submodels = await SubmodelRepository.select_by_model_id(db, model_id)
    return [SubmodelSchema.model_validate(submodel) for submodel in submodels]


async def get_submodel_by_name(name: str, db: AsyncSession) -> SubmodelSchema:
    submodel = await SubmodelRepository.select_by_name(db, name)

    if not submodel:
        raise SubmodelNotFound(f"Submodel with name '{name}' not found")

    return SubmodelSchema.model_validate(submodel)
