from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class GenerationBase(BaseModel):
    submodel_id: UUID
    name: str
    year_from: int | None = None
    year_to: int | None = None


class GenerationCreate(GenerationBase):
    @field_serializer("submodel_id")
    def serialize_submodel_id(self, submodel_id: UUID, _info):
        return str(submodel_id)


class Generation(GenerationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id", "submodel_id")
    def serialize_uuid(self, value: UUID, _info):
        return str(value)
