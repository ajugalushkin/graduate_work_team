import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.urls import router
from src.core.logger import LOGGING

dictConfig(LOGGING)

logger = logging.getLogger("Alice API")

app = FastAPI(
    title="Alice API",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
