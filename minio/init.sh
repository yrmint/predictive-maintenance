#!/bin/sh

set -e

echo "Waiting for MinIO..."

until mc alias set local http://minio:9000 minio miniopassword
do
    sleep 2
done

echo "Creating bucket..."

mc mb local/mlflow --ignore-existing

echo "Bucket created."

mc anonymous set none local/mlflow