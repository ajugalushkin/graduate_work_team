import json
import os
import time

from core.config import settings
from elastic.client import get_es_client, create_index_if_not_exists
from utils.logger import setup_logger

logger = setup_logger(__name__)

def load_dump():
    es=get_es_client()

    create_index_if_not_exists(es)

    if not os.path.exists(settings.dump_file):
        logger.error(f"Файл дампа не найден: {settings.dump_file}")
        exit(1)

    try:
        with open(settings.dump_file, "r", encoding="utf-8") as f:
            movies = json.load(f)
        logger.info(f"Загружено {len(movies)} фильмов из дампа")
    except Exception as e:
        logger.error(f"Ошибка чтения JSON: {e}")
        exit(1)

    actions = []
    for movie in movies:
        action = {"index": {"_index": settings.elastic_index, "_id": movie["id"]}}
        actions.append(action)
        actions.append(movie)

    try:
        response = es.bulk(operations=actions)
        if response.get("errors"):
            logger.warning(f"Ошибки в bulk: {response['items']}")
        else:
            logger.info(f"Успешно загружено {len(movies)} документов")
    except Exception as e:
        logger.error(f"Ошибка загрузки в Elastic: {e}")
        exit(1)

    logger.info("Загрузка завершена.")
    time.sleep(2)