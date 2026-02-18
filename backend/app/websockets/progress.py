import asyncio
from fastapi import APIRouter, WebSocket
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.entities import ContentJob

router = APIRouter()


@router.websocket("/ws/jobs/{job_id}")
async def job_progress(websocket: WebSocket, job_id: int):
    await websocket.accept()
    try:
        while True:
            db: Session = SessionLocal()
            try:
                job = db.query(ContentJob).filter(ContentJob.id == job_id).first()
                if job:
                    await websocket.send_json({"job_id": job.id, "status": job.status.value, "updated_at": job.updated_at.isoformat()})
                    if job.status.value in {"completed", "failed"}:
                        break
            finally:
                db.close()
            await asyncio.sleep(1)
    finally:
        await websocket.close()
