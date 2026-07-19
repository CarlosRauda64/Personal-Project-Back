---
name: fastapi-templates
description: Project structure and layered architecture for FastAPI applications. Use when scaffolding a new FastAPI project, organizing modules into layers, or deciding where new code belongs. For code-level conventions (Annotated dependencies, return types, routing, Pydantic, async, streaming, tooling), always follow the `fastapi` skill.
---

# FastAPI Project Structure

Layered project structure for FastAPI applications. This skill covers **only
where code lives** and how layers interact. **How the code is written** always
follows the `fastapi` skill, which takes precedence over anything in this
skill.

## When to Use This Skill

- Scaffolding a new FastAPI project
- Organizing an existing app into layers
- Deciding where a new feature/module belongs

For anything code-related (endpoints, dependencies, models, schemas,
streaming, async, tooling), use the `fastapi` skill instead.

## Project Structure

```
app/
├── api/                    # API layer (HTTP concerns)
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── users.py
│   │   │   ├── auth.py
│   │   │   └── items.py
│   │   └── router.py       # Aggregates all v1 endpoint routers
│   └── dependencies.py     # Shared dependencies (Annotated type aliases)
├── core/                   # Configuration and infrastructure
│   ├── config.py           # Settings (pydantic-settings)
│   ├── security.py         # Auth helpers (tokens, password hashing)
│   └── database.py         # Engine/session setup and DB dependency
├── models/                 # Database models
│   ├── user.py
│   └── item.py
├── schemas/                # Pydantic request/response schemas
│   ├── user.py
│   └── item.py
├── services/               # Business logic
│   ├── user_service.py
│   └── auth_service.py
├── repositories/           # Data access (optional for simple CRUD)
│   ├── user_repository.py
│   └── item_repository.py
└── main.py                 # Application entry point
tests/                      # Mirrors the app/ structure
├── api/
│   └── v1/
│       └── test_users.py
├── services/
└── conftest.py
```

## Layer Responsibilities

| Layer | Contains | Must NOT contain |
|---|---|---|
| `api/v1/endpoints` | Routers, path operations, status codes, `HTTPException` | Business logic, direct DB queries |
| `api/dependencies.py` | Shared dependency functions and their `Annotated` aliases | Endpoint code |
| `core/` | Settings, DB engine/session, security utilities | Anything request-specific |
| `models/` | Database table models | Request validation logic |
| `schemas/` | Request/response validation models | DB code |
| `services/` | Business logic, orchestration | HTTP concerns (`Request`, `HTTPException`) |
| `repositories/` | Data access queries | Business rules |

## Dependency Flow

Dependencies point inward only:

```
endpoints → services → repositories → models
    │           │           │
    └───────────┴───────────┴──→ schemas (cross-cutting, any layer may use)
    └────────────────────────────→ core (config, db, security)
```

- Endpoints never query the database directly; they call services.
- Services never touch HTTP objects; they raise domain errors that endpoints
  translate into `HTTPException`.
- Repositories never contain business rules; they only read and write data.

## Code Conventions (precedence rule)

All code-level style follows the **`fastapi` skill**. In case of any conflict
with examples or habits from other sources, the `fastapi` skill wins. In
particular:

- `Annotated[..., Depends(...)]` with reusable type aliases; never
  `param = Depends(...)` defaults.
- Return types on path operations; `response_model` only when the public
  schema differs from the return type.
- Router-level `prefix`, `tags`, and shared `dependencies` on `APIRouter(...)`;
  the version prefix (`/api/v1`) at `include_router()` time is the accepted
  exception for versioning.
- Pydantic v2 style: no `...` defaults, no `RootModel`, `model_dump()`
  instead of `dict()`.
- SQLModel for database models when starting fresh; otherwise modern
  SQLAlchemy 2.0 style.
- `async` only when the called code is truly async-compatible; `def` when in
  doubt.
- uv, Ruff, ty, Asyncer, SQLModel, and HTTPX for tooling.

## Detailed Structure Guide

Per-layer placement rules, router aggregation, and a checklist for adding a
new feature module live in [references/details.md](references/details.md).
