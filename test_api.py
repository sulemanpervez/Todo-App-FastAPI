from main import app
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_todo():
    response = client.post("/todo", json={"title": "Test todo", "description": "This is a test todo"}) 
    assert response.status_code == 200
    assert response.json()["title"] == "Test todo"
    
    
def test_update_todo():
    response = client.put("/todo/1", json={"title": "Updated todo", "description": "This is an updated todo"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated todo"
    
    
def test_delete_todo():
    response = client.delete("/todo/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Deleted todo" 