from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.car_data_schemas import CarDataResponse
from app.services import car_data_service


router = APIRouter(prefix="/car-data")


@router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=List[CarDataResponse]
)
async def get_all_car_data(db: AsyncSession = Depends(get_db)):
    return await car_data_service.get_all_car_data(db)
