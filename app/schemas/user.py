from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional

from app.schemas.base import AppBaseModel


class UserBasic(BaseModel):
    email: EmailStr
    full_name: str
    organization_name: str = None
    organizational_role: str = None

    class Config:
        from_attributes = True


class UserId(BaseModel):
    id: UUID4


class UserCreateRequest(BaseModel):
    full_name: str
    password: str
    confirm_password: str
    token: str

    class Config:
        extra = 'forbid'
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    organization_name: str
    organizational_role: str = Optional
    role: str
    invited_by_id: UUID4 | None = Optional

    class Config:
        extra = 'forbid'
        from_attributes = True


class UserCreatewithID(BaseModel):
    id: UUID4
    email: EmailStr
    full_name: str
    password: str
    organization_name: str
    organizational_role: str = Optional
    role: str
    invited_by_id: UUID4 | None = Optional

    class Config:
        extra = 'forbid'
        from_attributes = True


class UserDetails(AppBaseModel, UserBasic, UserId):
    role: str
    invited_by_id: UUID4 = Optional

    class Config:
        from_attributes = True


class UserUpdate(UserId):
    email: Optional[EmailStr]
    password: Optional[str]
    full_name: Optional[str]
    bio: Optional[str]

    class Config:
        extra = 'forbid'
        from_attributes = True


class UserList(BaseModel):
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True
