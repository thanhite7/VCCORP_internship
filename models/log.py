from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.model import Image
from base import Base
import uuid


class Log(Base):
    __tablename__ = "log"
    id = Column(String(200), primary_key=True, default=uuid.uuid4)
    image_id = Column(String(200), ForeignKey(Image.id), nullable=False)
    action = Column(String(200), nullable=False)
