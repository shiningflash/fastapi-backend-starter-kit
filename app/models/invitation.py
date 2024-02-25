import uuid
from datetime import datetime, timedelta
from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from core.config import settings


class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    organization = Column(String(100), nullable=False)
    organizational_role = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False, default='Invited')
    unique_token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resent_count = Column(Integer, default=0)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    created_by = relationship("User", back_populates="invitations")

    @property
    def expires_at(self):
        return self.updated_at + timedelta(hours=settings.INVITATION_URL_MAX_AGE)
