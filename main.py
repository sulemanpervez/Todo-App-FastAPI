from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Todo
from pydantic import BaseModel
import Jwt.models as models
import Jwt.auth as auth
from database import engine, SessionLocal, Base
from typing import Annotated
from sqlalchemy.orm import Session
from Jwt.auth import get_current_user
app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(engine)

class TodoCreate(BaseModel):
    id : int
    title: str
    description: str = None

class TodoUpdate(BaseModel):
    todo_id: int
    title: str
    description: str = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}

@app.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos")
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated_todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}