import time
import requests
import os

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")

def wait_for_elasticsearch(max_retries=10, base_delay=1.0):
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(ELASTIC_URL)
            if response.status_code == 200:
                print("[Elastic] Elasticsearch is ready")
                return
            else:
                print(f"[Elastic] Unexpected status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[Elastic] Not reachable (attempt {attempt + 1})")

        sleep_time = base_delay * (2 ** attempt)
        print(f"[Elastic] Waiting {sleep_time:.1f}s before retry...")
        time.sleep(sleep_time)
        attempt += 1

    raise RuntimeError("Elasticsearch is not available after multiple attempts.")
