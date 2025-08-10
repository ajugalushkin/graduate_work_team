import os
import json
import time

from etl.src.core.config import settings
from etl.src.elastic.client import get_es_client
from etl.src.elastic.schema import MOVIE_INDEX_SCHEMA

print("✅ main.py: Скрипт запущен")
print(f"🌍 Подключение к: {settings.elastic_url}")
print(f"📂 Файл дампа: {settings.dump_file}")

def load_dump(es):
    if not os.path.exists(DUMP_FILE):
        print(f"❌ Файл дампа не найден: {DUMP_FILE}")
        print(f"📁 Содержимое / {os.listdir('/data')}")
        exit(1)

    try:
        with open(DUMP_FILE, "r", encoding="utf-8") as f:
            movies = json.load(f)
        print(f"✅ Загружено {len(movies)} фильмов из дампа")
    except Exception as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        exit(1)

    actions = []
    for movie in movies:
        action = {"index": {"_index": INDEX_NAME, "_id": movie["id"]}}
        actions.append(action)
        actions.append(movie)

    try:
        response = es.bulk(operations=actions)
        if response.get("errors"):
            print(f"⚠️ Ошибки в bulk: {response['items']}")
        else:
            print(f"✅ Успешно загружено {len(movies)} документов")
    except Exception as e:
        print(f"❌ Ошибка загрузки в Elastic: {e}")
        exit(1)


if __name__ == "__main__":
    es=get_es_client()

    load_dump(es)

    print("🎉 Загрузка завершена.")
    time.sleep(2)