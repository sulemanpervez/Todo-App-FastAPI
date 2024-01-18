from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Todo
from pydantic import BaseModel

app = FastAPI()

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