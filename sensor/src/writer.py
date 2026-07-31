from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from sensor.src.models import SensorReading
from shared import influxdb_config


class InfluxWriter:
    def __init__(self) -> None:
        self.client = InfluxDBClient(
            url=influxdb_config.INFLUX_URL,
            token=influxdb_config.INFLUX_TOKEN,
            org=influxdb_config.INFLUX_ORG
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write(self, reading: SensorReading) -> None:
        point = (
            Point("sensor")
            .tag("device_id", "motor_001")
            .time(reading.timestamp)
        )
        fields = {
            "temperature": reading.temperature,
            "pressure": reading.pressure,
            "vibration": reading.vibration,
            "rpm": reading.rpm,
            "current": reading.current,
            "humidity": reading.humidity,
            "wear": reading.wear,
            "load": reading.load,
            "failure": reading.failure,
        }

        for key, value in fields.items():
            if value is not None:
                point.field(key, value)

        self.write_api.write(
            bucket=influxdb_config.INFLUX_BUCKET,
            org=influxdb_config.INFLUX_ORG,
            record=point
        )
