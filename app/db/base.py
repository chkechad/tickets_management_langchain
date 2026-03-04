"""base."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):  # type: ignore[misc]
    """Base class for all ORM models."""


metadata = Base.metadata
