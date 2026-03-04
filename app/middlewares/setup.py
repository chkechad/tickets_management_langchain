"""Middlewares setup for the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .logs import LoggingMiddleware


def register_middlewares(app: FastAPI) -> None:
    """Setup middlewares for the app, the order is important.

    Args:
        app: FastAPI instance to setup middlewares for.
    """
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
