from uuid import uuid4
from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class CarModel(Base):
    __tablename__ = "models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=False)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)

    brand = relationship("Brand", back_populates="models")
    # submodels = relationship("Submodel", back_populates="model")
