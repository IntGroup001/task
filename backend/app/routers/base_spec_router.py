from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.base_spec_schemas import (
    BaseSpecification,
    BaseSpecificationCreate,
)
from app.services import base_spec_service
from app.exceptions.base_spec_exc import (
    BaseSpecificationAlreadyExists,
    GenerationNotFound,
    BaseSpecificationNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/base-specifications")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseSpecification)
async def post_base_specification(
    data: BaseSpecificationCreate, db: AsyncSession = Depends(get_db)
):
    try:
        base_spec = await base_spec_service.create_base_specification(data, db)
        return base_spec

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except BaseSpecificationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[BaseSpecification])
async def get_all_base_specifications(db: AsyncSession = Depends(get_db)):
    base_specs = await base_spec_service.get_all_base_specifications(db)
    return base_specs


@router.get(
    "/by-id/{base_spec_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseSpecification,
)
async def get_base_specification_by_id(
    base_spec_id: UUID, db: AsyncSession = Depends(get_db)
):
    try:
        base_spec = await base_spec_service.get_base_specification_by_id(
            base_spec_id, db
        )
        return base_spec

    except BaseSpecificationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/by-generation/{generation_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[BaseSpecification],
)
async def get_base_specifications_by_generation_id(
    generation_id: UUID, db: AsyncSession = Depends(get_db)
):
    try:
        base_specs = await base_spec_service.get_base_specifications_by_generation_id(
            generation_id, db
        )
        return base_specs

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/by-year", status_code=status.HTTP_200_OK, response_model=List[BaseSpecification]
)
async def get_base_specifications_by_year_and_generation(
    year: int = Query(..., description="Year to search for"),
    generation_id: UUID = Query(..., description="Generation ID"),
    db: AsyncSession = Depends(get_db),
):
    try:
        base_specs = (
            await base_spec_service.get_base_specifications_by_year_and_generation(
                year, generation_id, db
            )
        )
        return base_specs

    except BaseSpecificationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
