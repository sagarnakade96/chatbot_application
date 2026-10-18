---
name: add-fastapi-endpoint
description: Add a new app (feature module) or endpoint to the FastAPI backend following the app/apps/<name> layout (router, schemas, service, test). Use when asked to create an API route, endpoint or app in backend/.
---

# Add a FastAPI app / endpoint

Work inside `backend/`. Replace `<name>` with the app name (snake_case).

1. **Module** - create `app/apps/<name>/` with `__init__.py`.
2. **Schemas** - `schemas.py`: Pydantic request/response models.
3. **Service** - `service.py`: the logic. LLM clients are passed in as
   arguments, never created inline.
4. **Router** - `router.py`:
   ```python
   router = APIRouter(prefix="/<name>", tags=["<name>"])

   @router.post("/run", response_model=RunResponse)
   def run(body: RunRequest, settings: Settings = Depends(get_settings)):
       return service.run(body, settings)
   ```
5. **Register** - in `app/api/v1/__init__.py`:
   `api_router.include_router(<name>_router)`.
6. **Test** - `tests/test_<name>.py` with `TestClient(app)`; replace the LLM via
   `app.dependency_overrides`. No network.
7. **Verify** - `python -m pytest` from `backend/` with the repo venv.
8. **Docs** - run the `update-backend-docs` skill: README Structure /
   Applications / Endpoints tables, AGENTS.md "Current apps", and
   `../.env.example` if new settings were added. Not optional.

Rules: thin routers, `response_model` on every route, `def` for blocking calls,
no cross-app imports, no secrets in code or logs.
