# AURORA CORE
**AI Content Operating System for Scalable Creators & Agencies**

A production-oriented, modular, multi-tenant SaaS platform built with FastAPI + Next.js. It supports enterprise-grade auth/RBAC, Stripe subscription workflows, Celery-based AI pipeline orchestration, and cloud-ready deployment.

## Stack
- Backend: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, Redis, Celery, JWT, Passlib bcrypt, structured logging.
- AI Engine: Ollama primary provider + OpenAI fallback, Coqui TTS voice, FFmpeg renderer, thumbnail generation.
- Frontend: Next.js App Router, TypeScript, TailwindCSS, Framer Motion, Zustand, React Query.
- Ops: Docker, Docker Compose, NGINX reverse proxy, Gunicorn/Uvicorn.

## Architecture highlights
- Clean architecture folders (`api`, `services`, `models`, `schemas`, `workers`, `ai`, `middleware`).
- Multi-tenant data model with strict organization scoping.
- Subscription controls + plan enforcement middleware.
- Stage-based content pipeline with retryable Celery tasks.
- Realtime job status updates via WebSockets.

## Local startup
```bash
cp .env.example .env
docker-compose up --build
```

Open:
- App: http://localhost
- API docs: http://localhost/api/docs (if proxied directly map as needed)

## Core API surface
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET/POST /api/v1/projects`
- `POST /api/v1/jobs`
- `GET /api/v1/jobs/{id}`
- `POST /api/v1/billing/checkout`
- `POST /api/v1/billing/webhook`
- `GET /api/v1/admin/stats`
- `WS /ws/jobs/{id}`

## Security controls
- JWT access tokens with tenant and role claims.
- Role-based route guards.
- Bcrypt password hashing.
- CSRF header enforcement for mutating API requests.
- CORS allowlist from environment.
- Rate limiting with `slowapi`.

## Production deployment
See [DEPLOYMENT.md](DEPLOYMENT.md).
