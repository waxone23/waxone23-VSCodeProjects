from pydantic import Field  # Add this import
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    # Ensure port is in a valid range
    DB_PORT: int = Field(ge=1024, le=65535)
    DB_USER: str
    DB_PASSWORD: str
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
# Test it out
print(f"Connecting to {settings.DB_HOST} on port {settings.DB_PORT}...")
print(f"Debug Mode: {settings.DEBUG}")
print(f"As Dictionary: {settings.model_dump()}")

# Add this to the end of your script
print("\nJSON Output:")
print(settings.model_dump_json(indent=2))
