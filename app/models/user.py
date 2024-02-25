import uuid
from sqlalchemy import Column, String, String, Column, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    full_name = Column(String(50), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    organization_name = Column(String(256), nullable=False)
    organizational_role = Column(String(256), nullable=True)
    role = Column(String(256), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    invited_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)

    blogs = relationship('Blog', back_populates='user')
    invitations = relationship('Invitation', back_populates='created_by')
