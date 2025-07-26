import os
import requests

ELASTIC_URL = os.getenv('ELASTIC_URL', 'http://elasticsearch:9200')
INDEX_NAME = os.getenv('INDEX_NAME', 'movies')

def index_exists() -> bool:
    res = requests.head(f'{ELASTIC_URL}/{INDEX_NAME}')
    return res.status_code == 200

def create_index(schema: dict):
    return requests.put(f'{ELASTIC_URL}/{INDEX_NAME}', json=schema)
