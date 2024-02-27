from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas import UserBasic


class InvitationCreateRequest(BaseModel):
    full_name: str
    email: EmailStr
    organization: str
    organizational_role: str
    role: str

    class Config:
        from_attributes = True
        validate_assignment = True


class InvitationCreate(InvitationCreateRequest):
    unique_token: str
    created_by_id: UUID4


class Invitation(InvitationCreate):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    created_by: UserBasic = Optional
    resent_count: int = Optional


class InvitationResend(BaseModel):
    unique_token: str
    resent_count: int = Optional
