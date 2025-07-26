def transform_item(movie: dict) -> dict:
    return {
        "id": str(movie["id"]),
        "title": movie.get("title"),
        "description": movie.get("overview", ""),
        "imdb_rating": movie.get("vote_average", 0.0),
        "genres": [],
        "actors": [],
        "actors_names": "",
        "directors": [],
        "directors_names": "",
        "writers": [],
        "writers_names": ""
    }
