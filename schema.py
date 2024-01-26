from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional


class AppBaseModel(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None


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

"""
class Blog(AppBase):
    __tablename__ = "blogs"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True, nullable=False)
    sub_title = Column(String(100), unique=True, index=True)
    author = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    body = Column(JSON, nullable=False)

    user = relationship('User', back_populates='blogs')
"""

class BlogBasic(BaseModel):
    title: str
    sub_title: str = None
    author: str


class BlogId(BaseModel):
    id: UUID4


class BlogList(BlogId, BlogBasic):
    class Config:
        orm_mode = True


class BlogCreate(BlogBasic):
    body: str

    class Config:
        extra = 'forbid'
        orm_mode = True


class BlogDetail(BlogId, BlogCreate):
    class Config:
        orm_mode = True


class BlogUpdate(BlogId):
    title: Optional[str]
    sub_title: Optional[str]
    body: Optional[str]

    class Config:
        extra = 'forbid'
        orm_mode = True
