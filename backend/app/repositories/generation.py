from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.generation import Generation


class GenerationRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[Generation]:
        result = await db.execute(select(Generation).where(Generation.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[Generation]:
        result = await db.execute(select(Generation))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_submodel_id(
        db: AsyncSession, submodel_id: UUID
    ) -> List[Generation]:
        result = await db.execute(
            select(Generation).where(Generation.submodel_id == submodel_id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def select_by_name_and_submodel(
        db: AsyncSession, name: str, submodel_id: UUID
    ) -> Optional[Generation]:
        result = await db.execute(
            select(Generation).where(
                Generation.name == name, Generation.submodel_id == submodel_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> Generation:
        generation = Generation(**obj_in)
        db.add(generation)
        await db.commit()
        await db.refresh(generation)
        return generation

    @staticmethod
    async def update(db: AsyncSession, db_obj: Generation, obj_in: dict) -> Generation:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[Generation]:
        result = await db.execute(select(Generation).where(Generation.id == id))
        generation = result.scalar_one_or_none()

        if generation:
            await db.delete(generation)
            await db.commit()

        return generation
