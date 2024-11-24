from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


class CommonSetting(BaseSettings):
    APP_NAME: str = 'TEST FARM'

    class Config:
        env_file = ".env"


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"


class DatabaseSettings(BaseSettings):
    mode: str = os.getenv('MODE')
    DB_URL_DEVELOPMENT: str = os.getenv('DB_URL_DEVELOPMENT')
    DB_URL_PRODUCTION: str = os.getenv('DB_URL_PRODUCTION')
    DB_URL: str = DB_URL_DEVELOPMENT if mode == 'development' else DB_URL_PRODUCTION

    class Config:
        env_file = ".env"


class TokenSetting(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 4000
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


class Settings(CommonSetting, ServerSettings, DatabaseSettings, TokenSetting):
    pass


settings = Settings()
