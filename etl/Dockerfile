FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипты
COPY src/*.py .
COPY src/dump/movies.json /data/movies.json

# Проверим, что файлы есть
RUN ls -la

CMD ["python", "main.py"]