import os
import json
import time
import requests
from elasticsearch import Elasticsearch
from elastic_schema import MOVIE_INDEX_SCHEMA

print("✅ load_dump.py: Скрипт запущен")

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
INDEX_NAME = os.getenv("INDEX_NAME", "movies")
DUMP_FILE = "/data/movies.json"  # 🔥 Важно: файл монтируется в /data

print(f"🌍 Подключение к: {ELASTIC_URL}")
print(f"📂 Файл дампа: {DUMP_FILE}")


def wait_for_es():
    print("⏳ Ожидание Elasticsearch...")
    for _ in range(60):  # максимум 5 минут
        try:
            response = requests.get(ELASTIC_URL, timeout=5)
            if response.status_code == 200:
                print("✅ Elasticsearch доступен")
                return
        except requests.ConnectionError:
            print("💤 Не могу подключиться к ES, жду...")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")

        time.sleep(10)

    print("❌ Не удалось подключиться к Elasticsearch")
    exit(1)


def create_index(es):
    try:
        if es.indices.exists(index=INDEX_NAME):
            print(f"ℹ️ Индекс '{INDEX_NAME}' уже существует")
            return

        es.indices.create(index=INDEX_NAME, body=MOVIE_INDEX_SCHEMA)
        print(f"✅ Индекс '{INDEX_NAME}' создан")
    except Exception as e:
        print(f"❌ Ошибка создания индекса: {e}")
        exit(1)


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
    wait_for_es()
    es = Elasticsearch(ELASTIC_URL)
    create_index(es)
    load_dump(es)
    print("🎉 Загрузка завершена.")
    time.sleep(2)