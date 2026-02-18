from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.entities import Organization, PlanEnum, User

PLAN_LIMITS = {
    PlanEnum.starter: {"monthly_content": 30, "projects": 2, "team": 3, "resolution": "1080p", "voices": ["alloy"]},
    PlanEnum.pro: {"monthly_content": 200, "projects": 15, "team": 15, "resolution": "1440p", "voices": ["alloy", "nova"]},
    PlanEnum.agency: {
        "monthly_content": 5000,
        "projects": 100,
        "team": 200,
        "resolution": "4k",
        "voices": ["alloy", "nova", "orion"],
    },
}


def require_active_subscription(user: User, db: Session) -> Organization:
    org = db.query(Organization).filter(Organization.id == user.organization_id).first()
    if not org or org.subscription_status not in {"active", "trialing"}:
        raise HTTPException(status_code=402, detail="Inactive subscription")
    return org


def enforce_voice_access(org: Organization, voice: str) -> None:
    allowed = PLAN_LIMITS[org.plan_type]["voices"]
    if voice not in allowed:
        raise HTTPException(status_code=403, detail="Voice unavailable for your plan")
