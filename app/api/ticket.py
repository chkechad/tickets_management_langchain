"""route tickets."""

import logging
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession as ASession

from app.db.session import async_get_adb
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services import ticket as ticket_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/tickets", status_code=status.HTTP_201_CREATED)  # type: ignore[untyped-decorator]
async def create_ticket(ticket: TicketCreate, db: ASession = Depends(async_get_adb)) -> TicketRead:
    """Create a new ticket.

    - **title**: the ticket title
    - **description**: the ticket description
    - **status**: the ticket status (default: open)
    """
    return await ticket_service.create_ticket(ticket, db)


@router.get("/tickets", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
async def get_tickets(db: ASession = Depends(async_get_adb)) -> list[TicketRead]:
    """Get all tickets.

    Returns a list of all tickets.
    """
    return await ticket_service.get_tickets(db)


@router.get("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
async def get_ticket(ticket_id: uuid.UUID, db: ASession = Depends(async_get_adb)) -> TicketRead:
    """Get a ticket by id.

    - **ticket_id**: the ticket UUID
    """
    return await ticket_service.get_ticket_by_id(ticket_id, db)


@router.put("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
async def update_ticket(
    ticket_id: uuid.UUID, ticket: TicketUpdate, db: ASession = Depends(async_get_adb)
) -> TicketRead:
    """Update a ticket.

    - **ticket_id**: the ticket UUID
    - **title**: the ticket title
    - **description**: the ticket description
    - **status**: the ticket status
    """
    return await ticket_service.update_ticket(ticket_id, ticket, db)


@router.patch("/tickets/{ticket_id}/close", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
async def close_ticket(ticket_id: uuid.UUID, db: ASession = Depends(async_get_adb)) -> TicketRead:
    """Close a ticket.

    - **ticket_id**: the ticket UUID to close
    """
    return await ticket_service.close_ticket(ticket_id, db)
