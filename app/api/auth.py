from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.schemas.auth import LoginResponse, LoginRequest
from app.utils.security import create_access_token
from app.services.auth import authenticate


auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginResponse, tags=["auth"])
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


@auth_router.post("/logout", tags=['auth'])
def logout():
    try:
        content = {
            "message" : "logout successful"
        }
        response = JSONResponse(content=content)
        response.delete_cookie(key='authorization')
        return response
    except Exception as e:
        # logger.error(e)
        pass
