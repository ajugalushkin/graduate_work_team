import requests

from core.config import settings


class TMDBClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get(self, path, **params):
        url = f"https://api.themoviedb.org/3{path}"
        params.update({"api_key": self.api_key, "language": settings.tmdb_language_code})
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def discover_movie_ids(self, pages=1):
        ids = []
        for page in range(1, pages + 1):
            data = self.get("/discover/movie", sort_by="popularity.desc", page=page)
            ids.extend([m["id"] for m in data["results"]])
        return ids

    def get_movie(self, movie_id):
        return self.get(f"/movie/{movie_id}")

    def get_movie_credits(self, movie_id):
        return self.get(f"/movie/{movie_id}/credits")

def get_tmdb_client():
    return TMDBClient(settings.tmdb_api_key)