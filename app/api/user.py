from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.logger import logger
from app import models, schemas
from app.db.base import get_db
from app.db.crud import CRUDBase
from app.utils.security import get_password_hash
from app.services.oauth2 import add_new_role
from core.role import Role


user_router = APIRouter(prefix='/user', tags=['User'])
user_crud = CRUDBase(model=models.User)


@user_router.post('', response_model=schemas.UserDetails)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user.model_dump()
    existing_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user.password = get_password_hash(new_user.password)
    user_dict = user_crud.create(db=db, obj_in=new_user)
    # Add role 'user' to the new user
    add_new_role(new_user.email, Role.USER, db)
    return user_dict
