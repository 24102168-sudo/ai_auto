from fastapi import APIRouter

from app.api.v1 import admin, auth, billing, jobs, projects

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(jobs.router)
api_router.include_router(billing.router)
api_router.include_router(admin.router)
