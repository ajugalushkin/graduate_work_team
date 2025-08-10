import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ESConnectionError
from core.config import settings
import time

from elastic.schema import MOVIE_INDEX_SCHEMA

from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_es_client(retries=10, delay=10) -> Elasticsearch:
    logger.info(f"Подключение к Elasticsearch: {settings.elasticsearch_url}")

    for attempt in range(retries):
        try:
            client = Elasticsearch(settings.elasticsearch_url)

            if client.ping():
                logger.info("Успешное подключение к Elasticsearch")
                return client
            else:
                logger.warning("Не удалось получить ping от Elasticsearch. Попытка %s", attempt + 1)

        except ESConnectionError as e:
            logger.warning("Ошибка подключения к Elasticsearch: %s (попытка %s)", e, attempt + 1)

        time.sleep(delay)

    raise RuntimeError("Elasticsearch недоступен")


def create_index_if_not_exists(es):
    if not es.indices.exists(index="movies"):
        es.indices.create(index="movies", body=MOVIE_INDEX_SCHEMA)

def index_bulk_movies(es, data):
    if not data:
        return
    payload = "".join(map(lambda d: json.dumps(d), data)) + ""
    resp = es.bulk(body=payload, index="movies", params={"refresh": "true"})
    if resp.get("errors"):
        raise Exception(f"Ошибки загрузки: {resp}")