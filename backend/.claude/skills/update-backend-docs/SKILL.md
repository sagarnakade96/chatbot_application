---
name: update-backend-docs
description: Update the backend documentation (README, docs/<app>/, AGENTS.md, skills, .env.example) after any change in backend/. Run at the end of every backend change - new or changed apps, routes, settings, dependencies, files, or commands.
---

# Update backend docs

Run after every change in `backend/`, before reporting the task done.

1. Review what changed (`git status`, `git diff`, or your own edit list).
2. Update `README.md`:
   - **Structure** tree matches the real files (`find app tests docs` to compare).
   - **Applications** table: one row per folder in `app/apps/`, with prefix and status.
   - **Endpoints** table: one row per route (check `/docs` or `app/api/v1/`).
   - **Configuration** table matches `Settings` in `app/core/config.py`.
   - Setup / Run / Test commands still work.
3. For every app whose behavior, routes, response contract, permissions,
   models, or cross-app dependencies changed, update `docs/<app>/README.md`
   and `docs/<app>/apis/<endpoint>.md`:
   - Purpose, code locations (`apis/`/`actions`/`services`/`schemas.py` as they
     exist), URL mapping, dependencies on other apps, config/jobs/external
     services actually found in the code.
   - Per API: method + route, auth, inputs, behavior, status codes, an example
     response body. **Source every example from a real test, schema default,
     or fixture** — cite which one. If none exists, label the example
     "illustrative (unverified)" instead of presenting it as observed.
   - Fix any file/line reference or cross-doc link that moved.
   - Platform-level routes (not under `app/apps/`, e.g. health) live in
     `docs/platform/`.
4. Update `AGENTS.md`: "Current apps" list, and any rule or path now inaccurate.
5. Update `.claude/skills/*/SKILL.md` if any step or example is now wrong.
6. If an environment variable was added, add a placeholder to `../.env.example`
   (never real values).
7. If the top-level backend layout changed, update the project map in `../AGENTS.md`.
8. Run `python -m pytest` from `backend/`; in the final message list the docs
   updated, or state that none needed changes.
