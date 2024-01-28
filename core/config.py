import os
from typing import Optional, ClassVar
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

if not os.getenv("DATABASE_URL"):
    load_dotenv()


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "Demo App"
    APP_ENV: str = os.environ['APP_ENV']

    # DB
    DATABASE_URL: Optional[str] = os.environ['DATABASE_URL']

    #JWT
    JWT_SECRET_KEY: str = os.environ['JWT_SECRET_KEY']
    ALGORITHM: ClassVar = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

settings = Settings()
