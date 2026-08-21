import pandas as pd
import numpy as np

def add_feature_failure_target(
        df: pd.DataFrame,
        horison_seconds: int = 30
) -> pd.DataFrame:
    """
    Adds "failure_within n seconds" feature to original dataset.
    :param df: original dataset
    :param horison_seconds: the window within which to detect failure
    :return: dateset with "failure_within n seconds" feature
    """
    result = df.copy()
    result["time"] = pd.to_datetime(result["time"])
    result = result.sort_values(["device_id", "time"])

    result["failure_next"] = 0

    for device_id, group in result.groupby("device_id"):
        failure_times = group.loc[
            group["failure"] == 1,
            "time"
        ].to_numpy()

        if len(failure_times) == 0:
            continue

        times = group["time"].to_numpy()

        for failure_time in failure_times:
            mask = ((times < failure_time)
                    & (times >= failure_time - np.timedelta64(horison_seconds, "s")))
            result.loc[group.index[mask], "failure_next"] = 1

    return result
