from __future__ import annotations

import random

from sensor.models import SensorReading


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
        pass

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
