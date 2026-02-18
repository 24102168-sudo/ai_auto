# Deployment Guide

## Production checklist
1. Provision managed PostgreSQL and Redis.
2. Configure object storage for media assets.
3. Set secure environment variables from `.env.example`.
4. Build and push images to your registry.
5. Run migrations: `alembic upgrade head`.
6. Deploy API and workers with at least 2 replicas each.
7. Put NGINX or cloud load balancer in front with TLS.
8. Configure Stripe webhook endpoint: `/api/v1/billing/webhook`.
9. Enable monitoring/log shipping from structured JSON logs.

## Cloud notes
- AWS: ECS Fargate + RDS + ElastiCache.
- DigitalOcean: App Platform + Managed DB + Redis.
- GCP: Cloud Run + Cloud SQL + Memorystore.
