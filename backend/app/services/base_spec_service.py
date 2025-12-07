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
