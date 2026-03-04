"""models ticket."""

from sqlalchemy import Column, Enum, String

from app.db.base import Base
from app.enums import TicketStatus
from app.mixins.common import BaseModelMixin


class Ticket(BaseModelMixin, Base):
    """tickets models."""

    __tablename__ = "tickets"

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.OPEN)
