#!/bin/bash
set -e  # Остановить скрипт при ошибке

echo "The application is starting..."
exec uvicorn src:app --host 0.0.0.0 --port 8080
