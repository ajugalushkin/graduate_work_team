import requests
import json
import time

API_KEY = 'YOUR_TMDB_API_KEY'
ELASTIC_URL = 'http://localhost:9200'
INDEX_NAME = 'movies'
LANG = 'ru'
HEADERS = {'Accept': 'application/json'}
BASE_URL = 'https://api.themoviedb.org/3'

def ensure_index_exists():
    response = requests.head(f'{ELASTIC_URL}/{INDEX_NAME}')
    if response.status_code == 200:
        print(f'✅ Индекс "{INDEX_NAME}" уже существует')
        return

    print(f'📦 Создаём индекс "{INDEX_NAME}"...')
    schema = {
        "settings": {
            "refresh_interval": "1s",
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    },
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "ru_en": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "english_stop",
                            "english_stemmer",
                            "english_possessive_stemmer",
                            "russian_stop",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": { "type": "keyword" },
                "imdb_rating": { "type": "float" },
                "genres": { "type": "keyword" },
                "title": {
                    "type": "text",
                    "analyzer": "ru_en",
                    "fields": {
                        "raw": { "type": "keyword" }
                    }
                },
                "description": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "directors_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "actors_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "writers_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "directors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": { "type": "keyword" },
                        "name": { "type": "text", "analyzer": "ru_en" }
                    }
                },
                "actors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": { "type": "keyword" },
                        "name": { "type": "text", "analyzer": "ru_en" }
                    }
                },
                "writers": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": { "type": "keyword" },
                        "name": { "type": "text", "analyzer": "ru_en" }
                    }
                }
            }
        }
    }

    res = requests.put(f'{ELASTIC_URL}/{INDEX_NAME}', json=schema)
    if res.status_code >= 400:
        print(f'❌ Ошибка создания индекса: {res.text}')
    else:
        print('✅ Индекс создан успешно')

def get_json(url, params=None):
    for _ in range(3):
        try:
            response = requests.get(url, params=params, headers=HEADERS)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        time.sleep(1)
    return {}

def fetch_credits(movie_id, media_type):
    url = f'{BASE_URL}/{media_type}/{movie_id}/credits'
    return get_json(url, {'api_key': API_KEY, 'language': LANG})

def extract_persons(credits, job):
    return [
        {'id': str(p['id']), 'name': p['name']}
        for p in credits.get('crew', []) if p.get('job') == job
    ]

def extract_actors(credits, limit=5):
    return [
        {'id': str(p['id']), 'name': p['name']}
        for p in credits.get('cast', [])[:limit]
    ]

def extract_names(items):
    return [p['name'] for p in items]

def transform_movie(item, media_type):
    movie_id = item['id']
    details = get_json(f'{BASE_URL}/{media_type}/{movie_id}', {
        'api_key': API_KEY,
        'language': LANG
    })

    if not details.get('title') and not details.get('name'):
        return None

    credits = fetch_credits(movie_id, media_type)

    directors = extract_persons(credits, 'Director')
    writers = extract_persons(credits, 'Writer')
    actors = extract_actors(credits)

    return {
        'id': str(movie_id),
        'title': details.get('title') or details.get('name'),
        'description': details.get('overview', ''),
        'genres': [g['name'] for g in details.get('genres', [])],
        'imdb_rating': float(details.get('vote_average', 0)),
        'directors': directors,
        'writers': writers,
        'actors': actors,
        'directors_names': extract_names(directors),
        'writers_names': extract_names(writers),
        'actors_names': extract_names(actors),
    }

def doc_exists(es_url, index, doc_id):
    response = requests.head(f'{es_url}/{index}/_doc/{doc_id}')
    return response.status_code == 200

def send_bulk(docs):
    bulk_payload = ''
    for doc in docs:
        bulk_payload += json.dumps({ "index": { "_index": INDEX_NAME, "_id": doc["id"] } }) + '\n'
        bulk_payload += json.dumps(doc, ensure_ascii=False) + '\n'

    response = requests.post(f'{ELASTIC_URL}/_bulk', headers={'Content-Type': 'application/json'}, data=bulk_payload.encode('utf-8'))
    if response.status_code >= 400:
        print(f'Ошибка загрузки в Elasticsearch: {response.text}')
    else:
        print(f'Загружено: {len(docs)}')

def fetch_and_upload(pages=5):
    buffer = []
    count = 0
    skipped = 0
    for media_type in ['movie', 'tv']:
        for page in range(1, pages + 1):
            print(f'Загружаем страницу {page} ({media_type})')
            data = get_json(f'{BASE_URL}/{media_type}/popular', {
                'api_key': API_KEY,
                'language': LANG,
                'page': page
            })
            for item in data.get('results', []):
                movie_id = str(item['id'])
                if doc_exists(ELASTIC_URL, INDEX_NAME, movie_id):
                    skipped += 1
                    continue

                doc = transform_movie(item, media_type)
                if doc:
                    buffer.append(doc)
                    count += 1
                    if len(buffer) >= 100:
                        send_bulk(buffer)
                        buffer = []
                time.sleep(0.25)

    if buffer:
        send_bulk(buffer)

    print(f'✅ Готово. Загружено: {count}, пропущено (уже есть): {skipped}')

if __name__ == '__main__':
    ensure_index_exists()
    fetch_and_upload(pages=50)
