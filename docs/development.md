# Pathwise Local Development Guide

## Development Model

Pathwise uses a deliberately small Local development model:

```text
React/Vite Frontend  → host process
FastAPI Backend      → host process
PostgreSQL 18.6      → Docker Compose dependency
```

Local Development targets behavioral parity where behavior exists; it does not
reproduce Production infrastructure identity. It does not emulate ECS, Fargate,
ALB, WAF, CloudFront, Cognito, RDS, EventBridge, or Secrets Manager. LocalStack
and other AWS emulators are not part of the workflow.

## Prerequisites

Install these before bootstrapping the repository:

- Git;
- uv compatible with the validated `0.12.17` workflow;
- CPython `3.14.7` available through uv;
- Node.js `24.21.0`;
- npm `11.x`;
- Docker Engine and Docker Compose.

The repository does not install or manage these workstation prerequisites.

## First-Time Setup

### Repository root

From the repository root in PowerShell:

```powershell
Copy-Item .env.example .env
Copy-Item backend\.env.example backend\.env.local
Copy-Item frontend\.env.example frontend\.env.local
```

Edit only the clone-local root `.env` and set a new disposable value for:

```text
PATHWISE_POSTGRES_PASSWORD
```

The template intentionally provides no password. Never reuse a Production
credential.

### Backend dependencies

From `backend/`:

```powershell
uv sync --locked
```

This creates `backend/.venv/` and restores the environment from
`pyproject.toml` and `uv.lock`.

### Frontend dependencies

From `frontend/`:

```powershell
npm ci
```

This creates `frontend/node_modules/` strictly from `package-lock.json`.

## Configuration Files

Real Local files are ignored; safe templates are tracked.

| Trust boundary | Local file | Tracked template | Purpose |
| --- | --- | --- | --- |
| Local infrastructure | `/.env` | `/.env.example` | Compose/PostgreSQL password |
| Backend application | `/backend/.env.local` | `/backend/.env.example` | FastAPI non-secret configuration |
| Browser application | `/frontend/.env.local` | `/frontend/.env.example` | Public Vite configuration |

### Backend configuration

The current Backend template defines:

```text
PATHWISE_ENVIRONMENT=local
PATHWISE_APP_NAME=Pathwise API
PATHWISE_CORS_ALLOWED_ORIGIN=http://localhost:5173
```

`PATHWISE_CORS_ALLOWED_ORIGIN` is required. The Local policy allows the exact
Frontend origin rather than `*`. Operating-system environment variables take
precedence over values in `backend/.env.local`.

There is no Backend database URL, database password, AWS, or Cognito
configuration in Stage 3.

### Frontend configuration and the public boundary

The current Frontend template defines:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**Any `VITE_*` value must be treated as public.** Values consumed by the
application are compiled into browser-visible assets. Never place database
passwords, AWS credentials, private API tokens, or confidential authentication
secrets under `VITE_*`.

The canonical browser URL is `http://localhost:5173/`, while the API base is
`http://127.0.0.1:8000`. These are intentionally different origins. Do not
casually substitute `127.0.0.1` for `localhost` on the Frontend side because
browser origin identity controls CORS behavior.

## Starting Local PostgreSQL

From the repository root:

```powershell
docker compose up -d
docker compose ps
```

Wait for `postgres` to report `healthy`.

Current Local database contract:

```text
image     postgres:18.6
binding   127.0.0.1:5432
database  pathwise
user      pathwise
storage   Docker-managed named volume
```

The password comes from the ignored root `.env` and must not be committed.

## Starting the Backend

From `backend/`:

```powershell
uv run uvicorn pathwise.main:app --reload
```

The Backend loads `backend/.env.local`, validates configuration, configures the
`pathwise` JSON logger, creates one FastAPI application, and listens on
`http://127.0.0.1:8000` by default. A successful construction emits an
`application_configured` record with the non-secret `environment` field.

The Backend does not connect to PostgreSQL in Stage 3.

## Starting the Frontend

From `frontend/`:

```powershell
npm run dev
```

Open <http://localhost:5173/>. Vite is a Local development server; the
Production direction remains a separately built static artifact.

## Browser/API Integration

The implemented request path is:

```text
Browser at http://localhost:5173
→ GET http://127.0.0.1:8000/health
→ FastAPI
```

This is genuine cross-origin browser traffic. FastAPI explicitly allows
`http://localhost:5173`; no Vite proxy is configured. The request is a simple
public GET and CORS is not authentication.

Activate **Check backend health** in the UI. With the Backend running, the
expected result is:

```text
Backend health: ok
```

If the Backend is stopped while Vite remains available, the UI reports:

```text
Backend health: error
```

## Running Backend Quality Gates

From `backend/`:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src/pathwise
uv run pytest
```

The current Stage 3 pytest baseline is eight tests covering configuration,
health, CORS, and bounded JSON logging. The suite supplies its own Test
configuration and does not require `backend/.env.local` or PostgreSQL.

Developer correction commands, when intentionally applying changes, are:

```powershell
uv run ruff check . --fix
uv run ruff format .
```

## Running Frontend Quality Gates

From `frontend/`:

```powershell
npm run lint
npm run format:check
npm run test:run
npm run build
```

The current Stage 3 Vitest baseline is eight tests covering foundation UI
rendering, health success/failure behavior, native fetch handling, response
validation, and missing public configuration. Tests run with jsdom and require
neither FastAPI nor PostgreSQL.

To apply the configured Frontend formatter intentionally:

```powershell
npm run format
```

## PostgreSQL Lifecycle

Run these commands from the repository root.

Start or recreate the service while retaining existing volume data:

```powershell
docker compose up -d
```

Inspect health and port publication:

```powershell
docker compose ps
```

Remove the container and network while preserving the named volume and Local
database state:

```powershell
docker compose down
```

**Destructive Local reset:**

```powershell
docker compose down -v
```

`down -v` also removes the named volume and destroys the disposable Local
database state. It is not a Production recovery procedure.

### Two different health signals

The Compose healthcheck runs `pg_isready` and answers whether PostgreSQL is
accepting connections for the configured Local database and user.

FastAPI `GET /health` answers only whether the application process is serving
HTTP. It is deliberately shallow and does not check PostgreSQL or another
external dependency.

## Clean Dependency Restoration

Canonical reproducibility commands are:

- from `backend/`: `uv sync --locked`;
- from `frontend/`: `npm ci`.

They use the committed lockfiles and fail rather than silently changing the
approved dependency graph. Do not use `pip install`, `npm install`, or
`uv --no-cache` as the normal clean-bootstrap workflow.

## Troubleshooting

### `npm ci` reports `EPERM` on Windows

An active Vite or Vitest process can hold a native Rolldown file under
`node_modules`, preventing npm from replacing it. Stop the relevant Pathwise
Vite/Vitest process cleanly, then rerun `npm ci`. Do not begin with aggressive
file deletion or terminate unrelated processes.

### PowerShell command context

The canonical commands were validated in the normal developer PowerShell
environment and in PowerShell 7. Do not globally weaken PowerShell execution
policy for Pathwise. Keep the working directory explicit: Compose commands run
at the repository root, uv commands in `backend/`, and npm commands in
`frontend/`.

### Configuration validation fails

Confirm the appropriate Local file was copied from its tracked template. Do not
invent a fallback URL, wildcard CORS policy, or committed secret to bypass a
validation failure.

### Line endings

The root `.gitattributes` establishes LF for repository text. Do not change
global Git `core.autocrlf` merely for Pathwise.

## What Local Development Does Not Reproduce

Current Local Development does not reproduce Production AWS infrastructure,
identity/authentication, persistence wiring, migrations, Product data, backup
and recovery, Production observability, or deployment orchestration. It proves
the Stage 3 application and tooling boundaries only; later roadmap stages add
their own validated behavior.
