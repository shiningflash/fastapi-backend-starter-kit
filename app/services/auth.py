from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from typing import Optional,Union, Any

from app.db.base import get_db
from app.db.crud import CRUDBase
from app import models
from core.config import settings
from core.logger import logger
from app.schemas.auth import TokenPayload
from app.services.oauth_client import OAuth2ClientCredentials
# import logging

from app.utils.security import verify_password


# logger = logging.getLogger(__name__)
userCrud = CRUDBase(model=models.User)

credentials_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials",
)

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

oauth2_scheme = OAuth2ClientCredentials(
    tokenUrl="token", 
    scopes={"write": "write_path"}
)

def validate_client_credentials(client_id, client_secret, scopes):
    scopes_dict = {
        scopes.split('/')[0] : scopes.split('/')[1]
    }
    if client_id == settings.OAUTH_CLIENT_ID and client_secret == settings.OAUTH_CLIENT_SECRET and scopes_dict == oauth2_scheme.model.flows.clientCredentials.scopes:
        return True
    else:
        return False


def authenticate(db: Session, *, email: Optional[str] = None, password: str):
    user = userCrud.get_by_field(db, field="email", value=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_token(token: str = Cookie(None, alias="authorization")):
    if token is None:
        raise HTTPException(status_code=403, detail="Forbidden: Missing token")
    return token


def get_current_active_user(token: str = Depends(get_token), db: Session = Depends(get_db)):
    try:
        if token is None:
            raise HTTPException(status_code=403, detail="Missing authorization token")
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="Token expired",
            )
        user: Union[dict[str, Any], None] = userCrud.get_by_field(db, field="email", value=token_data.sub)
        print(f'\n\n\n1: {user}\n\n\n')
        user: Union[dict[str, Any], None] = userCrud.get_by_field(db, field="id", value=token_data.sub)
        print(f'\n\n\n2: {user}\n\n\n')
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        logger.error(f"User not authenticated {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not authenticated')


def validate_client_credentials(client_id, client_secret, scopes):
    scopes_dict = {
        scopes.split('/')[0] : scopes.split('/')[1]
    }
    if client_id == settings.OAUTH_CLIENT_ID and client_secret == settings.OAUTH_CLIENT_SECRET and scopes_dict == oauth2_scheme.model.flows.clientCredentials.scopes:
        return True
    else:
        return False
