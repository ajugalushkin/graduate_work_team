import os
import json
import time

from etl.src.core.config import settings
from etl.src.elastic.client import get_es_client, create_index_if_not_exists, index_bulk_movies

print("✅ main.py: Скрипт запущен")
print(f"🌍 Подключение к: {settings.elastic_url}")
print(f"📂 Файл дампа: {settings.dump_file}")

def load_dump(es):
    if not os.path.exists(settings.dump_file):
        print(f"❌ Файл дампа не найден: {settings.dump_file}")
        print(f"📁 Содержимое / {os.listdir('/data')}")
        exit(1)

    try:
        with open(settings.dump_file, "r", encoding="utf-8") as f:
            movies = json.load(f)
        print(f"✅ Загружено {len(movies)} фильмов из дампа")
    except Exception as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        exit(1)

    actions = []
    for movie in movies:
        action = {"index": {"_index": settings.elastic_index, "_id": movie["id"]}}
        actions.append(action)
        actions.append(movie)

    index_bulk_movies(es, actions)


if __name__ == "__main__":
    es=get_es_client()

    create_index_if_not_exists(es)

    load_dump(es)

    print("🎉 Загрузка завершена.")
    time.sleep(2)