from uuid import uuid4

from sqlalchemy import Column, String, Integer, UUID, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Generation(Base):
    __tablename__ = "generations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    submodel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("submodels.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String, nullable=False, unique=True, index=True)
    year_from = Column(Integer)
    year_to = Column(Integer)

    submodel = relationship("Submodel", back_populates="generations")
    specs = relationship(
        "BaseSpecification", back_populates="generation", cascade="all, delete-orphan"
    )
