from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Todo
from Jwt.auth import create_access_token
from main import app, get_db
from datetime import timedelta
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
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependencies in the app
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

def test_create_todo():
    todo_data = {"title": "Test Todo", "description": "Test Description"}

    # Create a user for authentication
    access_token = create_access_token("testuser", 1, timedelta(minutes=20))

    # Make a request to create a todo
    response = client.post(
        "/todos",
        json=todo_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == todo_data["title"]

def test_read_todos():
    # Create a user for authentication
    access_token = create_access_token("testuser", 1, timedelta(minutes=20))

    # Make a request to read todos
    response = client.get("/todos", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 0  # Assuming the database is empty initially

def test_update_todo():
    # Create a user for authentication
    access_token = create_access_token("testuser", 1, timedelta(minutes=20))

    # Create a todo to update
    todo_data = {"title": "Test Todo", "description": "Test Description"}
    response_create = client.post(
        "/todos",
        json=todo_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    todo_id = response_create.json()["id"]

    # Make a request to update the todo
    updated_todo_data = {"todo_id": todo_id, "title": "Updated Todo"}
    response_update = client.put(
        f"/todos/{todo_id}",
        json=updated_todo_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_update.status_code == 200
    assert response_update.json()["title"] == updated_todo_data["title"]

def test_delete_todo():
    # Create a user for authentication
    access_token = create_access_token("testuser", 1, timedelta(minutes=20))

    # Create a todo to delete
    todo_data = {"title": "Test Todo", "description": "Test Description"}
    response_create = client.post(
        "/todos",
        json=todo_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    todo_id = response_create.json()["id"]

    # Make a request to delete the todo
    response_delete = client.delete(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_delete.status_code == 200
    assert response_delete.json()["message"] == "Todo deleted"
