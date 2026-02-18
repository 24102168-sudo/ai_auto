from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    niche: str
    tone: str
    platform: str


class ProjectRead(ProjectCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
