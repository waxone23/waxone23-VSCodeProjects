import os
import sys
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

# ==========================================
# PART 1: THE OLD WAY (Steps 1-4)
# ==========================================
print("--- OLD WAY: os.environ ---")
load_dotenv()

# We have to manually provide defaults and types
name = os.environ.get("APP_NAME", "MyApp")
port = os.environ.get("APP_PORT", "8080")
debug = os.environ.get("DEBUG", "false")

# Step 4: Manual conversion (Annoying and error-prone!)
port_int = int(port)
debug_bool = debug.lower() == "true"

print(f"Name: {name} ({type(name)})")
print(f"Port: {port_int} ({type(port_int)})")
print(f"Debug: {debug_bool} ({type(debug_bool)})\n")


# ==========================================
# PART 2: THE MODERN WAY (Step 5)
# ==========================================
print("--- MODERN WAY: Pydantic BaseSettings ---")


class AppSettings(BaseSettings):
    # Tell Pydantic which file to read
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "MyApp"
    app_port: int = 8080  # Auto-converted to int
    secret_key: str  # REQUIRED: Script crashes if missing from .env
    debug: bool = False  # Auto-converted to bool


try:
    s = AppSettings()
    print(f"App Name: {s.app_name}")
    print(f"App Port: {s.app_port} ({type(s.app_port)})")
    print(f"Debug Mode: {s.debug} ({type(s.debug)})")
    print(f"Secret Key: {s.secret_key}")

except ValidationError as e:
    print("\n❌ STEP 5 BONUS: Validation Failed!")
    print("This happened because 'secret_key' is missing from your .env file.")
    print(e)
