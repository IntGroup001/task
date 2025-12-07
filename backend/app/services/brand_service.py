from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.brand_schemas import Brand as BrandSchema, BrandCreate
from app.repositories.brand import BrandRepository
from app.exceptions.brand_exc import BrandAlreadyExists, BrandNotFound
from app.exceptions.common import DatabaseIntegrityError


async def create_brand(brand_data: BrandCreate, db: AsyncSession) -> BrandSchema:
    try:
        brand = await BrandRepository.insert(db, brand_data.model_dump())
        return BrandSchema.model_validate(brand)

    except IntegrityError as e:
        original = e.orig

        if isinstance(original, UniqueViolationError):
            raise BrandAlreadyExists(
                f"Brand with name '{brand_data.name}' already exists"
            )

        else:
            raise DatabaseIntegrityError(str(original))


async def get_all_brands(db: AsyncSession) -> List[BrandSchema]:
    brands = await BrandRepository.select_all(db)
    return [BrandSchema.model_validate(brand) for brand in brands]


async def get_brand_by_id(brand_id: UUID, db: AsyncSession) -> BrandSchema:
    brand = await BrandRepository.select_by_id(db, brand_id)

    if not brand:
        raise BrandNotFound(f"Brand with id '{brand_id}' not found")

    return BrandSchema.model_validate(brand)


async def get_brand_by_name(name: str, db: AsyncSession) -> BrandSchema:
    brand = await BrandRepository.select_by_name(db, name)

    if not brand:
        raise BrandNotFound(f"Brand with name '{name}' not found")

    return BrandSchema.model_validate(brand)
