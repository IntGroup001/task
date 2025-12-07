from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from app.utils.enums import FuelTypeEnum


class BaseSpecificationBase(BaseModel):
    generation_id: UUID
    year: int | None = None
    engine: str | None = None
    engine_displacement: int | None = None
    fuel_type: FuelTypeEnum
    horsepower: int | None = None
    torque: int | None = None
    transmission: str | None = None
    drivetrain: str | None = None
    doors: int | None = None
    seats: int | None = None
    weight: int | None = None
    zero_to_100: float | None = None
    top_speed: int | None = None


class BaseSpecificationCreate(BaseSpecificationBase):
    @field_serializer("generation_id")
    def serialize_generation_id(self, generation_id: UUID, _info):
        return str(generation_id)


class BaseSpecification(BaseSpecificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id", "generation_id")
    def serialize_uuid(self, value: UUID, _info):
        return str(value)
