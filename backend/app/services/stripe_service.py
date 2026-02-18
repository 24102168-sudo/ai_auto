import stripe
from fastapi import HTTPException

from app.core.config import get_settings

settings = get_settings()
stripe.api_key = settings.stripe_secret_key

PRICE_MAP = {
    "starter": lambda: settings.stripe_price_starter,
    "pro": lambda: settings.stripe_price_pro,
    "agency": lambda: settings.stripe_price_agency,
}


def create_checkout_session(customer_id: str, plan: str, success_url: str, cancel_url: str) -> str:
    price_id = PRICE_MAP.get(plan, lambda: "")()
    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid plan")
    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url


def validate_webhook(payload: bytes, sig_header: str):
    return stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
