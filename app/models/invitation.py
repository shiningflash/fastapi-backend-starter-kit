import uuid
from sqlalchemy import Column, String, String, Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import timedelta

from app.db.base import Base
from core.config import settings


class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    email = Column(String(100), index=True, nullable=False)
    unique_token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    # TODO
    # created_by = ''
    
    @property
    def expires_at(self):
        return self.created_at + timedelta(hours=settings.INVITATION_EXPIRY_IN_HOURS)
