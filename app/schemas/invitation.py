from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional


class InvitationCreate(BaseModel):
    email: EmailStr
    unique_token: UUID4