from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas
from app.db.base import get_db
from app.db.crud import CRUDBase
from app.services.oauth2 import get_current_user
from app.utils.invitation import generate_unique_token
from app.services.mail import send_email_async
from core.config import settings
from app.models import User


invitation_router = APIRouter(tags=['Invitation'])
invitation_crud = CRUDBase(model=models.Invitation)


@invitation_router.post('/invite')
async def invite(
    invitation_data: schemas.InvitationCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    unique_token = generate_unique_token()
    created_by_id = db.query(User).filter(User.email == current_user.email).first()
    
    new_invitation = schemas.InvitationCreate(
        full_name=invitation_data.full_name,
        email=invitation_data.email,
        organization=invitation_data.organization,
        organizational_role=invitation_data.organizational_role,
        role=invitation_data.role,
        unique_token=unique_token,
        created_by_id=created_by_id.id
    )
    
    new_invitation.model_dump()
    _ = invitation_crud.create(db=db, obj_in=new_invitation)
    
    await send_email_async(
      subject='Invitation to Join Our Company X',
      email_to=invitation_data.email,
      body={"title": "Invitation", "name": "Dear Mr. X", "invitation_url": f"{settings.BASE_URL}/invitation/{unique_token}"}
    )
    
    return {'message': 'Invitation sent successfully'}


@invitation_router.get('/invitation/{email}/{unique_token}')
async def accept_invitation(
    email: str,
    unique_token: str,
    db: Session = Depends(get_db)
):
    invitation = db.query(models.Invitation).filter_by(unique_token=unique_token).first()
    
    if not invitation or invitation.email != email or invitation.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail='Invalid or expired invitation link')
    
    # Handle user registration or other actions here
    # You can redirect the user to a registration form or perform any other necessary operations
    
    return {'message': 'You can now join our platform'}
