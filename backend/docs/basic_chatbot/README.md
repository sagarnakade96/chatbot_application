# basic_chatbot

## Status: placeholder — no functionality implemented

This application exists only as a routing stub. It was created to prove out
the multi-app layout; the owner will implement its actual behavior.

## Purpose (intended)
Working name for what will become the project's basic chatbot endpoint(s).
Not yet implemented, so no real user-facing behavior exists today.

## Where the code lives

| Piece | File |
|---|---|
| Router | `app/apps/basic_chatbot/router.py` |
| Package marker | `app/apps/basic_chatbot/__init__.py` |

There is no `schemas.py`, `service.py`, model, or `actions`/`services` split
yet — just the one router function. See `../../AGENTS.md` for the
`apis` / `actions` / `services` convention this and future applications
should grow into once real functionality is added.

## URL mapping
Registered in `app/api/v1/__init__.py` as
`api_router.include_router(basic_chatbot_router)`, mounted under the shared
`/api/v1` prefix (from `Settings.api_v1_prefix`) with its own
`/basic-chatbot` prefix (set on the router itself).

## Dependencies on other applications
None. Depends only on the platform layer (FastAPI `APIRouter`); imports
nothing from `app/core` or any other app.

## Configuration / background jobs / external services
None used by this application's code today.

## APIs
- [`GET /api/v1/basic-chatbot`](apis/basic-chatbot.md)
