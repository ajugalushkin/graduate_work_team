from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router
from src.core import Container, get_settings, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan setup and teardown."""
    # Setup
    settings = get_settings()
    setup_logging(log_level=settings.log_level, log_name=settings.module_name)
    container = Container()

    Container.init_config_from_settings(container, settings)
    container.wire(modules=["src.api.v1.health", "src.api.v1.movie"])
    app.container = container

    # Start services
    logging.info(
        f"Starting {settings.module_name} in {settings.environment} mode"
    )

    await app.container.elasticsearch_platform().connect()
    logging.info("Elasticsearch platform has been connected")

    await app.container.nlp_search_service().sync_genres()
    logging.info("Genres were synced")

    yield

    # Teardown
    logging.info(f"Shutting down {settings.module_name}")
    await app.container.elasticsearch_platform().disconnect()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.module_name,
        version="0.0.1",
        lifespan=lifespan,
        docs_url="/api/docs" if settings.environment != "production" else None,
        redoc_url="/api/redoc" if settings.environment != "production" else None,  # noqa
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(router=router, prefix=settings.api_v1_prefix)

    return app


app = create_application()


@app.get("/")
async def root():
    """Root endpoint redirecting to documentation."""
    return {"message": "Welcome to the NLP Module", "docs": "/api/docs"}
