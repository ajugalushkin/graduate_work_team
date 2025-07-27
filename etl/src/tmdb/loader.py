import time
from tmdb.tmdb_client import get_tmdb_client
from tmdb.movie_loader import extract_movie_data
from elastic.es_client import get_es_client, create_index_if_not_exists, index_bulk_movies

def load_movies():
    tmdb = get_tmdb_client()
    es = get_es_client()
    create_index_if_not_exists(es)

    movie_ids = tmdb.discover_movie_ids(pages=3)
    print(f"Всего фильмов к загрузке: {len(movie_ids)}")

    bulk_data = []

    for movie_id in movie_ids:
        try:
            movie = tmdb.get_movie(movie_id)
            credits = tmdb.get_movie_credits(movie_id)
            data = extract_movie_data(movie, credits)

            bulk_data.append({
                "index": {
                    "_index": "movies",
                    "_id": data["id"]
                }
            })
            bulk_data.append(data)
            print(f"Загружено {len(data)} записей")
        except Exception as e:
            print(f"Ошибка загрузки фильма {movie_id}: {e}")

        time.sleep(0.2)

    index_bulk_movies(es, bulk_data)
    index_bulk_movies(es, bulk_data)