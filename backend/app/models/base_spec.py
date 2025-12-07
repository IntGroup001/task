from uuid import uuid4

from sqlalchemy import Column, String, Integer, Float, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db import Base
from app.utils.enums import FuelTypeEnum


class BaseSpecification(Base):
    __tablename__ = "base_specs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    generation_id = Column(
        UUID(as_uuid=True), ForeignKey("generations.id"), nullable=False
    )

    year = Column(Integer)

    engine = Column(String)
    engine_displacement = Column(Integer)

    fuel_type = Column(Enum(FuelTypeEnum), nullable=False)

    horsepower = Column(Integer)
    torque = Column(Integer)

    transmission = Column(String)
    drivetrain = Column(String)

    doors = Column(Integer)
    seats = Column(Integer)
    weight = Column(Integer)

    zero_to_100 = Column(Float)
    top_speed = Column(Integer)

    generation = relationship("Generation", back_populates="specs")
