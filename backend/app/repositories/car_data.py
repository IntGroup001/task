from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.base_spec import BaseSpecification
from app.models.generation import Generation
from app.models.submodel import Submodel
from app.models.car_model import CarModel


class CarDataRepository:
    @staticmethod
    async def select_all_car_data(db: AsyncSession) -> list[BaseSpecification]:
        result = await db.execute(
            select(BaseSpecification).options(
                joinedload(BaseSpecification.generation)
                .joinedload(Generation.submodel)
                .joinedload(Submodel.model)
                .joinedload(CarModel.brand)
            )
        )
        return list(result.unique().scalars().all())
