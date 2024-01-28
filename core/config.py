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
    
    # Rollbar
    ROLLBAR_ACCESS_TOKEN:str = os.environ['ROLLBAR_ACCESS_TOKEN']

    # GCS
    BUCKET_NAME:str = os.environ['BUCKET_NAME']

    # client credentials
    OAUTH_CLIENT_ID: str = os.environ['OAUTH_CLIENT_ID']
    OAUTH_CLIENT_SECRET: str = os.environ['OAUTH_CLIENT_SECRET']

settings = Settings()
