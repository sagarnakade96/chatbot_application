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
  `app/apps/<name>/`. Apps must not import from each other — if one app
  needs another's data, that's a signal it belongs in `app/core/` instead.
- **Code-style convention (apply going forward; no app is fully split yet):**
  within `app/apps/<name>/`, separate:
  - `apis/` — route functions only: parse the request, call an action, return
    the response. No business logic, no direct Bedrock/LangChain/boto3 calls.
  - `actions/` — one orchestration step per use case (e.g. "handle an incoming
    chat message"); calls into `services/` and shapes the result for `apis/`.
  - `services/` — the actual logic: LLM calls, external APIs, data access.
  `schemas.py` (Pydantic models) sits alongside these. A route handler's only
  job is to depend on an action and return its result — if you find LLM/boto3
  code in a file under `apis/`, that's a bug to fix, not a style choice.
  `basic_chatbot` currently has only a flat `router.py` because it has no
  functionality yet; split it into this layout when real logic is added.
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
  Verify the version actually installed (`pip show <pkg>`) rather than guessing —
  don't write a version you haven't checked.
- `requirements.txt` here (and `../requirement_v2.txt` at repo root) are
  **direct-dependency files**, not freeze/lock files: list only packages the
  code imports by name, or that are required to run/test it even if not
  imported (say why, in a comment, e.g. `uvicorn` as the ASGI server). Do not
  dump `pip freeze`'s transitive closure into them. `../requirement.txt`
  remains the full frozen snapshot for the repo-root project — do not treat
  this file as replacing it.
- Never silently drop a package whose purpose is uncertain; flag it in your
  report instead and ask, or leave it with a comment explaining the doubt.

## Documentation (mandatory)
After ANY change in `backend/` - new/removed/renamed app, route, setting,
dependency, file/folder, or run/test command - update the docs in the same
change, before reporting the task done:
- `README.md`: Structure tree, Applications table, Endpoints table, Configuration
  table, Setup/Run/Test commands (whichever apply).
- `docs/<app>/README.md` and `docs/<app>/apis/<endpoint>.md` for every app whose
  behavior, routes, response contracts, permissions, models, or cross-app
  dependencies changed. Update file/line references and links if files moved.
  **Verify every example response against a real test, schema, or fixture** —
  if none exists, label it "illustrative (unverified)" and say what wasn't
  checked; never present an invented response as observed.
- `AGENTS.md`: any rule, path, or the "Current apps" list that became inaccurate.
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
