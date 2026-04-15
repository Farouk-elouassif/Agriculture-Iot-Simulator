from __future__ import annotations

import random
from typing import Dict

from simulator.crop_profiles import get_crop_profile
from simulator.models import WeatherSnapshot


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class SoilModelService:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def next_soil(
        self,
        crop: str,
        weather: WeatherSnapshot,
        previous: Dict[str, float] | None,
        irrigation_on: bool,
    ) -> Dict[str, float]:
        base = previous.copy() if previous else get_crop_profile(crop)

        heat_factor = max(0.0, weather.air_temperature - 24.0) * 0.28
        wind_factor = weather.wind_speed * 0.07
        evaporation = heat_factor + wind_factor + self.rng.uniform(0.0, 0.5)

        moisture = base["moisture"] - evaporation
        if irrigation_on:
            moisture += self.rng.uniform(1.8, 3.2)
        if weather.rain_detected:
            moisture += min(4.5, weather.rain_intensity * 1.5)

        base["moisture"] = _clamp(moisture, 20.0, 95.0)

        # Soil temperature follows ambient temperature with slight lag.
        base["temperature"] = _clamp(
            (base["temperature"] * 0.72) + (weather.air_temperature * 0.28) + self.rng.uniform(-0.4, 0.4),
            5.0,
            45.0,
        )

        # Nutrients slowly drift down as crops consume them.
        base["nitrogen"] = _clamp(base["nitrogen"] - self.rng.uniform(0.02, 0.12), 5.0, 100.0)
        base["phosphorus"] = _clamp(base["phosphorus"] - self.rng.uniform(0.01, 0.08), 3.0, 100.0)
        base["potassium"] = _clamp(base["potassium"] - self.rng.uniform(0.02, 0.10), 5.0, 100.0)

        base["ph"] = _clamp(base["ph"] + self.rng.uniform(-0.03, 0.03), 4.5, 8.5)
        base["ec"] = _clamp(base["ec"] + self.rng.uniform(-0.03, 0.03), 0.2, 3.0)
        base["organic_matter"] = _clamp(base["organic_matter"] + self.rng.uniform(-0.02, 0.02), 0.5, 8.0)
        salinity = base["salinity"] + self.rng.uniform(-0.02, 0.02)
        if weather.rain_detected:
            salinity -= 0.03
        base["salinity"] = _clamp(salinity, 0.1, 2.5)

        return {k: round(v, 2) for k, v in base.items()}
