"""business logic."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import TicketStatus
from app.exceptions.business import TicketAlreadyClosedError, TicketNotFoundError
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate


async def create_ticket(ticket: TicketCreate, db: AsyncSession) -> TicketRead:
    """Create a ticket.

    :param ticket: TicketCreate - the ticket data to create
    :param db: Session - the database session
    :return: TicketRead - the created ticket
    """
    db_ticket = Ticket(**ticket.model_dump())
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return TicketRead.model_validate(db_ticket)


async def get_tickets(db: AsyncSession) -> list[TicketRead]:
    """Get all tickets.

    :param db: Session - the database session
    :return: list[TicketRead] - the list of tickets
    """
    tickets = await db.scalars(select(Ticket))
    return [TicketRead.model_validate(t) for t in tickets]


async def get_ticket_by_id(ticket_id: uuid.UUID, db: AsyncSession) -> TicketRead:
    """Get a ticket by id.

    :param ticket_id: uuid.UUID - the ticket id
    :param db: Session - the database session
    :return: TicketRead - the ticket
    """
    ticket = await db.scalar(select(Ticket).filter(Ticket.id == ticket_id))
    if not ticket:
        raise TicketNotFoundError(ticket_id)
    return TicketRead.model_validate(ticket)


async def update_ticket(ticket_id: uuid.UUID, ticket: TicketUpdate, db: AsyncSession) -> TicketRead:
    """Update a ticket.

    :param ticket_id: uuid.UUID - the ticket id
    :param ticket: TicketUpdate - the ticket data to update
    :param db: Session - the database session
    :return: TicketRead - the updated ticket
    """
    db_ticket = await db.scalar(select(Ticket).filter(Ticket.id == ticket_id))
    if not db_ticket:
        raise TicketNotFoundError(ticket_id)
    for field, value in ticket.model_dump(exclude_unset=True).items():
        setattr(db_ticket, field, value)
    await db.commit()
    await db.refresh(db_ticket)
    return TicketRead.model_validate(db_ticket)


async def close_ticket(ticket_id: uuid.UUID, db: AsyncSession) -> TicketRead:
    """Close a ticket by setting its status to CLOSED.

    :param ticket_id: uuid.UUID - the ticket id
    :param db: Session - the database session
    :return: TicketRead - the closed ticket
    """
    db_ticket = await db.scalar(select(Ticket).filter(Ticket.id == ticket_id))
    if not db_ticket:
        raise TicketNotFoundError(ticket_id)
    if db_ticket.status == TicketStatus.CLOSED:
        raise TicketAlreadyClosedError(ticket_id)
    db_ticket.status = TicketStatus.CLOSED
    await db.commit()
    await db.refresh(db_ticket)
    return TicketRead.model_validate(db_ticket)
