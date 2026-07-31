from datetime import datetime


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
    