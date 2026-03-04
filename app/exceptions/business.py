"""custom exceptions for business logic."""


class TicketNotFoundError(Exception):
    """Raised when a ticket is not found."""


class TicketAlreadyClosedError(Exception):
    """Raised when a ticket is already closed."""
