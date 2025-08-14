from src.services.nlp_service import NLPService
from src.services.search_service import MoviesSearchService


class NLPSearchService:
    def __init__(
            self,
            search_service: MoviesSearchService,
            nlp_service: NLPService
        ):
        self.search_service = search_service
        self.nlp_service = nlp_service

    async def sync_genres(self) -> None:
        await self.nlp_service.update_genres(
            await self.search_service.search_all_genres()
        )

    async def get_by_id(self, movie_id: str):
        """Returns  movie info by id."""

        return await self.search_service.get_movie_from_search_platform(
            movie_id=movie_id
        )
    
    async def parse_query(self, query: str) -> str:
        return await self.nlp_service.parse_query(query=query)
    
    async def search_by_pattern(self, query: str) -> str:
        return await self.nlp_service.parse_pattern(query=query) 
