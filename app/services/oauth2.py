from fastapi import HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services import token
from app import schemas
from app.db.base import engine

# import casbinx
# import casbin_sqlalchemy_adapter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth-login")
# adapter = casbin_sqlalchemy_adapter.Adapter(engine)


def get_current_user(data: str = Depends(oauth2_scheme)):
    print('Inside get_current_user')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    ret = token.verify_token(data, credentials_exception)
    return ret


# def get_current_user_authorization(req: Request, current_user: schemas.User = Depends(get_current_user)):
#     e = casbin.Enforcer("model.conf", adapter)
#     sub = current_user.email
#     obj = req.url.path
#     act = req.method
#     if not(e.enforce(sub, obj, act)):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Method not authorized for this user")
#     return current_user