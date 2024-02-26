from pydantic import BaseModel
from datetime import datetime


class AppBaseModel(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None
