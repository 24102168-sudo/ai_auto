from fastapi import HTTPException, Request

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


async def csrf_guard(request: Request, call_next):
    if request.method not in SAFE_METHODS and request.url.path.startswith("/api"):
        token = request.headers.get("x-csrf-token")
        if not token:
            raise HTTPException(status_code=403, detail="Missing CSRF token")
    return await call_next(request)
