# PGMS – Personal Growth Management System

This project follows a clean-architecture structure with four main layers:

- Domain: entities and business rules in [app/entities](app/entities)
- Use cases: application logic in [app/use_cases](app/use_cases)
- Interface adapters: controllers, schemas, and repository contracts in [app/interface_adapters](app/interface_adapters)
- Frameworks: FastAPI app, database, and persistence in [app/frameworks](app/frameworks)

## Structure

- [app/entities](app/entities): domain models such as users, goals, habits, and tasks
- [app/use_cases](app/use_cases): business workflows for each entity
- [app/interface_adapters](app/interface_adapters): controller and schema layer
- [app/frameworks](app/frameworks): API bootstrap and SQLAlchemy setup
- [app/presentation](app/presentation): runnable CLI entrypoint for the application
- [tests](tests): regression tests for startup and user use cases

## Run the app

From the project root:

```bash
python -m app.presentation.cli.main
```

Or with Uvicorn directly:

```bash
uvicorn app.frameworks.main:app --host 0.0.0.0 --port 8000
```

## Run the tests

```bash
pytest -q
```
