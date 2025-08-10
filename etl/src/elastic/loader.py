import json
import os
import time

from core.config import settings
from elastic.client import get_es_client, create_index_if_not_exists, index_bulk_movies

def load_dump():
    es=get_es_client()

    create_index_if_not_exists(es)

    if not os.path.exists(settings.dump_file):
        print(f"❌ Файл дампа не найден: {settings.dump_file}")
        exit(1)

    try:
        with open(settings.dump_file, "r", encoding="utf-8") as f:
            movies = json.load(f)
        print(f"✅ Загружено {len(movies)} фильмов из дампа")
    except Exception as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        exit(1)

    bulk_data = []

    for movie in movies:
        try:
            bulk_data.append({
                "index": {
                    "_index": "movies",
                    "_id": movie["id"]
                }
            })
            bulk_data.append(movie)
            print(f"Загружено {len(movie)} записей")
        except Exception as e:
            print(f"Ошибка загрузки фильма {movie["id"]}: {e}")

        time.sleep(0.2)

    index_bulk_movies(es, bulk_data)

    print("🎉 Загрузка завершена.")
    time.sleep(2)