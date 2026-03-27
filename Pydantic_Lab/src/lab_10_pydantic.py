import os
from pydantic import BaseModel, Field, ValidationError

# --- Part 1: Manual Environment Reading ---
os.environ["APP_ENV"] = "development"
print(f"APP_ENV set to: {os.environ.get('APP_ENV')}")

# Safe reading with a default value
version = os.environ.get("APP_VERSION", "0.1.0")
print(f"APP_VERSION (defaulted): {version}")


# --- Part 2: Pydantic Validation ---
class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=120)  # ge = greater or equal, le = less or equal
    email: str
    active: bool = True


print("\n--- Testing Pydantic Model ---")
try:
    # Notice '25' is a string, but Pydantic will convert it to an int!
    user = User(name="Brede", age="25", email="brede@oslomet.no")
    print(f"User validated: {user.model_dump()}")

except ValidationError as e:
    print(f"Validation Error: {e}")
