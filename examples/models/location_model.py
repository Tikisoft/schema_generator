from models.config.base import Base
from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enums.status import Status

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    adress = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
