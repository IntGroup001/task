from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.schemas.car_model_schemas import CarModel as CarModelSchema, CarModelCreate
from app.repositories.car_model import CarModelRepository
from app.repositories.brand import BrandRepository
from app.exceptions.car_model_exc import (
    CarModelAlreadyExists,
    BrandNotFound,
    CarModelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


async def create_car_model(
    car_model_data: CarModelCreate, db: AsyncSession
) -> CarModelSchema:
    brand = await BrandRepository.select_by_id(db, car_model_data.brand_id)
    if not brand:
        raise BrandNotFound(f"Brand with id '{car_model_data.brand_id}' not found")

    try:
        car_model = await CarModelRepository.insert(db, car_model_data.model_dump())
        return CarModelSchema.model_validate(car_model)

    except IntegrityError as e:
        original = e.orig

        if isinstance(original, ForeignKeyViolationError):
            raise BrandNotFound(f"Brand with id '{car_model_data.brand_id}' not found")

        elif isinstance(original, UniqueViolationError):
            raise CarModelAlreadyExists(
                f"Car model with name '{car_model_data.name}' already exists for this brand"
            )

        else:
            raise DatabaseIntegrityError(str(original))


async def get_all_car_models(db: AsyncSession) -> List[CarModelSchema]:
    car_models = await CarModelRepository.select_all(db)
    return [CarModelSchema.model_validate(car_model) for car_model in car_models]


async def get_car_model_by_id(car_model_id: UUID, db: AsyncSession) -> CarModelSchema:
    car_model = await CarModelRepository.select_by_id(db, car_model_id)

    if not car_model:
        raise CarModelNotFound(f"Car model with id '{car_model_id}' not found")

    return CarModelSchema.model_validate(car_model)


async def get_car_models_by_brand_id(
    brand_id: UUID, db: AsyncSession
) -> List[CarModelSchema]:
    brand = await BrandRepository.select_by_id(db, brand_id)
    if not brand:
        raise BrandNotFound(f"Brand with id '{brand_id}' not found")

    car_models = await CarModelRepository.select_by_brand_id(db, brand_id)
    return [CarModelSchema.model_validate(car_model) for car_model in car_models]


async def get_car_model_by_name_and_brand(
    name: str, brand_id: UUID, db: AsyncSession
) -> CarModelSchema:
    car_model = await CarModelRepository.select_by_name_and_brand(db, name, brand_id)

    if not car_model:
        raise CarModelNotFound(
            f"Car model with name '{name}' not found for brand id '{brand_id}'"
        )

    return CarModelSchema.model_validate(car_model)
