from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.car_data_schemas import CarDataResponse
from app.repositories.car_data import CarDataRepository


async def get_all_car_data(db: AsyncSession) -> List[CarDataResponse]:
    specs = await CarDataRepository.select_all_car_data(db)
    car_data_list = []
    for spec in specs:
        print(spec.__dict__)
        car_data = CarDataResponse(
            brand_id=str(spec.generation.submodel.model.brand.id),
            brand_name=spec.generation.submodel.model.brand.name,
            brand_country=spec.generation.submodel.model.brand.country,
            model_id=str(spec.generation.submodel.model.id),
            model_name=spec.generation.submodel.model.name,
            model_description=spec.generation.submodel.model.description,
            submodel_id=str(spec.generation.submodel.id),
            submodel_name=spec.generation.submodel.name,
            generation_id=str(spec.generation.id),
            generation_name=spec.generation.name,
            generation_year_from=spec.generation.year_from,
            generation_year_to=spec.generation.year_to,
            spec_id=str(spec.id),
            spec_year=spec.year,
            engine=spec.engine,
            engine_displacement=spec.engine_displacement,
            fuel_type=spec.fuel_type.value,
            horsepower=spec.horsepower,
            torque=spec.torque,
            transmission=spec.transmission,
            drivetrain=spec.drivetrain,
            doors=spec.doors,
            seats=spec.seats,
            weight=spec.weight,
            zero_to_100=spec.zero_to_100,
            top_speed=spec.top_speed,
        )
        car_data_list.append(car_data)

    return car_data_list
