import os
import requests

from tmdb.transform import transform_item

API_KEY = os.getenv('TMDB_API_KEY')
LANG = 'ru'
TMDB_URL = 'https://api.themoviedb.org/3'

def fetch_tmdb_data(page=1):
    url = f'{TMDB_URL}/movie/popular'
    params = {
        'api_key': API_KEY,
        'language': LANG,
        'page': page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    movies = response.json().get('results', [])
    return [transform_item(movie) for movie in movies]
