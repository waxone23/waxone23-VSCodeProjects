from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# 1. Define the nested model for the database
class DatabaseSettings(BaseModel):
    host: str
    port: int
    name: str
    password: str


# 2. Define the main config
class AppConfig(BaseSettings):
    app_name: str
    api_key: str
    max_retries: int
    verbose: bool

    # This matches the DATABASE__ prefix in your .env
    database: DatabaseSettings

    # Use env_nested_delimiter to handle the double underscore '__'
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )


def main():
    try:
        config = AppConfig()
        print("✅ --- Config Loaded Successfully ---")
        print(f"App: {config.app_name}")
        print(f"DB Host: {config.database.host}")
        print(
            f"DB Port: {config.database.port} (Verified as {type(config.database.port)})"
        )
    except Exception as e:
        print(f"❌ Error loading config: {e}")


if __name__ == "__main__":
    main()
