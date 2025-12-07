from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class BrandBase(BaseModel):
    name: str
    country: str


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
