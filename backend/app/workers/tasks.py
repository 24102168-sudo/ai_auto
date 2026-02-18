import time
from datetime import datetime

from celery import chain
from sqlalchemy.orm import Session

from app.ai.providers import get_provider
from app.ai.thumbnail import create_thumbnail
from app.ai.video import render_video
from app.ai.voice import synthesize_voice
from app.core.logging import get_logger
from app.db.session import SessionLocal
from app.models.entities import ContentJob, JobStatusEnum
from app.workers.celery_app import celery_app

logger = get_logger(__name__)


def _update_job(job_id: int, **kwargs):
    db: Session = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        if not job:
            return
        for key, value in kwargs.items():
            setattr(job, key, value)
        db.commit()
    finally:
        db.close()


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def stage_research(self, job_id: int):
    _update_job(job_id, status=JobStatusEnum.researching)
    logger.info("pipeline_stage", stage="researching", job_id=job_id)
    return job_id


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def stage_script(self, job_id: int):
    db: Session = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        _update_job(job_id, status=JobStatusEnum.generating_script)
        provider = get_provider()
        script = provider.generate(f"Create a polished script about {job.topic} for {job.title}")
        job.script = script
        db.commit()
    finally:
        db.close()
    return job_id


@celery_app.task(bind=True)
def stage_seo(self, job_id: int):
    db: Session = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        _update_job(job_id, status=JobStatusEnum.generating_seo)
        job.seo_title = f"{job.title} | Aurora SEO"
        job.description = f"{job.topic} explained for scalable creators and agencies"
        job.tags = ["aurora", "content", "ai"]
        job.hashtags = ["#auroracore", "#aiops", "#creator"]
        job.pinned_comment = "What should we automate next?"
        db.commit()
    finally:
        db.close()
    return job_id


@celery_app.task(bind=True)
def stage_voice(self, job_id: int):
    db: Session = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        _update_job(job_id, status=JobStatusEnum.generating_voice)
        audio_path = f"media/audio/job_{job_id}.wav"
        synthesize_voice(job.script or job.topic, audio_path)
        job.audio_path = audio_path
        db.commit()
    finally:
        db.close()
    return job_id


@celery_app.task(bind=True)
def stage_thumbnail(self, job_id: int):
    db: Session = SessionLocal()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        _update_job(job_id, status=JobStatusEnum.generating_thumbnail)
        thumb = f"media/thumbs/job_{job_id}.png"
        create_thumbnail(job.title, thumb)
        job.thumbnail_path = thumb
        db.commit()
    finally:
        db.close()
    return job_id


@celery_app.task(bind=True)
def stage_render(self, job_id: int):
    db: Session = SessionLocal()
    start = time.time()
    try:
        job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
        _update_job(job_id, status=JobStatusEnum.rendering_video)
        video_path = f"media/video/job_{job_id}.mp4"
        render_video(job.audio_path, job.thumbnail_path, video_path, job.duration_seconds)
        job.video_path = video_path
        job.status = JobStatusEnum.completed
        job.processing_time = int(time.time() - start)
        job.updated_at = datetime.utcnow()
        db.commit()
    except Exception:
        _update_job(job_id, status=JobStatusEnum.failed)
        raise
    finally:
        db.close()
    return job_id


def enqueue_content_pipeline(job_id: int):
    chain(stage_research.s(job_id), stage_script.s(), stage_seo.s(), stage_voice.s(), stage_thumbnail.s(), stage_render.s()).delay()
