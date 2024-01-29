# import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.db.base import get_db
from app import schemas
from app.services.oauth_client import OAuth2ClientCredentialsRequestForm, create_client_access_token, get_subject_from_token
from app.services.auth import validate_client_credentials


token_router = APIRouter(tags=['Token'])
# logger = logging.getLogger(__name__)


@token_router.post("/token", response_model=schemas.ClientTokenResponse)
def get_token(form_data: OAuth2ClientCredentialsRequestForm = Depends()):
    client_id = form_data.client_id
    client_secret = form_data.client_secret
    scopes = form_data.scopes

    if validate_client_credentials(client_id, client_secret, scopes[0]):
        access_token = create_client_access_token(data={"sub": client_id, "scope": scopes[0]}, secret_key=client_secret, expires_delta=timedelta(hours=2))
        response =  schemas.ClientTokenResponse(access_token=access_token, token_type="bearer")

        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))
    else:
        raise HTTPException(status_code=403, detail="Invalid client credentials")
