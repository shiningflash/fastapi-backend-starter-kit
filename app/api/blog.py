from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.logger import logger
from app import models, schemas
from app.db.base import get_db
from app.db.crud import CRUDBase
from app.services.oauth2 import get_current_user


blog_router = APIRouter(prefix='/blog', tags=['Blog'])
blog_crud = CRUDBase(model=models.Blog)


@blog_router.post('', response_model=schemas.BlogDetails)
def create_blog(
    new_blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_blog.model_dump()
    blog = blog_crud.create(db=db, obj_in=new_blog)
    return blog
