from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

import requests

from simulator.models import WeatherSnapshot


def _degrees_to_direction(deg: float) -> str:
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round((deg % 360) / 45) % 8
    return directions[idx]


class OpenMeteoClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout_seconds: int = 10) -> None:
        self.timeout_seconds = timeout_seconds

    def _build_params(self, lat: float, lon: float) -> Dict[str, Any]:
        return {
            "latitude": lat,
            "longitude": lon,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "surface_pressure",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "precipitation",
                    "uv_index",
                    "is_day",
                ]
            ),
            "timezone": "UTC",
        }

    def fetch(self, lat: float, lon: float) -> WeatherSnapshot:
        response = requests.get(
            self.BASE_URL,
            params=self._build_params(lat, lon),
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        current = payload.get("current", {})

        rain_intensity = float(current.get("precipitation", 0.0))
        is_day = int(current.get("is_day", 1))

        # When solar data is unavailable from the free endpoint, estimate lux by UV and day state.
        uv_index = float(current.get("uv_index", 0.0))
        if is_day:
            light_lux = max(1500.0, uv_index * 1800.0)
        else:
            light_lux = 10.0

        return WeatherSnapshot(
            air_temperature=float(current.get("temperature_2m", 22.0)),
            humidity=float(current.get("relative_humidity_2m", 55.0)),
            pressure=float(current.get("surface_pressure", 1013.0)),
            wind_speed=float(current.get("wind_speed_10m", 5.0)),
            wind_direction=_degrees_to_direction(float(current.get("wind_direction_10m", 0.0))),
            rain_detected=rain_intensity > 0.1,
            rain_intensity=rain_intensity,
            light_lux=light_lux,
            uv_index=uv_index,
            source="live",
        )


def default_weather() -> WeatherSnapshot:
    hour = datetime.now(tz=timezone.utc).hour
    is_day = 6 <= hour <= 18
    return WeatherSnapshot(
        air_temperature=24.0 if is_day else 19.0,
        humidity=58.0,
        pressure=1012.0,
        wind_speed=7.0,
        wind_direction="NW",
        rain_detected=False,
        rain_intensity=0.0,
        light_lux=9000.0 if is_day else 10.0,
        uv_index=4.0 if is_day else 0.0,
        source="fallback",
    )
