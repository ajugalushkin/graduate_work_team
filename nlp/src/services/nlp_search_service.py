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
        search_data = await self.nlp_service.parse_pattern(query=query)
        
        if not search_data:
            return None
        
        if search_data.get("category") == "movie":
            search_data["category"] = "title"
        elif search_data.get("category") == "author":
            search_data["category"] = "writers_names"

        if search_data.get("intent") == "movie":
            search_data["intent"] = "title"
        elif search_data.get("intent") == "author":
            search_data["intent"] = "writers_names"
        elif search_data.get("intent") == "actors":
            search_data["intent"] = "actors_names"
        elif search_data.get("intent") == "rating":
            search_data["intent"] = "imdb_rating"
        elif search_data.get("intent") == "genre":
            search_data["intent"] = "genres"
        
        if search_data["intent"] == "count_movies":
            return await self.search_service.search_count_by_query(
                keyword=search_data.get("keyword"),
                keyword_field=search_data.get("category"),
                search_field=search_data.get("intent"),
            )

        return await self.search_service.search_one_by_query(
            keyword=search_data.get("keyword"),
            keyword_field=search_data.get("category"),
            search_field=search_data.get("intent"),
        ) 
