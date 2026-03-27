import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError


class Settings(BaseSettings):
    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "student"
    db_password: str = "secret"
    debug: bool = False

    # App Configuration (Adding these prevents the Extra Forbidden error)
    app_name: str = "MyPythonApp"
    app_port: int = 8080
    secret_key: str = "super-secret-123"

    # The Bouncer Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # This tells Pydantic: "If you see other stuff, just ignore it"
    )


try:
    settings = Settings()
except ValidationError as e:
    print("❌ Configuration Error!")
    print(e)
    sys.exit(1)
