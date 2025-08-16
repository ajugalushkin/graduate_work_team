import logging

from src.services.search_platform import ElasticSearchPlatform


class MoviesSearchService:
    """ "
    A service class responsible for retrieving movies data from search
    platform.
    """

    def __init__(self, search_platform: ElasticSearchPlatform):
        self.search_platform = search_platform
        self.index = 'movies'

    async def get_movie_from_search_platform(self, movie_id: str):
        """Returns movie by id."""

        doc = await self.search_platform.get(self.index, movie_id)
        if doc is None:
            return None

        return doc
    
    async def search_all_genres(self) -> list[str]:
        body = {
            "size": 0,
            "aggs": {
                "unique_statuses": {
                    "terms": {
                        "field": "genres"
                    }
                }
            }
        }
        results = await self.search_platform.search(self.index, body=body)

        genres = [
            buckets.get("key")
            for buckets in results.get("aggregations")
            .get("unique_statuses")
            .get("buckets")
        ]

        return genres
    
    async def search_by_query(
            self,
            keyword: str,
            keyword_field: str,
            search_field: str
    ) -> list[str] | None:
        
        logging.debug(
            f"Searching for - keyword: {keyword}; keyword_field: {keyword_field}; search_field: {search_field}"
        )
        body: dict[str, dict] = {
            "size": 1,
            "query": {
                "bool": {
                    "must": [
                        {"match": {keyword_field: keyword}},
                    ]
                }
            } 
        }
        
        search_results = await self.search_platform.search(self.index, body=body)

        if not search_results:
            return None
        
        hits = search_results.get("hits").get("hits")
        if not hits:
            return None
        
        logging.debug(f"search_results: {hits}")
        result = hits[0].get("_source").get(search_field)

        return result