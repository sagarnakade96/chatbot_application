# Backend (FastAPI)

FastAPI service hosting multiple chatbot applications behind one API. This
document covers the backend only (`backend/`).

## Structure

Platform code (config, health, routing) is separate from **apps**: each
application is a self-contained folder under `app/apps/`.

```
backend/
├── app/
│   ├── main.py              App factory (create_app), CORS, mounts api_router at /api/v1
│   ├── core/
│   │   └── config.py        Settings (pydantic-settings), reads repo-root .env
│   ├── api/v1/
│   │   ├── __init__.py      api_router: registers health + every app router
│   │   └── health.py        GET /health
│   └── apps/
│       └── basic_chatbot/   Placeholder app (router.py only, no functionality yet)
├── tests/                   pytest + TestClient (test_health.py, test_basic_chatbot.py)
├── requirements.txt         Backend dependencies (pinned)
├── AGENTS.md                Rules for AI coding agents (includes docs-update rule)
├── CLAUDE.md                Imports AGENTS.md for Claude Code
└── .claude/skills/          add-fastapi-endpoint, update-backend-docs
```

## Applications

| App | Prefix | Status |
|-----|--------|--------|
| basic_chatbot | `/api/v1/basic-chatbot` | Placeholder route only; to be implemented by the owner |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Liveness check: `{"status","app","version"}` |
| GET | `/api/v1/basic-chatbot` | basic_chatbot placeholder: `{"app","status":"not implemented"}` |

Interactive docs: `/docs` (Swagger UI) and `/redoc`.

## Setup

Uses the repo-level virtualenv (`../venv`) and repo-root `../.env`
(see `../.env.example`).

```powershell
# from repo root
venv\Scripts\activate
pip install -r backend\requirements.txt
```

## Run

```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```

Health check: http://localhost:8000/api/v1/health

## Test

```powershell
cd backend
python -m pytest
```

## Configuration

Settings live in `app/core/config.py` (`Settings`) and are overridable by
environment variables or the repo-root `.env` (case-insensitive; unknown keys
ignored). Access via `Depends(get_settings)`.

| Setting | Default | Notes |
|---------|---------|-------|
| `app_name` | `Chatbot Backend` | |
| `app_version` | `0.1.0` | |
| `debug` | `false` | |
| `api_v1_prefix` | `/api/v1` | |
| `cors_origins` | `["http://localhost:8501"]` | Streamlit default |
| `aws_access_key_id`, `aws_secret_access_key`, `aws_region` | none | From `.env` |
| `knowledge_base_id`, `tavily_api_key` | none | From `.env` |

## Adding a new app

1. Create `app/apps/<name>/` with `__init__.py` (suggested: `router.py`, `schemas.py`, `service.py`)
2. Register the router in `app/api/v1/__init__.py`
3. Add `tests/test_<name>.py` (override dependencies; no network)
4. Update this README (Structure, Applications, Endpoints) - see `AGENTS.md`

The `add-fastapi-endpoint` skill walks through these steps.

## Keeping docs current

Any change to routes, apps, settings, dependencies, structure or run/test
commands must update this README, `AGENTS.md` and the skills in the same
change. See the "Documentation" section of `AGENTS.md`.
