from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.schemas.base_spec_schemas import (
    BaseSpecification as BaseSpecificationSchema,
    BaseSpecificationCreate,
)
from app.repositories.base_spec import BaseSpecificationRepository
from app.repositories.generation import GenerationRepository
from app.exceptions.base_spec_exc import (
    BaseSpecificationAlreadyExists,
    GenerationNotFound,
    BaseSpecificationNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


async def create_base_specification(
    base_spec_data: BaseSpecificationCreate, db: AsyncSession
) -> BaseSpecificationSchema:
    generation = await GenerationRepository.select_by_id(
        db, base_spec_data.generation_id
    )
    if not generation:
        raise GenerationNotFound(
            f"Generation with id '{base_spec_data.generation_id}' not found"
        )

    try:
        base_spec = await BaseSpecificationRepository.insert(
            db, base_spec_data.model_dump()
        )
        return BaseSpecificationSchema.model_validate(base_spec)

    except IntegrityError as e:
        original = e.orig

        if isinstance(original, ForeignKeyViolationError):
            raise GenerationNotFound(
                f"Generation with id '{base_spec_data.generation_id}' not found"
            )

        elif isinstance(original, UniqueViolationError):
            raise BaseSpecificationAlreadyExists(
                "Base specification already exists for this generation"
            )

        else:
            raise DatabaseIntegrityError(str(original))


async def get_all_base_specifications(
    db: AsyncSession,
) -> List[BaseSpecificationSchema]:
    base_specs = await BaseSpecificationRepository.select_all(db)
    return [
        BaseSpecificationSchema.model_validate(base_spec) for base_spec in base_specs
    ]


async def get_base_specification_by_id(
    base_spec_id: UUID, db: AsyncSession
) -> BaseSpecificationSchema:
    base_spec = await BaseSpecificationRepository.select_by_id(db, base_spec_id)

    if not base_spec:
        raise BaseSpecificationNotFound(
            f"Base specification with id '{base_spec_id}' not found"
        )

    return BaseSpecificationSchema.model_validate(base_spec)


async def get_base_specifications_by_generation_id(
    generation_id: UUID, db: AsyncSession
) -> List[BaseSpecificationSchema]:
    generation = await GenerationRepository.select_by_id(db, generation_id)
    if not generation:
        raise GenerationNotFound(f"Generation with id '{generation_id}' not found")

    base_specs = await BaseSpecificationRepository.select_by_generation_id(
        db, generation_id
    )
    return [
        BaseSpecificationSchema.model_validate(base_spec) for base_spec in base_specs
    ]


async def get_base_specifications_by_year_and_generation(
    year: int, generation_id: UUID, db: AsyncSession
) -> List[BaseSpecificationSchema]:
    base_specs = await BaseSpecificationRepository.select_by_year_and_generation(
        db, year, generation_id
    )

    if not base_specs:
        raise BaseSpecificationNotFound(
            f"Base specifications not found for year '{year}' and generation id '{generation_id}'"
        )

    return [
        BaseSpecificationSchema.model_validate(base_spec) for base_spec in base_specs
    ]
