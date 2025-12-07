from typing import List
from uuid import UUID

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
    GenerationNotFound,
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


async def get_all_generations(db: AsyncSession) -> List[GenerationSchema]:
    generations = await GenerationRepository.select_all(db)
    return [GenerationSchema.model_validate(generation) for generation in generations]


async def get_generation_by_id(
    generation_id: UUID, db: AsyncSession
) -> GenerationSchema:
    generation = await GenerationRepository.select_by_id(db, generation_id)

    if not generation:
        raise GenerationNotFound(f"Generation with id '{generation_id}' not found")

    return GenerationSchema.model_validate(generation)


async def get_generations_by_submodel_id(
    submodel_id: UUID, db: AsyncSession
) -> List[GenerationSchema]:
    submodel = await SubmodelRepository.select_by_id(db, submodel_id)
    if not submodel:
        raise SubmodelNotFound(f"Submodel with id '{submodel_id}' not found")

    generations = await GenerationRepository.select_by_submodel_id(db, submodel_id)
    return [GenerationSchema.model_validate(generation) for generation in generations]


async def get_generation_by_name_and_submodel(
    name: str, submodel_id: UUID, db: AsyncSession
) -> GenerationSchema:
    generation = await GenerationRepository.select_by_name_and_submodel(
        db, name, submodel_id
    )

    if not generation:
        raise GenerationNotFound(
            f"Generation with name '{name}' not found for submodel id '{submodel_id}'"
        )

    return GenerationSchema.model_validate(generation)
