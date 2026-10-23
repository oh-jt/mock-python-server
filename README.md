# mock-python-server

> **Intentionally vulnerable on branch `pr/create-user`. Interview use only. Do not deploy.**

A small identity-style service (users in tenants) used for code-review exercises.

## Run

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

## Test

    pytest -q

## Layout

- `app/main.py`      – HTTP endpoints
- `app/db.py`        – SQLite connection and schema
- `app/models.py`    – request/response models and validation
- `app/security.py`  – password hashing
- `app/logs.py`      – structured logging helper
