import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "student"
    db_password: str = "secret"
    debug: bool = False
    app_name: str = "fixed"
    app_port: int = 8080
    secret_key: str = "fixed"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


try:
    settings = Settings()
except ValidationError as e:
    print(e)
    sys.exit(1)
