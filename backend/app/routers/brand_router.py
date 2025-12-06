from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.brand import Brand, BrandCreate


router = APIRouter(prefix="/brands")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Brand)
async def post_router(data: BrandCreate, db: AsyncSession = Depends(get_db)):
    pass


