from __future__ import annotations

import random
from datetime import UTC, datetime

from sensor.src.models import SensorReading


class EquipmentSimulator:
    """
    Simulates an industrial rotating machine.

    Internal state:
        * load:   current workload [0..1].
        * wear:   accumulated wear [0..1].
        * failed: equipment failure flag.
    """

    def __init__(self) -> None:
        self.load = 0.55
        self.wear = 0.0
        self.failed = False

    def step(self) -> SensorReading:
        """Advance simulation by one time step."""
        if not self.failed:
            self._update_load()
            self._update_wear()

        temperature = self._temperature()
        pressure = self._pressure()
        vibration = self._vibration()
        rpm = self._rpm()
        current = self._current()
        humidity = self._humidity()

        if not self.failed:
            failure_probability = (
                0.0002
                + 0.15 * self.wear
                + 0.01 * max(vibration - 1.5, 0)
                + 0.005 * max(temperature - 80, 0)
            )

            if random.random() < failure_probability:
                self.failed = True

        if self.failed:
            temperature = random.gauss(110, 2)
            pressure = random.gauss(2.0, 0.2)
            vibration = random.gauss(6.0, 0.4)
            rpm = random.gauss(250, 50)
            current = random.gauss(2.0, 0.3)
            humidity = random.gauss(45, 3)

        return SensorReading(
            timestamp=datetime.now(UTC),
            temperature=round(temperature, 2),
            pressure=round(pressure, 2),
            vibration=round(vibration, 2),
            rpm=round(rpm, 0),
            current=round(current, 2),
            humidity=round(humidity, 1),
            load=round(self.load, 3),
            wear=round(self.wear, 4),
            failure=int(self.failed),
        )

    def repair(self) -> None:
        self.wear = 0.0
        self.failed = False

    def _update_load(self) -> None:
        drift = random.gauss(0, 0.015)
        self.load = min(max(self.load + drift, 0.2), 1.0)

    def _update_wear(self) -> None:
        self.wear += 0.00005 + self.load * 0.00015
        self.wear = min(self.wear, 1.0)

    def _temperature(self) -> float:
        return (
            40.0
            + 35 * self.load
            + 25 * self.wear
            + random.gauss(0, 0.8)
        )

    def _pressure(self) -> float:
        return (
            6.0
            - 1.5 * self.wear
            + random.gauss(0, 0.05)
        )

    def _vibration(self) -> float:
        return (
            0.3
            + 0.8 * self.wear
            + 0.5 * self.load
            + random.gauss(0, 0.05)
        )

    def _rpm(self) -> float:
        return (
            1500
            + 1200 * self.load
            + random.gauss(0, 20)
        )

    def _current(self) -> float:
        return (
            5
            + 18 * self.load
            + 8 * self.wear
            + random.gauss(0, 0.4)
        )

    @staticmethod
    def _humidity() -> float:
        return random.gauss(45, 4)
