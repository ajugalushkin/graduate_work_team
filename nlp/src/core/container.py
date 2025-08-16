"""Dependency injection container for the application."""

from dependency_injector import containers, providers

from src.core.config import Settings
from src.services import (
    NLPSearchService,
    NLPService,
    ElasticSearchPlatform,
    MoviesSearchService
)


class Container(containers.DeclarativeContainer):
    """Application container for dependency injection."""

    config = providers.Configuration()

    @classmethod
    def init_config_from_settings(cls, container, settings: Settings):
        """Initialize configuration from settings."""
        container.config.set("environment", settings.environment)
        container.config.set("log_level", settings.log_level)

        container.config.set("patterns_path", settings.patterns_path)

        container.config.set(
            "elasticsearch_host", str(settings.elasticsearch_host)
        )
        container.config.set(
            "elasticsearch_port", str(settings.elasticsearch_port)
        )
        container.config.set(
            "elasticsearch_username", str(settings.elasticsearch_username)
        )
        container.config.set(
            "elasticsearch_password", str(settings.elasticsearch_password)
        )

    # ELK
    elasticsearch_platform = providers.Singleton(
        ElasticSearchPlatform,
        elasticsearch_host=config.elasticsearch_host,
        elasticsearch_port=config.elasticsearch_port,
        elasticsearch_username=config.elasticsearch_username,
        elasticsearch_password=config.elasticsearch_password,
    )

    movies_search_service = providers.Factory(
        MoviesSearchService,
        search_platform=elasticsearch_platform,
    )

    nlp_service = providers.Singleton(
        NLPService,
        config.patterns_path
    )

    nlp_search_service = providers.Factory(
        NLPSearchService,
        search_service=movies_search_service,
        nlp_service=nlp_service
    )
