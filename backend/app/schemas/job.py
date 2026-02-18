from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    project_id: int
    title: str
    topic: str
    duration_seconds: int = 60
    voice_type: str = "alloy"


class JobRead(BaseModel):
    id: int
    project_id: int
    title: str
    topic: str
    status: str
    script: str | None
    seo_title: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
