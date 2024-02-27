import os
import json

from app.db.crud import CRUDBase
from app.models import User
from app.schemas.user import UserCreatewithID
from app.utils.security import get_password_hash

from core.logger import logger

userCrud = CRUDBase(model=User)


def push_user_data(db, db_data):
    users = db_data['users']
    for user in users:
        user_in_create = UserCreatewithID(
            id=user['id'],
            email=user['email'],
            full_name=user['full_name'],
            organization_name=user['organization_name'],
            organizational_role=user['organizational_role'],
            role=user['role'],
            password=get_password_hash(user['password']),
            invited_by_id=None
        )
        user_in_create.model_dump()
        user_obj = userCrud.create(db, obj_in=user_in_create)
    return user_obj


def push_data_into_test_db(db):
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, 'data.json')
    with open(json_file_path, "r") as f:
        db_data = json.loads(f.read())
    
    _ = push_user_data(db=db, db_data=db_data)
