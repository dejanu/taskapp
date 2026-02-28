from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Body
from pydantic import BaseModel, validator
from typing import List

app = FastAPI()

@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})

# Pydantic models
class TaskCreate(BaseModel):
    title: str

    @validator("title")
    def title_length(cls, v):
        if len(v) < 3:
            raise ValueError("Title must be at least 3 characters long.")
        return v

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
    try:
        new_task = Task(id=next_id, title=task.title)
        tasks.append(new_task)
        next_id += 1
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# List all tasks
@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return tasks

# Get task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
