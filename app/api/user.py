from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app import models, schemas
from app.db.base import get_db
from app.db.crud import CRUDBase
from app.utils.invitation import confirm_invitation_token
from app.utils.security import get_password_hash
from app.services.oauth2 import add_new_role_in_org

user_router = APIRouter(prefix='/user', tags=['User'])
user_crud = CRUDBase(model=models.User)


@user_router.post('', response_model=schemas.UserDetails)
def create_user(
    data: schemas.UserCreateRequest,
    db: Session = Depends(get_db)
):
    token_data = confirm_invitation_token(token=data.token)
    invitation = db.query(models.Invitation
                          ).filter_by(unique_token=data.token
                                      ).first()

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail='Password did not match')

    if (not token_data or not invitation or
            invitation.expires_at < datetime.now()):
        raise HTTPException(
            status_code=400,
            detail='Invalid information or expired invitation link')

    existing_user = db.query(models.User
                             ).filter(models.User.email == invitation.email
                                      ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    user = schemas.UserCreate(
        full_name=data.full_name,
        email=invitation.email,
        organization_name=invitation.organization,
        organizational_role=invitation.organizational_role,
        password=get_password_hash(data.password),
        role=invitation.role,
        invited_by_id=invitation.created_by_id
    )
    user.model_dump()
    user_dict = user_crud.create(db=db, obj_in=user)

    # Add role to the new user
    add_new_role_in_org(
        user.email, invitation.role, invitation.organization, db
    )

    return user_dict


@user_router.get('')
def get_users(
    db: Session = Depends(get_db)
) -> List[schemas.UserList]:
    db_users = db.query(models.User)
    return db_users
