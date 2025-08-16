import logging
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError


class ElasticSearchPlatform:
    """Class for using elasticsearch."""

    def __init__(
        self,
        elasticsearch_host: str,
        elasticsearch_port: int = 9200,
        elasticsearch_username: str = "",
        elasticsearch_password: str = "",
    ):
        self.elasticsearch_host: str = elasticsearch_host
        self.elasticsearch_port: int = elasticsearch_port
        self.elasticsearch_username: str = elasticsearch_username
        self.elasticsearch_password: str = elasticsearch_password
        self.elasticsearch_client: AsyncElasticsearch | None = None
    
    async def connect(self) -> None:
        self.elasticsearch_client = AsyncElasticsearch(
            hosts=[f"http://{self.elasticsearch_host}:{self.elasticsearch_port}"],
            basic_auth=(
                self.elasticsearch_username,
                self.elasticsearch_password,
            )
            if self.elasticsearch_username
            else None,
        )

    async def disconnect(self):
        if self.elasticsearch_client:
            await self.elasticsearch_client.close()
            self.elasticsearch_client = None

    async def get(self, index: str, obj_id: str) -> dict[str, Any] | None:
        try:
            result = await self.elasticsearch_client.get(
                index=index, id=obj_id
            )
        except NotFoundError:
            return None
        return result

    async def search(
            self, index: str, body: dict[str, Any]
        ) -> dict[str, Any] | None:
        try:
            results = await self.elasticsearch_client.search(
                index=index, body=body
            )
        except NotFoundError:
            return None
        return results
