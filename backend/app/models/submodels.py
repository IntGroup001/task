from uuid import uuid4

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Submodel(Base):
    __tablename__ = "submodels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=False)
    name = Column(String, nullable=False)

    model = relationship("CarModel", back_populates="submodels")
    generations = relationship("Generation", back_populates="submodel")
