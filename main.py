from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Body
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})

# Pydantic models
class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    
# In-memory task storage
tasks: List[Task] = []
next_id = 1

# Create task
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, title=task.title)
    tasks.append(new_task)
    next_id += 1
    return new_task

# List all tasks
@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return tasks
