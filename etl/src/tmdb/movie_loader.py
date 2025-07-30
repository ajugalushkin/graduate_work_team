def extract_movie_data(movie, credits):
    crew = credits.get("crew", [])
    cast = credits.get("cast", [])

    genres = [g["name"] for g in movie.get("genres", [])]

    directors_list = [
        {"id": str(p["id"]), "name": p["name"]}
        for p in crew if p["job"] == "Director"
    ]
    directors_names = ", ".join([d["name"] for d in directors_list])

    writers_list = [
        {"id": str(p["id"]), "name": p["name"]}
        for p in crew if p["job"] in ("Writer", "Screenplay", "Author")
    ]
    writers_names = ", ".join([w["name"] for w in writers_list])

    actors_list = [
        {"id": str(p["id"]), "name": p["name"]}
        for p in cast[:5]
    ]
    actors_names = ", ".join([a["name"] for a in actors_list])

    return {
        "id": str(movie["id"]),
        "imdb_rating": movie.get("vote_average") or 0.0,
        "genres": genres,
        "title": movie.get("title") or "",
        "description": movie.get("overview") or "",
        "directors": directors_list,
        "directors_names": directors_names,
        "writers": writers_list,
        "writers_names": writers_names,
        "actors": actors_list,
        "actors_names": actors_names,
    }