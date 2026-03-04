"""exception api."""

import logging

from fastapi import HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

logger = logging.getLogger(__name__)


async def http_exception_handler_logging(request: Request, exc: HTTPException) -> Response:
    """Log HTTP exceptions and return the default FastAPI error response.

    :param request: the incoming HTTP request
    :param exc: the HTTP exception raised
    :return: the default HTTP exception response
    """
    logger.error(f"kechad HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
