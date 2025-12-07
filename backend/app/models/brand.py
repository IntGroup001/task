from uuid import uuid4

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from app.db import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    country = Column(String)

    models = relationship(
        "CarModel", back_populates="brand", cascade="all, delete-orphan"
    )
