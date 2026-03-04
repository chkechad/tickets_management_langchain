"""logging middleware."""

import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)

STATUS_COLORS = {
    2: "\033[32m",
    3: "\033[34m",
    4: "\033[33m",
    5: "\033[31m",
}
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


class LoggingMiddleware(BaseHTTPMiddleware):  # type: ignore[misc]
    """logging middleware."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch the request and log the method, url, status code and duration."""
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        status = response.status_code
        color = STATUS_COLORS.get(status // 100, RESET)

        logger.info(
            f"{BOLD}%-6s{RESET} {DIM}%-35s{RESET} {color}%3s{RESET}  {DIM}%.3fs{RESET}",
            request.method,
            request.url.path,
            status,
            duration,
        )
        return response
