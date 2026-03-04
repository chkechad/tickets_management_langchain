"""mixins."""

import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class UUIDMixin:
    """uuid mixin."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)


class TimestampMixin:
    """timestamps mixin."""

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class BaseModelMixin(UUIDMixin, TimestampMixin):
    """baseModelMixin."""


# Pydantic schemas for the common fields


class UUIDSchemaMixin(BaseModel):  # type: ignore[misc]
    """UUID Schema mixin."""

    id: uuid.UUID


class TimestampSchemaMixin(BaseModel):  # type: ignore[misc]
    """Timestamp Schema mixin."""

    created_at: datetime


class BaseReadSchemaMixin(UUIDSchemaMixin, TimestampSchemaMixin):
    """multiple inheritance for db."""

    model_config = {"from_attributes": True}
