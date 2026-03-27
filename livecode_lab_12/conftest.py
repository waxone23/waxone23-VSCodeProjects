import pytest
from fastapi.testclient import TestClient
from main import app, db


@pytest.fixture
def client():
    # Clear the "database" before each test
    db.clear()
    return TestClient(app)
