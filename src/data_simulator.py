"""
IoT data simulator for the smart building digital twin.

This module provides functions to generate synthetic sensor readings
that mimic real IoT devices. It is used for testing and development
when live sensor data is not available.
"""

import random
import json
from datetime import datetime, timezone


def generate_sensor_reading(sensor_id: str) -> dict:
    """Generate a random sensor reading for a given sensor ID.

    Args:
        sensor_id (str): Unique identifier of the sensor (e.g., 'temp_zone_101').

    Returns:
        dict: A JSON‑serializable dictionary with the sensor reading.
          Example:
          {
            "sensor_id": "temp_zone_101",
            "timestamp": "2025-01-15T14:30:00Z",
            "value": 22.5,
            "unit": "celsius",
            "metadata": {"floor": 1, "room": "101"}
          }

    The value range depends on the sensor type inferred from the sensor_id:
      - Temperature sensors (prefix 'temp_'): 18.0 to 25.0 °C
      - Humidity sensors (prefix 'humid_'): 30.0 to 70.0 %RH
      - Occupancy sensors (prefix 'occ_'): 0 (unoccupied) or 1 (occupied)
      - Lighting sensors (prefix 'light_'): 0 to 1000 lux
      - CO₂ sensors (prefix 'co2_'): 400 to 1500 ppm
      - Default (unknown type): random float between 0 and 100
    """
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Infer sensor type from ID prefix
    if sensor_id.startswith("temp_"):
        value = round(random.uniform(18.0, 25.0), 1)
        unit = "celsius"
        metadata = {"sensor_type": "temperature"}
    elif sensor_id.startswith("humid_"):
        value = round(random.uniform(30.0, 70.0), 1)
        unit = "percent"
        metadata = {"sensor_type": "humidity"}
    elif sensor_id.startswith("occ_"):
        value = random.choice([0, 1])
        unit = "boolean"
        metadata = {"sensor_type": "occupancy"}
    elif sensor_id.startswith("light_"):
        value = random.randint(0, 1000)
        unit = "lux"
        metadata = {"sensor_type": "illuminance"}
    elif sensor_id.startswith("co2_"):
        value = random.randint(400, 1500)
        unit = "ppm"
        metadata = {"sensor_type": "co2"}
    else:
        value = round(random.uniform(0, 100), 2)
        unit = "unknown"
        metadata = {"sensor_type": "generic"}

    return {
        "sensor_id": sensor_id,
        "timestamp": now,
        "value": value,
        "unit": unit,
        "metadata": metadata,
    }


def generate_batch(sensor_ids, count=10):
    """Generate a batch of simulated readings.

    Args:
        sensor_ids (list): List of sensor IDs to simulate.
        count (int): Number of readings to generate per sensor.

    Returns:
        list: List of reading dictionaries.
    """
    readings = []
    for _ in range(count):
        for sid in sensor_ids:
            readings.append(generate_sensor_reading(sid))
    return readings


if __name__ == "__main__":
    # Example usage: generate a few readings and print them as JSON
    import sys

    sensors = ["temp_zone_101", "humid_zone_101", "occ_room_202", "light_lobby"]
    batch = generate_batch(sensors, count=2)
    for reading in batch:
        print(json.dumps(reading, indent=2))
        print("---")
    sys.exit(0)