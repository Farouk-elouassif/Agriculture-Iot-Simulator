from __future__ import annotations

from simulator.models import WeatherSnapshot


class IrrigationService:
    def __init__(self, moisture_on: float = 56.0, moisture_off: float = 70.0) -> None:
        self.moisture_on = moisture_on
        self.moisture_off = moisture_off

    def decide_status(self, moisture: float, weather: WeatherSnapshot, current_on: bool) -> bool:
        if weather.rain_detected and weather.rain_intensity > 0.3:
            return False
        if current_on and moisture >= self.moisture_off:
            return False
        if (not current_on) and moisture <= self.moisture_on:
            return True
        return current_on
