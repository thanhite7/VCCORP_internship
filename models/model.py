from sqlalchemy import Column, String, DateTime, Boolean
import uuid
import sqlalchemy as sa
from base import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(String(200), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
