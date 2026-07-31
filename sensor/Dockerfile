FROM python:3.12-slim

WORKDIR /app

COPY shared /app/shared
COPY sensor /app/sensor

RUN pip install --no-cache-dir ./sensor

CMD ["python", "-m", "sensor.src.main"]