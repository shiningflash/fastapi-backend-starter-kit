from pydantic import BaseModel, UUID4
from typing import Optional

from app.schemas.base import AppBaseModel


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


class BlogDetail(BlogId, BlogCreate, AppBaseModel):
    class Config:
        orm_mode = True


class BlogUpdate(BlogId):
    title: Optional[str]
    sub_title: Optional[str]
    body: Optional[str]

    class Config:
        extra = 'forbid'
        orm_mode = True
