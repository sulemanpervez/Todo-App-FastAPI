from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from Jwt.auth import router
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use a test database
TEST_DATABASE_URL = os.environ.get("TestDatabaseConnectionString")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Override dependency to use the test database
@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependencies in the router
router.dependencies = [Depends(test_db)]

client = TestClient(router)

def test_create_user():
    response = client.post(
        "/auth/create/user",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 201
    assert response.json() == {"detail": "User created successfully"}

def test_login():
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
