---
name: update-backend-docs
description: Update the backend documentation (README, AGENTS.md, skills, .env.example) after any change in backend/. Run at the end of every backend change - new or changed apps, routes, settings, dependencies, files, or commands.
---

# Update backend docs

Run after every change in `backend/`, before reporting the task done.

1. Review what changed (`git status`, `git diff`, or your own edit list).
2. Update `README.md`:
   - **Structure** tree matches the real files (`find app tests` to compare).
   - **Applications** table: one row per folder in `app/apps/`, with prefix and status.
   - **Endpoints** table: one row per route (check `/docs` or `app/api/v1/`).
   - **Configuration** table matches `Settings` in `app/core/config.py`.
   - Setup / Run / Test commands still work.
3. Update `AGENTS.md`: "Current apps" list, and any rule or path now inaccurate.
4. Update `.claude/skills/*/SKILL.md` if any step or example is now wrong.
5. If an environment variable was added, add a placeholder to `../.env.example`
   (never real values).
6. If the top-level backend layout changed, update the project map in `../AGENTS.md`.
7. Run `python -m pytest` from `backend/`; in the final message list the docs
   updated, or state that none needed changes.
