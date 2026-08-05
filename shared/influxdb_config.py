from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class InfluxDBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

    INFLUX_URL: str
    INFLUX_TOKEN: str
    INFLUX_ORG: str
    INFLUX_BUCKET: str


influxdb_config = InfluxDBConfig()
