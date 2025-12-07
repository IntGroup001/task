from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base_spec import BaseSpecification


class BaseSpecificationRepository:
    @staticmethod
    async def select_by_id(db: AsyncSession, id: UUID) -> Optional[BaseSpecification]:
        result = await db.execute(
            select(BaseSpecification).where(BaseSpecification.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def select_all(db: AsyncSession) -> List[BaseSpecification]:
        result = await db.execute(select(BaseSpecification))
        return list(result.scalars().all())

    @staticmethod
    async def select_by_generation_id(
        db: AsyncSession, generation_id: UUID
    ) -> List[BaseSpecification]:
        result = await db.execute(
            select(BaseSpecification).where(
                BaseSpecification.generation_id == generation_id
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def select_by_year_and_generation(
        db: AsyncSession, year: int, generation_id: UUID
    ) -> List[BaseSpecification]:
        result = await db.execute(
            select(BaseSpecification).where(
                BaseSpecification.year == year,
                BaseSpecification.generation_id == generation_id,
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def insert(db: AsyncSession, obj_in: dict) -> BaseSpecification:
        base_spec = BaseSpecification(**obj_in)
        db.add(base_spec)
        await db.commit()
        await db.refresh(base_spec)
        return base_spec

    @staticmethod
    async def update(
        db: AsyncSession, db_obj: BaseSpecification, obj_in: dict
    ) -> BaseSpecification:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: UUID) -> Optional[BaseSpecification]:
        result = await db.execute(
            select(BaseSpecification).where(BaseSpecification.id == id)
        )
        base_spec = result.scalar_one_or_none()

        if base_spec:
            await db.delete(base_spec)
            await db.commit()

        return base_spec
