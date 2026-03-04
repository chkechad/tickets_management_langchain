"""ticket pydantic schemas."""

from pydantic import BaseModel

from app.enums import TicketStatus
from app.mixins.common import BaseReadSchemaMixin


class TicketCreate(BaseModel):  # type: ignore[misc]
    """Ticket creation."""

    title: str
    description: str
    status: TicketStatus = TicketStatus.OPEN


class TicketUpdate(BaseModel):  # type: ignore[misc]
    """Ticket update."""

    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None


class TicketRead(BaseReadSchemaMixin):
    """Ticket read."""

    title: str
    description: str
    status: TicketStatus
