from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Body
from pydantic import BaseModel, validator
from typing import List


app = FastAPI()

@app.get("/health")
"""Return a simple health-check response indicating the service is running."""
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
    new_task = Task(id=next_id, title=task.title)
    tasks.append(new_task)
    next_id += 1
    return new_task


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

# Update task (complete/incomplete)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, completed: bool = Body(...)):
    for task in tasks:
        if task.id == task_id:
            # Add completed field if not present
            if not hasattr(task, 'completed'):
                setattr(task, 'completed', False)
            task.completed = completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Delete task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")

# Serve web UI
from fastapi.responses import HTMLResponse
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>TaskApp</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; background: #f7f7f7; }
            h1 { color: #333; }
            #task-form { margin-bottom: 1em; }
            #tasks { list-style: none; padding: 0; }
            .task { background: #fff; margin-bottom: 0.5em; padding: 1em; border-radius: 5px; display: flex; align-items: center; justify-content: space-between; }
            .completed { text-decoration: line-through; color: #888; }
            button { margin-left: 0.5em; }
        </style>
    </head>
    <body>
        <h1>TaskApp</h1>
        <form id='task-form'>
            <input type='text' id='title' placeholder='New task...' maxlength='100' required />
            <button type='submit'>Add Task</button>
        </form>
        <ul id='tasks'></ul>
        <script>
        async function fetchTasks() {
            const res = await fetch('/tasks');
            const tasks = await res.json();
            const list = document.getElementById('tasks');
            list.innerHTML = '';
            tasks.forEach(task => {
                const li = document.createElement('li');
                li.className = 'task' + (task.completed ? ' completed' : '');
                li.innerHTML = `
                    <span class="${task.completed ? 'completed' : ''}">${task.title}</span>
                    <span>
                        <button onclick="toggleTask(${task.id}, ${!task.completed})">${task.completed ? 'Undo' : 'Complete'}</button>
                        <button onclick="deleteTask(${task.id})">Delete</button>
                    </span>
                `;
                list.appendChild(li);
            });
        }

        document.getElementById('task-form').onsubmit = async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value.trim();
            if (!title) return;
            await fetch('/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            document.getElementById('title').value = '';
            fetchTasks();
        };

        async function toggleTask(id, completed) {
            await fetch(`/tasks/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(completed)
            });
            fetchTasks();
        }

        async function deleteTask(id) {
            await fetch(`/tasks/${id}`, { method: 'DELETE' });
            fetchTasks();
        }

        fetchTasks();
        </script>
    </body>
    </html>
    """
