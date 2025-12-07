from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from app.schemas.brand_schemas import Brand as BrandSchema, BrandCreate
from app.repositories.brand import BrandRepository
from app.exceptions.brand_exc import BrandAlreadyExists
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
