from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Todo
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use a test database
TEST_DATABASE_URL = os.environ.get("TestDatabaseConnectionString")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_create_todo_model():
    todo_data = {"title": "Test Todo", "description": "Test Description"}

    # Create an instance of the Todo model
    todo_instance = Todo(**todo_data)

    # Check that attributes are set correctly
    assert todo_instance.title == todo_data["title"]
    assert todo_instance.description == todo_data["description"]

def test_save_todo_to_database():
    todo_data = {"title": "Test Todo", "description": "Test Description"}

    # Create an instance of the Todo model
    todo_instance = Todo(**todo_data)

    # Use a test database
    db = TestingSessionLocal()

    try:
        # Add the todo to the test database
        db.add(todo_instance)
        db.commit()

        # Retrieve the todo from the database
        db_todo = db.query(Todo).filter(Todo.title == todo_data["title"]).first()

        # Check that the retrieved todo matches the original todo
        assert db_todo.title == todo_data["title"]
        assert db_todo.description == todo_data["description"]
    finally:
        db.close()

