from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.generation_schemas import Generation, GenerationCreate
from app.services import generation_service
from app.exceptions.generation_exc import (
    GenerationAlreadyExists,
    SubmodelNotFound,
    GenerationNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/generations")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Generation)
async def post_generation(data: GenerationCreate, db: AsyncSession = Depends(get_db)):
    try:
        generation = await generation_service.create_generation(data, db)
        return generation

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except GenerationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Generation])
async def get_all_generations(db: AsyncSession = Depends(get_db)):
    generations = await generation_service.get_all_generations(db)
    return generations


@router.get(
    "/by-id/{generation_id}", status_code=status.HTTP_200_OK, response_model=Generation
)
async def get_generation_by_id(generation_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        generation = await generation_service.get_generation_by_id(generation_id, db)
        return generation

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/by-submodel/{submodel_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[Generation],
)
async def get_generations_by_submodel_id(
    submodel_id: UUID, db: AsyncSession = Depends(get_db)
):
    try:
        generations = await generation_service.get_generations_by_submodel_id(
            submodel_id, db
        )
        return generations

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/by-name", status_code=status.HTTP_200_OK, response_model=Generation)
async def get_generation_by_name_and_submodel(
    name: str = Query(..., description="Generation name to search for"),
    submodel_id: UUID = Query(..., description="Submodel ID"),
    db: AsyncSession = Depends(get_db),
):
    try:
        generation = await generation_service.get_generation_by_name_and_submodel(
            name, submodel_id, db
        )
        return generation

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{generation_id}", status_code=status.HTTP_200_OK, response_model=Generation
)
async def update_generation(
    generation_id: UUID, data: GenerationCreate, db: AsyncSession = Depends(get_db)
):
    try:
        generation = await generation_service.update_generation(generation_id, data, db)
        return generation

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except GenerationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{generation_id}", status_code=status.HTTP_200_OK, response_model=Generation
)
async def delete_generation(generation_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        generation = await generation_service.delete_generation(generation_id, db)
        return generation

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
