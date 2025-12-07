from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class CarModelBase(BaseModel):
    brand_id: UUID
    name: str
    description: str | None = None


class CarModelCreate(CarModelBase):
    @field_serializer("brand_id")
    def serialize_brand_id(self, brand_id: UUID, _info):
        return str(brand_id)


class CarModel(CarModelBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id", "brand_id")
    def serialize_uuid(self, value: UUID, _info):
        return str(value)
