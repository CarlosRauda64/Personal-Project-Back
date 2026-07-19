# fastapi-templates — detailed structure guide

This guide covers **where code lives**. For **how to write the code**
(`Annotated` dependencies, return types, routing, Pydantic, streaming, async,
tooling), follow the `fastapi` skill — it takes precedence over anything in
this document.

## Entry Point: `main.py`

Responsibilities only:

- Create the `FastAPI` app (title, version, lifespan).
- Add middleware (CORS, etc.).
- Include the versioned API routers.

Nothing else lives here: no endpoints, no business logic, no DB setup.

## API Layer

### `api/v1/router.py`

Aggregates every endpoint router of one API version into a single router that
`main.py` includes. Endpoint modules declare their own `APIRouter` with
router-level `prefix`, `tags`, and shared `dependencies` (per the `fastapi`
skill); the version router only includes them, and the version prefix
(`/api/v1`) is applied when including it in `main.py`.

### `api/v1/endpoints/*.py`

One module per resource (`users.py`, `items.py`, ...). Each module owns:

- Its `APIRouter` (with prefix/tags/dependencies).
- Path operations for that resource: one HTTP operation per function.

Endpoints only translate between HTTP and the service layer:

- Input: path/query parameters and schemas.
- Output: schemas (declared as return types), status codes.
- Errors: catch domain errors from services and raise `HTTPException`.

### `api/dependencies.py`

Shared dependencies used across routers: current user, pagination, etc.
Declare each as a function plus its `Annotated` type alias (per the `fastapi`
skill).

## Core Layer

- `core/config.py`: `Settings` class (pydantic-settings) plus a cached
  accessor.
- `core/database.py`: engine and session factory. The DB-session dependency
  lives here **or** in `api/dependencies.py` — pick one place and keep it
  consistent.
- `core/security.py`: password hashing, token creation/verification. No
  request handling.

`core` must not import from `api`, `services`, or `repositories`.

## Models and Schemas

- `models/`: database models, one module per entity. With SQLModel (preferred
  by the `fastapi` skill), table models and base schemas can share fields.
- `schemas/`: API-facing validation models, one module per entity, named
  `EntityCreate`, `EntityUpdate`, `EntityPublic`, etc.

Keep both directories even when using SQLModel: table models go in `models/`,
request/response variants in `schemas/`.

## Services

One module per domain area. Services:

- Receive the DB session (or repositories) as parameters; never create them.
- Raise plain domain exceptions (`ValueError` or custom exception classes).
- Contain all business rules and orchestration.

## Repositories

One module per entity. Repositories only execute queries; no business rules.

For simple CRUD in small projects this layer can be skipped — services use
the session directly. Add it when queries are reused across services or grow
complex.

## Adding a New Feature Module (Checklist)

Example: a new `products` resource.

1. `models/product.py` — table model.
2. `schemas/product.py` — `ProductCreate`, `ProductUpdate`, `ProductPublic`.
3. `repositories/product_repository.py` — data access (optional).
4. `services/product_service.py` — business logic.
5. `api/v1/endpoints/products.py` — `APIRouter(prefix="/products",
   tags=["products"])` plus path operations.
6. Register the router in `api/v1/router.py`.
7. `tests/api/v1/test_products.py` — endpoint tests; `tests/services/` for
   service tests.

## Testing Layout

- `tests/` mirrors `app/`: `tests/api/v1/`, `tests/services/`, etc.
- `tests/conftest.py` holds shared fixtures: the test app, an HTTPX
  `AsyncClient` (with `ASGITransport`), and DB-session overrides via
  `app.dependency_overrides`.
- Use pytest with pytest-asyncio configured with `asyncio_mode = "auto"`.
