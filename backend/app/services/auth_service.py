from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.entities import Organization, PlanEnum, RoleEnum, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


def register_user(payload: RegisterRequest, db: Session) -> TokenResponse:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    org = Organization(name=payload.organization_name, plan_type=PlanEnum.starter, subscription_status="trialing")
    db.add(org)
    db.flush()
    user = User(
        organization_id=org.id,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=RoleEnum.admin,
    )
    db.add(user)
    db.commit()
    return TokenResponse(access_token=create_access_token(user.email, user.organization_id, user.role.value))


def login_user(payload: LoginRequest, db: Session) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email, user.organization_id, user.role.value))
