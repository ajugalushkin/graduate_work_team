"""Health check endpoints."""

import logging

from fastapi import APIRouter

from src.schemas import HealthResponse


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify service status.

    Returns:
        HealthResponse: Service health information
    """

    logging.debug("Healthcheck requested")

    components = {"api": "healthy"}

    # Determine overall status
    if all(v == "healthy" for v in components.values()):
        status = "healthy"
    else:
        status = "degraded"

    return HealthResponse(
        status=status,
        components=components,
    )
