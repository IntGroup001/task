from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.submodel import Submodel


class SubmodelRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[Submodel]:
        result = await db.execute(select(Submodel).where(Submodel.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[Submodel]:
        result = await db.execute(select(Submodel))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_model_id(db: AsyncSession, model_id: UUID) -> List[Submodel]:
        result = await db.execute(select(Submodel).where(Submodel.model_id == model_id))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_name(db: AsyncSession, name: str) -> Optional[Submodel]:
        result = await db.execute(select(Submodel).where(Submodel.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> Submodel:
        submodel = Submodel(**obj_in)
        db.add(submodel)
        await db.commit()
        await db.refresh(submodel)
        return submodel

    @staticmethod
    async def update(db: AsyncSession, db_obj: Submodel, obj_in: dict) -> Submodel:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[Submodel]:
        result = await db.execute(select(Submodel).where(Submodel.id == id))
        submodel = result.scalar_one_or_none()

        if submodel:
            await db.delete(submodel)
            await db.commit()

        return submodel
