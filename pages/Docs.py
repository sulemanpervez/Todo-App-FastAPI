import streamlit as st
# Streamlit documentation for the JWT Authentication Tutorial

## Introduction and File Overview
st.title("Todo App With JWT Authentication in FastAPI")

## Hashed Passwords
st.subheader("Hashed Passwords")
st.write("Emphasizes the importance of using hashed passwords for security.")

## Dependency Installation
st.subheader("Dependency Installation")
st.write("Installation of dependencies for JWT authentication, including `python-jose`, `passlib`, and `python-multipart`.")
st.write("Explanation of the six total dependencies required for the application.")

## Authentication Module Setup
st.subheader("Authentication Module Setup")
st.write("Creation of an `auth.py` file to handle authentication-related tasks.")
st.write("Importing and configuring dependencies for working with JWTs, FastAPI, and password hashing.")
st.write("Definition of secret key and algorithm for JWT.")
st.write("Setting up the API router with a prefix and tag.")

## User and Token Models
st.subheader("User and Token Models")
st.write("Definition of user and token models using Pydantic for data validation.")
st.write("User model includes fields for the username and hashed password.")
st.write("Token model specifies the structure of the JWT that will be issued to authenticated users.")

## User Registration Endpoint
st.subheader("User Registration Endpoint")
st.write("Updating `main.py` to include the auth router.")
st.write("Testing the user registration endpoint using Swagger UI to create a new user with a hashed password.")

## Login Endpoint and User Authentication
st.subheader("Login Endpoint and User Authentication")
st.write("Addition of the login endpoint to issue JWTs upon successful authentication.")
st.write("Demonstration of using Swagger UI to authenticate a user and receive a JWT.")

## Finalizing Authentication Flow
st.subheader("Finalizing Authentication Flow")
st.write("Creation of a method to decode JWTs and validate user authentication.")
st.write("Updating `main.py` to use the JWT validation method for a protected endpoint.")

## Testing Protected Endpoint
st.subheader("Testing Protected Endpoint")
st.write("Testing a protected endpoint in Swagger UI, demonstrating the requirement of a valid JWT for access.")
# Streamlit documentation for auth.py
st.header("auth.py")
## Import Libraries
st.subheader("1. Import Libraries")
st.code("from datetime import timedelta, datetime\nfrom fastapi import APIRouter, Depends, HTTPException\nfrom fastapi.security import OAuth2PasswordBearer\nfrom jose import JWTError, jwt\nfrom sqlalchemy.orm import Session\nfrom typing import Optional\nfrom pydantic import BaseModel")

## Configure Environment
st.subheader("2. Configure Environment")
st.code("Load environment variables from a `.env` file, setting values for `JWT_SECRET_KEY` and `ALGORITHM_JWT`.")

## Router Setup
st.subheader("3. Router Setup")
st.code("Create an instance of `APIRouter` for handling authentication-related routes.")

## Constants and Dependencies
st.subheader("4. Constants and Dependencies")
st.code("Define constants for JWT secret key and algorithm. Also, set up a dependency (`get_db`) for handling database sessions.")

## Data Models
st.subheader("5. Data Models")
st.code("Define data models such as `CreateUserRequest` and `Token` using Pydantic.")

## Database Session Dependency
st.subheader("6. Database Session Dependency")
st.code("Create a dependency to obtain a database session (`db_dependency`).")

## User Creation Endpoint
st.subheader("7. User Creation Endpoint")
st.code("Implement an endpoint (`/auth/create/user`) for creating a new user in the database.")

## Token Generation Endpoint
st.subheader("8. Token Generation Endpoint")
st.code("Implement an endpoint (`/auth/token`) for generating an access token upon successful authentication.")

## User Authentication Function
st.subheader("9. User Authentication Function")
st.code("Define a function (`authenticate_user`) to authenticate users by checking their credentials against the stored hashed password.")

## Access Token Creation Function
st.subheader("10. Access Token Creation Function")
st.code("Implement a function (`create_access_token`) for creating a JWT token containing user information.")

## Get Current User Endpoint
st.subheader("11. Get Current User Endpoint")
st.code("Implement an endpoint (`/auth/get_current_user`) for retrieving the current user based on the provided JWT token.")

st.write("The authentication flow involves creating a user, obtaining an access token through the `/auth/token` endpoint, and validating the token using the `/auth/get_current_user` endpoint.")
st.write("Note: The code snippet lacks the definition of the `Session` model, and there's a typo in 'Depneds' (should be 'Depends'). Additionally, the actual implementation and usage of the `/auth/get_current_user` endpoint are not provided in this snippet.")

# Streamlit documentation for models.py
st.header("models.py")
## Import Statements
st.subheader("1. Import Statements")
st.code("from database import Base\nfrom sqlalchemy import Column, Integer, String")
st.write("- The `Base` class is presumably a SQLAlchemy base class, often used for declarative class definitions.")
st.write("- `Column`, `Integer`, and `String` are components from SQLAlchemy used to define the structure of database tables.")

## User Model Definition
st.subheader("2. User Model Definition")
st.code("class User(Base):\n    __tablename__ = 'users'")
st.write("- `User` is a class that inherits from `Base`, suggesting it's a SQLAlchemy model.")
st.write("- `__tablename__` specifies the name of the database table to which instances of this class will be mapped. In this case, it's set to 'users'.")

## Columns
st.subheader("3. Columns")
st.code("id = Column(Integer, primary_key=True, index=True)\nusername = Column(String, unique=True)\nhashed_password = Column(String)")
st.write("- `id`: An integer column serving as the primary key for the table. It is marked as `primary_key=True`, indicating it uniquely identifies each row.")
st.write("- `username`: A string column for storing usernames. It is marked as `unique=True` to ensure each username is unique.")
st.write("- `hashed_password`: A string column for storing hashed passwords.")

st.write("So, the `User` model represents a user entity in the database with an integer primary key (`id`), a unique username, and a hashed password. Instances of this class will be mapped to a table named 'users' in the database. This model is typically used in conjunction with SQLAlchemy to interact with the underlying database, such as creating, querying, and updating user records.")

# Streamlit documentation for database.py
st.header("database.py")
## Import Statements
st.subheader("1. Import Statements")
st.code("from sqlalchemy import create_engine, Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import declarative_base, sessionmaker\nfrom dotenv import load_dotenv")
st.write("- `create_engine`: SQLAlchemy function for creating a database engine. It connects to the database and manages connections.")
st.write("- `Column`, `Integer`, and `String`: Components from SQLAlchemy used to define the structure of database tables.")
st.write("- `declarative_base`: A function from SQLAlchemy that returns a base class for declarative class definitions.")
st.write("- `sessionmaker`: A function to create a new `Session` class for interacting with the database.")

## Load Environment Variables
st.subheader("2. Load Environment Variables")
st.code("load_dotenv()")
st.write("- This line loads environment variables from a `.env` file, if present. In your case, it's loading environment variables related to the database connection.")

## Database Connection Configuration
st.subheader("3. Database Connection Configuration")
st.code("DatabaseConnection = os.environ.get(\"DatabaseConnectionString\")\nSQLALCHEMY_DATABASE_URL = DatabaseConnection")
st.write("- `DatabaseConnection`: Retrieves the database connection string from environment variables.")
st.write("- `SQLALCHEMY_DATABASE_URL`: Set to the retrieved database connection string.")

## Database Engine Setup
st.subheader("4. Database Engine Setup")
st.code("engine = create_engine(SQLALCHEMY_DATABASE_URL)")
st.write("- `engine`: Creates a SQLAlchemy database engine using the specified connection URL.")

## SessionLocal Setup
st.subheader("5. SessionLocal Setup")
st.code("SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)")
st.write("- `SessionLocal`: A factory for creating database sessions. Sessions are used to interact with the database.")

## Base Class Definition
st.subheader("6. Base Class Definition")
st.code("Base = declarative_base()")
st.write("- `Base`: A base class for declarative class definitions. Models (such as `Todo` in this case) will inherit from this base class.")

## Todo Model Definition
st.subheader("7. Todo Model Definition")
st.code("class Todo(Base):\n    __tablename__ = \"todos\"\n    id = Column(Integer, primary_key=True, index=True)\n    title = Column(String, index=True)\n    description = Column(String, index=True)")
st.write("- `Todo`: A SQLAlchemy model representing a todo item.")
st.write("- `__tablename__`: Specifies the name of the database table to which instances of this class will be mapped.")
st.write("- `id`, `title`, `description`: Columns of the table, where `id` is the primary key, and `title` and `description` are strings.")

# Streamlit documentation for main.py
st.header("main.py")
## Imports
st.subheader("1. Imports")
st.code("from fastapi import FastAPI, status, HTTPException, Depends\nfrom sqlalchemy.orm import Session\nfrom database import SessionLocal, engine, Todo\nfrom pydantic import BaseModel\nimport Jwt.models as models\nimport Jwt.auth as auth\nfrom typing import Annotated\nfrom Jwt.auth import get_current_user")
st.write("- Various FastAPI modules, SQLAlchemy components, Pydantic for data validation, and modules for authentication are imported.")
st.write("- `Jwt.models` and `Jwt.auth` are modules likely containing user-related models and authentication functions.")
st.write("- `SessionLocal`, `engine`, and `Todo` are imported from the `database` module.")
st.write("- `Annotated` is used for type hinting with additional metadata.")

## FastAPI Application Setup
st.subheader("2. FastAPI Application Setup")
st.code("app = FastAPI()\napp.include_router(auth.router)")
st.write("- A FastAPI application is created.")
st.write("- The authentication router from the `Jwt.auth` module is included in the main application.")

## Database Table Creation
st.subheader("3. Database Table Creation")
st.code("models.Base.metadata.create_all(engine)")
st.write("- Database tables are created based on the models defined in the `Jwt.models` module.")

## Pydantic Models for TODOs
st.subheader("4. Pydantic Models for TODOs")
st.code("class TodoCreate(BaseModel):\n    id: int\n    title: str\n    description: str = None\n\nclass TodoUpdate(BaseModel):\n    todo_id: int\n    title: str\n    description: str = None")
st.write("- Pydantic models `TodoCreate` and `TodoUpdate` are defined for creating and updating TODO items, respectively.")

## Dependency Functions
st.subheader("5. Dependency Functions")
st.code("def get_db():\n    db = SessionLocal()\n    try:\n        yield db\n    finally:\n        db.close()\n\ndb_dependency = Annotated[Session, Depends(get_db)]\nuser_dependency = Annotated[dict, Depends(get_current_user)]")
st.write("- `get_db`: A function to get a database session, used as a dependency in other functions.")
st.write("- `db_dependency` and `user_dependency`: Annotations for dependencies on the database session and current user, respectively.")

## Endpoints
st.subheader("6. Endpoints")
st.write("### User Endpoint:")
st.code("@app.get(\"/\", status_code=status.HTTP_200_OK)\nasync def user(user: user_dependency, db: db_dependency):\n    if user is None:\n        raise HTTPException(status_code=401, detail=\"Authentication Failed\")\n    return {\"User\": user}")
st.write("- An endpoint for retrieving user information. It depends on the current user (`user_dependency`) and a database session (`db_dependency`).")

st.write("### TODO Endpoints:")
st.write("#### Create TODO:")
st.code("@app.post(\"/todos\")\ndef create_todo(todo: TodoCreate, db: Session = Depends(get_db)):\n    # Implementation details")

st.write("#### Read TODOs:")
st.code("@app.get(\"/todos\")\ndef read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):\n    # Implementation details")

st.write("#### Update TODO:")
st.code("@app.put(\"/todos/{todo_id}\")\ndef update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):\n    # Implementation details")

st.write("#### Delete TODO:")
st.code("@app.delete(\"/todos/{todo_id}\")\ndef delete_todo(todo_id: int, db: Session = Depends(get_db)):\n    # Implementation details")

st.write("- These endpoints handle CRUD operations for TODO items, interacting with the database using SQLAlchemy.")

# Header for the Streamlit app
st.header("FastAPI Application Testing")

# Testing auth.py
st.subheader("Testing auth.py")
st.write("""
To ensure secure user authentication, we extensively test `auth.py`. This file contains functions for user registration, token generation, and user authentication. Our tests cover user creation, token generation, and authentication checks, ensuring a robust authentication system for our FastAPI application.
""")

# Testing models.py
st.subheader("Testing models.py")
st.write("""
`models.py` defines the database models used in our FastAPI application, particularly the `User` model. We rigorously test the creation and attributes of the `User` model to guarantee accurate data storage and retrieval. Our tests ensure the integrity of the user data model, an essential aspect of our application's functionality.
""")

# Testing database.py
st.subheader("Testing database.py")
st.write("""
In `database.py`, we define the database structure and interactions for our FastAPI application. Our tests for this file focus on creating and saving data, ensuring that the `Todo` model behaves as expected. By testing database operations, we verify the reliability and correctness of our application's data storage capabilities.
""")

# Testing main.py
st.subheader("Testing main.py")
st.write("""
`main.py` contains the core logic of our FastAPI application, including CRUD operations for managing todos and user authentication. Our tests cover the entire application flow, from user authentication to todo creation, retrieval, and modification. By testing the main application file, we ensure the smooth functioning of our FastAPI application.
""")


st.sidebar.subheader("JWT Authentication in FastAPI")
st.sidebar.markdown("Secure your FastAPI application with JSON Web Token (JWT) authentication.")
st.sidebar.markdown("Implement user registration, login, and token generation for enhanced security.")

# Key Features
st.sidebar.subheader("Key Features")
st.sidebar.markdown("- **User Registration:** Create new user accounts securely.")
st.sidebar.markdown("- **User Authentication:** Authenticate users and issue JWTs for secure access.")
st.sidebar.markdown("- **Token Generation:** Generate access tokens upon successful user authentication.")
st.sidebar.markdown("- **Protecting Endpoints:** Finalize the authentication flow with JWT decoding and validation.")
st.sidebar.markdown("- **Our Todo List:** Add, delete, and update tasks effortlessly")
st.sidebar.markdown("- **Experience Personalization:** sign up and personalize your experience with easy login")
st.sidebar.markdown("- **FastAPI fortified**: Secure auth, flawless tokens, robust data. Elevate your app security effortlessly with testing.")
