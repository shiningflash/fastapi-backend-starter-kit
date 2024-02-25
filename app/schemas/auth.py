from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr = None
    password: str

    class Config:
        extra = 'forbid'


class LoginResponse(BaseModel):
    message: str


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenData(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    organization_name: Optional[str] = None


class ClientTokenResponse(BaseModel):
    access_token: str
    token_type: str
