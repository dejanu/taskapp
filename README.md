# Minimal FastAPI Health Check App

## Overview
This is a minimal FastAPI application with a single `/health` endpoint that returns a simple health status.

## Features
- **Batch Task Creation**: Use the provided shell script to create multiple tasks at once.

## Local Development
## Example: Creating Tasks

To create a task using curl:

```bash
curl -X POST http://localhost:8000/tasks \
   -H "Content-Type: application/json" \
   -d '{"title": "First Task"}'
```

Response:
```json
{
   "id": 1,
   "title": "First Task"
}
```

To list all tasks:

```bash
curl http://localhost:8000/tasks
```

## Batch Task Creation

To quickly create 5 tasks, use the provided shell script:

```bash
./create_tasks.sh
```

This will send 5 POST requests to the API, creating tasks titled "Task 1" through "Task 5".

You can inspect or modify the script in [create_tasks.sh](create_tasks.sh).
1. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   uvicorn main:app --reload
   ```
5. Access the health endpoint:
   - [http://localhost:8000/health](http://localhost:8000/health)

## Using Docker
1. Build the Docker image:
   ```bash
   docker build -t fastapi-app .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 fastapi-app
   ```
3. Access the health endpoint:
   - [http://localhost:8000/health](http://localhost:8000/health)

## Requirements
- Python 3.11+
- FastAPI
- Uvicorn

## License
MIT

```mermaid
                                         START
                                           │
                             ┌─────────────┴─────────────┐
                             │                           │
                       Task Type?                   Task Type?
                 Thinking / Reasoning            Coding / IDE Work
           (ideas, explanations, research)  (implement, refactor, autocomplete)
                             │                           │
          ┌──────────────────┴──────────────┐            │
          │                                 │            │
Need Web / Docs Info?                Private / Sensitive? IDE Supports Agent?
          │                                 │            │
          ▼                                 ▼            │
      Yes → Use Google Gemini         Yes → Use Claude AI  │
      (multimodal, web+docs)          (private reasoning)│
          │                                 │            │
Optional: Summarization / doc analysis     ▼            │
 ───────────────────────────────► ChatGPT / Claude AI   │
          │                                                 │
          ▼                                                 ▼
         Done                                          Coding / IDE Branch
                                                       ┌─────────────┬─────────────┐
                                                       │                           │
                                               IDE Agent Available?            No Agent
                                                       │                           │
                                                    Yes → IDE Agent             Manual coding
                                                    │
                     ┌───────────────────────────────┴───────────────────────────────┐
                     │                                                               │
               GitHub Copilot                                                Claude AI Agent
            (inline code completions, repo context)                 (reasoning, tests, doc generation)
```