from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.brand_schemas import Brand, BrandCreate
from app.services import brand_service
from app.exceptions.brand_exc import BrandAlreadyExists, BrandNotFound
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/brands")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Brand)
async def post_brand(data: BrandCreate, db: AsyncSession = Depends(get_db)):
    try:
        brand = await brand_service.create_brand(data, db)
        return brand

    except BrandAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Brand])
async def get_all_brands(db: AsyncSession = Depends(get_db)):
    brands = await brand_service.get_all_brands(db)
    return brands


@router.get("/by-id/{brand_id}", status_code=status.HTTP_200_OK, response_model=Brand)
async def get_brand_by_id(brand_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        brand = await brand_service.get_brand_by_id(brand_id, db)
        return brand

    except BrandNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/by-name", status_code=status.HTTP_200_OK, response_model=Brand)
async def get_brand_by_name(
    name: str = Query(..., description="Brand name to search for"),
    db: AsyncSession = Depends(get_db),
):
    try:
        brand = await brand_service.get_brand_by_name(name, db)
        return brand

    except BrandNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{brand_id}", status_code=status.HTTP_200_OK, response_model=Brand)
async def update_brand(
    brand_id: UUID, data: BrandCreate, db: AsyncSession = Depends(get_db)
):
    try:
        brand = await brand_service.update_brand(brand_id, data, db)
        return brand

    except BrandNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except BrandAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{brand_id}", status_code=status.HTTP_200_OK, response_model=Brand)
async def delete_brand(brand_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        brand = await brand_service.delete_brand(brand_id, db)
        return brand

    except BrandNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
