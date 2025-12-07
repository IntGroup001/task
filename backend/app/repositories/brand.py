from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.brand import Brand


class BrandRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id) -> Optional[Brand]:
        result = await db.execute(select(Brand).where(Brand.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[Brand]:
        result = await db.execute(select(Brand))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_name(db: AsyncSession, name: str) -> Optional[Brand]:
        result = await db.execute(select(Brand).where(Brand.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> Brand:
        brand = Brand(**obj_in)
        db.add(brand)
        await db.commit()
        await db.refresh(brand)
        return brand

    @staticmethod
    async def update(db: AsyncSession, db_obj: Brand, obj_in: dict) -> Brand:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id) -> Optional[Brand]:
        result = await db.execute(select(Brand).where(Brand.id == id))
        brand = result.scalar_one_or_none()

        if brand:
            await db.delete(brand)
            await db.commit()

        return brand
