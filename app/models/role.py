import uuid
from sqlalchemy import Column, String, String, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.base_class import Base


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
