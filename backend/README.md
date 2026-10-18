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
├── docs/                    Functional + API docs per application (see "Documentation")
│   ├── platform/            Shared plumbing: health route, settings
│   └── basic_chatbot/       The basic_chatbot app
├── requirements.txt         Backend direct dependencies (verified versions, not a freeze file)
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

Interactive (auto-generated) docs: `/docs` (Swagger UI) and `/redoc`.
Hand-written functional/API docs per application: `docs/<app>/README.md` and
`docs/<app>/apis/<endpoint>.md` — start at [docs/platform/README.md](docs/platform/README.md)
and [docs/basic_chatbot/README.md](docs/basic_chatbot/README.md).

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

1. Create `app/apps/<name>/` with `__init__.py`. Once the app has real
   functionality, split it into `apis/` (route functions), `actions/`
   (orchestration), `services/` (LLM/external calls) and `schemas.py` — see
   "Architecture rules" in `AGENTS.md`. A placeholder with no functionality
   yet (like `basic_chatbot`) may start as a flat `router.py`.
2. Register the router in `app/api/v1/__init__.py`
3. Add `tests/test_<name>.py` (override dependencies; no network)
4. Update this README (Structure, Applications, Endpoints), add
   `docs/<name>/README.md` and `docs/<name>/apis/<endpoint>.md` - see `AGENTS.md`

The `add-fastapi-endpoint` skill walks through these steps.

## Dependency files

`requirements.txt` here (and `../requirement_v2.txt` at the repo root) list
**direct dependencies only** — packages imported by name, or required to
run/test the code even if not imported (noted in a comment why). They are
not a `pip freeze` dump. `../requirement.txt` at the repo root is the full,
fully-pinned freeze/lock file for reproducing the whole shared environment;
these direct-dependency files don't replace it and nothing here changes it.

## Keeping docs current

Any change to routes, apps, settings, dependencies, structure or run/test
commands must update this README, `docs/<app>/`, `AGENTS.md` and the skills
in the same change. See the "Documentation" section of `AGENTS.md`.
