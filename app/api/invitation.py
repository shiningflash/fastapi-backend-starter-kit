from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app import models, schemas
from app.db.base import get_db
from app.db.crud import CRUDBase
from app.services.oauth2 import get_current_user
from app.utils.invitation import generate_invitation_token, confirm_invitation_token
from app.services.mail import send_email_async
from core.config import settings
from app.models import User


invitation_router = APIRouter(tags=['Invitation'])
invitation_crud = CRUDBase(model=models.Invitation)


@invitation_router.get("/invitations")
def get_invitations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> List[schemas.Invitation]:
    db_invitations = db.query(models.Invitation)
    return db_invitations


@invitation_router.post('/invite')
async def invite(
    invitation_data: schemas.InvitationCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    unique_token = generate_invitation_token(data=invitation_data)
    created_by = db.query(User).filter(User.email == current_user.email).first()
    
    new_invitation = schemas.InvitationCreate(
        full_name=invitation_data.full_name,
        email=invitation_data.email,
        organization=invitation_data.organization,
        organizational_role=invitation_data.organizational_role,
        role=invitation_data.role,
        unique_token=unique_token,
        created_by_id=created_by.id
    )
    
    new_invitation.model_dump()
    _ = invitation_crud.create(db=db, obj_in=new_invitation)
    
    await send_email_async(
      subject=f'Invitation to Join {invitation_data.organization}',
      email_to=invitation_data.email,
      body={
          "full_name": invitation_data.full_name,
          "email": invitation_data.email,
          "organization": invitation_data.organization,
          "created_by_name": created_by.full_name,
          "invitation_url": f"{settings.BASE_URL}/accept-invitation/{unique_token}"}
    )
    
    return {'message': 'Invitation sent successfully'}


@invitation_router.post("/accept-invitation/{token}")
async def accept_invitation(
    token: str,
    db: Session = Depends(get_db)
):
    data = confirm_invitation_token(token=token)
    invitation = db.query(models.Invitation).filter_by(unique_token=token).first()
    
    if not data or not invitation or invitation.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail='Invalid or expired invitation link')
    
    # Redirect to the signup page with pre-filled information (data)
    # return RedirectResponse(url=f"/user?email={invitation.email}&full_name={invitation.full_name}&organization_name={invitation.organization}&organizational_role='user'")
    return data
    

@invitation_router.get("/resend-invitation/{email}")
async def resend_invitation(
    email: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    invitation = db.query(models.Invitation).filter_by(email=email).first()
    
    if not invitation:
        raise HTTPException(status_code=400, detail='No existing invitation found for this email.')
        
    created_by = db.query(User).filter(User.email==current_user.email).first()
    
    data_to_create_unique_token = schemas.InvitationCreateRequest(
        full_name=invitation.full_name,
        email=invitation.email,
        organization=invitation.organization,
        organizational_role=invitation.organizational_role,
        role=invitation.role
    )
    unique_token = generate_invitation_token(data=data_to_create_unique_token)
    
    invitation.unique_token = unique_token
    invitation.resent_count += 1
    _ = invitation_crud.update(db=db, obj_in=invitation)
    
    await send_email_async(
      subject=f'Invitation to Join {invitation.organization}',
      email_to=invitation.email,
      body={
          "full_name": invitation.full_name,
          "email": invitation.email,
          "organization": invitation.organization,
          "created_by_name": created_by.full_name,
          "invitation_url": f"{settings.BASE_URL}/accept-invitation/{unique_token}"}
    )
    
    return {'message': 'Invitation resent successfully'}
    