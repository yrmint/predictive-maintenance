from dataclasses import dataclass

from datetime import datetime


@dataclass
class SensorReading:
    timestamp: datetime

    temperature: float
    vibration: float
    pressure: float
    rpm: float
    current: float
    humidity: float

    wear: float
    load: float

    failure: int
    