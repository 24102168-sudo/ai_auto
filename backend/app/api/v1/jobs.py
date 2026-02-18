from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.middleware.subscription import enforce_voice_access, require_active_subscription
from app.models.entities import ContentJob, Project, User
from app.schemas.job import JobCreate, JobRead
from app.workers.tasks import enqueue_content_pipeline

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead)
def create_job(payload: JobCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = require_active_subscription(user, db)
    enforce_voice_access(org, payload.voice_type)
    project = db.query(Project).filter(Project.id == payload.project_id, Project.organization_id == user.organization_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    job = ContentJob(
        project_id=payload.project_id,
        title=payload.title,
        topic=payload.topic,
        duration_seconds=payload.duration_seconds,
        voice_type=payload.voice_type,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    enqueue_content_pipeline(job.id)
    return job


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = (
        db.query(ContentJob)
        .join(Project, Project.id == ContentJob.project_id)
        .filter(ContentJob.id == job_id, Project.organization_id == user.organization_id)
        .first()
    )
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
