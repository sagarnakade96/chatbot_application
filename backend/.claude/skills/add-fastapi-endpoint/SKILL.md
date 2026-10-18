---
name: add-fastapi-endpoint
description: Add a new app (feature module) or endpoint to the FastAPI backend following the app/apps/<name> layout (apis/actions/services, schemas, test). Use when asked to create an API route, endpoint or app in backend/.
---

# Add a FastAPI app / endpoint

Work inside `backend/`. Replace `<name>` with the app name (snake_case).

1. **Module** - create `app/apps/<name>/` with `__init__.py`.
2. **Schemas** - `schemas.py`: Pydantic request/response models.
3. **Services** - `services/`: the actual logic (LLM calls, external APIs,
   data access). LLM/HTTP clients are passed in as arguments, never created
   inline, so tests can override them.
4. **Actions** - `actions/`: one orchestration function per use case; calls
   into `services/` and shapes the result for the route. If a request needs
   no orchestration beyond a single service call, an action can be a thin
   pass-through — but keep the layer so routes stay uniform.
5. **API (route)** - `apis/` (or `router.py` for a trivial/placeholder app
   with no real logic yet, like `basic_chatbot` today):
   ```python
   router = APIRouter(prefix="/<name>", tags=["<name>"])

   @router.post("/run", response_model=RunResponse)
   def run(body: RunRequest, settings: Settings = Depends(get_settings)):
       return actions.run(body, settings)
   ```
   The route function parses the request and calls an action — nothing else.
   No Bedrock/LangChain/boto3 code belongs in `apis/`.
6. **Register** - in `app/api/v1/__init__.py`:
   `api_router.include_router(<name>_router)`.
7. **Test** - `tests/test_<name>.py` with `TestClient(app)`; replace the LLM via
   `app.dependency_overrides`. No network.
8. **Verify** - `python -m pytest` from `backend/` with the repo venv.
9. **Docs** - run the `update-backend-docs` skill: README Structure /
   Applications / Endpoints tables, `docs/<name>/README.md` +
   `docs/<name>/apis/<endpoint>.md` (source every example response from a
   real test/schema, label unverified ones as illustrative), AGENTS.md
   "Current apps", and `../.env.example` if new settings were added. Not optional.

Rules: thin routes (`apis/` only parses + calls an action), `response_model`
on every route, `def` for blocking calls, no cross-app imports, no secrets in
code or logs.
