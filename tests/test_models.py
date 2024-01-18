from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use a test database
TEST_DATABASE_URL = os.environ.get("TestDatabaseConnectionString")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_create_user_model():
    user_data = {"username": "testuser", "hashed_password": "testhashedpassword"}

    # Create an instance of the User model
    user_instance = User(**user_data)

    # Check that attributes are set correctly
    assert user_instance.username == user_data["username"]
    assert user_instance.hashed_password == user_data["hashed_password"]

def test_save_user_to_database():
    user_data = {"username": "testuser", "hashed_password": "testhashedpassword"}

    # Create an instance of the User model
    user_instance = User(**user_data)

    # Use a test database
    db = TestingSessionLocal()

    try:
        # Add the user to the test database
        db.add(user_instance)
        db.commit()

        # Retrieve the user from the database
        db_user = db.query(User).filter(User.username == user_data["username"]).first()

        # Check that the retrieved user matches the original user
        assert db_user.username == user_data["username"]
        assert db_user.hashed_password == user_data["hashed_password"]
    finally:
        db.close()