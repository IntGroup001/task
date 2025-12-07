from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class SubmodelBase(BaseModel):
    model_id: UUID
    name: str


class SubmodelCreate(SubmodelBase):
    @field_serializer("model_id")
    def serialize_model_id(self, model_id: UUID, _info):
        return str(model_id)


class Submodel(SubmodelBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id", "model_id")
    def serialize_uuid(self, value: UUID, _info):
        return str(value)
