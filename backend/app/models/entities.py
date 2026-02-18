from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RoleEnum(str, Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class PlanEnum(str, Enum):
    starter = "starter"
    pro = "pro"
    agency = "agency"


class JobStatusEnum(str, Enum):
    queued = "queued"
    researching = "researching"
    generating_script = "generating_script"
    generating_seo = "generating_seo"
    generating_metadata = "generating_metadata"
    generating_voice = "generating_voice"
    generating_thumbnail = "generating_thumbnail"
    rendering_video = "rendering_video"
    optimizing_output = "optimizing_output"
    completed = "completed"
    failed = "failed"


class Organization(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    plan_type: Mapped[PlanEnum] = mapped_column(SAEnum(PlanEnum), default=PlanEnum.starter)
    subscription_status: Mapped[str] = mapped_column(String(64), default="inactive")
    stripe_customer_id: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="organization", cascade="all,delete")
    projects = relationship("Project", back_populates="organization", cascade="all,delete")
    api_keys = relationship("ApiKey", back_populates="organization", cascade="all,delete")


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(SAEnum(RoleEnum), default=RoleEnum.viewer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="users")


class Project(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), index=True)
    niche: Mapped[str] = mapped_column(String(100))
    tone: Mapped[str] = mapped_column(String(100))
    platform: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="projects")
    jobs = relationship("ContentJob", back_populates="project", cascade="all,delete")


class ContentJob(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    topic: Mapped[str] = mapped_column(String(255))
    script: Mapped[str | None] = mapped_column(Text)
    seo_title: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(JSON)
    hashtags: Mapped[list[str] | None] = mapped_column(JSON)
    pinned_comment: Mapped[str | None] = mapped_column(Text)
    voice_type: Mapped[str | None] = mapped_column(String(120))
    audio_path: Mapped[str | None] = mapped_column(String(255))
    video_path: Mapped[str | None] = mapped_column(String(255))
    thumbnail_path: Mapped[str | None] = mapped_column(String(255))
    duration_seconds: Mapped[int] = mapped_column(Integer, default=60)
    processing_time: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[JobStatusEnum] = mapped_column(SAEnum(JobStatusEnum), default=JobStatusEnum.queued)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="jobs")


class AuditLog(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(index=True)
    actor_user_id: Mapped[int | None] = mapped_column(index=True)
    action: Mapped[str] = mapped_column(String(200))
    payload: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ApiKey(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), index=True)
    name: Mapped[str] = mapped_column(String(140))
    key_hash: Mapped[str] = mapped_column(String(255), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="api_keys")


class WebhookEndpoint(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(index=True)
    url: Mapped[str] = mapped_column(String(300))
    secret: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class UsageMetric(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(index=True)
    metric: Mapped[str] = mapped_column(String(120), index=True)
    value: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


Index("ix_contentjob_project_status", ContentJob.project_id, ContentJob.status)
Index("ix_usage_organization_metric", UsageMetric.organization_id, UsageMetric.metric)
