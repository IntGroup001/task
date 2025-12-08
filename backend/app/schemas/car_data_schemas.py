from pydantic import BaseModel

from app.utils.enums import FuelTypeEnum


class CarDataResponse(BaseModel):
    brand_id: str
    brand_name: str
    brand_country: str | None

    model_id: str
    model_name: str
    model_description: str | None

    submodel_id: str
    submodel_name: str

    generation_id: str
    generation_name: str
    generation_year_from: int | None
    generation_year_to: int | None

    spec_id: str
    spec_year: int | None
    engine: str | None
    engine_displacement: int | None
    fuel_type: FuelTypeEnum
    horsepower: int | None
    torque: int | None
    transmission: str | None
    drivetrain: str | None
    doors: int | None
    seats: int | None
    weight: int | None
    zero_to_100: float | None
    top_speed: int | None
