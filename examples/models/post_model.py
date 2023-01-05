from models.config.base import Base
from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enums.status import Status

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Status), nullable=False, default=Status.DELETED)
    user_id = Column(ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="posts")
