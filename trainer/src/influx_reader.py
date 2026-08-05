
import pandas as pd
from influxdb_client import InfluxDBClient

from shared.influxdb_config import influxdb_config
from trainer.src.config import training_config


def load_data() -> pd.DataFrame:
    """
    Read data from InfluxDB bucket mlops.
    :return: DataFrame with selected records.
    """

    client = InfluxDBClient(
        url=influxdb_config.INFLUX_URL,
        token=influxdb_config.INFLUX_TOKEN,
        org=influxdb_config.INFLUX_ORG
    )

    start = training_config.TRAINING_WINDOW

    query = f"""
    from(bucket: "sensors")
        |> range(start: {start})
        |> filter(fn: (r) => r._measurement == "sensor")
    """

    tables = client.query_api().query(query)

    results = {}

    for table in tables:
        for record in table.records:
            time = record.get_time().isoformat()

            if time not in results:
                results[time] = {
                    "time": time,
                }

            results[time][record["_field"]] = record["_value"]

    return pd.DataFrame(results.values())
