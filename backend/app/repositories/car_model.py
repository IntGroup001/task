from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.car_model import CarModel


class CarModelRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[CarModel]:
        result = await db.execute(select(CarModel).where(CarModel.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[CarModel]:
        result = await db.execute(select(CarModel))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_brand_id(db: AsyncSession, brand_id: UUID) -> List[CarModel]:
        result = await db.execute(select(CarModel).where(CarModel.brand_id == brand_id))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_name_and_brand(
        db: AsyncSession, name: str, brand_id: UUID
    ) -> Optional[CarModel]:
        result = await db.execute(
            select(CarModel).where(CarModel.name == name, CarModel.brand_id == brand_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> CarModel:
        car_model = CarModel(**obj_in)
        db.add(car_model)
        await db.commit()
        await db.refresh(car_model)
        return car_model

    @staticmethod
    async def update(db: AsyncSession, db_obj: CarModel, obj_in: dict) -> CarModel:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[CarModel]:
        result = await db.execute(select(CarModel).where(CarModel.id == id))
        car_model = result.scalar_one_or_none()

        if car_model:
            await db.delete(car_model)
            await db.commit()

        return car_model
