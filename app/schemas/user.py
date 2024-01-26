from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional

from app.schemas.base import AppBaseModel


class UserBasic(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserId(BaseModel):
    id: UUID4


class UserCreate(UserBasic):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        extra = 'forbid'
        orm_mode = True
        

class User(UserId, UserBasic, AppBaseModel):
    pass

    class Config:
        orm_mode = True


class UserUpdate(UserId):
    email: Optional[EmailStr]
    password: Optional[str]
    organization_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        extra = 'forbid'
        orm_mode = True
