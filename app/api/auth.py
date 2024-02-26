from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.auth import LoginResponse, LoginRequest
from app.utils.security import create_access_token
from app.services.auth import authenticate
from app import models
from app.services import token
from app.services.hash import Hash


auth_router = APIRouter(prefix='', tags=['Auth'])


@auth_router.post("/login", response_model=LoginResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user_data.model_dump()
        user_auth = authenticate(db, email=user_data.email, password=user_data.password)
        if not user_auth:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        content = {
            "message": "login successful",
        }
        response = JSONResponse(content=content)
        access_token = create_access_token(user_auth.email)
        response.set_cookie(key='authorization', value=access_token, samesite='none', secure=True)
        return response
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@auth_router.post('/oauth-login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
def logout():
    try:
        content = {
            "message": "logout successful"
        }
        response = JSONResponse(content=content)
        response.delete_cookie(key='authorization')
        return response
    except Exception as e:
        # logger.error(e)
        pass
