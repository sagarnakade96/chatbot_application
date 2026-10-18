# AGENTS.md (backend)

Guidance for AI coding agents working in `backend/`. This scope is the FastAPI
app only; see `../AGENTS.md` for the rest of the repository.

## Environment
- Use the repo venv: `..\venv\Scripts\python.exe` (Windows). Never create another venv.
- Config comes from the repo-root `../.env` via `app/core/config.py`. Never read
  `os.environ` directly, never print or commit secrets, never edit `.env`.
- Run: `uvicorn app.main:app --reload` from `backend/`. Test: `python -m pytest`.

## Architecture rules
- Platform code lives in `app/core/` (settings, shared clients) and `app/api/v1/`
  (health + router registration). Each feature is a self-contained module
  `app/apps/<name>/` with `router.py` (HTTP only), `service.py` (logic, LLM calls),
  `schemas.py` (Pydantic models). Apps must not import from each other.
- Routers stay thin; no Bedrock/LangChain/LangGraph code in routers.
- Register each app router in `app/api/v1/__init__.py`.
- Every endpoint declares `response_model` and typed Pydantic request bodies.
- Use `Depends(...)` for settings and shared clients (so tests can override them).
- Use plain `def` for blocking work (boto3 is blocking); `async def` only for
  non-blocking I/O. Raise `HTTPException` with proper status codes.
- Settings: add fields to `Settings` in `config.py`; mirror new keys in `../.env.example`.

## Style
- Python 3.x type hints everywhere; format with `black` (already in the venv).
- Match existing naming: snake_case modules, one router per resource.

## Testing
- Every new endpoint gets a `tests/test_<name>.py` using `TestClient`.
- Mock AWS/LLM calls with `app.dependency_overrides`; tests must not hit the network.
- Application code under `app/apps/` is written by the owner; do not add app logic unless asked.

## Dependencies
- Add new packages to `requirements.txt` with pinned versions, installed in the repo venv.

## Documentation (mandatory)
After ANY change in `backend/` - new/removed/renamed app, route, setting,
dependency, file/folder, or run/test command - update the docs in the same
change, before reporting the task done:
- `README.md`: Structure tree, Applications table, Endpoints table, Configuration
  table, Setup/Run/Test commands (whichever apply).
- `AGENTS.md`: any rule or path that became inaccurate.
- `.claude/skills/*/SKILL.md`: any step or example that became inaccurate.
- `../.env.example`: placeholders for any new environment variable.
- `../AGENTS.md` project map, if top-level backend layout changed.
Use the `update-backend-docs` skill for the checklist. Say in your final message
which docs you updated (or that none needed changes).

## Current apps
- `basic_chatbot` - placeholder router only (`/api/v1/basic-chatbot`).

## Skills
- `.claude/skills/add-fastapi-endpoint` - step-by-step for new apps/endpoints.
- `.claude/skills/update-backend-docs` - docs checklist to run after every change.
