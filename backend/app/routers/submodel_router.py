from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.submodel_schemas import Submodel, SubmodelCreate
from app.services import submodel_service
from app.exceptions.submodel_exc import (
    SubmodelAlreadyExists,
    CarModelNotFound,
    SubmodelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/submodels")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Submodel)
async def post_submodel(data: SubmodelCreate, db: AsyncSession = Depends(get_db)):
    try:
        submodel = await submodel_service.create_submodel(data, db)
        return submodel

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except SubmodelAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Submodel])
async def get_all_submodels(db: AsyncSession = Depends(get_db)):
    submodels = await submodel_service.get_all_submodels(db)
    return submodels


@router.get(
    "/by-id/{submodel_id}", status_code=status.HTTP_200_OK, response_model=Submodel
)
async def get_submodel_by_id(submodel_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        submodel = await submodel_service.get_submodel_by_id(submodel_id, db)
        return submodel

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/by-model/{model_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[Submodel],
)
async def get_submodels_by_model_id(model_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        submodels = await submodel_service.get_submodels_by_model_id(model_id, db)
        return submodels

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/by-name", status_code=status.HTTP_200_OK, response_model=Submodel)
async def get_submodel_by_name(
    name: str = Query(..., description="Submodel name to search for"),
    db: AsyncSession = Depends(get_db),
):
    try:
        submodel = await submodel_service.get_submodel_by_name(name, db)
        return submodel

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{submodel_id}", status_code=status.HTTP_200_OK, response_model=Submodel)
async def update_submodel(
    submodel_id: UUID, data: SubmodelCreate, db: AsyncSession = Depends(get_db)
):
    try:
        submodel = await submodel_service.update_submodel(submodel_id, data, db)
        return submodel

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except SubmodelAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{submodel_id}", status_code=status.HTTP_200_OK, response_model=Submodel
)
async def delete_submodel(submodel_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        submodel = await submodel_service.delete_submodel(submodel_id, db)
        return submodel

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
