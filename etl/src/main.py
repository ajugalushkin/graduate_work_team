from elastic.index import ensure_index_exists
from elastic.connection import wait_for_elasticsearch
from tmdb.client import fetch_tmdb_data
from uploader.bulk import upload_bulk

if __name__ == '__main__':
    wait_for_elasticsearch()

    ensure_index_exists()
    for page in range(1, 51):
        items = fetch_tmdb_data(page=page)
        if items:
            upload_bulk(items)
