import warnings
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from fastapi import Header
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from core.config import settings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="int_from_bytes is deprecated")
    from jose import JWTError, jwt


def create_client_access_token(
    data: dict,
    expires_delta: timedelta,
    secret_key: str,
    now: Optional[datetime] = None,
) -> str:
    to_encode = data.copy()
    expire = (now or datetime.now(timezone.utc)) + expires_delta
    to_encode["exp"] = expire
    encoded_jwt: str = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def get_subject_from_token(token: str =  Header(alias='Authorization')):#, secret_key: str='secret'):
    try:
        payload = jwt.decode(token, settings.OAUTH_CLIENT_SECRET, algorithms=["HS256"])
        sub = payload["sub"]
        # token_data = TokenPayload(**payload)
        return sub
    except JWTError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))


class OAuth2ClientCredentialsRequestForm:
    def __init__(
        self,
        grant_type: str = 'client_credentials', #Form(None, regex="^(client_credentials)$"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


class OAuth2ClientCredentials(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=True)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme_param = get_authorization_scheme_param(authorization)
        scheme: str = scheme_param[0]
        param: str = scheme_param[1]

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return param
