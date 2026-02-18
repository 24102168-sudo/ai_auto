from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.entities import Organization, User
from app.services.stripe_service import create_checkout_session, validate_webhook

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/checkout")
def checkout(plan: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == user.organization_id).first()
    url = create_checkout_session(
        customer_id=org.stripe_customer_id,
        plan=plan,
        success_url="http://localhost:3000/billing?success=1",
        cancel_url="http://localhost:3000/billing?cancel=1",
    )
    return {"url": url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    event = validate_webhook(payload, request.headers.get("stripe-signature", ""))
    if event["type"] == "customer.subscription.updated":
        sub = event["data"]["object"]
        org = db.query(Organization).filter(Organization.stripe_customer_id == sub["customer"]).first()
        if org:
            org.subscription_status = sub["status"]
            db.commit()
    return {"received": True}
