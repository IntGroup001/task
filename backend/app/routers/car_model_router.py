from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.car_model_schemas import CarModel, CarModelCreate
from app.services import car_model_service
from app.exceptions.car_model_exc import (
    CarModelAlreadyExists,
    BrandNotFound,
    CarModelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/car-models")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CarModel)
async def post_car_model(data: CarModelCreate, db: AsyncSession = Depends(get_db)):
    try:
        car_model = await car_model_service.create_car_model(data, db)
        return car_model

    except BrandNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except CarModelAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CarModel])
async def get_all_car_models(db: AsyncSession = Depends(get_db)):
    car_models = await car_model_service.get_all_car_models(db)
    return car_models


@router.get(
    "/by-id/{car_model_id}", status_code=status.HTTP_200_OK, response_model=CarModel
)
async def get_car_model_by_id(car_model_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        car_model = await car_model_service.get_car_model_by_id(car_model_id, db)
        return car_model

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/by-brand/{brand_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[CarModel],
)
async def get_car_models_by_brand_id(
    brand_id: UUID, db: AsyncSession = Depends(get_db)
):
    try:
        car_models = await car_model_service.get_car_models_by_brand_id(brand_id, db)
        return car_models

    except BrandNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/by-name", status_code=status.HTTP_200_OK, response_model=CarModel)
async def get_car_model_by_name_and_brand(
    name: str = Query(..., description="Car model name to search for"),
    brand_id: UUID = Query(..., description="Brand ID"),
    db: AsyncSession = Depends(get_db),
):
    try:
        car_model = await car_model_service.get_car_model_by_name_and_brand(
            name, brand_id, db
        )
        return car_model

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{car_model_id}", status_code=status.HTTP_200_OK, response_model=CarModel)
async def update_car_model(
    car_model_id: UUID, data: CarModelCreate, db: AsyncSession = Depends(get_db)
):
    try:
        car_model = await car_model_service.update_car_model(car_model_id, data, db)
        return car_model

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except CarModelAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{car_model_id}", status_code=status.HTTP_200_OK, response_model=CarModel
)
async def delete_car_model(car_model_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        car_model = await car_model_service.delete_car_model(car_model_id, db)
        return car_model

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
