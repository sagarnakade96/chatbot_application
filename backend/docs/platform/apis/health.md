# GET /api/v1/health

## Purpose
Liveness check: confirms the process is up and settings loaded.

## Auth / permissions
None.

## Inputs
None.

## Behavior
Reads `Settings` via `Depends(get_settings)` and echoes `app_name` /
`app_version` back. No I/O, no side effects.

## Response
- **200 OK** — always, if the process is running.

```json
{
  "status": "ok",
  "app": "Chatbot Backend",
  "version": "0.1.0"
}
```
Verified against `tests/test_health.py` (asserts `status_code == 200` and
`json()["status"] == "ok"`) and the literal field values in `app/core/config.py`
defaults — not a fabricated example.

## Source
- Route: `app/api/v1/health.py`
- Schema: `HealthResponse` (defined inline in the same file)
- Test: `tests/test_health.py`
