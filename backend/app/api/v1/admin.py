from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models.entities import ContentJob, Organization, RoleEnum, User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def stats(
    _: User = Depends(require_role(RoleEnum.admin)),
    db: Session = Depends(get_db),
):
    return {
        "organizations": db.query(func.count(Organization.id)).scalar(),
        "jobs": db.query(func.count(ContentJob.id)).scalar(),
    }
