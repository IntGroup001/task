from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.car_model_schemas import CarModel, CarModelCreate
from app.services import car_model_service
from app.exceptions.car_model_exc import (
    CarModelAlreadyExists,
    BrandNotFound,
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
