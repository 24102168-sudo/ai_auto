"""initial

Revision ID: 20261218_01
Revises: 
Create Date: 2026-12-18
"""

from alembic import op
import sqlalchemy as sa


revision = "20261218_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organization",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=140), nullable=False),
        sa.Column("plan_type", sa.Enum("starter", "pro", "agency", name="planenum"), nullable=False),
        sa.Column("subscription_status", sa.String(length=64), nullable=False),
        sa.Column("stripe_customer_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("admin", "editor", "viewer", name="roleenum"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organization.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("niche", sa.String(length=100), nullable=False),
        sa.Column("tone", sa.String(length=100), nullable=False),
        sa.Column("platform", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organization.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contentjob",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("topic", sa.String(length=255), nullable=False),
        sa.Column("script", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("hashtags", sa.JSON(), nullable=True),
        sa.Column("pinned_comment", sa.Text(), nullable=True),
        sa.Column("voice_type", sa.String(length=120), nullable=True),
        sa.Column("audio_path", sa.String(length=255), nullable=True),
        sa.Column("video_path", sa.String(length=255), nullable=True),
        sa.Column("thumbnail_path", sa.String(length=255), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("processing_time", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "queued",
                "researching",
                "generating_script",
                "generating_seo",
                "generating_metadata",
                "generating_voice",
                "generating_thumbnail",
                "rendering_video",
                "optimizing_output",
                "completed",
                "failed",
                name="jobstatusenum",
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table("auditlog", sa.Column("id", sa.Integer(), nullable=False), sa.Column("organization_id", sa.Integer(), nullable=False), sa.Column("actor_user_id", sa.Integer(), nullable=True), sa.Column("action", sa.String(length=200), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table("apikey", sa.Column("id", sa.Integer(), nullable=False), sa.Column("organization_id", sa.Integer(), nullable=False), sa.Column("name", sa.String(length=140), nullable=False), sa.Column("key_hash", sa.String(length=255), nullable=False), sa.Column("active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.ForeignKeyConstraint(["organization_id"], ["organization.id"]), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("key_hash"))
    op.create_table("webhookendpoint", sa.Column("id", sa.Integer(), nullable=False), sa.Column("organization_id", sa.Integer(), nullable=False), sa.Column("url", sa.String(length=300), nullable=False), sa.Column("secret", sa.String(length=255), nullable=False), sa.Column("active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_table("usagemetric", sa.Column("id", sa.Integer(), nullable=False), sa.Column("organization_id", sa.Integer(), nullable=False), sa.Column("metric", sa.String(length=120), nullable=False), sa.Column("value", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint("id"))


def downgrade() -> None:
    for table in ["usagemetric", "webhookendpoint", "apikey", "auditlog", "contentjob", "project", "user", "organization"]:
        op.drop_table(table)
    op.execute("DROP TYPE IF EXISTS jobstatusenum")
    op.execute("DROP TYPE IF EXISTS roleenum")
    op.execute("DROP TYPE IF EXISTS planenum")
