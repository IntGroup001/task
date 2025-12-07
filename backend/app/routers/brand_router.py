from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.brand_schemas import Brand, BrandCreate
from app.services import brand_service
from app.exceptions.brand_exc import BrandAlreadyExists
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/brands")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Brand)
async def post_router(data: BrandCreate, db: AsyncSession = Depends(get_db)):
    try:
        brand = await brand_service.create_brand(data, db)
        return brand

    except BrandAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(str(e)))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(str(e)))
