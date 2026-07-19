# AGENTS.md

## Project Context

- Personal backend project built with **FastAPI**.
- **Python 3.14**, Windows environment.
- Virtual environment lives in `env/` (created with pip + venv).
- Dependencies are managed with **pip** and tracked in `requirements.txt`.

## Skills Rules (read first)

This project has two skills installed under `.agents/skills/`. Use them like this:

- **`fastapi`** → governs **ALL code-level conventions**: endpoints, dependencies,
  Pydantic models, routing, responses, async usage, streaming, tooling.
- **`fastapi-templates`** → governs **ONLY the project structure**: folder layout,
  layer responsibilities, and where new modules belong.
- **On any conflict, the `fastapi` skill always wins.**

Key code conventions inherited from the `fastapi` skill:

- `Annotated[..., Depends(...)]` with reusable type aliases; never
  `param = Depends(...)` defaults.
- Return types on path operations; `response_model` only when the public schema
  differs from the return type.
- Router-level `prefix`, `tags`, and shared `dependencies` on `APIRouter(...)`;
  the version prefix (`/api/v1`) at `include_router()` time is the accepted
  exception for versioning.
- Pydantic v2 style: no `...` defaults, no `RootModel`, `model_dump()` instead
  of `dict()`.
- `async` only when the called code is truly async-compatible; `def` when in
  doubt.

## Project Structure

Follow the layered structure defined by the `fastapi-templates` skill
(`app/api/v1/endpoints`, `app/api/dependencies.py`, `app/core/`, `app/models/`,
`app/schemas/`, `app/services/`, optional `app/repositories/`, `app/main.py`).
See `.agents/skills/fastapi-templates/SKILL.md` and its `references/details.md`
for layer responsibilities and the new-feature checklist.

Dependency flow: `endpoints → services → repositories → models`, with `schemas`
and `core` as cross-cutting layers.

## Database: SQLModel + SQLite

- **SQLModel** is the single way to talk to the database; do not mix in raw
  SQLAlchemy patterns.
- Engine and session factory live in `app/core/database.py`.
- The session dependency is declared once with an `Annotated` type alias
  (e.g. `SessionDep`) and reused everywhere.
- Table models go in `app/models/`; request/response variants (`*Create`,
  `*Update`, `*Public`) go in `app/schemas/`.

## Security (from day one)

The project uses **OAuth2 Password Bearer + JWT**, following the current
official FastAPI security tutorial:

- **PyJWT** for token creation/verification. Do **not** use `python-jose`.
- **pwdlib with Argon2** (`pwdlib[argon2]`, `PasswordHash.recommended()`) for
  password hashing. Do **not** use `passlib`.
- Use `datetime.now(timezone.utc)` for token expiration; never `utcnow()`.
- `app/core/security.py`: password hash/verify helpers, token create/decode
  helpers.
- `app/api/dependencies.py`: `get_current_user` declared as an `Annotated`
  type alias; failed auth returns `401` with `WWW-Authenticate: Bearer`.
- Login endpoint (`OAuth2PasswordRequestForm`) lives under `/api/v1/auth`.
- Always verify against a dummy hash when the user does not exist, to mitigate
  timing attacks.
- `SECRET_KEY` and related settings come from pydantic-settings + `.env`;
  **never hardcode secrets** and never commit `.env`.

## Configuration

- Settings via **pydantic-settings** in `app/core/config.py`, with a cached
  accessor.
- `.env` file is gitignored; provide a `.env.example` with placeholder values.

## Commands

```powershell
# Activate the virtual environment
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
fastapi dev app/main.py

# Run tests
pytest
```

## Testing

- `tests/` mirrors the `app/` structure (`tests/api/v1/`, `tests/services/`).
- pytest + pytest-asyncio with `asyncio_mode = "auto"` (no `event_loop`
  fixture).
- HTTPX `AsyncClient` with `ASGITransport` for endpoint tests.
- Override dependencies (e.g. the DB session) via `app.dependency_overrides`.

## Dependencies

Core runtime/test dependencies (install into `env/` and pin in
`requirements.txt`):

- `fastapi`, `uvicorn`
- `sqlmodel`
- `pyjwt`
- `pwdlib[argon2]`
- `pydantic-settings`
- `python-multipart` (required for the OAuth2 password form data)
- `pytest`, `pytest-asyncio`, `httpx`
