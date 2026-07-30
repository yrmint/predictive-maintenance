FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install \
    mlflow \
    boto3 \
    psycopg2-binary

WORKDIR /app