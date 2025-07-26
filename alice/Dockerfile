FROM python:3.13 AS base

RUN apt-get update && apt-get install -y \
    vim \
    iputils-ping

WORKDIR /app
COPY ./requirements.txt ./


FROM base AS stage_one
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]