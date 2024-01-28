from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional

from app.schemas.base import AppBaseModel


class UserBasic(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    bio: str = None


class UserId(BaseModel):
    id: UUID4


class UserCreate(UserBasic):
    password: str
    
    class Config:
        extra = 'forbid'
        orm_mode = True
        

class UserDetails(AppBaseModel, UserBasic, UserId):
    class Config:
        orm_mode = True


class UserUpdate(UserId):
    email: Optional[EmailStr]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]

    class Config:
        extra = 'forbid'
        orm_mode = True
