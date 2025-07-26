import os
import requests

from elastic.client import INDEX_NAME, ELASTIC_URL

def upload_bulk(docs: list):
    if not docs:
        return

    bulk_payload = ""
    for doc in docs:
        bulk_payload += f'{ {"index": {"_index": INDEX_NAME, "_id": doc["id"]}} }\n'
        bulk_payload += f'{doc}\n'

    headers = {"Content-Type": "application/x-ndjson"}
    res = requests.post(f"{ELASTIC_URL}/_bulk", data=bulk_payload, headers=headers)

    if res.status_code >= 400:
        print("Ошибка загрузки:", res.text)
    else:
        print(f"Загружено {len(docs)} записей")
