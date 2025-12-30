"""
Core asset models for the smart building digital twin.

This module defines the classes that represent physical building assets
(e.g., HVAC systems, lighting) and their current operational state.
"""


class HVACSystem:
    """Model of an HVAC (Heating, Ventilation, and Air Conditioning) unit.

    Attributes:
        asset_id (str): Unique identifier for the HVAC unit.
        temperature_setpoint (float): Desired temperature in degrees Celsius.
        current_temperature (float): Last measured temperature in degrees Celsius.
        status (str): Operational status, one of 'on', 'off', 'idle'.
        last_updated (datetime): Timestamp of the last state update.
        metadata (dict): Additional asset information (manufacturer, model, location, etc.).
    """

    def __init__(self, asset_id: str, temperature_setpoint: float = 21.0):
        """Initialize an HVAC system with default values."""
        self.asset_id = asset_id
        self.temperature_setpoint = temperature_setpoint
        self.current_temperature = None
        self.status = "off"
        self.last_updated = None
        self.metadata = {}

    def update_temperature(self, new_temperature: float):
        """Update the current temperature reading."""
        self.current_temperature = new_temperature
        self.last_updated = self._current_timestamp()

    def set_status(self, new_status: str):
        """Set the operational status."""
        allowed = ("on", "off", "idle")
        if new_status not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        self.status = new_status
        self.last_updated = self._current_timestamp()

    def set_setpoint(self, new_setpoint: float):
        """Change the temperature setpoint."""
        self.temperature_setpoint = new_setpoint
        self.last_updated = self._current_timestamp()

    def _current_timestamp(self):
        """Return current UTC timestamp (simplified placeholder)."""
        from datetime import datetime
        return datetime.utcnow()

    def __repr__(self):
        return (f"HVACSystem(asset_id={self.asset_id!r}, "
                f"setpoint={self.temperature_setpoint}, "
                f"current={self.current_temperature}, "
                f"status={self.status!r})")


# Placeholder for future asset classes (LightingSystem will be added in Issue #2).