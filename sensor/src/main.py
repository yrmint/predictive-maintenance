import logging
import time

from sensor.src.simulator import EquipmentSimulator
from sensor.src.writer import InfluxWriter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main() -> None:
    simulator = EquipmentSimulator()
    writer = InfluxWriter()

    try:
        while True:
            reading = simulator.step()

            writer.write(reading)

            logging.info(
                "T=%.1f°C V=%.2f RPM=%d Wear=%.3f Failure=%s",
                reading.temperature,
                reading.vibration,
                int(reading.rpm),
                reading.wear,
                reading.failure,
            )

            if reading.failure:
                logging.warning("Equipment failure detected. Repairing...")
                simulator.repair()

            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Stopping sensor simulator...")

    finally:
        writer.close()


if __name__ == "__main__":
    main()
