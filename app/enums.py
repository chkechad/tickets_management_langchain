"""list of enums."""

from enum import StrEnum


class TicketStatus(StrEnum):
    """Enum."""

    OPEN = "open"
    STALLED = "stalled"
    CLOSED = "closed"
