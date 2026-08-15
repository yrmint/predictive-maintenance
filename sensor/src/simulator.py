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
        """
        Advance simulation by one time step.
        """

        if not self.failed:
            self._update_load()
            self._update_wear()

        temperature = self._temperature()
        pressure = self._pressure()
        vibration = self._vibration()
        rpm = self._rpm()
        current = self._current()
        humidity = self._humidity()

        if not self.failed and self._should_fail(vibration, temperature, current):
                self.failed = True

        if self.failed:
            (
                temperature,
                pressure,
                vibration,
                rpm,
                current,
                humidity
             ) = self._failure_state()

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
        base_rate = 0.00003
        load_effect = 0.00008 * self.load ** 2
        wear_effect = 0.00015 * self.wear ** 2
        noise = max(random.gauss(0, 0.00001), 0)
        self.wear += base_rate + load_effect + wear_effect + noise
        self.wear = min(self.wear, 1.0)

    def _temperature(self) -> float:
        wear_effect = 15 * self.wear + 35 * self.wear ** 3
        noise_std = 0.8 + 1.5 * self.wear

        return (
            40.0
            + 35 * self.load
            + wear_effect
            + random.gauss(0, noise_std)
        )

    def _pressure(self) -> float:
        wear_effect = 0.5 * self.wear + 2.0 * self.wear ** 2
        noise_std = 0.05 + 0.8 * self.wear
        return (
            6.0
            - wear_effect
            + random.gauss(0, noise_std)
        )

    def _vibration(self) -> float:
        wear_effect = 0.5 * self.wear + 3.0 * self.wear ** 3
        noise_std = 0.05 + 0.3 * self.wear ** 2

        return (
            0.3
            + wear_effect
            + 0.5 * self.load
            + random.gauss(0, noise_std)
        )

    def _rpm(self) -> float:
        noise_std = 15.0 + 60 * self.wear
        return (
            1500
            + 1200 * self.load
            - 200 * self.wear ** 2
            + random.gauss(0, noise_std)
        )

    def _current(self) -> float:
        wear_effect = 4 * self.wear + 10 * self.wear ** 2
        noise_std = 0.4 + 0.8 * self.wear

        return (
            5
            + 18 * self.load
            + wear_effect
            + random.gauss(0, noise_std)
        )

    @staticmethod
    def _humidity() -> float:
        return min(100, random.gauss(45.0, 4.0))

    def _should_fail(
            self, vibration:float, temperature: float, current: float
    ) -> bool:
        """
        Calculate failure risk.
        """

        base_probability = 0.00001
        wear_risk = 0.00005 * self.wear ** 4

        vibration_risk = 0.0005 * max(vibration - 1.2, 0.0) ** 2
        temperature_risk = 0.0002 * max(temperature - 85.0, 0.0) ** 2
        current_risk = 0.0001 * max(current - 25.0, 0.0) ** 2

        probability = (
            base_probability
            + wear_risk
            + vibration_risk
            + temperature_risk
            + current_risk
        )

        probability = min(probability, 0.05)

        return random.random() < probability

    @staticmethod
    def _failure_state() ->\
            tuple[float, float, float, float, float, float]:
        """
        Sensor values after a failure.
        """

        temperature = random.gauss(110, 2)
        pressure = random.gauss(2.0, 0.2)
        vibration = random.gauss(6.0, 0.4)
        rpm = random.gauss(250, 50)
        current = random.gauss(2.0, 0.3)
        humidity = random.gauss(45, 3)

        return temperature, pressure, vibration, rpm, current, humidity
