import uuid
from sqlalchemy import Column, String, String, ForeignKey, Column, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Blog(Base):
    __tablename__ = "blogs"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True, nullable=False)
    sub_title = Column(String(100), unique=True, index=True)
    author = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    body = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='blogs')
