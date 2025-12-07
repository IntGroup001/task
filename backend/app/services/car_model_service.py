from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.schemas.car_model_schemas import CarModel as CarModelSchema, CarModelCreate
from app.repositories.car_model import CarModelRepository
from app.repositories.brand import BrandRepository
from app.exceptions.car_model_exc import (
    CarModelAlreadyExists,
    BrandNotFound,
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
