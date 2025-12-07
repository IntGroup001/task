from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.schemas.generation_schemas import (
    Generation as GenerationSchema,
    GenerationCreate,
)
from app.repositories.generation import GenerationRepository
from app.repositories.submodel import SubmodelRepository
from app.exceptions.generation_exc import (
    GenerationAlreadyExists,
    SubmodelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


async def create_generation(
    generation_data: GenerationCreate, db: AsyncSession
) -> GenerationSchema:
    submodel = await SubmodelRepository.select_by_id(db, generation_data.submodel_id)
    if not submodel:
        raise SubmodelNotFound(
            f"Submodel with id '{generation_data.submodel_id}' not found"
        )

    try:
        generation = await GenerationRepository.insert(db, generation_data.model_dump())
        return GenerationSchema.model_validate(generation)

    except IntegrityError as e:
        original = e.orig

        if isinstance(original, ForeignKeyViolationError):
            raise SubmodelNotFound(
                f"Submodel with id '{generation_data.submodel_id}' not found"
            )

        elif isinstance(original, UniqueViolationError):
            raise GenerationAlreadyExists(
                f"Generation with name '{generation_data.name}' already exists for this submodel"
            )

        else:
            raise DatabaseIntegrityError(str(original))
