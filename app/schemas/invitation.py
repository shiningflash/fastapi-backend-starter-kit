from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional


class InvitationCreateRequest(BaseModel):
    full_name: str
    email: EmailStr
    organization: str
    organizational_role: str
    role: str


class InvitationCreate(InvitationCreateRequest):
    unique_token: str
    created_by_id: UUID4
    