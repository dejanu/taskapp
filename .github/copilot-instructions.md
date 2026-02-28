# Copilot Instructions for TaskApp Repository

## Architecture Style

This repository implements a **monolithic minimal FastAPI application**. All API endpoints, data models, and business logic reside in a single file (main.py). There is no modularization or separation of concerns between API, data models, or storage.

## Coding Conventions

- **Single-file Implementation**: All code must be placed in main.py. Do not create additional Python modules or packages.
- **Pydantic Models**: Use Pydantic models for request validation and response serialization.
- **Global In-memory Storage**: Use global variables for storing application state (e.g., tasks: List[Task], next_id).
- **Endpoint Definitions**: Define all FastAPI endpoints directly on the app instance.
- **Input Validation**: Enforce input constraints using Pydantic validators.
- **Error Handling**: Use FastAPI's HTTPException for error responses. Return appropriate HTTP status codes.
- **Response Models**: Specify response_model for endpoints to ensure consistent output serialization.
- **Consistent Naming**: Use descriptive and consistent names for endpoints and models.

## Module and Dependency Boundaries

- **All logic must reside in main.py**. Do not split code into multiple files or modules.
- **Global State**: Application state (tasks, IDs) must be managed via global variables in main.py.
- **No External Persistence**: Do not introduce databases or file-based storage. All data must remain in-memory.
- **No Authentication/Authorization**: All endpoints are public and do not require authentication.
- **Minimal Dependencies**: Only use FastAPI, Uvicorn, and Pydantic as specified in requirements.txt.

## Testing Expectations

- **No Automated Tests Present**: There are currently no test files or test frameworks in the repository.
- **Manual Testing Only**: API functionality is tested manually via curl commands (see create_tasks.sh and README.md).
- **If adding tests, document as a risk**: Introducing automated tests would be inconsistent with the current structure.

## Anti-patterns (Violations of Current Design)

- **Modularization**: Do not split code into multiple files, modules, or packages.
- **Persistent Storage**: Do not add database integration or file-based storage.
- **Automated Testing**: Do not add test files or test frameworks unless the repository structure is updated to support them.
- **Complex Dependency Graphs**: Do not introduce additional dependencies beyond those listed in requirements.txt.
- **Encapsulation of State**: Do not encapsulate global state in classes or separate modules.
- **Authentication/Authorization**: Do not add authentication or authorization mechanisms.
- **Redundant Error Handling**: Avoid unnecessary try/except blocks where Pydantic validation already enforces constraints.

## Risks and Inconsistencies

- **Global Mutable State**: Using global variables for state is not thread-safe and may cause issues in concurrent environments.
- **No Separation of Concerns**: Mixing models, endpoints, and storage logic in one file reduces maintainability.
- **Redundant Error Handling**: The POST endpoint's try/except block is unnecessary due to Pydantic validation.
- **No Automated Testing**: Lack of tests increases risk of undetected regressions.
- **No Persistence**: All data is lost on application restart.

---

**Follow these instructions to maintain consistency with the current repository design. Document any deviations as risks.**
