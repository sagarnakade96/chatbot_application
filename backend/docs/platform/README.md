# Platform

Not an "application" under `app/apps/` — this is the shared plumbing every
application runs on: app factory, settings, and the versioned API router
that mounts each application's routes.

## Where the code lives

| Piece | File | Role |
|---|---|---|
| App factory | `app/main.py` | Builds the `FastAPI` instance, adds CORS middleware, mounts `api_router` under `settings.api_v1_prefix` |
| Settings | `app/core/config.py` | `Settings` (pydantic-settings); reads the repo-root `../.env`; `get_settings()` is the DI provider |
| Route registration | `app/api/v1/__init__.py` | Builds `api_router`; every application registers its router here |
| Health route | `app/api/v1/health.py` | Only concrete route owned directly by the platform (see API doc below) |

## Dependents

Every application under `app/apps/` depends on this layer for settings
(`Depends(get_settings)`) and for being reachable at all (its router must be
registered in `app/api/v1/__init__.py`). A change to `Settings` field names,
`api_v1_prefix`, or the CORS config affects every application. A change to
`app/api/v1/__init__.py` that fails to register an app's router makes that
app unreachable even though its code is otherwise correct.

## Configuration

| Setting | Default | Source |
|---|---|---|
| `app_name` | `"Chatbot Backend"` | code default |
| `app_version` | `"0.1.0"` | code default |
| `debug` | `false` | code default / env |
| `api_v1_prefix` | `"/api/v1"` | code default / env |
| `cors_origins` | `["http://localhost:8501"]` | code default / env |
| `aws_access_key_id`, `aws_secret_access_key`, `aws_region` | none | `../.env` |
| `knowledge_base_id`, `tavily_api_key` | none | `../.env` |

No background jobs or external services are wired up at the platform level
today; the AWS/Tavily settings exist in `Settings` but nothing in `backend/`
currently reads them (verified: no application code imports them as of
2026-10-18).

## APIs

- [`GET /api/v1/health`](apis/health.md)
