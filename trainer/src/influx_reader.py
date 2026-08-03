import pandas as pd
from influxdb_client import InfluxDBClient

from shared import influxdb_config


def load_data(start: str="-24h") -> pd.DataFrame:
    """
    Read data from InfluxDB bucket mlops.
    :param start: start of the time range from which data is to be selected.
    :return: DataFrame with selected records.
    """

    client = InfluxDBClient(
        url=influxdb_config.INFLUX_URL,
        token=influxdb_config.INFLUX_TOKEN,
        org=influxdb_config.INFLUX_ORG
    )

    query = f"""
    from(bucket: "sensors")
        |> range(start: {start})
        |> filter(fn: (r) => r._measurement == "sensor")
    """

    tables = client.query_api().query(query)

    records = []

    for table in tables:
        for record in table.records:
            records.append(
                {
                    "time": record.get_time(),
                    record.get_field(): record.get_value()
                }
            )

    return pd.DataFrame(records)
