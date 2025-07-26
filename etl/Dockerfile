FROM python:3.11-slim

WORKDIR /app

COPY tmdb_to_elastic.py .

RUN pip install --no-cache-dir requests

CMD ["python", "tmdb_to_elastic.py"]
