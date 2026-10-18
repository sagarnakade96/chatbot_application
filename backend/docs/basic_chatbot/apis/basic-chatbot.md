# GET /api/v1/basic-chatbot

## Purpose
Placeholder route proving the app is registered and reachable. Carries no
real functionality.

## Auth / permissions
None.

## Inputs
None.

## Behavior
Returns a fixed dict literal. No service/action layer, no external calls.

## Response
- **200 OK** — always.

```json
{
  "app": "basic_chatbot",
  "status": "not implemented"
}
```
Verified against `tests/test_basic_chatbot.py` (asserts
`json()["app"] == "basic_chatbot"`) and the literal return value in
`app/apps/basic_chatbot/router.py` — not a fabricated example.

## Source
- Route: `app/apps/basic_chatbot/router.py`
- Test: `tests/test_basic_chatbot.py`

## Not yet implemented
No schemas, no service layer, no persistence, no auth. This doc will need a
rewrite once real behavior is added — see the documentation rule in
`../../AGENTS.md`.
