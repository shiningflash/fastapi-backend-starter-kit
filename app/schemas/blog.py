from pydantic import BaseModel, UUID4
from typing import Optional

from app.schemas.base import AppBaseModel


class BlogBasic(BaseModel):
    title: str
    sub_title: str = None
    author: UUID4


class BlogBasicWithAuthor(BlogBasic):
    author: UUID4


class BlogId(BaseModel):
    id: UUID4


class BlogList(BlogBasicWithAuthor, BlogId):
    class Config:
        from_attributes = True


class BlogCreate(BaseModel):
    title: str
    sub_title: str = None
    body: str
    author: UUID4 = '57785471-bc81-4062-a621-15657ccc0a0c'

    class Config:
        from_attributes = True


class BlogDetails(AppBaseModel, BlogCreate, BlogId):
    class Config:
        from_attributes = True


class BlogUpdate(BlogId):
    title: Optional[str]
    sub_title: Optional[str]
    body: Optional[str]

    class Config:
        extra = 'forbid'
        from_attributes = True
